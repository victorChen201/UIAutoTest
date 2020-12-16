#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import Case_Struct
class Button():
    def __init__(self,button_name):
        self.precondition = ''
        self.platform_name = ''
        self.project_name = ''
        self.model_name = ''
        self.sub_model_name = ''
        self.function_name = button_name
        # self.priority = ''
        # self.is_access = '否'
        # self.is_auto = '否'
        self.relative_need = ''
        self.version = ''
        self.author = ''
        self.image = ''
        # self.test_result = ''
        # self.remarks = ''
        self.case = dict()
        self.add_case(button_name + "单击", "单击%s后，响应正常，结果显示正确。"%button_name, '单击按钮')
        # self.add_case(button_name + "双击", "双击%s后，响应正常，结果显示正确。"%button_name, '双击按钮','P2')
    def __eq__(self, other):
        if  isinstance(other, Button):
            return (self.function_name == other.function_name)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return  hash(self.function_name)

    def add_case(self, case_name, case_pre='', case_step='', priority='P0'):
        self.case[case_name] = Case_Struct.Case_Struct(pre_result=case_pre, steps=case_step, priority=priority)
        return self.case[case_name]
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
    def set_version(self,version):
        self.version = version
    def set_relative_need(self,relative):
        self.relative_need = relative
    def all_cases(self):
        return self.case
class Add_Button(Button):
    def __init__(self, button_name):
        super(Add_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，跳转到新增页面，页面字段数量、标签，是否必选项、控件类型显示正确。" % button_name, '单击按钮')
class Edit_Button(Button):
    def __init__(self, button_name):
        super(Edit_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，跳转到编辑页面，页面字段数量及内容显示正确。" % button_name, '单击按钮')

class Save_Button(Button):
    def __init__(self, button_name):
        super(Save_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，检查字段类型及是否必填，满足条件则保存成功，否则提示失败详情。" % button_name, '单击按钮')

class Delete_Button(Button):
    def __init__(self, button_name):
        super(Delete_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，所选数据从库中删除。" % button_name, '单击按钮')

class Search_Button(Button):
    def __init__(self, button_name):
        super(Search_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，会根据所选条件刷新显示数据。" % button_name, '单击按钮')
class Return_Button(Button):
    def __init__(self, button_name):
        super(Return_Button,self).__init__(button_name)
        self.add_case(button_name + "单击","单击%s后，不会保存当前数据。" % button_name, '单击按钮')