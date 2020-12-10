#!/usr/bin/env python
# _*_ coding:utf-8 _*_
class Button():
    def __init__(self,button_name):
        self.precondition = ''
        self.platform_name = ''
        self.project_name = ''
        self.model_name = ''
        self.sub_model_name = ''
        self.function_name = button_name
        self.case = dict()
        self.case[button_name + "单击"] = ["单击%s后，响应正常，结果显示正确。"%button_name, '单击按钮']
        self.case[button_name + "双击"] = ["双击%s后，响应正常，结果显示正确。"%button_name, '双击按钮']
    def __eq__(self, other):
        if  isinstance(other, Button):
            return (self.function_name == other.function_name)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return  hash(self.function_name)
    def add_case(self,case_name,case_pre='',case_step=''):
        self.case[case_name] = [case_pre,case_step]
    def set_precondition(self,precondition):
        self.precondition = precondition
    def set_platform_name(self,plName):
        self.platform_name = plName
    def set_project_name(self,pjName):
        self.project_name = pjName
    def set_model_name(self,mdName):
        self.model_name = mdName
    def set_sub_model_name(self,smdName):
        self.sub_model_name = smdName
    def set_function_name(self,ftName):
        self.function_name = ftName
    def all_cases(self):
        return self.case