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


class EasyList:
    def __init__(self, initial_items=None):
        """初始化一个新的 EasyList，可以选择提供初始元素列表"""
        self.items = initial_items if initial_items is not None else list()

    def add(self, item):
        """向列表添加一个元素"""
        self.items.append(item)

    def remove(self, item):
        """从列表中移除一个元素"""
        if item in self.items:
            self.items.remove(item)

    def get(self, index):
        """获取指定索引的元素"""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None  # 如果索引超出范围，返回 None

    def size(self):
        """返回列表的大小"""
        return len(self.items)

    def clear(self):
        """清空列表"""
        self.items = []

    def sort(self):
        """对列表进行排序"""
        self.items.sort()

    def reverse(self):
        """将列表中的元素顺序翻转"""
        self.items.reverse()

    def contains(self, item):
        """检查列表是否包含某个元素"""
        return item in self.items

    def extend(self, other):
        """扩展列表，添加另一个列表中的所有元素"""
        self.items.extend(other)

    def index_of(self, item):
        """返回元素在列表中的索引，如果不存在则返回 -1"""
        try:
            return self.items.index(item)
        except ValueError:
            return -1

    def insert(self, index, item):
        """在指定索引位置插入一个新元素"""
        self.items.insert(index, item)

    def pop(self, index=-1):
        """移除并返回指定位置的元素，默认为最后一个"""
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def replace(self, index, item):
        """替换指定索引位置的元素，如果索引有效"""
        if 0 <= index < len(self.items):
            self.items[index] = item
        else:
            print("Index out of bounds") 

    def __str__(self):
        """返回列表的字符串表示形式"""
        return str(self.items)
    