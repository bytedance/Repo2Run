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

BASH_FENCE = ['```bash', '```']

# 用来提取对话里面的thought和action
def extract_dialogue(text):
    pattern = re.compile(
        r"\s*###\s*Thought\s*:\s*(.*?)\s*###\s*Action\s*:\s*(.*)", 
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.match(text)
    
    if match:
        thought = match.group(1).strip()
        action = match.group(2).strip()
        return thought, action
    else:
        return None, None

# 含有警告地提取thought和action，优先调用使用
def extract_dialogue_warnings(text):
    text = text.strip()
    thought, action = extract_dialogue(text)
    if not thought or not action:
        print(f'''All your answer must contain Thought and Action. Calling CLI tools Action using bash block like {BASH_FENCE[0]}  {BASH_FENCE[1]}. Please modify the format of your answer and resubmit it.
For example, below shows an answer with legal format:
### Thought: I need to read the README.md file.
### Action:
{BASH_FENCE[0]} 
cat README.md
{BASH_FENCE[1]}
''')
    return thought, action

if __name__ == '__main__':
    print(extract_dialogue_warnings('''
    ### Thught:
thought   1

### action:
Action!!!
    '''))