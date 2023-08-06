# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 20:41:00 2020

@author: yonder_sky
"""

# 基于ndarray的数据表类工具库，春秋迭代，yondersky@126.com，2020-11-27
# 更新日期：2022-02-15

import copy
import numpy as np
import pandas as pd
from bisect import bisect
from pandas import DataFrame, Series

from arraytool.pytool import ExpandSize, \
    IsArray, IsBool, IsDataFrame, IsIndex, IsInteger, IsIterable, \
    IsMultiIndex, IsSeries, IsSimpleIndex, IsSingleType, IsSingleType2, \
    IsSlice, NA, \
    TupleProduct, argsort, leftex, lexsort, rank, temap, which

# 1. 通用模块

# 1.1 通用参数

# ArrayFrame及其派生类、ArraySeries及其派生类、ArrayValueIndex类
AnsiDType = object
AnsiInitLen = 1
AnsiAutoExpand = True
AnsiExpandCount = 0
AnsiExpandRatio = 1.5
# ArraySeries及其派生类
AnsiSelfIndex = False
# ArrayFrame及其派生类
AnsiColInitLen = 1
AnsiColExpandCount = 1
AnsiColExpandRatio = 1.2
AnsiOrder = 'F'
# ArrayIndex及其派生类
AnsiPosDtype = np.int64

# 1.2 通用类

# 2021-04-15
class AssignManager:
    '''
    赋值计数类。
    '''
    
    # 2021-04-15
    def __init__(self, startID = 0):
        self.AssignID = startID
        return
    
    # 2021-04-15
    def AssignOnce(self):
        self.AssignID += 1
        return

# 2. 数据索引

# 2.1 数据索引基类

# 2021-02-14
class ArrayIndex:
    '''
    数据索引基类。
    【示例】
    >>> aindex = ArrayIndex(10)
    >>> aindex[True]
    0
    >>> aindex[1]
    1
    >>> aindex[slice(5)]
    slice(None, 5, None)
    >>> aindex[[2,3,6]]
    [2, 3, 6]
    
    >>> aindex.reindex(3)
    (array([3], dtype=int64), None)
    >>> aindex.reindex([3,8,13],'ignore')
    (array([3, 8], dtype=int64), None)
    >>> aindex.reindex([3,8,13],'ffill')
    (array([3, 8, 9], dtype=int64), None)
    >>> aindex.reindex([3,8,13],'keep')
    (array([ 3,  8, -1], dtype=int64), None)
    '''
    simple = True
    
    # 2021-02-14
    def __init__(self, length):
        self._ValidLen = length
        return
    
    # 2021-02-14
    def __getitem__(self, item):
        if IsBool(item):
            return 0 if item else None
        else:
            return item
    
    # 2021-07-17
    def __iter__(self):
        return range(len(self)).__iter__()
        
    # 2021-02-14
    def __len__(self):
        return self._ValidLen
        
    # 2021-02-14
    def __repr__(self):
        return 'ArrayIndex({:d})'.format(self._ValidLen)
    
    # 2021-07-14
    @property
    def empty(self):
        '''是否为空（只读属性）'''
        return len(self)==0
    
    # 2021-09-26
    @property
    def values(self):
        '''索引值数组（只读属性）'''
        return np.arange(self._ValidLen)
    
    # 2021-12-16
    def _ArgSort(self, ascending = True, na_option = 'last', method = 'first',
        key = None):
        '''下标排序（内部使用）'''
        return None
    
    # 2021-06-25
    def _GetPrep(self, item):
        '''
        取值预处理。
        【注】函数依次返回下标、是否简单类型。
        '''
        if IsBool(item):
            if item:
                return 0, True
            else:
                return None, None
        elif IsInteger(item):
            return item, True
        else:
            return item, False
    
    # 2021-06-17
    def _SetPrep(self, item):
        '''
        赋值预处理。
        【注】本函数依次返回下标、所需最大长度。
        '''
        if IsBool(item):
            if item:
                return 0, 1
            else:
                return None, None
        elif IsInteger(item):
            return item, item+1
        elif IsSlice(item):
            return item, item.stop
        else:
            if IsArray(item) and item.dtype is bool:
                item = np.where(item)[0]
            if len(item)==0:
                return None, None
            else:
                return item, max(item)+1
    
    # 2021-06-20
    def _UpdateLen(self, length):
        '''更新索引长度'''
        self._ValidLen = length
        return
    
    # 2021-09-25
    def copy(self):
        '''拷贝'''
        return ArrayIndex(self._ValidLen)
    
    # 2022-02-08
    def items(self):
        '''键值对遍历器'''
        for i in self:
            yield i, i
        return
    
    # 2022-02-08
    def keys(self):
        '''键遍历器'''
        return self.__iter__()

    # 2022-02-03
    def reindex(self, index, method = 'keep', dupl_method = 'all', 
        drop_index = False):
        '''
        索引。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        dupl_method - 重复值处理方式（本类无重复值，不适用此参数）
        drop_index - 返回值是否不返回索引（对本类无意义）
        '''
        if IsInteger(index):
            index = np.array([index],AnsiPosDtype)
        elif not IsArray(index):
            index = np.array(index,AnsiPosDtype)
        
        vlen = self._ValidLen
        if method=='keep':
            index[(index<0) | (index>=vlen)] = -1
        elif method=='ffill' or method=='pad':
            index[index>=vlen] = vlen-1
            index[index<0] = -1
        elif method=='bfill' or method=='backfill':
            index[index<0] = 0
            index[index>=vlen] = -1
        else:
            index = index[(index>=0) & (index<vlen)]
        return index, None
    
    # 2021-07-19
    def take(self, pos):
        '''切片'''
        return None

# 2.2 字典索引类

# 2021-02-14
class ArrayKeyIndex(ArrayIndex):
    '''
    字典索引类。
    【基类】ArrayIndex
    【示例】
    >>> akindex = ArrayKeyIndex(list('cbdfy'))
    >>> akindex['b']
    1
    >>> akindex[list('ddcc')]
    [2, 2, 0, 0]
    >>> akindex['b':'f']
    slice(1, 4, 1)
    >>> akindex['f':'b']
    slice(3, 0, -1)
    
    >>> akindex.reindex(list('abkfz'))
    (array([-1,  1, -1,  3, -1], dtype=int64), ['a', 'b', 'k', 'f', 'z'])
    >>> akindex.reindex(list('abkfz'),'ignore')
    (array([1, 3], dtype=int64), ['a', 'b', 'k', 'f', 'z'])
    >>> akindex.reindex(list('abkfz'),'ffill')
    (array([-1,  1,  3,  3,  4], dtype=int64), ['a', 'b', 'k', 'f', 'z'])
    >>> akindex.reindex(list('abkfz'),'bfill')
    (array([ 1,  1,  4,  3, -1], dtype=int64), ['a', 'b', 'k', 'f', 'z'])
    '''
    simple = False
    
    # 2021-02-14
    def __init__(self, key = None):
        if key is None:
            self._Keys = {}
        elif IsSingleType(key):
            self._Keys = {key:0}
        else:
            keydict = {}
            keycount = 0
            for k in key:
                if not k in keydict:
                    keydict[k] = keycount
                    keycount += 1
            self._Keys = keydict
        self._KeyList = list(self._Keys)
        self._SortedKeys = None
        super().__init__(len(self._KeyList))
        return
    
    # 2021-02-16
    def __getitem__(self, item):
        keys = self._Keys
        if IsSingleType(item):
            return keys[item] if item in keys else item
        elif IsSlice(item):
            istart = item.start
            istop = item.stop
            startNone = istart is None
            stopNone = istop is None
            if startNone and stopNone:
                return item
            rtstart = 0 if startNone else keys[istart]
            rtstop = len(self) if stopNone else keys[istop]
            rtstep = item.step
            if rtstep is None:
                rtstep = 1 if rtstart<=rtstop else -1
            if rtstep>0:
                return slice(rtstart,rtstop+1,rtstep)
            else:
                return slice(rtstart,rtstop-1,rtstep)
        else:
            return [keys[i] if i in keys else i for i in item]
    
    # 2021-05-30
    def __iter__(self):
        return self._Keys.__iter__()
    
    # 2021-06-27
    def __len__(self):
        return len(self._KeyList)
    
    # 2021-02-15
    def __repr__(self):
        return 'ArrayKeyIndex({})'.format(list(self._Keys.keys()))
    
    # 2021-09-26
    @property
    def values(self):
        '''索引值数组（重载只读属性）'''
        return np.array(self._KeyList)
    
    # 2021-12-16
    def _ArgSort(self, ascending = True, na_option = 'last', method = 'first',
        key = None):
        '''下标排序（内部使用，重载函数）'''
        values = self._KeyList
        if not key is None:
            values = key(values)
        return argsort(values,ascending,na_option,method)
    
    # 2021-07-17
    def _GetPrep(self, item):
        '''取值预处理（重载函数）'''
        keys = self._Keys
        if IsSingleType(item):
            return keys[item] if item in keys else item, True
        elif IsSlice(item):
            istart = item.start
            istop = item.stop
            startNone = istart is None
            stopNone = istop is None
            if startNone and stopNone:
                return item, False
            rtstart = 0 if startNone else keys[istart]
            rtstop = len(self) if stopNone else keys[istop]
            rtstep = item.stop
            if rtstep is None:
                rtstep = 1 if rtstart<=rtstop else -1
            if rtstep>0:
                return slice(rtstart,rtstop+1,rtstep), False
            else:
                return slice(rtstart,rtstop-1,rtstep), False
        else:
            return [keys[i] if i in keys else i for i in item], False
    
    # 2021-07-08
    def _SetPrep(self, item):
        '''
        赋值预处理（重载函数）。
        【注】对索引中不存在的项将追加索引项。
        '''
        keys = self._Keys
        keylist = self._KeyList
        keylen = len(keys)
        
        if IsSingleType(item):
            if item in keys:
                rti = keys[item]
                return rti, rti+1
            else:
                keys[item] = keylen
                keylist.append(item)
                return keylen, keylen+1
        
        if IsSlice(item):
            startNone = item.start is None
            stopNone = item.stop is None
            if startNone and stopNone:
                return item, item.stop
            rtstart = 0 if startNone else keys[item.start]
            rtstop = keylen if stopNone else keys[item.stop]
            rtstep = item.step
            if rtstep is None:
                rtstep = 1 if rtstart<=rtstop else -1
            if rtstep>0:
                return slice(rtstart,rtstop+1,rtstep), rtstop+1
            else:
                return slice(rtstart,rtstop-1,rtstep), rtstart
        
        rt = []
        maxlen = 0
        for i in item:
            if i in keys:
                rti = keys[i]
                rt.append(rti)
                maxlen = max(maxlen,rti+1)
            elif IsInteger(i):
                rt.append(i)
                maxlen = max(maxlen,i+1)
            else:
                keys[keylen] = i
                keylist.append(i)
                keylen += 1
                maxlen = keylen
        return rt, maxlen
    
    # 2022-02-04
    def _SetSortedKeys(self):
        ''''储存排序后的索引列表'''
        self._SortedKeys = sorted(self._Keys)
        return
    
    # 2021-07-10
    def append(self, item):
        '''追加索引项'''
        if item in self._Keys:
            return
        self._Keys[item] = len(self._Keys)
        self._KeyList.append(item)
        self._SortedKeys = None
        return
    
    # 2022-01-30
    def copy(self):
        '''拷贝（重载函数）'''
        return ArrayKeyIndex(self._KeyList)
    
    # 2022-02-08
    def items(self):
        '''键值对遍历器（重载函数）'''
        yield from self._Keys.items()
        return

    # 2022-02-08
    def keys(self):
        '''键遍历器（重载函数）'''
        return self._Keys.__iter__()
    
    # 2022-02-03
    def reindex(self, index, method = 'keep', dupl_method = 'all',
        drop_index = False):
        '''
        索引（重载函数）。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        dupl_method - 重复值处理方式（本类无重复值，不适用此参数）
        drop_index - 返回值是否不包含索引
        '''
        if IsSingleType2(index):
            index = np.array([index])
        keys = self._Keys
        
        if method=='keep':
            rt = [keys[i] if i in keys else -1 for i in index]
        elif method=='ffill' or method=='pad':
            sortedKeys = self._SortedKeys
            rt = []
            for i in index:
                if i in keys:
                    rt.append(keys[i])
                else:
                    if sortedKeys is None:
                        self._SetSortedKeys()
                        sortedKeys = self._SortedKeys
                    p = bisect(sortedKeys,i)-1
                    rt.append(keys[sortedKeys[p]] if p>=0 else -1)
        elif method=='bfill' or method=='backfill':
            sortedKeys = self._SortedKeys
            rt = []
            klen = len(keys)
            for i in index:
                if i in keys:
                    rt.append(keys[i])
                else:
                    if sortedKeys is None:
                        self._SetSortedKeys()
                        sortedKeys = self._SortedKeys
                    p = bisect(sortedKeys,i)
                    rt.append(keys[sortedKeys[p]] if p<klen else -1)
        else:
            rt = [keys[i] for i in index if i in keys]
        return np.array(rt,AnsiPosDtype), (None if drop_index else index)
    
    # 2021-06-09
    @temap
    def take(self, pos):
        '''切片（重载函数）'''
        return self._KeyList[pos]

# 2.3 数据索引类

# 2021-02-16
class ArrayValueIndex(ArrayIndex):
    '''
    数据索引类。
    【注】_assign_manager仅为内部使用参数，构造时无需提供。
    【示例】
    >>> avindex = ArrayValueIndex(list('cbdda'))
    >>> avindex['b']
    1
    >>> avindex[list('ddcc')]
    [2, 3, 2, 3, 0, 0]
    >>> avindex.take(slice(3))
    ArrayValueIndex(['c', 'b', 'd'])
    
    >>> avindex.reindex(list('ddaf'))
    (array([ 2,  3,  2,  3,  4, -1], dtype=int64), ['d', 'd', 'd', 'd', 'a', 'f'])
    >>> avindex.reindex(list('ddaf'),dupl_method='first')
    (array([ 2,  2,  4, -1], dtype=int64), ['d', 'd', 'a', 'f'])
    >>> avindex.reindex(list('ddaf'),dupl_method='last')
    (array([ 3,  3,  4, -1], dtype=int64), ['d', 'd', 'a', 'f'])
    '''
    simple = False
    
    # 2021-02-16
    def __init__(self, values, dtype = None, copy = False, init_len = None, 
        auto_expand = None, expand_count = None, expand_ratio = None,
        _assign_manager = None):
        # 拷贝构造
        if isinstance(values,ArrayValueIndex):
            values = values._Value
            if dtype is None:
                dtype = values.dtype
            if init_len is None:
                init_len = values._ValidLen
            if auto_expand is None:
                auto_expand = values._AutoExpand
            if expand_count is None:
                expand_count = values._ExpandCount
            if expand_ratio is None:
                expand_ratio = values._ExpandRatio
            _assign_manager = values._AssignManager
        
        if isinstance(values,ArraySeries) and not copy:
            self._Value = values
        else:
            self._Value = ArraySeries(
                data = values,
                dtype = dtype,
                copy = copy,
                init_len = init_len,
                auto_expand = auto_expand,
                expand_count = expand_count,
                expand_ratio = expand_ratio,
                _assign_manager = _assign_manager
            )
        
        self._Keys = {}
        self._MultiValues = False
        self._SortedKeys = None
        self._AssignID = -1
        return
    
    # 2021-03-28
    def __getitem__(self, item):
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        if IsSingleType2(item):
            if IsSlice(item):
                return item
            rt = self._Keys[item]
            return rt[0] if len(rt)==1 else rt
        else:
            rt = []
            for i in item:
                rt += self._Keys[i]
            return rt
    
    # 2021-03-28
    def __iter__(self):
        return self._Value.__iter__()
    
    # 2021-03-10
    def __len__(self):
        return len(self._Value)
    
    # 2021-03-28
    def __repr__(self):
        return 'ArrayValueIndex({})'.format(list(self._Value))
    
    # 2021-09-26
    @property
    def values(self):
        '''索引值数组（重载只读属性）'''
        return self._Value._ValidData
    
    # 2021-12-16
    def _ArgSort(self, ascending = True, na_option = 'last', method = 'first',
        key = None):
        '''下标排序（内部使用，重载函数）'''
        values = self._Value._ValidData
        if not key is None:
            values = key(values)
        return argsort(values,ascending,na_option,method)
    
    # 2021-07-17
    def _GetPrep(self, item):
        '''取值预处理（重载函数）'''
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        
        keys = self._Keys
        if IsSingleType2(item):
            if IsSlice(item):
                return item, False
            rt = keys[item]
            if len(rt)==1:
                return rt[0], True
            else:
                return rt, False
        else:
            rt = []
            for i in item:
                rt += keys[i]
            return rt, False
    
    # 2021-07-17
    def _SetPrep(self, item):
        '''赋值预处理（重载函数）'''
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        
        keys = self._Keys
        vlen = len(self._Value)
        appendList = []
        if IsSingleType2(item):
            if IsSlice(item):
                return item, item.stop
            if item in keys:
                rt = keys[item]
                if len(rt)==1:
                    rt = rt[0]
            else:
                rt = vlen
                appendList.append(item)
        else:
            rt = []
            for i in item:
                if i in keys:
                    rt += keys[i]
                else:
                    rt.append(vlen)
                    appendList.append(i)
                    vlen += 1
        if len(appendList)>0:
            self.append(appendList)
        return super()._SetPrep(rt)
    
    # 2022-02-04
    def _SetSortedKeys(self):
        ''''储存排序后的索引列表'''
        self._SortedKeys = sorted(self._Keys)
        return
    
    # 2021-03-10
    def _UpdateKey(self, start = None, end = None, remove = True):
        slen = len(self)
        if start is None:
            start = 0
        if end is None:
            end = slen
        if remove:
            if start==0 and end==slen:
                self._Keys = {}
                self._MultiValues = False
                self._SortedKeys = None
            else:
                try:
                    for i in range(start,end):
                        self._Keys[self._Value[i]].remove(i)
                except KeyError or ValueError:
                    pass
        
        i = start
        for v in self._Value._Data[start:end]:
            if v in self._Keys:
                self._Keys[v].append(i)
                self._MultiValues = True
            else:
                self._Keys[v] = [i]
                self._SortedKeys = None
            i += 1
        self._AssignID = self._Value._AssignManager.AssignID
        return
    
    # 2021-04-07
    def append(self, data, inplace = True):
        '''追加数据'''
        rt = self if inplace else self.copy()
        oldlen = len(rt)
        sync = rt._AssignID==rt._Value._AssignManager.AssignID
        if isinstance(data,ArrayValueIndex):
            data = data._Value
        rt._Value.append(data)
        if sync:
            rt._UpdateKey(oldlen,len(rt),False)
        else:
            rt._UpdateKey()
        return rt
    
    # 2022-01-30
    def copy(self):
        '''拷贝（重载函数）'''
        value = self._Value
        return ArrayValueIndex(
            values = value._ValidData,
            dtype = value.dtype,
            copy = True,
            auto_expand = value._AutoExpand,
            expand_count = value._ExpandCount,
            expand_ratio = value._ExpandRatio
        )
    
    # 2022-02-08
    def items(self):
        '''键值对遍历器（重载函数）'''
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        yield from self._Keys.items()
        return

    # 2022-02-08
    def keys(self):
        '''键遍历器（重载函数）'''
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        return self._Keys.__iter__()
    
    # 2022-02-04
    def reindex(self, index, method = 'keep', dupl_method = 'all',
        drop_index = False):
        '''
        索引（重载函数）。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含索引
        '''
        if self._AssignID!=self._Value._AssignManager.AssignID:
            self._UpdateKey()
        if IsSingleType2(index):
            index = np.array([index])
        keys = self._Keys
        klen = len(keys)
        rt = []
        
        if method in ('ffill','pad','bfill','backfill'):
            if self._SortedKeys is None:
                self._SetSortedKeys()
            sortedKeys = self._SortedKeys
        
        if dupl_method=='all':
            if self._MultiValues and not drop_index:
                rtindex = []
                for i in index:
                    if i in keys:
                        pos = keys[i]
                        plen = len(pos)
                        rt += pos
                        if plen>1:
                            rtindex += [i]*plen
                        else:
                            rtindex.append(i)
                    elif method=='keep':
                        rt.append(-1)
                        rtindex.append(i)
                    elif method=='ffill' or method=='pad':
                        p = bisect(sortedKeys,i)-1
                        if p>=0:
                            pos = keys[sortedKeys[p]]
                            plen = len(pos)
                            rt += pos
                            if plen>1:
                                rtindex += [i]*plen
                            else:
                                rtindex.append(i)
                        else:
                            rt.append(-1)
                            rtindex.append(i)
                    elif method=='bfill' or method=='backfill':
                        p = bisect(sortedKeys,i)
                        if p<klen:
                            pos = keys[sortedKeys[p]]
                            plen = len(pos)
                            rt += pos
                            if plen>1:
                                rtindex += [i]*plen
                            else:
                                rtindex.append(i)
                        else:
                            rt.append(-1)
                            rtindex.append(i)
            else:
                for i in index:
                    if i in keys:
                        rt += keys[i]
                    elif method=='keep':
                        rt.append(-1)
                    elif method=='ffill' or method=='pad':
                        p = bisect(sortedKeys,i)-1
                        if p>=0:
                            rt += keys[sortedKeys[p]]
                        else:
                            rt.append(-1)
                    elif method=='bfill' or method=='backfill':
                        p = bisect(sortedKeys,i)
                        if p<klen:
                            rt += keys[sortedKeys[p]]
                        else:
                            rt.append(-1)
                if drop_index:
                    rtindex = None
                else:
                    rtindex = self.take(rt) if method=='ignore' else index
        elif dupl_method=='last':
            for i in index:
                if i in keys:
                    rt.append(keys[i][-1])
                elif method=='keep':
                    rt.append(-1)
                elif method=='ffill' or method=='pad':
                    p = bisect(sortedKeys,i)-1
                    rt.append(keys[sortedKeys[p]][-1] if p>0 else -1)
                elif method=='bfill' or method=='backfill':
                    p = bisect(sortedKeys,i)
                    rt.append(keys[sortedKeys[p]][-1] if p<klen else -1)
            if drop_index:
                rtindex = None
            else:
                rtindex = self.take(rt) if method=='ignore' else index
        else:
            for i in index:
                if i in keys:
                    rt.append(keys[i][0])
                elif method=='keep':
                    rt.append(-1)
                elif method=='ffill' or method=='pad':
                    p = bisect(sortedKeys,i)-1
                    rt.append(keys[sortedKeys[p]][0] if p>0 else -1)
                elif method=='bfill' or method=='backfill':
                    p = bisect(sortedKeys,i)
                    rt.append(keys[sortedKeys[p]][0] if p<klen else -1)
            if drop_index:
                rtindex = None
            else:
                rtindex = self.take(rt) if method=='ignore' else index
        
        return np.array(rt,AnsiPosDtype), rtindex

    # 2021-05-07
    def take(self, indices, copy = False):
        '''切片（重载函数）'''
        series = self._Value
        return ArrayValueIndex(
            values = series[indices],
            dtype = series.dtype,
            copy = copy,
            auto_expand = series._AutoExpand,
            expand_count = series._ExpandCount,
            expand_ratio = series._ExpandRatio,
            _assign_manager = series._AssignManager if IsSlice(indices) \
                else None
        )

# 2.4 多重索引类

# 2021-09-26
class ArrayMultiIndex(ArrayIndex):
    '''
    多重索引类。
    【注】
    1. 由于本类的特殊设计，与DataFrame的多重索引不同，为便于向量化操作，本类的多
       重索引为列主序的，即传入索引的每一分量代表一个维度（索引列），最终构成多重索引。
    2. 若sort_codes参数为True，因子化时将对各分量进行排序。
    【示例】
    >>> l = [2,2,NA,1,1,1,NA,2,2,3]
    >>> l2 = list('aacceffsec')
    >>> amindex = ArrayMultiIndex([l,l2])
    >>> amindex[2,'a']
    [0, 1]
    '''
    simple = False
    
    # 2021-09-26
    def __init__(self, levels, names = None, sort_codes = False):
        self._SortCodes = sort_codes
        self._LevelNames = names
        self._Levels = []
        codes = []
        
        # 因子化
        if isinstance(levels,ArrayFrame):
            simpleIndex = type(levels.columns) is ArrayIndex
            values = levels._ValidData
            if names is None:
                names = levels.columns.values
                if not simpleIndex:
                    self._LevelNames = list(names)
            if simpleIndex:
                for n in names:
                    cs, ls = pd.factorize(values[:,n],sort_codes)
                    codes.append(cs)
                    self._Levels.append(ls)
            else:
                for n in names:
                    cs, ls = pd.factorize(
                        values[:,levels.columns[n]],sort_codes)
                    codes.append(cs)
                    self._Levels.append(ls)
        elif IsDataFrame(levels):
            simpleIndex = IsSimpleIndex(levels.columns)
            if names is None:
                names = levels.columns.values
                if not simpleIndex:
                    self._LevelNames = list(names)
            if simpleIndex:
                values = levels.values
                for n in names:
                    cs, ls = pd.factorize(values[:,n],sort_codes)
                    codes.append(cs)
                    self._Levels.append(ls)
            else:
                for n in names:
                    cs, ls = pd.factorize(levels[n],sort_codes)
                    codes.append(cs)
                    self._Levels.append(ls)
        elif IsArray(levels):
            for i in range(levels.shape[1]):
                cs, ls = pd.factorize(levels[:,i],sort_codes)
                codes.append(cs)
                self._Levels.append(ls)
        else:
            for l in levels:
                cs, ls = pd.factorize(l,sort_codes)
                codes.append(cs)
                self._Levels.append(ls)
        llen = len(self._Levels)
        
        # NA处理
        self._NAIncluded = np.repeat(False,llen)
        for i in range(llen):
            cs = codes[i]
            pos = which(cs==-1)
            if len(pos)>0:
                self._NAIncluded[i] = True
                cs[pos] = len(self._Levels[i])
                self._Levels[i] = np.concatenate((self._Levels[i],[NA]))
        
        self._LevelNames = ArrayKeyIndex(self._LevelNames)
        self._LevelCount = llen
        self._LevelShape = [len(l) for l in self._Levels]
        self._LevelBase = np.ones(llen,dtype=AnsiPosDtype)
        i = llen-2
        while i>=0:
            self._LevelBase[i] *= self._LevelShape[i+1]
            i -= 1
        
        self._MultiCodes = codes[0]
        for i in range(1,llen):
            self._MultiCodes = self._MultiCodes*self._LevelShape[i]+codes[i]
        self._ValidLen = len(self._MultiCodes)
        
        self._MultiKeys = None
        self._GenKeys()
        return
    
    # 2021-10-06
    def __getitem__(self, item):
        return item if IsSlice(item) \
            else self._MultiKeys[self._IndexToMultiCode(item)]
    
    # 2021-10-06
    def __iter__(self):
        for i in self.values:
            yield tuple(i)
        return
    
    # 2021-10-06
    def __repr__(self):
        return 'ArrayMultiIndex'+('([])' if self.empty
            else leftex(self.values.__repr__(),5))
    
    # 2021-10-06
    @property
    def values(self):
        '''索引值数组（重载只读属性）'''
        return self._MultiCodeToIndex(return_kind='array')
    
    # 2021-12-16
    def _ArgSort(self, ascending = True, na_option = 'last', method = 'first',
        key = None, level = None):
        '''下标排序（内部使用，重载函数）'''
        sort_codes = self._SortCodes
        values = self._MultiCodeToIndex(
            index_kind = 'code' if sort_codes else 'value'
        )
        if not key is None:
            values = key(values)
        vlen = len(values)
        
        # level过滤
        if level is None:
            level = range(vlen)
        elif IsSingleType2(level):
            if IsSlice(level):
                level = range(vlen)[level]
            else:
                level = [level]
        llen = len(level)
        
        # NA处理
        if sort_codes:
            naList = isinstance(na_option,list)
            for l in level:
                naop = na_option[l] if naList else na_option
                if self._NAIncluded[l] and naop=='first':
                    vl = values[l]
                    vl[vl==len(vl)-1] = -1
        
        if llen==1:
            return argsort(values[level[0]],ascending,na_option,method)
        else:
            return lexsort(
                [values[l] for l in level],ascending,na_option,method)
    
    # 2021-10-04
    def _GenKeys(self):
        '''生成内部索引'''
        self._Keys = []
        for l in self._Levels:
            self._Keys.append(ArrayValueIndex(l))
        self._MultiKeys = ArrayValueIndex(self._MultiCodes)
        return
    
    # 2021-10-06
    def _GetPrep(self, item):
        '''取值预处理（重载函数）'''
        if IsSlice(item):
            return item, False
        pos = self._MultiKeys[self._IndexToMultiCode(item)]
        return pos, IsSingleType(pos)
    
    # 2021-10-05
    def _IndexToMultiCode(self, index):
        '''普通索引转复合代码'''
        if isinstance(index,ArrayFrame):
            index = index._ValidData
        elif IsDataFrame(index):
            index = index.values
        
        if IsArray(index):
            if index.ndim==1:
                index = index.reshape((1,len(index)))
            rt = np.array(self._Keys[0][index[:,0]],dtype=AnsiPosDtype)
            for i in range(1,self._LevelCount):
                rt = rt*self._LevelShape[i]+self._Keys[i][index[:,i]]
        else:
            rt = np.array(self._Keys[0][index[0]],dtype=AnsiPosDtype)
            for i in range(1,self._LevelCount):
                rt = rt*self._LevelShape[i]+self._Keys[i][index[i]]
        return rt
    
    # 2021-10-04
    def _MultiCodeToIndex(self, codes = None, index_kind = 'value', 
        return_kind = 'list'):
        '''
        复合代码转普通索引。
        【注】
        1. 返回索引值indexKind类型：
           value - 返回索引值
           code - 返回索引编码
        2. 返回值retureKind类型：
           list - 列表
           array - 数组
        '''
        if codes is None:
            codes = self._MultiCodes
        elif not IsSingleType(codes) and not IsArray(codes):
            codes = np.array(codes,AnsiPosDtype)
        levelCount = self._LevelCount
        
        if return_kind=='array':
            if index_kind=='code':
                rt = np.ndarray(
                    (len(codes),levelCount),AnsiPosDtype,order='F')
                for i in range(levelCount-1):
                    lbi = self._LevelBase[i]
                    rt[:,i] = codes//lbi
                    codes = codes%lbi
                rt[:,-1] = codes
            else:
                rt = np.ndarray((len(codes),levelCount),object,order='F')
                for i in range(levelCount-1):
                    lbi = self._LevelBase[i]
                    rt[:,i] = self._Levels[i][codes//lbi]
                    codes = codes%lbi
                rt[:,-1] = self._Levels[-1][codes]
        else:
            rt = []
            if index_kind=='code':
                for i in range(levelCount-1):
                    lbi = self._LevelBase[i]
                    rt.append(codes//lbi)
                    codes = codes%lbi
                rt.append(codes)
            else:
                for i in range(levelCount-1):
                    lbi = self._LevelBase[i]
                    rt.append(self._Levels[i][codes//lbi])
                    codes = codes%lbi
                rt.append(self._Levels[-1][codes])
        return rt
        
    # 2021-10-06
    def _SetPrep(self, item):
        '''赋值预处理（重载函数）'''
        if IsSlice(item):
            return item, item.stop
        else:
            return super()._SetPrep(self._MultiKeys[
                self._IndexToMultiCodes(item)])
    
    # 2022-01-30
    def copy(self):
        '''拷贝（重载函数）'''
        return copy.deepcopy(self)
    
    # 2022-02-04
    def reindex(self, index, method = 'keep', dupl_method = 'all',
        drop_index = False):
        '''
        索引（重载函数）。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含索引
        【注】
        1. 在method参数为ffill/pad/bfill/backfill时，欲获得精确结果，对象构造时构
           造函数的sort_codes参数必须为True。
        2. 对于无法被因子化的索引项，返回值和索引暂会将其忽略。
        '''
        if isinstance(index,ArrayFrame):
            index = index._ValidData
        elif IsDataFrame(index):
            index = index.values
        keys = self._Keys
        kmethod = method
        if kmethod=='ignore':
            kmethod = 'keep'
        
        if IsArray(index):
            if index.ndim==1:
                index = index.reshape((1,len(index)))
            codes = keys[0].reindex(index[:,0],kmethod,drop_index=drop_index)[0]
            multiCodes = codes.copy()
            pos = which(codes>=0)
            plen = len(pos)
            clen = len(codes)
            for i in range(1,self._LevelCount):
                if plen==clen:
                    codes = keys[i].reindex(
                        index[:,i],kmethod,drop_index=drop_index)[0]
                else:
                    codes[pos] = keys[i].reindex(
                        index[pos,i],kmethod,drop_index=drop_index)[0]
                pos = which(codes>=0)
                plen = len(pos)
                if plen==clen:
                    multiCodes = multiCodes*self._LevelShape[i]+codes
                else:
                    multiCodes[pos] \
                        = multiCodes[pos]*self._LevelShape[i]+codes[pos]
        else:
            codes = keys[0].reindex(index[0],kmethod,drop_index=drop_index)[0]
            multiCodes = codes.copy()
            pos = which(codes>=0)
            plen = len(pos)
            clen = len(codes)
            for i in range(1,self._LevelCount):
                if plen==clen:
                    codes = keys[i].reindex(
                        index[i],kmethod,drop_index=drop_index)[0]
                else:
                    codes[pos] = keys[i].reindex(
                        index[i][pos],kmethod,drop_index=drop_index)[0]
                pos = which(codes>=0)
                plen = len(pos)
                if plen==clen:
                    multiCodes = multiCodes*self._LevelShape[i]+codes
                else:
                    multiCodes[pos] \
                        = multiCodes[pos]*self._LevelShape[i]+codes[pos]
        
        if plen==clen:
            rtpos, rtindex = self._MultiKeys.reindex(
                multiCodes,method,dupl_method,drop_index)
        else:
            rtpos, rtindex = self._MultiKeys.reindex(
                multiCodes[pos],method,dupl_method,drop_index)
        if rtindex is None:
            return rtpos, None
        else:
            return rtpos, self._MultiCodeToIndex(rtindex)
    
    # 2021-10-06
    def take(self, indices):
        '''切片（重载函数）'''
        if IsSingleType(indices):
            indices = [indices]
        return ArrayMultiIndex(
            levels = self._MultiCodeToIndex(self._MultiCodes[indices]),
            names = self._LevelNames
        )

# 3. 数据系列

# 3.1 数据系列类

# 2020-11-28
class ArraySeries:
    '''
    基于ndarray的数据系列（Series）类。
    
    【注】
    1. 可直接使用下标遍历代替iloc下标遍历。
    2. _assign_manager仅为内部使用参数，构造时无需提供。
    3. 使用arraytool体系外的ndarray（包含Series中的ndarray）进行构造且copy参数设
       为False时，请勿在体系外对该ndarray进行赋值，否则该ndarray作为索引时可能会
       因值变化未被记录而出错。
    
    【参数表】
    data - 系列数据
    index - 系列索引
    dtype - 数据类型
    copy - 是否复制数据
    init_shape - 初始长度
    auto_expand - 是否自动扩展长度
    expand_count - 单次扩展数量
    expand_ratio - 单次扩展比例（仅在expand_count为0时有效）
    drop_index - 拷贝构造时是否不复制索引
    
    【示例】
    >>> s1 = ArraySeries(['a','bb','ccc'])
    >>> s1
    0      a
    1     bb
    2    ccc
    dtype: object
    >>> s1[2]
    'ccc'
    >>> s1[:2]
    0     a
    1    bb
    dtype: object
    >>> s1[3] = 'dddd'
    >>> len(s1)
    4
    
    >>> s2 = ArraySeries([2,3,4,5],list('aabc'))
    >>> s2.iloc[:2]
    a    2
    a    3
    dtype: object
    >>> s2.loc['a']
    a    2
    a    3
    dtype: object
    >>> s2.loc['b']
    4
    >>> s2.loc[list('ab')]
    a    2
    a    3
    b    4
    dtype: object
    '''
    
    # 2020-11-28
    def __init__(
        self, 
        data = None, 
        index = None, 
        dtype = None, 
        name = None,
        copy = False, 
        init_len = None, 
        auto_expand = None, 
        expand_count = None,
        expand_ratio = None, 
        drop_index = False, 
        _assign_manager = None
    ):
        # 拷贝构造
        if isinstance(data,ArraySeries):
            if dtype is None:
                dtype = data.dtype
            if name is None:
                name = data.name
            if init_len is None:
                init_len = data._ValidLen
            if auto_expand is None:
                auto_expand = data._AutoExpand
            if expand_count is None:
                expand_count = data._ExpandCount
            if expand_ratio is None:
                expand_ratio = data._ExpandRatio
            _assign_manager = data._AssignManager
            if not drop_index and index is None:
                index = data.index
            data = data._ValidData
        elif IsSeries(data):
            if dtype is None:
                dtype = data.dtype
            if name is None:
                name = data.name
            if index is None and not drop_index:
                dindex = data.index
                if not IsSimpleIndex(dindex):
                    index = dindex.values
            data = data.values
        
        self.dtype = AnsiDType if dtype is None else dtype
        self.name = name
        self._InitLen = AnsiInitLen if init_len is None else init_len
        self._Data = None
        self._ValidData = None
        self._Len = 0
        self._ValidLen = 0
        self._AutoExpand = AnsiAutoExpand if auto_expand is None \
            else auto_expand
        self._ExpandCount = AnsiExpandCount if expand_count is None \
            else expand_count
        self._ExpandRatio = AnsiExpandRatio if expand_ratio is None \
            else expand_ratio
        
        self._SetData(data,copy,_assign_manager)
        self.iloc = ArraySeriesLocIndexer(self,iloc=True)
        self._SetLoc(index,copy)
        return
    
    # 2022-02-09
    def __add__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData+other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented
    
    # 2022-01-10
    def __eq__(self, other):
        return self._ValidData==other
    
    # 2022-02-10
    def __floordiv__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData//other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-01-10
    def __ge__(self, other):
        return self._ValidData>=other
    
    # 2021-03-28
    def __getitem__(self, item):
        if IsBool(item):
            return self._ValidData[0] if item else None
        elif IsInteger(item):
            return self._ValidData[item]
        else:
            return ArraySeries(
                data = self._ValidData[item],
                index = None if self._NoLoc else self.index.take(item),
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
                _assign_manager \
                    = self._AssignManager if IsSlice(item) else None
            )
    
    # 2022-01-10
    def __gt__(self, other):
        return self._ValidData>other
    
    # 2021-02-18
    def __iter__(self):
        return self._ValidData.__iter__()
    
    # 2022-01-10
    def __le__(self, other):
        return self._ValidData<=other
    
    # 2021-02-18
    def __len__(self):
        return self._ValidLen
    
    # 2022-01-10
    def __lt__(self, other):
        return self._ValidData<other
    
    # 2022-02-10
    def __mod__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData%other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __mul__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData*other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-01-10
    def __ne__(self, other):
        return self._ValidData!=other

    # 2022-02-10
    def __pow__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData**other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented
    
    # 2022-02-10
    def __radd__(self, other):
        return self+other

    # 2021-02-18
    def __repr__(self):
        rt = self.series.__repr__()
        if self.empty:
            rt = rt.replace('Series',self.__class__.__name__)
        return rt
    
    # 2022-02-10
    def __rfloordiv__(self, other):
        try:
            return ArraySeries(
                data = other//self._ValidData,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __rmod__(self, other):
        try:
            return ArraySeries(
                data = other%self._ValidData,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __rmul__(self, other):
        return self*other
    
    # 2022-02-10
    def __rpow__(self, other):
        try:
            return ArraySeries(
                data = other**self._ValidData,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __rsub__(self, other):
        try:
            return ArraySeries(
                data = other-self._ValidData,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __rtruediv__(self, other):
        try:
            return ArraySeries(
                data = other/self._ValidData,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2021-02-16
    def __setitem__(self, item, value):
        # 值处理
        if isinstance(value,ArraySeries):
            value = value._ValidData
        
        # 下标处理
        if IsBool(item):
            if item:
                item = 0
            else:
                return
        if IsInteger(item):
            maxlen = item+1
        elif IsSlice(item):
            maxlen = item.stop
        else:
            if IsArray(item) and item.dtype is bool:
                item = np.where(item)[0]
            if len(item)==0:
                return
            maxlen = max(item)+1
        if not maxlen is None and maxlen>self._ValidLen:
            self._UpdateValidLen(maxlen)
        
        self._ValidData[item] = value
        self._AssignManager.AssignOnce()
        return
    
    # 2022-02-10
    def __sub__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData-other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2022-02-10
    def __truediv__(self, other):
        try:
            return ArraySeries(
                data = self._ValidData/other,
                index = self.index,
                dtype = self.dtype,
                name = self.name,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
            )
        except TypeError:
            return NotImplemented

    # 2021-02-18
    @property
    def empty(self):
        '''是否为空（只读属性）'''
        return self._ValidLen==0
    
    # 2021-03-28
    @property
    def series(self):
        '''将数据系列转为Series（只读属性）'''
        index = self.index
        if type(index) is ArrayIndex:
            index = None
        return Series(self._ValidData,index,self.dtype,self.name)
    
    # 2021-10-06
    @property
    def values(self):
        '''数组值（只读属性）'''
        return self._ValidData
    
    # 2021-02-16
    def _Expand(self, targetLen):
        '''扩展数组'''
        if self._Data is None:
            targetLen = max(targetLen,self._InitLen)
            self._Data = np.ndarray(targetLen,self.dtype)
            self._AssignManager = AssignManager()
            self._Len = targetLen
            return
        
        newlen = ExpandSize(self._Len,targetLen,self._ExpandCount,
            self._ExpandRatio)
        newdata = np.ndarray(newlen,self.dtype)
        newdata[:self._ValidLen] = self._ValidData
        self._Data = newdata
        self._AssignManager = AssignManager(self._AssignManager.AssignID)
        self._ValidData = newdata[:self._ValidLen]
        self._Len = newlen
        return

    # 2021-02-16
    def _SetData(self, data, copy = False, assign_manager = None):
        '''设置数据'''
        if data is None:
            return
        init_len = self._InitLen
        if IsSingleType(data):
            dlen = 1
            data = [data]
        else:
            dlen = len(data)
        if dlen>=init_len:
            if copy:
                self._Data = np.array(data,self.dtype)
                self._AssignManager = AssignManager()
            else:
                self._Data = data if IsArray(data) \
                    else np.array(data,self.dtype,copy=False)
                self._AssignManager = AssignManager() \
                    if assign_manager is None else assign_manager
            self._Len = dlen
        else:
            self._Data = np.ndarray(init_len,self.dtype)
            self._Data[:dlen] = data
            self._AssignManager = AssignManager()
            self._Len = init_len
        self._ValidData = self._Data[:dlen]
        self._ValidLen = dlen
        return

    # 2021-09-04
    def _SetLoc(self, index, copy):
        '''设置Loc索引器'''
        if index is None or type(index) is ArrayIndex:
            self.loc = ArraySeriesLocIndexer(self,self.iloc.index,False,copy)
            self._NoLoc = True
        else:
            self.loc = ArraySeriesLocIndexer(self,index,False,copy)
            self._NoLoc = False
        self.index = self.loc.index
        return
    
    # 2021-06-26
    def _UpdateValidLen(self, targetLen):
        '''更新有效长度'''
        if targetLen>self._Len:
            if self._AutoExpand:
                self._Expand(targetLen)
            else:
                targetLen = self._Len
        self._ValidLen = targetLen
        self._ValidData = self._Data[:targetLen]
        self.iloc._UpdateLen(targetLen)
        return
    
    # 2021-04-07
    def append(self, data, ignore_index = False, inplace = True):
        '''追加数据'''
        rt = self if inplace else self.copy()
        dlen = 1 if IsSingleType(data) else len(data)
        vlen = rt._ValidLen
        rt[vlen:(vlen+dlen)] = data
        if not ignore_index and not rt._NoLoc \
            and (isinstance(data,ArraySeries) and not data._NoLoc \
                 or IsSeries(data)):
            rt.index.append(data.index)
        return rt
    
    # 2021-12-03
    def argsort(self, ascending = True, na_option = 'last', method = 'first',
        kind = None):
        pos = argsort(self._ValidData,ascending,na_option,method,kind)
        return ArraySeries(
            data = pos,
            index = self.index,
            dtype = pos.dtype,
            name = self.name,
            auto_expand = self._AutoExpand,
            expand_count = self._ExpandCount,
            expand_ratio = self._ExpandRatio,
        )
    
    # 2022-02-14
    def astype(self, dtype, inplace = False):
        '''数据类型转换'''
        if inplace:
            if dtype!=self.dtype:
                self._Data = self._Data.astype(dtype)
                self._ValidData = self._Data[:self._ValidLen]
                self._AssignManager.AssignOnce()
                self.dtype = dtype
            return self
        else:
            if dtype==self.dtype:
                return self.copy()
            else:
                return ArraySeries(
                    data = self._ValidData.astype(dtype),
                    index = self.index,
                    dtype = dtype,
                    name = self.name,
                    auto_expand = self._AutoExpand,
                    expand_count = self._ExpandCount,
                    expand_ratio = self._ExpandRatio
                )
    
    # 2021-04-07
    def copy(self):
        return copy.deepcopy(self)
    
    # 2021-09-27
    def head(self, n = 5):
        '''返回前n个元素'''
        return self.iloc[:n]
    
    # 2021-10-24
    def rank(self, ascending = True, na_option = 'keep', method = 'average'):
        '''
        排名。
        【注】
        1. 参数na_option可选项（同Series.rank函数同名参数）：keep/top/bottom。
        2. 参数method可选项（同rank函数同名参数）：
          average/min/max/dense/first/last。
        '''
        data = rank(self._ValidData,ascending,na_option)
        return ArraySeries(
            data = data,
            index = self.index,
            dtype = data.dtype,
            name = self.name,
            auto_expand = self._AutoExpand,
            expand_count = self._ExpandCount,
            expand_ratio = self._ExpandRatio
        )
    
    # 2022-02-08
    def reindex(self, index, method = 'keep', fill_value = NA, 
        dupl_method = 'all', drop_index = False):
        '''
        索引。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        fill_value - 默认填充值
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含下标
        【注】在method参数为ffill/pad/bfill/backfill时，欲获得精确结果，对象构造时
        构造函数的sort_codes参数必须为True。
        '''
        return self.loc.reindex(index,method,fill_value,dupl_method,drop_index)

    # 2021-03-28
    def set_index(self, index, copy = False, _assign_manager = None):
        '''设置索引'''
        if index is None:
            return
        if self._NoLoc:
            self._SetLoc(index,copy)
        else:
            self.loc.set_index(index,copy,_assign_manager)
        return
    
    # 2021-12-07
    def sort_index(self, ascending = True, na_position = 'last',
        method = 'first', axis = 0, level = None, inplace = False, key = None):
        '''
        索引排序。
        【注】simple类索引不进行此类排序。
        '''
        index = self.index
        if index.simple:
            return self if inplace else self.copy()
        if isinstance(index,ArrayMultiIndex):
            pos = index._ArgSort(ascending,na_position,method,key,level)
        else:
            pos = index._ArgSort(ascending,na_position,method,key)
        if inplace:
            self._ValidData[:,:] = self._ValidData[pos,:]
            self.set_index(index.take(pos))
            return self
        else:
            return self.iloc[pos]
    
    # 2021-10-24
    def sort_values(self, ascending = True, na_position = 'last', 
        method = 'first', kind = None, inplace = False, key = None):
        '''值排序'''
        values = self._ValidData
        if not key is None:
            values = key(values)
        pos = argsort(values,ascending,na_position,method,kind)
        
        if inplace:
            self._ValidData[:] = self._ValidData[pos]
            if not self.index.simple:
                self.set_index(self.index.take(pos))
            return self
        else:
            return self[pos]
    
    # 2021-09-27
    def tail(self, n = 5):
        '''返回后n个元素'''
        return self.iloc[-n:]

# 3.2 数据系列索引器类

# 2021-03-28
class ArraySeriesLocIndexer:
    '''
    数据系列Loc索引器类。
    '''
    
    # 2021-03-28
    def __init__(self, series, index = None, iloc = False, copy = False, 
        _assign_manager = None):
        if not isinstance(series,ArraySeries):
            raise TypeError('ArraySeries required.')
        self.series = series
        self._ILoc = iloc
        self.set_index(index,copy,_assign_manager)
        return
    
    # 2021-06-25
    def __getitem__(self, item):
        item, singleType = self.index._GetPrep(item)
        if singleType:
            return self.series._ValidData[item]
        else:
            series = self.series
            data = series._ValidData[item]
            return ArraySeries(
                data = data,
                index = None if series._NoLoc else series.index.take(item),
                dtype = series.dtype,
                name = series.name,
                auto_expand = series._AutoExpand,
                expand_count = series._ExpandCount,
                expand_ratio = series._ExpandRatio,
                _assign_manager
                    = None if data.flags.owndata else series._AssignManager
            )
    
    # 2022-02-10
    def __iter__(self):
        return self.index.__iter__()
    
    # 2021-06-25
    def __setitem__(self, item, value):
        series = self.series
        
        # 值处理
        if isinstance(value,ArraySeries):
            value = value._ValidData
        
        # 空数据系列处理
        if not self._ILoc and series.empty:
            series._SetData(value)
            if not IsSlice(item):
                self.set_index(item)
                series.index = self.index
                series._NoLoc = False
            return
        
        # 下标处理
        item, maxlen = self.index._SetPrep(item)
        if not maxlen is None and maxlen>series._ValidLen:
            series._UpdateValidLen(maxlen)
        
        series._ValidData[item] = value
        series._AssignManager.AssignOnce()
        return
    
    # 2021-06-26
    def _UpdateLen(self, length):
        '''更新索引长度'''
        self.index._UpdateLen(length)
        return

    # 2022-02-08
    def reindex(self, index, method = 'keep', fill_value = NA, 
        dupl_method = 'all', drop_index = False):
        '''
        索引。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        fill_value - 默认填充值
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含索引
        【注】在method参数为ffill/pad/bfill/backfill时，欲获得精确结果，对象构造时
        构造函数的sort_codes参数必须为True。
        '''
        series = self.series
        pos, rtindex = self.index.reindex(index,method,dupl_method,drop_index)
        plen = len(pos)
        ppos = which(pos>=0)
        pplen = len(ppos)
        if plen==0:
            rtdata = None
            rtindex = None
        elif pplen==plen:
            rtdata = series._ValidData[pos]
        else:
            rtdata = np.repeat(fill_value,plen).astype(series.dtype)
            if pplen>0:
                rtdata[ppos] = series._ValidData[pos[ppos]]
        return ArraySeries(
            data = rtdata,
            index = rtindex,
            dtype = series.dtype,
            name = series.name,
            auto_expand = series._AutoExpand,
            expand_count = series._ExpandCount,
            expand_ratio = series._ExpandRatio,
        )
    
    # 2021-07-19
    def set_index(self, index = None, copy = False, _assign_manager = None):
        '''设置索引'''
        series = self.series
        if self._ILoc or index is None or type(index) is ArrayIndex:
            self.index = series.iloc.index if hasattr(series,'iloc') \
                else ArrayIndex(len(series))
            return
        
        if isinstance(index,ArrayIndex):
            if len(index)!=series._ValidLen:
                raise ValueError('Index size mismatch.')
            self.index = copy.deepcopy(index) if copy else index
        elif IsSingleType(index):
            if series._ValidLen!=1:
                raise ValueError('Index size mismatch.')
            self.index = ArrayValueIndex(index)
        elif IsIndex(index):
            if len(index)!=series._ValidLen:
                raise ValueError('Index size mismatch.')
            if IsMultiIndex(index):
                self.index = ArrayMultiIndex(np.array(tuple(index.values)))
            else:
                index = index.values
                self.index = ArrayValueIndex(
                    values = index,
                    dtype = index.dtype,
                    copy = copy,
                    auto_expand = series._AutoExpand,
                    expand_count = series._ExpandCount,
                    expand_ratio = series._ExpandRatio,
                    _assign_manager = _assign_manager
                )
        elif IsSingleType(index[0]):
            if len(index)!=series._ValidLen:
                raise ValueError('Index size mismatch.')
            self.index = ArrayValueIndex(
                values = index,
                dtype = index.dtype if IsArray(index) else None,
                copy = copy,
                auto_expand = series._AutoExpand,
                expand_count = series._ExpandCount,
                expand_ratio = series._ExpandRatio,
                _assign_manager = _assign_manager
            )
        else:
            vlen = series._ValidLen
            for i in range(len(index)):
                if len(index[i])!=vlen:
                    raise ValueError('Index size mismatch.')
            self.index = ArrayMultiIndex(index)
        return

# 4. 数据表

# 4.1 数据表类

# 2021-04-11
class ArrayFrame:
    '''
    基于nadarry的数据表（DataFrame）类。
    
    【注】
    1. 列（字段）名不可以“_”开头。
    2. _assign_manager仅为内部使用参数，构造时无需提供。
    3. 使用arraytool体系外的ndarray（包含Series中的ndarray）进行构造且copy参数设
       为False时，请勿在体系外对该ndarray进行赋值，否则该ndarray作为索引时可能会
       因值变化未被记录而出错。
    
    【参数表】
    data - 表数据
    index - 行索引
    columns - 列索引
    dtype - 数据类型
    copy - 是否复制数据
    init_shape - 初始大小
    auto_expand - 是否自动扩展行/列
    expand_count - 单次扩展行/列数量
    expand_ratio - 单次扩展行/列比例
    order - 数据库主序
      F - 列主序（默认）
      C - 行主序
    drop_index - 拷贝构造时是否不复制行索引
    drop_columns - 拷贝构造时是否不复制列索引
    
    【示例】
    >>> af = ArrayFrame()
    >>> af['A'] = list('abcd')
    >>> af['B'] = range(4)
    >>> af['C'] = [True,True,False,False]
    >>> af
       A  B      C
    0  a  0   True
    1  b  1   True
    2  c  2  False
    3  d  3  False
    >>> af[list('BC')]
       B      C
    0  0   True
    1  1   True
    2  2  False
    3  3  False
    >>> af.shape
    (4, 3)
    
    >>> af.iloc[0,0]
    'a'
    >>> af.iloc[0]
       A  B     C
    0  a  0  True
    '''
    
    # 2021-04-11
    def __init__(
        self,
        data = None,
        index = None,
        columns = None,
        dtype = None,
        copy = False,
        init_shape = None,
        auto_expand = None,
        expand_count = None,
        expand_ratio = None,
        order = None,
        drop_index = False,
        drop_columns = False,
        _assign_manager = None
    ):
        # 拷贝构造
        if isinstance(data,ArrayFrame):
            if columns is None:
                columns = data.columns
            if dtype is None:
                dtype = data.dtype
            if init_shape is None:
                init_shape = data._ValidShape
            if auto_expand is None:
                auto_expand = data._AutoExpand
            if expand_count is None:
                expand_count = data._ExpandCount
            if expand_ratio is None:
                expand_ratio = data._ExpandRatio
            _assign_manager = data._AssignManager
            if not drop_index and index is None:
                index = data.index
            if not drop_columns and columns is None:
                columns = data.columns
            data = data._ValidData
        elif IsDataFrame(data):
            if dtype is None:
                dtype = data.dtypes.dtype
            if init_shape is None:
                init_shape = data.shape
            if not drop_index and index is None:
                index = data.index
            if not drop_columns and columns is None:
                columns = data.columns
            data = data.values
        
        self.dtype = AnsiDType if dtype is None else dtype
        self._Data = None
        self._ValidData = None
        self._Shape = (0,0)
        self._ValidShape = (0,0)
        self._InitShape = (AnsiInitLen,AnsiColInitLen) if init_shape is None \
            else init_shape
        self._AutoExpand = (AnsiAutoExpand,AnsiAutoExpand) \
            if auto_expand is None else auto_expand
        self._ExpandCount = (AnsiExpandCount,AnsiColExpandCount) \
            if expand_count is None else expand_count
        self._ExpandRatio = (AnsiExpandRatio,AnsiColExpandRatio) \
            if expand_ratio is None else expand_ratio
        
        self._SetData(data,init_shape,copy,order,_assign_manager)
        self.iloc = ArrayFrameLocIndexer(self,iloc=True)
        self._SetLoc(index,columns,copy)
        return
    
    # 2021-06-15
    def __getattr__(self, name):
        if name in ['loc','iloc']:
            return super().__getattribute__(name)
        columns = self.columns
        if not type(columns) is ArrayIndex and name in columns:
            if len(self)==1:
                return self._ValidData[0,columns[name]]
            else:
                return ArraySeries(
                    data = self._ValidData[:,columns[name]],
                    index = self.index,
                    dtype = self.dtype,
                    name = name,
                    auto_expand = self._AutoExpand[0],
                    expand_count = self._ExpandCount[0],
                    expand_ratio = self._ExpandRatio[0],
                    _assign_manager = self._AssignManager
                )
        else:
            return super().__getattribute__(name)
    
    # 2021-06-15
    def __getitem__(self, item):
        columns = self.columns
        empty_col = type(columns) is ArrayIndex
        if not empty_col:
            item = columns[item]
        data = self._ValidData[:,item]
        
        if data.ndim==1:
            return ArraySeries(
                data = data,
                index = self.index,
                dtype = data.dtype,
                name = None if empty_col else item,
                auto_expand = self._AutoExpand[0],
                expand_count = self._ExpandCount[0],
                expand_ratio = self._ExpandRatio[0],
                _assign_manager = None if data.flags.owndata \
                    else self._AssignManager
            )
        else:
            return ArrayFrame(
                data = data,
                index = self.index,
                columns = None if empty_col else columns.take(item),
                dtype = self.dtype,
                auto_expand = self._AutoExpand,
                expand_count = self._ExpandCount,
                expand_ratio = self._ExpandRatio,
                _assign_manager = None if data.flags.owndata \
                    else self._AssignManager
            )
    
    # 2022-02-10
    def __iter__(self):
        return self.columns.__iter__()
    
    # 2021-05-30
    def __len__(self):
        return self._ValidShape[0]
    
    # 2021-05-30
    def __repr__(self):
        rt = self.frame.__repr__()
        if self.empty:
            rt = rt.replace('DataFrame',self.__class__.__name__)
        return rt
    
    # 2021-07-11
    def __setitem__(self, item, value):
        self.loc[:,item] = value
        return
    
    # 2021-05-30
    @property
    def empty(self):
        '''是否为空（只读属性）'''
        return self._ValidShape[0]==0 or self._ValidShape[1]==0
    
    # 2021-05-30
    @property
    def frame(self):
        '''将数据表转为DataFrame（只读属性）'''
        index = self.index
        if type(index) is ArrayIndex:
            index = None
        else:
            ilen = len(index)
            flen = self._ValidShape[0]
            if ilen<flen:
                index = index.append([None]*(flen-ilen),False)
        
        columns = self.columns
        if type(columns) is ArrayIndex:
            columns = None
        else:
            clen = len(columns)
            flen = self._ValidShape[1]
            if clen<flen:
                columns = columns.append([None]*(flen-clen),False)
        
        return DataFrame(self._ValidData,index,columns,self.dtype)
    
    # 2021-06-29
    @property
    def shape(self):
        '''数据表形状（只读属性）'''
        return self._ValidShape
    
    # 2021-10-06
    @property
    def values(self):
        '''数组值（只读属性）'''
        return self._ValidData
    
    # 2021-06-29
    def _Expand(self, targetShape, order = None):
        '''扩展数组'''
        if order is None:
            order = AnsiOrder
        initShape = self._InitShape
        targetShape = (max(targetShape[0],initShape[0]),
            max(targetShape[1],initShape[1]))
        
        if self._Data is None:
            self._Data = np.ndarray(targetShape,self.dtype,order=order)
            self._AssignManager = AssignManager()
            self._Shape = targetShape
            return
        
        shape = self._Shape
        validShape = self._ValidShape
        expandCount = self._ExpandCount
        expandRatio = self._ExpandRatio
        
        newx = ExpandSize(
            shape[0],targetShape[0],expandCount[0],expandRatio[0])
        newy = ExpandSize(
            shape[1],targetShape[1],expandCount[1],expandRatio[1])
        newdata = np.ndarray((newx,newy),self.dtype,order=order)
        newdata[:validShape[0],:validShape[1]] = self._ValidData
        self._Data = newdata
        self._AssignManager = AssignManager(self._AssignManager.AssignID)
        self._ValidData = newdata[:validShape[0],:validShape[1]]
        self._Shape = (newx,newy)
        return
    
    # 2021-05-19
    def _SetData(self, data, init_shape = None, copy = False, order = None,
        assign_manager = None):
        '''设置数据'''
        if data is None:
            return
        if init_shape is None:
            init_shape = self._InitShape
        else:
            init_shape = (max(init_shape[0],self._InitShape[0]),
                max(init_shape[1],self._InitShape[1]))
        if order is None:
            order = AnsiOrder
        if copy or not IsArray(data):
            data = np.array([[data]] if IsSingleType(data) else data,
                self.dtype,copy=copy,order=order)
        if data.ndim==1:
            data = data.reshape((len(data),1))
        
        dlen = data.shape[0]
        dcol = data.shape[1]
        ilen = init_shape[0]
        icol = init_shape[1]
        if dlen>=ilen and dcol>=icol:
            self._Data = data
            self._AssignManager = AssignManager() \
                if copy or assign_manager is None else assign_manager
        else:
            self._Data = np.ndarray((max(dlen,ilen),max(dcol,icol)),self.dtype,
                order=order)
            self._Data[:dlen,:dcol] = data
            self._AssignManager = AssignManager()
        self._Shape = self._Data.shape
        self._ValidData = self._Data[:dlen,:dcol]
        self._ValidShape = data.shape
        return
    
    # 2021-08-22
    def _SetLoc(self, index, columns, copy):
        '''设置Loc索引器'''
        if index is None and columns is None:
            self.loc = ArrayFrameLocIndexer(
                self,self.iloc.index,self.iloc.columns)
            self._NoLoc = True
        else:
            self.loc = ArrayFrameLocIndexer(self,index,columns,copy)
            self._NoLoc = False
        self.index = self.loc.index
        self.columns = self.loc.columns
        self.ix = ArrayFrameLocIndexer(self,self.iloc.index,self.columns,copy)
        return
    
    # 2021-12-17
    def _UpdateEmptyAxisLen(self, axis, targetLen):
        '''更新空表轴长度（不改变数组内容，内部使用）'''
        if axis==0:
            self._Shape = (targetLen,0)
            self.iloc.index._UpdateLen(targetLen)
        else:
            self._Shape = (0,targetLen)
            self.iloc.columns._UpdateLen(targetLen)
        self._ValidShape = self._Shape
        return
    
    # 2021-06-27
    def _UpdateValidShape(self, targetShape):
        '''更新有效形状'''
        needExpand = False
        for i in range(2):
            if targetShape[i]>self._Shape[i]:
                if self._AutoExpand[i]:
                    needExpand = True
                else:
                    targetShape = list(targetShape)
                    targetShape[i] = self._Shape[i]
        if needExpand:
            self._Expand(targetShape)
        self._ValidData = self._Data[:targetShape[0],:targetShape[1]]
        self._ValidShape = targetShape
        self.iloc._UpdateValidShape(targetShape)
        return
    
    # 2022-01-30
    def append(self, data, ignore_index = False, inplace = True):
        '''追加数据'''
        rt = self if inplace else self.copy()
        vlen = self._ValidShape[0]
        
        if isinstance(data,ArrayFrame):
            if data._ValidShape[1]!=self._ValidShape[1]:
                raise ValueError('Column size mismatch.')
            rt.iloc[vlen:(vlen+data._ValidShape[0])] = data._ValidData
            if not ignore_index and not rt.index.simple \
                and not data.index.simple:
                rt.index.append(data.index.values)
            return rt
        elif IsDataFrame(data):
            if data.shape[1]!=self._ValidShape[1]:
                raise ValueError('Column size mismatch.')
            rt.iloc[vlen:(vlen+data._ValidShape[0])] = data
            if not ignore_index and not rt.index.simple:
                rt.index.append(data.index.values)
            return rt
        
        if IsSingleType2(data):
            dlen = 1
        elif IsSingleType2(data[0]):
            if len(data)!=self._ValidShape[1]:
                raise ValueError('Column size mismatch.')
            dlen = 1
        else:
            if len(data[0])!=self._ValidShape[1]:
                raise ValueError('Column size mismatch.')
            dlen = len(data)
        rt.iloc[vlen:(vlen+dlen)] = data
        return rt
    
    # 2022-02-14
    def astype(self, dtype, inplace = False):
        '''数据类型转换'''
        if inplace:
            if dtype!=self.dtype:
                self._Data = self._Data.astype(dtype)
                self._ValidData = self._Data[
                    :self._ValidShape[0],:self._ValidShape[1]]
                self._AssignManager.AssignOnce()
                self.dtype = dtype
            return self
        else:
            if dtype==self.dtype:
                return self.copy()
            else:
                return ArrayFrame(
                    data = self._ValidData.astype(dtype),
                    index = self.index,
                    columns = self.columns,
                    dtype = dtype,
                    auto_expand = self._AutoExpand,
                    expand_count = self._ExpandCount,
                    expand_ratio = self._ExpandRatio
                )

    # 2021-09-25
    def copy(self):
        return ArrayFrame(
            data = self._ValidData,
            index = self.index,
            columns = self.columns,
            dtype = self.dtype,
            copy = True,
            auto_expand = self._AutoExpand,
            expand_count = self._ExpandCount,
            expand_ratio = self._ExpandRatio
        )
    
    # 2021-09-27
    def head(self, n = 5):
        '''返回前n行'''
        return self.iloc[:n]
    
    def reindex(self, index = None, columns = None, method = 'keep', 
        fill_value = NA, dupl_method = 'all', drop_index = False, axis = 0):
        '''
        索引。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        fill_value - 默认填充值
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含下标
        '''
        return self.loc.reindex(index,columns,method,fill_value,dupl_method,
            drop_index,axis)

    # 2021-05-30
    def set_columns(self, columns, copy = False, _assign_manager = None):
        '''设置列索引'''
        if columns is None:
            return
        if self._NoLoc:
            self._SetLoc(None,columns,copy)
        else:
            self.loc.set_index(columns,1,copy,_assign_manager)
            self.columns = self.loc.columns
            self.ix.set_index(columns,1)
        return

    # 2021-08-25
    def set_index(self, index, copy = False, _assign_manager = None):
        '''设置列索引'''
        if index is None:
            return
        if self._NoLoc:
            self._SetLoc(index,None,copy)
        else:
            self.loc.set_index(index,0,copy,_assign_manager)
            self.index = self.loc.index
        return
    
    # 2022-01-23
    def sort_index(self, ascending = True, na_position = 'last',
        method = 'first', axis = 0, level = None, inplace = False, key = None):
        '''
        索引排序。
        【注】simple类索引不进行此类排序。
        '''
        if axis==0:
            index = self.index
            if index.simple:
                return self if inplace else self.copy()
            if isinstance(index,ArrayMultiIndex):
                pos = index._ArgSort(ascending,na_position,method,key,level)
            else:
                pos = index._ArgSort(ascending,na_position,method,key)
            if inplace:
                self._ValidData[:,:] = self._ValidData[pos,:]
                self.set_index(index.take(pos))
                return self
            else:
                return self.iloc[pos]
        else:
            columns = self.columns
            if columns.simple:
                return self if inplace else self.copy()
            if isinstance(columns,ArrayMultiIndex):
                pos = columns._ArgSort(ascending,na_position,method,key,level)
            else:
                pos = columns._ArgSort(ascending,na_position,method,key)
            if inplace:
                self._ValidData[:,:] = self._ValidData[:,pos]
                self.set_columns(columns.take(pos))
                return self
            else:
                return self.iloc[:,pos]
    
    # 2021-12-14
    def sort_values(self, by = None, ascending = True, na_position = 'last',
        method = 'first', axis = 0, inplace = False, key = None):
        '''
        值排序。
        【注】函数参数意义同DataFrame.sort_values对应参数。
        '''
        index = self.index
        columns = self.columns
        if axis==0:
            if by is None:
                by = columns.values
            if IsSingleType(by):
                values = self._ValidData[:,columns[by]]
                if not key is None:
                    values = key(values)
                pos = argsort(values,ascending,na_position,method)
            else:
                if isinstance(ascending,dict):
                    asc = []
                    for b in by:
                        asc.append(ascending[b] if b in ascending else True)
                else:
                    asc = ascending
                if isinstance(na_position,dict):
                    na = []
                    for b in by:
                        na.append(
                            na_position[b] if b in na_position else 'last')
                else:
                    na = na_position
                
                keyDict = isinstance(key,dict)
                keyList = isinstance(key,list)
                values = []
                i = 0
                for b in by:
                    v = self._ValidData[:,columns[b]]
                    if not key is None:
                        if keyDict:
                            v = key[b](v)
                        elif keyList:
                            v = key[i](v)
                        else:
                            v = key(v)
                    values.append(v)
                    i += 1
                pos = lexsort(values,asc,na,method)
            
            if inplace:
                self._ValidData[:,:] = self._ValidData[pos,:]
                if not index.simple:
                    self.set_index(index.take(pos))
                return self
            else:
                return self.iloc[pos]
        else:
            if by is None:
                by = index.values
            if IsSingleType(by):
                values = self._ValidData[index[by]]
                if not key is None:
                    values = key(values)
                pos = argsort(values,ascending,na_position,method)
            else:
                if isinstance(ascending,dict):
                    asc = []
                    for b in by:
                        asc.append(ascending[b] if b in ascending else True)
                else:
                    asc = ascending
                if isinstance(na_position,dict):
                    na = []
                    for b in by:
                        na.append(
                            na_position[b] if b in na_position else 'last')
                else:
                    na = na_position
                
                keyDict = isinstance(key,dict)
                keyList = isinstance(key,list)
                values = []
                i = 0
                for b in by:
                    v = self._ValidData[index[b]]
                    if not key is None:
                        if keyDict:
                            v = key[b](v)
                        elif keyList:
                            v = key[i](v)
                        else:
                            v = key(v)
                    values.append(v)
                    i += 1
                pos = lexsort(values,asc,na,method)
            
            if inplace:
                self._ValidData[:,:] = self._ValidData[:,pos]
                if not columns.simple:
                    self.set_columns(columns.take(pos))
                return self
            else:
                return self.iloc[:,pos]
        return
    
    # 2021-09-27
    def tail(self, n = 5):
        '''返回后n行'''
        return self.iloc[-n:]

# 4.2 数据表索引器类

# 2021-05-27
class ArrayFrameLocIndexer:
    '''
    简单数据表ILoc索引器类。
    '''
    
    # 2021-05-29
    def __init__(self, frame, index = None, columns = None, copy = False,
        iloc = False):
        if not isinstance(frame,ArrayFrame):
            raise TypeError('ArrayFrame required.')        
        self.frame = frame
        self._ILoc = iloc
        self.set_index(index,0,copy)
        self.set_index(columns,1,copy)
        return
    
    # 2021-05-29
    def __getitem__(self, item):
        if self._NeedSplit(item):
            x, xsingle = self.index._GetPrep(item[0])
            y = self.columns[item[1]]
        else:
            x, xsingle = self.index._GetPrep(item)
            y = None
        
        frame = self.frame
        if IsIterable(x) and IsIterable(y):
            data = frame._ValidData[TupleProduct(x,y,order=AnsiOrder)].reshape(
                (len(x),len(y)),order=AnsiOrder)
            owndata = True
        else:
            data = frame._ValidData[x] if y is None else frame._ValidData[x,y]
            if not IsArray(data):
                return data
            owndata = data.flags.owndata
        
        if data.ndim==1:
            if xsingle:
                return ArrayFrame(
                    data = data.reshape((1,len(data)),order=AnsiOrder),
                    index = frame.index.take(x),
                    columns = frame.columns,
                    dtype = frame.dtype,
                    auto_expand = frame._AutoExpand,
                    expand_count = frame._ExpandCount,
                    expand_ratio = frame._ExpandRatio,
                    _assign_manager = None if owndata else frame._AssignManager
                )
            else:
                return ArraySeries(
                    data = data,
                    index = frame.index.take(x),
                    dtype = data.dtype,
                    name = item[1],
                    auto_expand = frame._AutoExpand[0],
                    expand_count = frame._ExpandCount[0],
                    expand_ratio = frame._ExpandRatio[0],
                    _assign_manager = None if owndata else frame._AssignManager
                )
        else:
            return ArrayFrame(
                data = data,
                index = frame.index.take(x),
                columns = frame.columns if y is None else frame.columns.take(y),
                dtype = frame.dtype,
                auto_expand = frame._AutoExpand,
                expand_count = frame._ExpandCount,
                expand_ratio = frame._ExpandRatio,
                _assign_manager = None if owndata else frame._AssignManager
            )
    
    # 2022-02-10
    def __iter__(self):
        return self.columns.__iter__()
    
    # 2021-06-15
    def __setitem__(self, item, value):
        frame = self.frame
        shape = frame.shape
        if self._NeedSplit(item):
            x = item[0]
            y = item[1]
        else:
            x = item
            y = None
        
        # 值处理
        vsingle = IsSingleType(value)
        if vsingle:
            vshape = (1,1)
        elif isinstance(value,ArraySeries):
            if value.empty:
                return
            vshape = (1,value._ValidLen) if IsInteger(x) \
                else (value._ValidLen,1)
            value = value._ValidData
        elif isinstance(value,ArrayFrame):
            if value.empty:
                return
            vshape = value._ValidShape
            value = value._ValidData
        else:
            if not IsArray(value):
                value = np.array(value,copy=False,order=AnsiOrder)
            if value.ndim==1:
                vlen = value.shape[0]
                if vlen==0:
                    return
                vshape = (1,vlen) if IsInteger(x) else (vlen,1)
            else:
                vshape = value.shape[:2]
                if vshape[0]==0 or vshape[1]==0:
                    return
        
        # 空数据框处理
        if not self._ILoc and frame.shape==(0,0):
            frame._SetData(value)
            if not IsSlice(x):
                self.set_index(x)
                frame.index = self.index
                frame._NoLoc = False
            if not y is None and not IsSlice(y):
                self.set_index(y,1)
                frame.columns = self.columns
                frame.ix.columns = self.columns
                frame._NoLoc = False
            return
        
        # 下标处理
        x, maxxlen = self.index._SetPrep(x)
        if maxxlen is None:
            maxxlen = shape[0] if shape[0]>0 else vshape[0]
        else:
            maxxlen = max(maxxlen,shape[0])
        if y is None:
            maxylen = shape[1] if shape[1]>0 else vshape[1]
        else:
            y, maxylen = self.columns._SetPrep(y)
            if maxylen is None:
                maxylen = shape[1] if shape[1]>0 else vshape[1]
            else:
                maxylen = max(maxylen,shape[1])
        if maxxlen>shape[0] or maxylen>shape[1]:
            frame._UpdateValidShape((maxxlen,maxylen))
        
        data = frame._ValidData
        if y is None:
            data[x] = value
        elif IsIterable(x) and IsIterable(y):
            data[TupleProduct(x,y,order=AnsiOrder)] = value if vsingle \
                else value.reshape((len(x)*len(y),),order=AnsiOrder)
        else:
            data[x,y] = value
        frame._AssignManager.AssignOnce()
        return
    
    # 2022-01-07
    def _NeedSplit(self, item):
        '''判定item是否需要按维度切分'''
        if isinstance(item,tuple):
            if self._ILoc:
                return True
            elif type(self.index) is ArrayMultiIndex:
                if isinstance(item[0],tuple) or isinstance(item[0],slice):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    
    # 2021-07-02
    def _UpdateValidShape(self, targetShape):
        '''更新索引形状'''
        self.index._UpdateLen(targetShape[0])
        self.columns._UpdateLen(targetShape[1])
        return
    
    # 2022-02-08
    def reindex(self, index = None, columns = None, method = 'keep', 
        fill_value = NA, dupl_method = 'all', drop_index = False, axis = 0):
        '''
        索引。
        【参数表】
        index - 索引
        method - 索引不存在时的处理方法（参考DataFrame.reindex同名参数）
          ffill/pad - 后向填充（取小于其的最大值）
          bfill/backfill - 前向填充（取大于其的最小值）
          keep - 保持空行
          ignore - 忽略本行
        fill_value - 默认填充值
        dupl_method - 重复值处理方式
          all - 返回全部下标
          first - 返回首个下标
          last - 返回最后一个下标
        drop_index - 返回值是否不包含下标
        '''
        frame = self.frame
        values = frame._ValidData
        
        if axis==0:
            pos, rtindex = self.index.reindex(
                index,method,dupl_method,drop_index)
            plen = len(pos)
            ppos = which(pos>=0)
            pplen = len(ppos)
            cpos = slice(None) if columns is None else self.columns[columns]
            
            if plen==0:
                rtdata = None
                rtindex = None
            elif pplen==plen:
                if columns is None:
                    rtdata = values[pos]
                elif values.flags.c_contiguous:
                    rtdata = values[:,cpos][pos]
                else:
                    rtdata = values[pos][:,cpos]
            else:
                if IsSingleType2(cpos):
                    clen = frame.shape[1] if IsSlice(cpos) else 1
                else:
                    clen = len(cpos)
                rtdata = np.ndarray(
                    shape = (plen,clen),
                    dtype = frame.dtype,
                    order = AnsiOrder
                )
                rtdata[:,:] = fill_value
                if pplen>0:
                    if columns is None:
                        v = values[pos[ppos]]
                    elif values.flags.c_contiguous:
                        v = values[:,cpos][pos[ppos]]
                    else:
                        v = values[pos[ppos]][:,cpos]
                    # v = frame._ValidData[pos[ppos],cpos]
                    if IsSingleType2(v):
                        rtdata[ppos] = v
                    elif v.ndim==1:
                        if pplen==1:
                            rtdata[ppos] = v.reshape((1,v.shape[0]))
                        else:
                            rtdata[ppos] = v.reshape((v.shape[0],1))
                    else:
                        rtdata[ppos] = v
            return ArrayFrame(
                data = rtdata,
                index = rtindex,
                columns = frame.columns if columns is None else columns,
                dtype = frame.dtype,
                auto_expand = frame._AutoExpand,
                expand_count = frame._ExpandCount,
                expand_ratio = frame._ExpandRatio
            )
        elif IsInteger(axis):
            pos, rtcols = self.columns.reindex(
                columns,method,dupl_method,drop_index)
            plen = len(pos)
            ppos = which(pos>=0)
            pplen = len(ppos)
            rpos = slice(None) if index is None else self.index[index]
            
            if plen==0:
                rtdata = None
                rtindex = None
            elif pplen==plen:
                if index is None:
                    rtdata = values[:,pos]
                elif values.flags.c_contiguous:
                    rtdata = values[:,pos][rpos]
                else:
                    rtdata = values[rpos][:,pos]
            else:
                if IsSingleType2(rpos):
                    rlen = frame.shape[1] if IsSlice(rpos) else 1
                else:
                    rlen = len(rpos)
                rtdata = np.ndarray(
                    shape = (rlen,plen),
                    dtype = frame.dtype,
                    order = AnsiOrder
                )
                rtdata[:,:] = fill_value
                if pplen>0:
                    if index is None:
                        v = values[:,pos[ppos]]
                    elif values.flags.c_contiguous:
                        v = values[:,pos[ppos]][rpos]
                    else:
                        v = values[rpos][:,pos[ppos]]
                    # v = frame._ValidData[rpos,pos[ppos]]
                    if IsSingleType2(v):
                        rtdata[:,ppos] = v
                    elif v.ndim==1:
                        if pplen==1:
                            rtdata[:,ppos] = v.reshape((v.shape[0],1))
                        else:
                            rtdata[:,ppos] = v.reshape((1,v.shape[0]))
                    else:
                        rtdata[:,ppos] = v
            return ArrayFrame(
                data = rtdata,
                index = frame.index if index is None else index,
                columns = rtcols,
                dtype = frame.dtype,
                auto_expand = frame._AutoExpand,
                expand_count = frame._ExpandCount,
                expand_ratio = frame._ExpandRatio
            )
        elif list(axis)==[0,1]:
            if isinstance(method,str):
                method = [method,method]
            if isinstance(dupl_method,str):
                dupl_method = [dupl_method,dupl_method]
            if isinstance(drop_index,bool):
                drop_index = [drop_index,drop_index]
            rpos, rtindex = self.index.reindex(
                index,method[0],dupl_method[0],drop_index[0])
            rlen = len(rpos)
            rppos = which(rpos>=0)
            rplen = len(rppos)
            cpos, rtcols = self.columns.reindex(
                columns,method[1],dupl_method[1],drop_index[1])
            clen = len(cpos)
            cppos = which(cpos>=0)
            cplen = len(cppos)
            
            if rlen==0:
                rtdata = None
                rtindex = None
            elif clen==0:
                rtdata = None
                rtcols = None
            elif rplen==rlen and cplen==clen:
                values = frame._ValidData
                if values.flags.c_contiguous:
                    rtdata = values[:,cpos][rpos]
                else:
                    rtdata = values[rpos][:,cpos]
            else:
                rtdata = np.ndarray(
                    shape = (rlen,clen),
                    dtype = frame.dtype,
                    order = AnsiOrder
                )
                rtdata[:,:] = fill_value
                if rplen>0 and cplen>0:
                    if rplen<cplen:
                        for r in rppos:
                            rtdata[r,cppos] = values[rpos[r],cppos]
                    else:
                        for c in cppos:
                            rtdata[rppos,c] = values[rppos,cpos[c]]
                    
                    # if values.flags.c_contiguous:
                    #     v = values[:,cpos[cppos]][rpos[rppos]]
                    # else:
                    #     v = values[rpos[rppos]][:,cpos[cppos]]
                    # if IsSingleType2(v):
                    #     rtdata[rppos,cppos] = v
                    # elif rplen==1:
                    #     rtdata[rppos,cppos] = v.reshape((1,cplen))
                    # elif cplen==1:
                    #     rtdata[rppos,cppos] = v.reshape((rplen,1))
                    # else:
                    #     rtdata[rppos,cppos] = v
            return ArrayFrame(
                data = rtdata,
                index = rtindex,
                columns = rtcols,
                dtype = frame.dtype,
                auto_expand = frame._AutoExpand,
                expand_count = frame._ExpandCount,
                expand_ratio = frame._ExpandRatio
            )
        else:
            return None
    
    # 2021-07-19
    def set_index(self, index = None, axis = 0, copy = False, 
        _assign_manager = None):
        '''
        设置索引。
        【注】axis为0对应行/index，为1对应列/columns。
        '''
        frame = self.frame
        if self._ILoc or index is None or type(index) is ArrayIndex \
            or IsSimpleIndex(index):
            if axis==0:
                self.index = frame.iloc.index if hasattr(frame,'iloc') \
                    else ArrayIndex(frame._ValidShape[0])
            else:
                self.columns = frame.iloc.columns if hasattr(frame,'iloc') \
                    else ArrayIndex(frame._ValidShape[1])
            return
        
        if isinstance(index,ArrayIndex):
            if frame._ValidShape[axis]==0:
                frame._UpdateEmptyAxisLen(axis,len(index))
            elif frame._ValidShape[axis]!=len(index):
                raise ValueError('Index size mismatch.')
            if copy:
                index = index.copy()
        elif IsSingleType(index):
            if frame._ValidShape[axis]==0:
                frame._UpdateEmptyAxisLen(axis,1)
            elif frame._ValidShape[axis]!=1:
                raise ValueError('Index size mismatch.')
            index = ArrayValueIndex(index)
        elif IsIndex(index):
            if frame._ValidShape[axis]==0:
                frame._UpdateEmptyAxisLen(axis,len(index))
            elif frame._ValidShape[axis]!=len(index):
                raise ValueError('Index size mismatch.')
            if IsMultiIndex(index):
                index = ArrayMultiIndex(np.array(tuple(index.values)))
            else:
                index = ArrayValueIndex(
                    values = index.values,
                    copy = copy,
                    _assign_manager = _assign_manager
                )
        elif IsSingleType(index[0]):
            if frame._ValidShape[axis]==0:
                frame._UpdateEmptyAxisLen(axis,len(index))
            elif frame._ValidShape[axis]!=len(index):
                raise ValueError('Index size mismatch.')
            index = ArrayValueIndex(
                values = index,
                copy = copy,
                _assign_manager = _assign_manager
            )
        else:
            vlen = len(index[0])
            for i in range(1,len(index)):
                if len(index[i])!=vlen:
                    raise ValueError('Index size mismatch.')
            if frame._ValidShape[axis]==0:
                frame._UpdateEmptyAxisLen(axis,vlen)
            elif frame._ValidShape[axis]!=vlen:
                raise ValueError('Index size mismatch.')
            index = ArrayMultiIndex(index)
        
        if axis==0:
            self.index = index
        else:
            self.columns = index
        return

if __name__=='__main__':
    import doctest
    doctest.testmod()
