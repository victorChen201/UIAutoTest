#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import Input_Case,Button_Case
from SaveCaseToExcel import SaveCaseToExcel
class ParseExcel():
    def __init__(self,name='config.xlsx'):
        self.df = pd.read_excel(name,usecols="A:M")
        self.cases = []
        self.__make_case__()
    def __make_case__(self):
        for i in self.df.index:
            if self.df.loc[i, "控件类型"] == "文本框":
                case = Input_Case.Input_Text(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "多行文本框":
                case = Input_Case.Input_Textarea(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "数字文本框":
                case = Input_Case.Input_Number(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "单选下拉框":
                case = Input_Case.Input_Select(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "多选下拉框":
                case = Input_Case.Input_Selects(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "单选框":
                case = Input_Case.Input_Radio(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "复选框":
                case = Input_Case.Input_Checkbox(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "左右选择框":
                case = Input_Case.Input_bootstrap_Select(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "日期":
                case = Input_Case.Input_Date(self.df.loc[i, "功能点"])
            elif self.df.loc[i, "控件类型"] == "按钮":
                case = Button_Case.Button(self.df.loc[i, "功能点"])
            else:
                print ("为定义类型")
                case = None
            if case:
                case.set_platform_name(self.df.loc[i, "项目类型"])
                case.set_project_name(self.df.loc[i, "项目"])
                case.set_model_name(self.df.loc[i, "模块"])
                case.set_sub_model_name(self.df.loc[i, "子模块"])
                case.set_function_name(self.df.loc[i, "功能点"])
                case.add_must_need_case(self.df.loc[i, "是否必填"])
                case.set_precondition(self.df.loc[i, "前置条件"])
                case.set_version(self.df.loc[i, "版本标签"])
                case.set_relative_need(self.df.loc[i, "关联需求"])
                self.cases.append(case)
    def get_cases(self):
        return self.cases
if __name__ == "__main__":
    pe = ParseExcel('config.xlsx')
    s = SaveCaseToExcel()
    s.writeCases(pe.get_cases())
    s.saveCaseToExcel("Testcase.xlsx")