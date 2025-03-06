# Copyright (2025) Bytedance Ltd. and/or its affiliates 

# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 


import subprocess
import os
import re
import enum
import difflib
import os
import json
import requests
import time
from pathlib import Path
import tempfile
from itertools import groupby

safe_cmd = [
    "cd", "ls", "cat", "echo", "pwd", "whoami", "who", "date", "cal", "df", "du",
    "free", "uname", "uptime", "w", "ps", "pgrep", "top", "htop", "vmstat", "iostat",
    "dmesg", "tail", "head", "more", "less", "grep", "find", "locate", "whereis", "which",
    "file", "stat", "cmp", "diff", "md5sum", "sha256sum", "gzip", "gunzip", "bzip2", "bunzip2",
    "xz", "unxz", "sort", "uniq", "wc", "tr", "cut", "paste", "tee", "awk", "sed", "env", "printenv",
    "hostname", "ping", "traceroute", "ssh", "journalctl","lsblk", "blkid", "uptime",
    "lscpu", "lsusb", "lspci", "lsmod", "dmidecode", "ip", "ifconfig", "netstat", "ss", "route", "nmap",
    "strace", "ltrace", "time", "nice", "renice", "killall", "printf"
    ]

TIME_OUT_LABEL= ' seconds. Partial output:'
DIFF_FENCE = ["```diff", "```"]
BASH_FENCE = ["```bash", "```"]
HEAD = "<<<<<<< SEARCH"
DIVIDER = "======="
UPDATED = ">>>>>>> REPLACE"

INIT_PROMPT = f"""
IN GOOD FORMAT: 
All your answer must contain Thought and Action. 
Calling CLI tools Action using bash block like {BASH_FENCE[0]}  {BASH_FENCE[1]}. 
Editing and Writing code Action using diff block like {DIFF_FENCE[0]} {DIFF_FENCE[1]}.
The command line you generate will be run in the bash sandbox environment, and the running results will be returned to you through the system messages.

IMPORTANT TIPS: 
        * Each round of reply can only contain one {BASH_FENCE[0]} {BASH_FENCE[1]} block, which means Each round of your answers contain only *ONE* action!
        * Please submit the first command first, then after receiving the response, you can issue the second command. You are free to use any other bash communication.
"""

EDIT_PROMPT = f"""
CODE EDITING AND WRITING: All changes to files must use the {DIFF_FENCE[0]}  {DIFF_FENCE[1]}  block format, with symbols {HEAD}, {DIVIDER} and {UPDATED} \n
You need to provide code patch. The patch should according to the original code, indent correctly, and do not include line numbers. The format is as follows: 
### Thought: Modify explanation...
### Action: 
{DIFF_FENCE[0]} 
/absolute/path/of/target.py
{HEAD}
    exact copy of old line(s) you would like to change
{DIVIDER}
    new line(s) to replace
{UPDATED}

{HEAD}
    exact copy of old line(s) you would like to change
{DIVIDER}
    new line(s) to replace
{UPDATED}
{DIFF_FENCE[1]} 
Every *SEARCH/REPLACE block must use this format:
1. The opening fence {DIFF_FENCE[0]} 
2. The file path alone on a line, verbatim. No bold asterisks, no quotes around it, no escaping of characters, etc.
3. The start of search block: {HEAD}
4. A contiguous chunk of lines to search for in the existing source code
5. The dividing line: {DIVIDER}
6. The lines to replace into the source code
7. The end of the replace block: {UPDATED}
8. The closing fence: {DIFF_FENCE[1]} 
Once you want to modify the code you MUST: 
        * Include *ALL* the code being searched and replaced!
        * Every *SEARCH* section must *EXACTLY MATCH* the existing source code, character for character, including all comments, docstrings, etc.
        * '{HEAD}', '{DIVIDER}' and  '{UPDATED}' symbols must be on a line by themselves and cannot be indented.
        * All code modifications must be expressed in the REPLACE format above (including delete an insert). We will find the source code with the highest matching degree in the original file and replace it. Please provide sufficient and unique old line(s) from snippet to facilitate matching.
        * If the code patch you provide is successfully applied, the differences before and after the code modification will be returned.
        * The paths of modified files must be completely absolute paths.
        * Make sure the patch you provide is indented correctly especially in python programs: The indentation of old lines is exactly the same as the original code, and the indentation of new lines is correct.
        * All patches must be based on the original code viewed by the tools, and fabricated code patch(es) is prohibited.
        * Previously successfully applied patches will modify the code, and new patches must be applied based on the current code. Please review the relevant code again then provide new patches.
        * If the old line(s) is empty, it is considered to be inserted at the beginning of the file. If the file does not exist, a new file will be created and the new line will be written. like:
### Thought: Create a.py
### Action:
{DIFF_FENCE[0]}
/project_path/.../a.py
{HEAD}
{DIVIDER}
    [new line(s) to add]
{UPDATED}
{DIFF_FENCE[1]}
"""

# def extract_commands(text):
#     pattern = rf'{BASH_FENCE[0]}([\s\S]*?){BASH_FENCE[1]}'
#     matches = re.findall(pattern, text)
#     command_text = ''
#     if len(matches) > 0:
#         command_text = matches[0]

#     commands = []
#     if command_text:
#         commands = list(filter(None, command_text.strip().split('\n')))
#     return commands
def extract_commands(text):
    BASH_FENCE = ('```bash', '```')
    pattern = rf'{re.escape(BASH_FENCE[0])}([\s\S]*?){re.escape(BASH_FENCE[1])}'
    matches = re.findall(pattern, text)
    
    return matches

# def extract_submit(text):
#     extract_text = extract_commands(text)
#     if len(extract_text) != 1:
#         return ''
#     extract_text = extract_text[0].strip()
#     if len(extract_text.split()) != 2:
#         return ''
#     extract_text_split = extract_text.split()
#     if extract_text_split[0] == 'submit':
#         return extract_text_split[1]
#     return ''
    
def append_trajectory(trajectory, messages, agent: str):
    # 对于messages中的每个message，添加一个agent字段
    for message in messages:
        message['agent'] = agent.lower()
        trajectory.append(message)

def save_trajectory(id, traj_dir, trajectory):
    # 获取一个唯一的文件名
    trial_index = 1
    def get_unique_filename(traj_dir, trial_index):
        filename = f"{id}_{trial_index}.txt"
        while os.path.exists(os.path.join(traj_dir, filename)):
            trial_index += 1
            filename = f"{id}_{trial_index}.txt"
        return filename
    
    traj_file = get_unique_filename(traj_dir, trial_index)
    trajectory_json = json.dumps(trajectory, indent=4, sort_keys=True, ensure_ascii=False)
    with open(os.path.join(traj_dir, traj_file), 'a', encoding='utf-8') as file:
        file.write(f"{trajectory_json}\n")

def save_report(id, report_path, report):
    trial_index = 1

    # 获取一个唯一的文件名
    def get_unique_filename(report_path, trial_index):
        filename = f"{id}_{trial_index}.md"
        while os.path.exists(os.path.join(report_path, filename)):
            trial_index += 1
            filename = f"{id}_{trial_index}.md"
        return filename

    report_file = get_unique_filename(report_path, trial_index)

    with open(os.path.join(report_path, report_file), 'w') as file:
        file.write(report)

def save_score(id, score_path, raw_score, agent_score):

    item = {'id': id, 'raw_score': raw_score, 'agent_score': agent_score}
    with open(os.path.join(score_path, 'score.jsonl'), 'a') as file:
        file.write(json.dumps(item) + '\n')

def extract_diffs(text):
    pattern = rf'{DIFF_FENCE[0]}([\s\S]*?){DIFF_FENCE[1]}'
    matches = re.findall(pattern, text)
    diffs = ''
    if len(matches) > 0:
        diffs = '\n'.join(matches)
    return diffs

def save_diff_description(text):
    temp_dir = "/tmp/patch"
    os.makedirs(temp_dir, exist_ok=True)
    cmd = f"sudo chmod -R 777 {temp_dir}"
    subprocess.run(cmd, check=True, shell=True)
    with tempfile.NamedTemporaryFile(mode='w+', dir=temp_dir, delete=False) as temp_file:
        temp_file_path = temp_file.name
        os.chmod(temp_file_path, 0o777)
        temp_file.write(text)
    return temp_file_path

if __name__=='__main__':
    text = '''```bash
submit python:3.10
pythonsdfkdl
```
'''
    print(extract_commands(text))