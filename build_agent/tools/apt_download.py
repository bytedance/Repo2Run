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
import subprocess
import argparse
import warnings
import sys
warnings.simplefilter('ignore', FutureWarning)

def update_apt(sudo=False):
    try:
        update_command = f'{"sudo " if sudo else ""}apt-get update'
        result = subprocess.run(update_command, shell=True, check=True, text=True, capture_output=True)
        print("Apt-get Update Ouput:\n", result.stdout)
        if result.stderr:
            print("Apt-get Update Warnings:\n", result.stderr)
        return True, result
    except subprocess.CalledProcessError as e:
        # 如果发生错误，打印错误信息
        print("An error occurred while 'apt-get update':", e.stderr)
        print(e.stdout)
        print("Please try again!")
        return False, e

# version_constraints如果要有，必须是'=[version]'，如"=1.0"
# 测试用，sudo一般不设置，因为默认在docker中为root
def run_apt(package_name, version_constraints, sudo=False):
    success, result = update_apt(sudo)
    if not success:
        return False, result
    if not version_constraints or len(version_constraints.strip()) == 0:
        full_name = package_name
    else:
        full_name = package_name + version_constraints
    apt_command = f'{"sudo " if sudo else ""}apt-get install -y ' + full_name
    print(f"Extract command `{apt_command}`, about to execute...")
    try:
        # 执行apt-get指令
        result = subprocess.run(apt_command, shell=True, check=True, text=True, capture_output=True)
        print("Apt-get Output:\n", result.stdout)
        if result.stderr:
            print("Apt-get Warnings:\n", result.stderr)
        return True, result
    except subprocess.CalledProcessError as e:
        # 如果发生错误，打印错误信息
        print("An error occurred while running 'apt-get install':", e.stderr)
        print(e.stdout)
        return False, e

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install a package with apt-get.')
    parser.add_argument('-p', '--package_name', required=True, type=str, help='The name of the package to install.')
    parser.add_argument('-v', '--version_constraints', type=str, default='', nargs='?', help='The version constraints of the package.')

    args = parser.parse_args()
    success, res = run_apt(args.package_name, args.version_constraints)
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)