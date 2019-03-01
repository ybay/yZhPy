#!/usr/bin/python
# -*- coding: utf-8 -*-

"""zhpy 关键字转换库

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007~ Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


# 通用关键字库
#: 在访问 WordDict 之前始终运行注释器
worddict = {}
#: 繁体中文关键词库
twdict = {}
#: 简体中文关键字库
cndict = {}

class ZhpyPlugin(object):
    """
    基本插件类
    """
    pass


def revert_dict(lang_dict):
    """从输入字典生成反向字典

    >>> revert_dict({'a':'1', 'b':'2'})
    {'1': 'a', '2': 'b'}
    """
    rev_dict = {}
    dict_keys = lang_dict.keys()
    dict_keys.reverse()
    #map(rev_dict.update, map(lambda i: {lang_dict[i]:i}, dict_keys))
    for i in dict_keys:
        rev_dict.update({lang_dict[i]:i})
    return rev_dict
