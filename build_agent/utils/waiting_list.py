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
import os

class WaitingListItem:
    def __init__(self, package_name, version_constraints, tool, timeouterror=0, othererror=0):
        self.package_name = package_name
        self.version_constraints = version_constraints if version_constraints else ''
        self.tool = tool
        self.timeouterror = timeouterror
        self.othererror = othererror

class WaitingList(EasyList):
    
    # 添加元素，往队尾
    # 参数: (package_name, version_constraints, tool)三元组，conflict_list冲突列表，如果有冲突则添加到这里
    # 如果添加进入waiting list，则输出True，如果添加进入conflict list，则输出False
    def add(self, package_name, version_constraints, tool, conflict_list, timeouterror=0, othererror=0):
        if self.index_of(package_name, tool) != -1:
            print(f"'{package_name}' (using {tool} to download) has been in waiting list. Therefore, it is about to add it to conflict list...")
            conflict_list.add(package_name, version_constraints, tool)
            return False
        item = WaitingListItem(package_name, version_constraints, tool, timeouterror, othererror)
        super().add(item)
        msg = f"'{package_name}{version_constraints if version_constraints else ''}' (using {tool} to download) has been added into the waiting list. If you have multiple elements to add to the waitinglist, you can use && to connect multiple `waitinglist add` statements and surround them with ```bash and ```. Please make sure to write the complete statements; we will only recognize complete statements. Do not use ellipses or other incomplete forms."
        print(msg)
        return True
        
    # 从队首取出第一个元素
    def pop(self):
        pop_item = super().pop(0)
        if pop_item:
            version_constraints = pop_item.version_constraints if pop_item.version_constraints else ''
            msg = f"'{pop_item.package_name}{version_constraints}' has been removed from the waiting list."
        else:
            msg = 'There are no elements pending download in the waiting list.'
        print(msg)
        return pop_item
    
    # 输入package_name和tool，返回对应元素下标，如果都没有，则返回-1
    def index_of(self, package_name, tool):
        package_name = package_name if package_name else ''
        for item in self.items:
            if (item.package_name.strip() if item.package_name else '') == package_name.strip() and item.tool.strip() == tool.strip():
                return super().index_of(item)
        return -1
    
    def clear(self):
        super().clear()
        print(f'Success clear all the items of waitinglist.')

    def replace(self, package_name, tool, confirmed_constraints):
        confirmed_item = WaitingListItem(package_name, confirmed_constraints, tool)
        index = self.index_of(package_name, tool)
        if index == -1:
            if not confirmed_constraints:
                command_msg = f'waitinglist add -p {package_name} -t {tool}'
            else:
                command_msg = f'waitinglist add -p {package_name} -v {confirmed_constraints.replace(" ", "")} -t {tool}'
            msg = f'''The {tool} required for downloading '{package_name}' was not originally in the waiting list. If you need to add '{package_name}{confirmed_constraints if confirmed_constraints else ''}' to the waiting list, please enter the command:
`{command_msg}`
'''
        else:
            super().replace(index, confirmed_item)
            msg = f"In the waiting list, the version of '{package_name}' has been updated or confirmed as '{confirmed_constraints}'."
        print(msg)

    # 以文件的形式添加，如将requirements.txt的条目都加入，输入waitinglist addfile /repo/requirements.txt
    # 参数：file_path路径，errorformat_list如果判断格式不正确则加入errorformat_list
    def addfile(self, file_path, conflict_list):
        if not os.path.exists(file_path):
            print(f'Error, the file {file_path} does not exist! Please re-enter the file path and ensure that this file can be found.')
            return False
        if 'requirement' not in file_path.lower():
            print('Please ensure that the file you add is like requirements.txt, where each entry is in the format <package_name><version_constraints>, and nothing else is included. If there are other elements, you can use waitinglist add multiple times.')
            return False
        if os.path.isdir(file_path):
            print(f'Error, the path {file_path} is not a file, but a directory!')
            return False
        with open(file_path, 'r') as r1:
            items = r1.readlines()
        successful_res = list()
        conflict_res = list()

        for item in items:
            item = item.split('#')[0].strip()
            if len(item.strip()) > 0 and len(item) > 0:
                package_name, version_constraints = parse_requirements(item)
                if package_name:
                    res = self.add(package_name, version_constraints, 'pip', conflict_list)
                    if res:
                        successful_res.append(item)
                    else:
                        conflict_res.append(item)
                # else:
                #     errorformat_list.add(item)
                #     errorformat_res.append(item)
        file_path = '/' + '/'.join(file_path.split('/')[-2:])
        if len(successful_res) > 0:
            print(f'The following entries in "{file_path}" have been successfully added to the waiting list:')
            for sl in successful_res:
                print(sl)
        else:
            print(f'No entries in "{file_path}" have been added to the waiting list.')
        
        if len(conflict_res) > 0:
            print(f'The following entries in "{file_path}" are correctly formatted, but they already exist in the original waiting list. Therefore, they have been temporarily placed in the conflict list. Please handle them later.')
            for cl in conflict_res:
                print(cl)
        else:
            print(f'There are no correctly formatted entries in "{file_path}" that have been placed in the conflict list.')
        
        # if len(errorformat_res) > 0:
        #     print(f"The following items in '{file_path}' don't meet the standard, the correct format is package_name followed by version_constraints(if no version_constraints, it means download the latest version), such as 'numpy==2.1' or 'numpy>1.0,<1.2', 'numpy' and so on. They are added into errorformat list, please solve it later. If you want to clear all the items in the errorformatlist, you can execute `errorformatlist clear`.")
        #     for el in errorformat_res:
        #         print(el)
        # else:
        #     print(f'There are no incorrectly formatted entries in "{file_path}".')
        return True

    # 输出当前waitinglist情况介绍
    def get_message(self):
        msg = ''
        for i in range(super().size()):
            item = super().get(i)
            if not item:
                break
            msg += item.package_name
            msg += item.version_constraints if item.version_constraints else ''
            msg += f' (using {item.tool} to download)'
            # msg += f' timed out {item.timeouterror} times during the past downloads. If {3 - item.timeouterror} more download timeouts occur, it will be abandoned.'
            # msg += f'  And there have already been {item.othererror} download errors due to non-timeout reasons in the past. If {3 - item.othererror} more non-timeout errors occur, it will be abandoned.'
            msg += '\n'
        msg = msg.strip()
        waitinglist_msg = ''
        mark_fence = '*'*100
        if super().size() > 0:
            waitinglist_msg = f'''There are {super().size()} third-party libraries in the waiting list, which will be downloaded together.
The following shows the first all items in the waiting list.
{mark_fence}
{msg}
{mark_fence}

If you need to download them, please enter the command `download`.
'''
        else:
            waitinglist_msg = 'There are no third-party libraries pending download in the waiting list.'
        print(waitinglist_msg)

if __name__ == '__main__':
    from conflict_list import ConflictList
    # from errorformat_list import ErrorformatList
    # errorformat_list = ErrorformatList()
    waiting_list = WaitingList()
    conflict_list = ConflictList()
    waiting_list.addfile('test_requirements.txt', conflict_list)
    print()
    waiting_list.get_message()
    # waiting_list.add('numpy', '>2.0,<3.0', 'pip', conflict_list)
    # waiting_list.add('pytorch', None, 'pip', conflict_list)
    # waiting_list.add('numpy', '==1.2', 'pip', conflict_list)
    # waiting_list.replace('pytorch', 'apt', '>2.3.0')
    # waiting_list.replace('pytorch', 'pip', '>2.3.0')
    # waiting_list.pop()
    # waiting_list.get_message()