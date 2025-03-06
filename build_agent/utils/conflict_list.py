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

class ConflictListItem:
    def __init__(self, package_name, version_constraint, tool):
        self.package_name = package_name
        self.version_constraints = list()
        self.version_constraints.append(version_constraint)
        self.tool = tool

    def add_constraints(self, extra_constraints):
        original_length = len(self.version_constraints)
        self.version_constraints.append(extra_constraints)
        # 如果有几种constraints，则去重并随机排
        self.version_constraints = list(set(self.version_constraints))
        now_length = len(self.version_constraints)
        if original_length == now_length:
            print(f"The version constraint '{extra_constraints}' you want to add is redundant; it already exists in the '{self.package_name}'(using {self.tool} to download) of the conflict list.")
        else:
            print(f"The version constraint '{extra_constraints}' has been successfully added into conflict list, serving as a potential version constraint for package '{self.package_name}'(using {self.tool} to download).")


class ConflictList(EasyList):
    # 往ConflictList中添加元素，如果没有相同的(package_name,tool)组合，则插入队尾，否则添加到相同的(package_name, tool)组合的constraits数组中
    def add(self, package_name, version_constraints, tool):
        index = self.index_of(package_name, tool)
        if index == -1:
            add_item = ConflictListItem(package_name, version_constraints, tool)
            super().add(add_item)
            print(f"The version constraint '{version_constraints}' has been successfully added into conflict list, serving as a potential version constraint for '{package_name}'(using {tool} to download).\n")
        else:
            add_item = super().get(index)
            add_item.add_constraints(version_constraints)
            super().replace(index, add_item)
            
    # 从队首取出第一个元素
    def pop(self):
        pop_item = super().pop(0)
        if pop_item:
            msg = f"'{pop_item.package_name}{pop_item.version_constraints}' has been removed from the conflict list, and there are {super().size()} remaining conflicts to be addressed in the conflict list.\n"
        else:
            msg = 'There are no conflicting entries left to be handled in the conflict list.\n'
        print(msg)
        return pop_item
    
    # 输入package_name和tool，返回对应元素下标，如果都没有，则返回-1
    def index_of(self, package_name, tool):
        for item in self.items:
            if item.package_name.strip() == package_name.strip() and item.tool.strip() == tool.strip():
                return super().index_of(item)
        return -1

    def solve(self, waiting_list, version_constraints, unchanged):
        first_item = self.pop()
        if not first_item:
            return
        version_constraints = version_constraints if version_constraints else ''
        if unchanged:
            print('The first item in the conflict list has been removed. If you have multiple elements to remove from the conflict list, you can use && to connect multiple `conflictlist solve` statements and surround them with ```bash and ```. Please make sure to write the complete statements; we will only recognize complete statements. Do not use ellipses or other incomplete forms.')
        else:
            index = waiting_list.index_of(first_item.package_name.strip(), first_item.tool)
            if index == -1:
                raise Exception(f"{first_item.package_name}(downloaded using {first_tool}) is not found in the waiting list.")
            waiting_item = waiting_list.get(index)
            if version_constraints.strip() not in first_item.version_constraints and version_constraints.strip() != waiting_item.version_constraints:
                print('The "version_constraints" you entered is neither in the original waiting list nor in the conflict list options. Please re-enter the command.')
                # self.get_message(waiting_list)
                return
            waiting_item.version_constraints = version_constraints
            waiting_list.replace(first_item.package_name.strip(), first_item.tool, version_constraints)
            print('The first conflict has been successfully resolved. If you have multiple elements to remove from the conflict list, you can use && to connect multiple `conflictlist solve` statements and surround them with ```bash and ```. Please make sure to write the complete statements; we will only recognize complete statements. Do not use ellipses or other incomplete forms.')
            # waiting_list_constraints = waiting_list.get(index).version_constraints
            # self.get_message(waiting_list)
    
    def clear(self):
        super().clear()
        print(f'Success clear all the items of conflictlist.')

    # 输出当前conflictlist情况介绍，需要传入waiting_list对象
    def get_message(self, waiting_list):
        if super().size() > 0:
            # 获得第一个元素的信息
            first_item = super().get(0)
            first_package_name = first_item.package_name.strip()
            first_version_constraints = first_item.version_constraints
            constraints_msg = " or ".join([f'"{x}"' for x in first_version_constraints])
            first_tool = first_item.tool.strip()
            msg = f'package_name: {first_package_name}, version_constraints: {constraints_msg}, tools: {first_tool}'
            # 获得第一个元素在waiting list中的限制
            index = waiting_list.index_of(first_package_name.strip(), first_tool)
            if index == -1:
                raise Exception(f"{first_package_name}(downloaded using {first_tool}) is not found in the waiting list.")
            waiting_list_constraints = waiting_list.get(index).version_constraints
            waiting_list_constraints_msg = ''
            if waiting_list_constraints and len(waiting_list_constraints) > 0:
                waiting_list_constraints_msg = f'Its original constraint in the waiting list was "{waiting_list_constraints}".'
            else:
                waiting_list_constraints_msg = 'Originally, it has no version constraints in the waiting list, meaning the latest version to be downloaded by default.'
            conflictlist_msg = f'''There are {super().size()} conflicts pending in the conflict list. They need to be compared one by one with the third-party libraries in the waiting list that have the same package name and download tool but different version constraints. This is to determine the final version of the third-party library to download. You need to carefully compare the differences between them.
With a priority for those that have a fixed version (i.e., connected by '=='), select the most suitable version constraint.
If it's not possible to determine, you can also choose not to restrict the version, meaning to download the latest version of the software by default.
Below is the first conflict that needs to be resolved:
{msg}
{waiting_list_constraints_msg}

If you want to resolve this conflict and have finalized the version of "{first_package_name}" (downloaded using {first_tool}), please enter the command `conflictlist solve [version_cosntraints]`. This will remove the entry from the conflict list and update the version constraint of this entry in the waiting list.
The following command formats are legal:
1. `conflictlist solve`
Explanation: The standalone `conflictlist solve` command means not to impose any version constraints, i.e., to default to downloading the latest version of the third-party library. This will update the version constraint in the waiting list to be unrestricted.
2. `conflictlist solve -v "==2.0"`
Explanation: Adding -v followed by a version constraint enclosed in double quotes updates the version constraint in the waiting list to that specific range, such as "==2.0", meaning to take version 2.0.
3. `conflictlist solve -v ">3.0"`
Explanation: Similar to the command 2, this constraint specifies a version number greater than 3.0.
4. `conflictlist solve -u`
Explanation: Adding -u indicates giving up all the constraints in the conflict list while still retaining the constraints in the waiting list, i.e., not updating the constraints for that library in the waiting list.
5. `conflictlist clear`
Explanation: Clear all the items in the conflict list.

*Note*: The final chosen version constraint must either come from the options provided in the conflict list or retain the original constraints from the waiting list. If it is really uncertain, you can choose to enter conflictlist solve alone without specifying a version, to download the latest version. Additionally, under reasonable circumstances, prioritize selections that have a specific version constraint (i.e., constraints connected with ==).
*Note*: If you want to use the -v command to select a constraint from the conflict list, you need to enclose the constraint in double quotes.
'''
        else:
            conflictlist_msg = 'The conflict list is empty; there are currently no version constraint conflicts to be resolved.\n'
        print(conflictlist_msg)

if __name__ == '__main__':
    from waiting_list import WaitingList
    waiting_list = WaitingList()
    conflict_list = ConflictList()
    waiting_list.add('numpy', '>2.0,<3.0', 'pip', conflict_list)
    waiting_list.add('pytorch', '==3.1', 'pip', conflict_list)
    waiting_list.add('pytorch', None, 'pip', conflict_list)
    waiting_list.add('pytorch', '==3.2', 'pip', conflict_list)
    waiting_list.replace('pytorch', 'apt', '>2.3.0')
    waiting_list.replace('pytorch', 'pip', '>2.3.0')
    waiting_list.get_message()
    print('-'*50+'CONFLICT_MSG'+'-'*50)
    conflict_list.add('numpy', '<3.0', 'pip')
    conflict_list.add('numpy', '==2.4.7', 'pip')
    conflict_list.add('matplotlib', '==1.0', 'pip')
    conflict_list.add('matplotlib', None, 'pip')
    conflict_list.get_message(waiting_list)
    conflict_list.solve(waiting_list, '==3.2', False)
    # conflict_list.get_message(waiting_list)
    waiting_list.get_message()