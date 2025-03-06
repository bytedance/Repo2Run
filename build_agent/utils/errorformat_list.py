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

from easylist import EasyList
from parser.parse_requirements import parse_requirements

class ErrorformatListItem:
    def __init__(self, error_string):
        if not isinstance(error_string, str):
            print("ErrorformatListItem needs string to input!\n")
        if len(error_string) == 0:
            print("ErrorformatListItem does not accept empty strings.\n")
        if '\n' in error_string.strip():
            print("ErrorformatListItem needs only one line to input!\n")
        # max_length = 100
        # if len(error_string) > max_length:
        #     # raise Exception(f"ErrorformatListItem requires a string input with a length less than {max_length}.\n")
        #     print(f"ErrorformatListItem requires a string input with a length less than {max_length}.\n")
        #     return
        self.error_string = str(error_string)

class ErrorformatList(EasyList):
    
    # 添加元素，往队尾
    def add(self, error_string):
        item = ErrorformatListItem(error_string)
        super().add(item)
        print(f"The entry with formatting errors, '{error_string}', has been added to the errorformat list.\n")
    
    # 从队首取出第一个元素
    def pop(self):
        pop_item = super().pop(0)
        if pop_item:
            error_string = pop_item.error_string
            msg = f"Errorformat string: '{error_string}', has been removed from the errorformat list.  If you want to clear all the items, you can execute `errorformatlist clear`.\n"
        else:
            msg = 'The errorformat list is empty; there are currently no entries with formatting errors that need to be processed.\n'
        print(msg)
        return pop_item
    
    def solve(self, waiting_list, conflict_list, entries):
        first_item = self.pop()
        for entry in entries:
            package_name, version_constraints = parse_requirements(entry)
            if not package_name:
                self.add(entry)
            else:
                waiting_list.add(package_name, version_constraints, 'pip', conflict_list)
        print(f'Success solve "{entries}"...')
        # self.get_message()
    
    def clear(self):
        super().clear()
        print(f'Success clear all the items of errorformatlist.')

    # 输出当前errorformatlist情况
    def get_message(self):
        if super().size() > 0:
            errorformatlist_msg = super().get(0).error_string
            waitinglist_msg = f'''There are {super().size()} formatting error entries pending in the errorformat list. You need to address each of these error entries one by one, adding the necessary elements to the waiting list. If you believe an entry is irrelevant to the third-party libraries to be downloaded, you can also choose to discard this formatting error entry and remove it from the errorformat list.
Below is the first formatting error you need to address. Please determine if this entry is related to the third-party libraries that need to be downloaded. If it is, adjust it to the format `package_name[version_constraints]`, such as `numpy==1.2.0` or `numpy>=2.0,<3.0`, or simply `numpy` (not adding version_constraints implies downloading the latest version by default).
{errorformatlist_msg}

If you want to extract it into the correctly formatted third-party library that needs to be downloaded, please enter the following command:
`errorformatlist solve "package_name[version_constraints]" ...`
If you need to submit an entry after adjusting its format, be sure to use `errorformatlist solve` followed by the structure "package_name[version_constraints]" enclosed in double quotes, which can list multiple entries. If there is only `errorformatlist solve` without any following entries, it indicates that no third-party libraries or their version constraints can be extracted or adjusted from the formatting error string.

Here are a few legal examples:
1. `errorformatlist solve "numpy==1.2.0"`
Explanation: This indicates that the entry numpy==1.2.0 has been extracted.
*Note*: "numpy==1.2.0" must be enclosed in double quotes.
2. `errorformatlist solve "numpy" "matplotlib>=2.0"`
Explanation: This indicates that two entries have been extracted: "numpy" (with no additional constraints, implying the latest version is to be downloaded by default) and "matplotlib>=2.0".
*Note*: If multiple entries are extracted, each must be enclosed in double quotes.
3. `errorformatlist solve`
Explanation: No entries follow "errorformatlist solve", indicating that no information about the third-party libraries to be downloaded can be extracted from this formatting error element.
4. `errorformatlist clear`
Explanation: Clear all the items in the errorformat list.
*Note*: In this case, no additional elements or spaces should be added afterward.
*Note*: If you want to clear all the items, you can execute `errorformatlist clear`.
*Note*: You must address every formatting error element in the errorformatlist before proceeding to other tasks.
'''
        else:
            waitinglist_msg = 'There are no formatting error entries pending processing in the errorformatlist. You can perform other operations.\n'
        print(waitinglist_msg)
    

if __name__ == '__main__':
    errorformat_list = ErrorformatList()
    errorformat_list.add('pytorch>3.9d python=3.7')
    errorformat_list.add('errormatd 2')
    errorformat_list.add('pytorch>?+d;+12')
    errorformat_list.pop()
    errorformat_list.get_message()
