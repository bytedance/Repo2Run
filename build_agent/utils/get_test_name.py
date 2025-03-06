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
import re
def collect_test_cases(file_content):
    lines = file_content.strip().split('\n')
    lines = lines[:-2]
    test_cases = []
    
    pattern = re.compile(r'^[^\[]+')

    for line in lines:
        match = pattern.match(line)
        if match:
            test_case = match.group()
            if test_case not in test_cases:
                test_cases.append(test_case)
    
    return test_cases

subprocess.run('pytest --collect-only -q > tests.txt', shell=True)
with open('tests.txt', 'r') as r1:
    file_content = r1.read()
test_cases = collect_test_cases(file_content)
for test_case in test_cases:
    print(test_case)
