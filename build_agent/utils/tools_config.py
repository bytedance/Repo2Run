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


from enum import Enum
class Tools(Enum):
    # apt_download = {
    #     "command": "apt_download -p package_name [-v package_version]",
    #     "description": "Use apt-get to download a third-party system library, ensuring that this library is available in the system's package repositories."
    # }
    # pip_download = {
    #     "command": "pip_download -p package_name [-v package_version]",
    #     "description": "Use pip to download third-party libraries in the current Python environment."
    # }
    waiting_list_add = {
        "command": "waitinglist add -p package_name [-v version_constraints] -t tool",
        "description": "Add item into waiting list. If no 'version_constraints' are specified, the latest version will be downloaded by default."
    }
    waiting_list_add_file = {
        "command": "waitinglist addfile file_path",
        "description": "Add all entries from a file similar to requirements.txt format to the waiting list."
    }
    waiting_list_clear = {
        "command": "waitinglist clear",
        "description": "Used to clear all the items in the waiting list."
    }
    waiting_list_show = {
        "command": "waitinglist show",
        "description": "Used to show all the items in the waiting list."
    }
    conflict_solve_constraints = {
        "command": 'conflictlist solve -v "[version_cosntraints]"',
        "description": "Resolve the conflict for the first element in the conflict list, and update the version constraints for the corresponding package_name and tool to version_constraints. If no 'version_constraints' are specified, the latest version will be downloaded by default."
    }
    conflict_solve_u = {
        "command": "conflictlist solve -u",
        "description": "Keep the original version constraint that exists in the waiting list, and discard the other version constraints with the same name and tool in the conflict list."
    }
    conflict_clear = {
        "command": "conflictlist clear",
        "description": "Used to clear all the items in the conflict list."
    }
    conflict_list_show = {
        "command": "conflictlist show",
        "description": "Used to show all the items in the conflict list."
    }
    # errorformat_solve = {
    #     "command": 'errorformatlist solve ["package_name[version_constraints]" ...]',
    #     "description": "Used to extract the first element from the errorformat list that can be added to the waiting list. The entries must be enclosed in double quotes and can list multiple entries. If you run `errorformatlist solve` alone, it indicates that no third-party libraries need to be extracted for download from this format error entry."
    # }
    # errorformat_clear = {
    #     "command": 'errorformatlist clear',
    #     "description": "Used to clear all the items in the errorformat list."
    # }
    download = {
        "command": 'download',
        "description": "Download all pending elements in the waiting list at once."
    }
    runtest = {
        "command": 'runtest',
        "description": "Check if the configured environment is correct."
    }
    poetryruntest = {
        "command": 'poetryruntest',
        "description": "Check if the configured environment is correct in poetry environment! If you want to run tests in poetry environment, run it."
    }
    runpipreqs = {
        "command": 'runpipreqs',
        "description": "Generate 'requirements_pipreqs.txt' and 'pipreqs_output.txt' and 'pipreqs_error.txt'."
    }
    # rollback = {
    #     "command": 'rollback',
    #     "description": "Manually revert to the previous state, which means discarding the last successfully executed command. Note that you can only revert once and cannot continuously go back."
    # }
    change_python_version = {
        "command": 'change_python_version python_version',
        "description": "Switching the Python version in the Docker container will forgo any installations made prior to the switch. The Python version number should be represented directly with numbers and dots, without any quotation marks."
    }
    change_base_image = {
        "command": 'change_base_image base_image',
        "description": "Switching the base image in the Docker container will forgo any installations made prior to the switch. The base image does not necessarily have to follow the format 'python:<Python version>'. Preferably, specify it in the form of 'base_image_name:tag', such as 'pytorch/pytorch:1.10.0-cuda11.1-cudnn8-runtime'. If no tag is provided, it defaults to 'latest'. No any quotation marks are needed."
    }
    clear_configuration = {
        "command": 'clear_configuration',
        "description": "Reset all the configuration to the initial setting of python:3.10."
    }