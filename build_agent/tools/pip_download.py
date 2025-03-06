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

def run_pip(package_name, version_constraints):
    if not version_constraints or len(version_constraints.strip()) == 0:
        full_name = package_name
    else:
        full_name = package_name + version_constraints
    if not full_name.strip().startswith('"') or not full_name.strip().startswith("'"):
        full_name = '"' + full_name + '"'
    pip_command = 'pip install ' + full_name
    try:
        # 执行pip指令
        result = subprocess.run(pip_command, shell=True, check=True, text=True, capture_output=True)

        # 检查返回码以确定是否安装成功
        if result.returncode == 0:
            print(f"The package {full_name} was installed successfully.")
            return True
        else:
            print(f"Failed to install the package {full_name}.")
            return False
    except subprocess.CalledProcessError as e:
        # 如果发生错误，打印错误信息
        print("An error occurred while running pip:\n", e.stderr.strip())
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install a Python package with pip.')
    parser.add_argument('-p', '--package_name', required=True, type=str, help='The name of the package to install.')
    parser.add_argument('-v', '--version_constraints', type=str, default='', nargs='?', help='The version constraints of the package.')
    args = parser.parse_args()

    success = run_pip(args.package_name, args.version_constraints)
    # print(success)
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)