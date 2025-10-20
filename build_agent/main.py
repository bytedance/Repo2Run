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


import argparse
import json
import multiprocessing
import threading
import time
import os
import sys
from datetime import datetime, timedelta
from utils.sandbox import Sandbox
from agents.configuration import Configuration
import subprocess
from utils.waiting_list import WaitingList
from utils.conflict_list import ConflictList
from utils.integrate_dockerfile import integrate_dockerfile
import ast
import shutil

def move_files_to_repo(source_folder):
    # 定义目标文件夹所处的路径
    target_folder = os.path.join(source_folder, 'repo_inner_directory_long_long_name_to_avoid_duplicate')
    
    # 检查目标文件夹是否存在，不存在则创建
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    
    # 遍历源文件夹中的所有文件和文件夹
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)
        
        # 跳过目标文件夹
        if item == 'repo_inner_directory_long_long_name_to_avoid_duplicate':
            continue
        
        # 移动文件或文件夹到目标文件夹
        shutil.move(item_path, os.path.join(target_folder, item))

    os.rename(target_folder, os.path.join(source_folder, 'repo'))

# 下载repo到utils/repo文件夹，并且去除最外层文件夹，去除可能存在的Dockerfile
def download_repo(root_path, full_name, sha):
    if len(full_name.split('/')) != 2:
        raise Exception("full_name Wrong!!!")
    author_name = full_name.split('/')[0]
    repo_name = full_name.split('/')[1]
    if not os.path.exists(f'{root_path}/utils/repo/{author_name}/{repo_name}'):
        os.system(f'mkdir -p {root_path}/utils/repo/{author_name}/{repo_name}')
    download_cmd = f"git clone https://github.com/{full_name}.git"
    subprocess.run(download_cmd, cwd=f'{root_path}/utils/repo/{author_name}', check=True, shell=True)
    move_files_to_repo(f'{root_path}/utils/repo/{author_name}/{repo_name}')
    if os.path.exists(f"{root_path}/utils/repo/{author_name}/{repo_name}/repo/Dockerfile") and not os.path.isdir(f"{root_path}/utils/repo/{author_name}/{repo_name}/repo/Dockerfile"):
        rm_dockerfile_cmd = f"rm -rf {root_path}/utils/repo/{author_name}/{repo_name}/repo/Dockerfile"
        subprocess.run(rm_dockerfile_cmd, check=True, shell=True)
    pipreqs_cmd = "pipreqs --savepath=.pipreqs/requirements_pipreqs.txt --force"
    os.system(f'mkdir {root_path}/utils/repo/{author_name}/{repo_name}/repo/.pipreqs')
    try:
        pipreqs_warnings = subprocess.run(pipreqs_cmd, cwd=f"{root_path}/utils/repo/{author_name}/{repo_name}/repo", check=True, shell=True, capture_output=True)
        with open(f'{root_path}/utils/repo/{author_name}/{repo_name}/repo/.pipreqs/pipreqs_output.txt', 'w') as w1:
            w1.write(pipreqs_warnings.stdout.decode('utf-8'))
        with open(f'{root_path}/utils/repo/{author_name}/{repo_name}/repo/.pipreqs/pipreqs_error.txt', 'w') as w2:
            w2.write(pipreqs_warnings.stderr.decode('utf-8'))
    except:
        pass

    checkout_cmd = f"git checkout {sha}"
    subprocess.run(checkout_cmd, cwd=f'{root_path}/utils/repo/{author_name}/{repo_name}/repo', capture_output=True, shell=True)

    # x = subprocess.run('git log -1 --format="%H"', cwd=f'{root_path}/utils/repo/{author_name}/{repo_name}/repo', capture_output=True, shell=True)
    with open(f'{root_path}/output/{author_name}/{repo_name}/sha.txt', 'w') as w1:
        w1.write(sha)

def main():
    # subprocess.run('docker rm -f $(docker ps -aq)', shell=True)
    parser = argparse.ArgumentParser(description='Run script with repository full name as an argument.')
    parser.add_argument('--full_name', type=str, help='The full name of the repository (e.g., user/repo).')
    parser.add_argument('--sha', type=str, help='sha')
    parser.add_argument('--root_path', type=str, help='root path')
    parser.add_argument('--llm', type=str, default='gpt-4o-2024-05-13', help='base LLM name')

    args = parser.parse_args()

    waiting_list = WaitingList()
    conflict_list = ConflictList()

    root_path = args.root_path

    if not os.path.isabs(root_path):
        root_path = os.path.abspath(root_path)

    full_name = args.full_name
    sha = args.sha
    llm = args.llm
    print(full_name)
    # if os.path.exists(f'{root_path}/{full_name}/TIMEOUT'):
    #     sys.exit(123)
    print(sha)
    if os.path.exists(f'{root_path}/output/{full_name}/patch'):
        rm_cmd = f"rm -rf {root_path}/output/{full_name}/patch"
        subprocess.run(rm_cmd, shell=True, check=True)
    if not os.path.exists(f'{root_path}/output/{full_name.split("/")[0]}/{full_name.split("/")[1]}'):
        subprocess.run(f'mkdir -p {root_path}/output/{full_name.split("/")[0]}/{full_name.split("/")[1]}', shell=True)
    if os.path.exists(f'{root_path}/utils/repo/{full_name}'):
        init_cmd = f"rm -rf {root_path}/utils/repo/{full_name} && mkdir -p {root_path}/utils/repo/{full_name}"
    else:
        init_cmd = f"mkdir -p {root_path}/utils/repo/{full_name}"
    subprocess.run(init_cmd, check=True, shell=True)
    
    def timer():
        time.sleep(3600*2)  # 等待2h
        print("Timeout for 2 hour!")
        os._exit(1)  # 强制退出程序

    # 启动定时器线程
    timer_thread = threading.Thread(target=timer)
    timer_thread.daemon = True
    timer_thread.start()

    download_repo(root_path, full_name, sha)

    trajectory = []

    configuration_sandbox = Sandbox("python:3.10", full_name, root_path)
    configuration_sandbox.start_container()
    configuration_agent = Configuration(configuration_sandbox, 'python:3.10', full_name, root_path, 100)
    msg, outer_commands = configuration_agent.run('/tmp', trajectory, waiting_list, conflict_list)
    with open(f'{root_path}/output/{full_name.split("/")[0]}/{full_name.split("/")[1]}/track.json', 'w') as w1:
        w1.write(json.dumps(msg, indent=4))
    commands = configuration_sandbox.stop_container()
    with open(f'{root_path}/output/{full_name.split("/")[0]}/{full_name.split("/")[1]}/inner_commands.json', 'w') as w2:
        w2.write(json.dumps(commands, indent=4))
    with open(f'{root_path}/output/{full_name.split("/")[0]}/{full_name.split("/")[1]}/outer_commands.json', 'w') as w3:
        w3.write(json.dumps(outer_commands, indent=4))
    try:
        integrate_dockerfile(f'{root_path}/output/{full_name}')
        msg = f'Generate success!'
        with open(f'{root_path}/output/{full_name}/track.txt', 'a') as a1:
            a1.write(msg + '\n')
    except Exception as e:
        msg = f'integrate_docker failed, reason:\n {e}'
        with open(f'{root_path}/output/{full_name}/track.txt', 'a') as a1:
            a1.write(msg + '\n')

if __name__ == '__main__':
    try:
        subprocess.run('docker rmi $(docker images --filter "dangling=true" -q) > /dev/null 2>&1', shell=True)
    except:
        print("No dangling images")
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Spend totally {elapsed_time}.')