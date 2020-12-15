#!/usr/bin/env python
# _*_ coding:utf-8 _*_

class Case_Struct():
    def __init__(self,priority='P0',is_access='否',is_auto = '否',steps = '',pre_result = ''):
        self.priority = priority
        self.is_access = is_access
        self.is_auto = is_auto
        self.steps = steps
        self.pre_result = pre_result
        self.test_result = ''
        self.remarks = ''

    def __eq__(self, other):
        if  isinstance(other, Button):
            return (self.function_name == other.function_name)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return  hash(self.function_name)
    def set_steps(self, steps):
        self.steps = steps
    def set_pre_result(self, pre_result):
        self.pre_result = pre_result
    def set_priority(self,priority):
        self.priority = priority
    def set_is_access(self,is_access):
        self.is_access = is_access
    def set_test_result(self,test_result):
        self.test_result = test_result
    def set_remarks(self,remarks):
        self.remarks = remarks
