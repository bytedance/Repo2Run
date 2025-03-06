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

def split_cmd_statements(cmd):
    # 删除 \ 后跟换行符
    cmd = re.sub(r'\\\s*\n', '', cmd)

    # 替换普通换行符为单个空格
    cmd = re.sub(r'\n', ' ', cmd)

    # 使用正则表达式按 && 分割子语句，并移除前后的空格
    statements = re.split(r'\s*&&\s*', cmd)
    
    return [statement.strip() for statement in statements]

if __name__ == "__main__":
    # 示例输入
    # cmd = "echo Hello World\\\necho This is\\ a test && echo Another command"
    cmd = '''waitinglist add -p crawlerdetect -v "~0.1.7" -t pip && \
waitinglist add -p fastapi -v "~0.110" -t pip && \
waitinglist add -p fuzzywuzzy -v "~0.18" -t pip && \
waitinglist add -p gitignore-parser -v "==0.1.11" -t pip && \
waitinglist add -p imy[docstrings] -v ">=0.4.0" -t pip && \
waitinglist add -p introspection -v "~1.9.2" -t pip && \
waitinglist add -p isort -v "~5.13" -t pip && \
waitinglist add -p keyring -v "~24.3" -t pip && \
waitinglist add -p langcodes -v ">=3.4.0" -t pip && \
waitinglist add -p narwhals -v ">=1.12.1" -t pip && \
waitinglist add -p ordered-set -v ">=4.1.0" -t pip && \
waitinglist add -p path-imports -v ">=1.1.2" -t pip && \
waitinglist add -p pillow -v "~10.2" -t pip && \
waitinglist add -p python-levenshtein -v "~0.23" -t pip && \
waitinglist add -p python-multipart -v "~0.0.6" -t pip && \
waitinglist add -p pytz -v "~2024.1" -t pip && \
waitinglist add -p revel -v "~0.9.1" -t pip && \
waitinglist add -p timer-dict -v "~1.0" -t pip && \
waitinglist add -p tomlkit -v "~0.12" -t pip && \
waitinglist add -p typing-extensions -v ">=4.5" -t pip && \
waitinglist add -p unicall -v "~0.1.5" -t pip && \
waitinglist add -p uniserde -v "~0.3.14" -t pip && \
waitinglist add -p uvicorn[standard] -v "~0.29.0" -t pip && \
waitinglist add -p watchfiles -v "~0.21" -t pip && \
waitinglist add -p yarl -v ">=1.9" -t pip
'''
    # 调用函数拆分子语句
    result = split_cmd_statements(cmd)
    print(result)

    # 打印结果
    for i, statement in enumerate(result, 1):
        print(f"Statement {i}: {statement}")