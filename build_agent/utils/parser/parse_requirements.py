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
# 功能：解析python依赖项
# 输入：python依赖项，格式为package_name[version_constraints]
# 输出：解析完成的元组，格式为(package_name, version_constraints)，如果没有写version_constraints，则为None，如果输入字符串格式错误，则package_name与version_constraints均为None
def parse_requirements(input_string):
    # 去除注释部分
    input_string = input_string.split('#')[0].strip()
    
    # 更新后的正则表达式
    pattern = r'^([\w\-_\.]+(\[[\w\-,_\.]+\])?)\s*((?:[><=!~]{1,2}\s*[\d\w\.\-\+]+(?:\s*,\s*)?)*)$'
    
    matches = re.match(pattern, input_string)
    
    if matches:
        package_name = matches.group(1)
        version_constraints = matches.group(3).strip() if matches.group(3) else None
        return package_name, version_constraints
    else:
        return None, None

if __name__ == '__main__':
    # 测试
    test_cases = [
        "numpy>2.0  <3.0",
        "numpy > 2.0, < 3.0",
        "numpy>=1.18,<1.19",
        "pandas==1.1.4",
        "scikit-learn!=0.20.3",
        "tensorflow >=2.2.0, !=2.5.0",
        "opentelemetry-instrumentation-celery==0.26b1",
        "opentelemetry-semantic-conventions==0.26b1",
        "opentelemetry-instrumentation-elasticsearch==0.26b1",
        "typing_extensions==3.7.4.3",
        "blueapps[opentelemetry]==4.4.2"
    ]

    for test in test_cases:
        print(parse_requirements(test))
