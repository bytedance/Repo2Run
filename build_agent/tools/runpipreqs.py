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
import os
warnings.simplefilter('ignore', FutureWarning)

def runpipreqs():
    if os.path.exists('/repo/requirements_pipreqs.txt') and os.path.exists('/repo/pipreqs_output.txt') and os.path.exists('/repo/pipreqs_error.txt'):
        print('The runpipreqs command executed successfully and has successfully generated "requirements_pipreqs.txt", "pipreqs_output.txt", and "pipreqs_error.txt" in /repo.')
    elif not os.path.exists('/repo/.pipreqs') or not os.path.exists('/repo/.pipreqs/pipreqs_error.txt') or not os.path.exists('/repo/.pipreqs/pipreqs_output.txt') or not os.path.exists('/repo/.pipreqs/requirements_pipreqs.txt'):
        raise Exception("The previous program encountered an error. Please use `pip install pipreqs` to generate 'requirements_pipreqs.txt' yourself.")
    else:
        result1 = subprocess.run('cp /repo/.pipreqs/pipreqs_error.txt /repo', shell=True, text=True, capture_output=True)
        result2 = subprocess.run('cp /repo/.pipreqs/pipreqs_output.txt /repo', shell=True, text=True, capture_output=True)
        result3 = subprocess.run('cp /repo/.pipreqs/requirements_pipreqs.txt /repo', shell=True, text=True, capture_output=True)
        if result1.returncode != 0 or result2.returncode != 0 or result3.returncode != 0:
            raise Exception("The previous program encountered an error. Please use `pip install pipreqs` to generate 'requirements_pipreqs.txt' yourself.")
        else:
            print('The runpipreqs command executed successfully and has successfully generated "requirements_pipreqs.txt", "pipreqs_output.txt", and "pipreqs_error.txt" in /repo.')
    
if __name__ == '__main__':
    runpipreqs()