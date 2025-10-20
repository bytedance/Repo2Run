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


import openai
import time

def get_llm_response(model: str, messages, temperature = 0.0, n = 1, max_tokens = 1024):
    max_retry = 5
    count = 0
    while count < max_retry:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                n=n,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content, response.usage
        except Exception as e:
            print(f"Error: {e}")
            count += 1
            time.sleep(3)
    return None, None