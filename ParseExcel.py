#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import re
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
                limit = self.df.loc[i, "限值"]
                limit = str(limit).split(',')
                if limit.__len__()>1:
                    case = Input_Case.Input_Text(self.df.loc[i, "功能点"],limit[0],limit[-1],is_need=self.df.loc[i, "是否必填"])
                elif limit.__len__()==1:
                    case = Input_Case.Input_Text(self.df.loc[i, "功能点"], max=limit[0],is_need=self.df.loc[i, "是否必填"])
                else:
                    case = Input_Case.Input_Text(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "多行文本框":
                limit = self.df.loc[i, "限值"]
                limit = str(limit).split(',')
                if limit.__len__() > 1:
                    case = Input_Case.Input_Textarea(self.df.loc[i, "功能点"], limit[0], limit[-1],is_need=self.df.loc[i, "是否必填"])
                elif limit.__len__() == 1:
                    case = Input_Case.Input_Textarea(self.df.loc[i, "功能点"], max=limit[0],is_need=self.df.loc[i, "是否必填"])
                else:
                    case = Input_Case.Input_Textarea(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "数字文本框":
                limit = self.df.loc[i, "限值"]
                limit = str(limit).split(',')
                if limit.__len__() > 1:
                    case = Input_Case.Input_Number(self.df.loc[i, "功能点"], limit[0], limit[-1],is_need=self.df.loc[i, "是否必填"])
                elif limit.__len__() == 1:
                    case = Input_Case.Input_Number(self.df.loc[i, "功能点"], max=limit[0],is_need=self.df.loc[i, "是否必填"])
                else:
                    case = Input_Case.Input_Number(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "单选下拉框":
                case = Input_Case.Input_Select(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "多选下拉框":
                case = Input_Case.Input_Selects(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "单选框":
                case = Input_Case.Input_Radio(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "复选框":
                case = Input_Case.Input_Checkbox(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "左右选择框":
                case = Input_Case.Input_bootstrap_Select(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "日期":
                case = Input_Case.Input_Date(self.df.loc[i, "功能点"],is_need=self.df.loc[i, "是否必填"])
            elif self.df.loc[i, "控件类型"] == "按钮":
                if re.search(".*(建|增).*",self.df.loc[i,"功能点"]):
                    case = Button_Case.Add_Button(self.df.loc[i, "功能点"])
                elif re.search(".*保存.*",self.df.loc[i,"功能点"]):
                    case = Button_Case.Save_Button(self.df.loc[i, "功能点"])
                elif re.search(".*查.*",self.df.loc[i,"功能点"]):
                    case = Button_Case.Search_Button(self.df.loc[i, "功能点"])
                elif re.search(".*删.*", self.df.loc[i, "功能点"]):
                    case = Button_Case.Delete_Button(self.df.loc[i, "功能点"])
                elif re.search(".*(返|取).*", self.df.loc[i, "功能点"]):
                    case = Button_Case.Return_Button(self.df.loc[i, "功能点"])
                elif re.search(".*(编|改).*", self.df.loc[i, "功能点"]):
                    case = Button_Case.Edit_Button(self.df.loc[i, "功能点"])
                else:
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