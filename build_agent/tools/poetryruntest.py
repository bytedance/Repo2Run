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


#!/usr/bin/env python3
# This is $runtest.py$
import subprocess
import argparse
import warnings
import sys
import os
warnings.simplefilter('ignore', FutureWarning)
import re

def extract_test_cases(file_path):
    # 用正则表达式匹配测试用例
    test_case_pattern = re.compile(r'^(tests/[\w/]+\.py::[\w_]+)$', re.MULTILINE)
    
    test_cases = []
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            test_cases = test_case_pattern.findall(content)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    
    return test_cases

def check_pytest():
    result = subprocess.run('pytest --version', shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        return True
    else:
        return False

def run_pytest():
    success = check_pytest()
    if not success:
        print('Pytest is not installed in your environment. Please install the latest version of pytest using `pip install pytest`.')
        sys.exit(100)
    # if not os.path.exists('/home/tools/.test_func'):
    try:
        with open('/home/tools/.test_func', 'w') as file:
            # 使用subprocess.run并传递标准输出和标准错误到文件
            result = subprocess.run(
                # ['poetry', 'run', 'pytest', '/repo', '--collect-only', '-q', '--disable-warnings'],
                ['poetry', 'run', 'pytest', '--collect-only', '-q', '--disable-warnings'],
                cwd='/repo',
                stdout=file,
                stderr=subprocess.STDOUT  # 将标准错误重定向到标准输出
            )
        if result.returncode == 5:
            print('No unit tests were detected in this repository, so it passes. Congratulations, you have successfully configured the environment!')
            sys.exit(5)
        if result.returncode != 0:
            print('Error: Please modify the configuration according to the error messages below. Once all issues are resolved, rerun the tests.')
            subprocess.run('cat /home/tools/.test_func', shell=True)
            sys.exit(result.returncode)
        else:
            print('Congratulations, you have successfully configured the environment!')
            subprocess.run('cat /home/tools/.test_func', shell=True)
            # print()
            # try:
            #     subprocess.run('pipdeptree', shell=True)
            #     subprocess.run('pipdeptree --json-tree', shell=True)
            # except:
            #     pass
            sys.exit(0)
            # test_cases = extract_test_cases('/home/tools/.test_func')
            # for test_case in test_cases:
            #     print(test_case)
            # sys.exit(0)

    except Exception as e:
        print(e)
        subprocess.run('rm -rf /home/tools/.test_func', shell=True)
        print('Error: Please modify the configuration according to the error messages below. Once all issues are resolved, rerun the tests.')
        sys.exit(200)

    # test_cases = extract_test_cases('/home/tools/.test_func')
    # pass_tests = list()
    # failed_tests = list()
    # for test_func in test_cases:
    #     pytest_command = f'run pytest {test_func}'
    #     try:
    #         result = subprocess.run(pytest_command, cwd='/repo', shell=True, check=True, text=True, capture_output=True)
    #         pass_tests.append(test_func)
    #     except subprocess.CalledProcessError as e:
    #         msg = 'Test Output:\n'
    #         msg += e.stdout if e.stdout else ''
    #         msg += '\n'
    #         msg += e.stderr if e.stderr else ''
    #         failed_tests.append([test_func, msg])
    
    # if len(pass_tests) == 0:
    #     print('In this round of testing, you did not successfully pass the task test.')
    # else:
    #     msg = f'In this round of testing, you successfully passed totally {len(pass_tests)} tests as followed:\n'
    #     for pass_test in pass_tests:
    #         msg += pass_test
    #         msg += '\n'
    #     print(msg)
    # if len(failed_tests) == 0:
    #     print('In this round of testing, you have no failed tests. Congratulations, you have successfully configured the environment!')
    # else:
    #     msg = f'Sorry, you still have {len(failed_tests)} tests that did not pass, which indicates that your environment is not configured successfully.'
    #     msg += 'Below, you will find the names of these tests and their error messages. You need to make adjustments based on these error messages and rerun the `run_test` command once you believe your configuration is sufficient, until you fully pass all the tests.\n'
    #     for failed_test in failed_tests:
    #         msg += failed_test[0].strip()
    #         msg += ':\n'
    #         msg += failed_test[1]
    #         msg += '\n'
    #     msg += '*Note*: All tests have been passed in a properly configured environment. If any tests fail, it is due to incorrect or incomplete configuration on your part. You need to adjust according to the error messages and the current environment.'
    #     print(msg)
    sys.exit(0)

if __name__ == '__main__':
    run_pytest()

    
