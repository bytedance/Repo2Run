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


import pytest
from basic_ops import add, subtract, multiply, divide, power

def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2

def test_subtract():
    assert subtract(10, 5) == 4
    assert subtract(-1, 1) == -2
    assert subtract(-1, -1) == 0

def test_multiply():
    assert multiply(3, 5) == 15
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(-10, 2) == -5

    with pytest.raises(ValueError):
        divide(10, 0)

def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(-2, 2) == 4