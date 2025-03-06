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


import re
from .parse_dialogue import extract_dialogue_warnings

BASH_FENCE = ['```bash', '```']

def extract_commands(text):
    pattern = rf'{BASH_FENCE[0]}([\s\S]*?){BASH_FENCE[1]}'
    matches = re.findall(pattern, text)

    commands = []
    for command_text in matches:
        if command_text:
            commands.extend(list(filter(None, command_text.strip().split('\n'))))
    
    return commands

def extract_commands_warnings(text):
    thought, action = extract_dialogue_warnings(text)
    if thought and action:
        commands = extract_commands(action)
        if len(commands) == 0:
            print(f'''Wrong! Please note that the Action part of your response does not contain any actionable commands surrounded by {BASH_FENCE[0]} and {BASH_FENCE[1]} that can be executed. Please regenerate the action.
*Note*: Each Action part of your responses must contain and only contain one actionable command surrounded by {BASH_FENCE[0]} and {BASH_FENCE[1]}.\n''')
            return -1
        if len(commands) > 1:
            command_msg = '\n'.join(commands)
            print(f'''Please note that the Action part of your response contains more than one actionable command surrounded by {BASH_FENCE[0]} and {BASH_FENCE[1]} , including:
{command_msg}
Please regenerate to ensure that the Action part contains exactly one command surrounded by {BASH_FENCE[0]} and {BASH_FENCE[1]}.
*Note*: If you want to execute multiple actions, you can write them all within one command block surrounded by {BASH_FENCE[0]} and {BASH_FENCE[1]}, or consider executing one action and then performing the next one in the subsequent round of the conversation.\n''')    
            return -1
        else:
            print(f"Successfully extracted the command `{commands[0]}`, about to execute...")
            return commands[0]
    else:
        return -1

# 匹配`download`指令，如果是这个指令，则返回True，否则返回False
def match_download(text):
    # 正则表达式
    pattern = re.compile(r'^\s*download\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(text)
    return bool(match)

# 匹配`runpipreqs`指令，如果是这个指令，则返回True，否则返回False
def match_runpipreqs(text):
    # 正则表达式
    pattern = re.compile(r'^\s*runpipreqs\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(text)
    return bool(match)

def match_runtest(text):
    # 正则表达式
    pattern = re.compile(r'^\s*runtest\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(text)
    return bool(match)

def match_poetryruntest(text):
    # 正则表达式
    pattern = re.compile(r'^\s*poetryruntest\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(text)
    return bool(match)

def match_conflict_solve(text):
    # 正则表达式模式
    pattern = re.compile(
        # r'\s*conflictlist\s+solve\s*(?:(-v| -V)\s*["\']([<>=!]=?\d+\.\d+)["\']\s*|\s*(-u\s*))?',
        r'\s*conflictlist\s+solve\s*(?:(-v| -V)\s*["\']([<>=!]=?\d+(\.\d+)*?)["\']\s*|\s*(-u\s*))?',
        re.IGNORECASE
    )
    
    match = pattern.fullmatch(text.strip())
    
    if not match:
        return -1
    
    args = {
        'conflictlist_solve': True,
        'version_constraint': None,
        'unchanged': False
    }
    
    # 检查-v的匹配段
    if match.group(1) and match.group(2):
        args['version_constraint'] = match.group(2)
    elif match.group(3) is not None:
        args['unchanged'] = True
    
    return args

# def match_errorformatlist_sovle(command):
#     # 正则表达式模式
#     pattern = re.compile(
#         # r'\s*errorformatlist\s+solve\s*(["\'].*?["\']\s*)*',
#         r'\s*errorformatlist\s+solve\s*(?:["\'].*?["\']\s*)*',
#         re.IGNORECASE
#     )

#     match = pattern.fullmatch(command.strip())

#     if not match:
#         return -1
    
#     # 提取所有以单引号或双引号包裹的条目
#     entries = re.findall(r'["\'](.*?)["\']', command)
    
#     args = {
#         'errorformatlist_solve': True,
#         'entries': entries
#     }

#     return args

def match_waitinglist_add(command):
    # Normalize the command by converting to lowercase and removing extra spaces
    command = re.sub(r'\s+', ' ', command.strip().lower())
    
    # Define the pattern to match the command format
    pattern = r"waitinglist add -p ([^\s]+)( -v ([^\s]+))? -t ([^\s]+)"
    
    # Match the command against the pattern
    match = re.match(pattern, command)
    
    if match:
        # Extract package_name, version_constraints, and tool
        package_name = match.group(1)
        version_constraints = match.group(3) if match.group(3) else None
        tool = match.group(4)
        return {
            "package_name": package_name,
            "version_constraints": version_constraints,
            "tool": tool
        }
    else:
        return -1

def match_waitinglist_addfile(command):
    # Normalize the command by converting to lowercase and removing extra spaces
    command = re.sub(r'\s+', ' ', command.strip().lower())
    
    # Define the pattern to match the command format
    pattern = r"waitinglist addfile ([^\s]+)"
    
    # Match the command against the pattern
    match = re.match(pattern, command)
    
    if match:
        # Extract file_path
        file_path = match.group(1)
        return {
            "file_path": file_path
        }
    else:
        return -1

def match_waitinglist_show(command):
    pattern = re.compile(r'^\s*waitinglist show\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(command)
    return bool(match)

def match_waitinglist_clear(command):
    pattern = re.compile(r'^\s*waitinglist clear\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(command)
    return bool(match)

# def match_errorformatlist_clear(command):
#     pattern = re.compile(r'^\s*errorformatlist clear\s*$', re.IGNORECASE | re.MULTILINE)
#     match = pattern.match(command)
#     return bool(match)

def match_conflictlist_show(command):
    pattern = re.compile(r'^\s*conflictlist show\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(command)
    return bool(match)

def match_conflictlist_clear(command):
    pattern = re.compile(r'^\s*conflictlist clear\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(command)
    return bool(match)

def match_clear_configuration(command):
    pattern = re.compile(r'^\s*clear_configuration\s*$', re.IGNORECASE | re.MULTILINE)
    match = pattern.match(command)
    return bool(match)

if __name__ == '__main__':
    print(extract_commands_warnings('''
### Thought: hello
### Action:
```bash
waitinglist solve
```
sdfldfks
'''))
    print('*'*100)
    print(extract_commands_warnings('''
### Thought:
```bash
waitinglist solve
```
### Action:
hello
'''))
    # 测试match_download
    commands = [
        'download',
        ' Download ',
        'DownlOad   ',
        'download -'
    ]
    for cmd in commands:
        print(f'Command: {cmd}')
        print(f'Parsed: {match_download(cmd)}')
        print('---')
    
    # 测试match_conflict_solve
    commands = [
        'conflictlist solve',
        'conflictlist    solve   -v  "==2.0"',
        "conflictlist solve -V '>3.0'",
        "Conflictlist   solve  -u",
        "cOnflictlist   solvE  -v '>=1.2'",
        'conflictlist  solve  -u',
        'conflict solve -v ">s"',
        'conflictlist solve -v "torch==2.5.0"'
    ]
    print('@'*100)
    for cmd in commands:
        print(f'Command: {cmd}')
        print(f'Parsed: {match_conflict_solve(cmd)}')
        print('---')

    # # 测试match_errorfomatlist_solve
    # commands = [
    #     'errorformatlist solve',
    #     'errorformatlist  Solve  "numpy==1.2.0"',
    #     'errorformatlist solve   "numpy" \'matplotlib>=2.0\'',
    #     "ErrorFormatList Solve 'pandas<=1.0'   'scipy' 'clash<1.2' \"sos.s > 1\"",
    #     'errorformatlist   solve',
    #     'errorformatlist solve "text>1"',
    #     "errorformat solve \"sss\" pandas<=1.0"
    # ]
    # for cmd in commands:
    #     print(f'Command: {cmd}')
    #     print(f'Parsed: {match_errorformatlist_sovle(cmd)}')
    #     print('---')

    # Test cases
    commands = [
        "waitinglist add -p package_name1 -v >=1.0.0 -t pip",
        "waitinglist add -p package_name2 -t pip",
        "waitinglist add -p package_name3 -v ==2.0.0 -t pip",
        "waitingList add -p package_name4 -t pip",
        "waitinglist add   -p package_name5 -t apt"
    ]

    for cmd in commands:
        print(f"Command: {cmd}")
        print(f"Version Constraints: {match_waitinglist_add(cmd)}\n")

    # Test cases for waiting_list_add_file
    file_commands = [
        "waitinglist addfile /path/to/file",
        "waitingList addfile  anotherfile.txt",
        "waitinglist addfilE  /path/with spaces/file.txt",
        "waitinglist add /sss"
    ]

    for cmd in file_commands:
        print(f"Command: {cmd}")
        print(f"Details: {match_waitinglist_addfile(cmd)}\n")