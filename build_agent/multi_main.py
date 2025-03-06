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


import multiprocessing
import subprocess
import os
import sys
import random
import time


def run_command(command):
    # os.system('docker images --filter "dangling=true" --format "{{.ID}}" | xargs -r docker rmi')
    current_time = time.time()
    # 将时间戳转换为本地时间的 struct_time 对象
    local_time = time.localtime(current_time)

    # 将 struct_time 对象格式化为字符串
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print(f'Start time: {formatted_time}')
    full_name = command.split('python -u main.py "')[1].split('"')[0]

    vdb = subprocess.run("df -h | grep '/dev/vdb' | awk '{print $5}'", shell=True, capture_output=True, text=True)
    if float(vdb.stdout.strip().split('%')[0]) > 90:
        print('Warning! The disk /dev/vdb has occupied over 90% memories!')
        sys.exit(1)
    try:
        print(f'Begin: {command}')
        subprocess.run(command, shell=True)
        print(f'Finish: {command}')
        finish_command.append(command.split('python main.py "')[1].split('"')[0].lower().replace('/', '_').replace('-', '_'))
        for fc in finish_command:
            try:
                rm_cmd = f'docker ps -a --filter ancestor={fc}:tmp -q | xargs -r docker rm'
                subprocess.run(rm_cmd, shell=True, capture_output=True, text=True)
            except:
                pass
    except Exception as e:
        print(f"Error: {command}, {e}")

if __name__ == '__main__':
    os.system('docker rm -f $(docker ps -aq)')

    if len(sys.argv) != 2:
        print('Usage: python multi_main.py <script_path>')
        sys.exit(1)
    script_path = sys.argv[1]


    # 要执行的命令列表
    try:
        with open(script_path, 'r') as r1:
            commands = r1.readlines()
    except:
        print(f'Error: {script_path}')
        sys.exit(1)

    finish_command = list()
    random.shuffle(commands)

    # 创建进程池，最多同时运行5个进程
    with multiprocessing.Pool(processes=3) as pool:
        # 运行所有的命令
        pool.map(run_command, commands)