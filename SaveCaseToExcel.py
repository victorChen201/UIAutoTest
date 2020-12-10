#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import re
import Input_Case
class SaveCaseToExcel(object):
    def __init__(self):
        heads = ('测试平台','项目名称','模块名称','子模块名称','功能','用例名称','前置条件','版本号','步骤','预期结果')
        self.df = pd.DataFrame(columns=heads)
        self.case_numbers = 1
    def writeCase(self,case):
        if not isinstance(case.all_cases(), dict):
            print ("用例集错误")
            return 1
        for key, value in case.all_cases().items():
            example = {'测试平台': case.platform_name,
                       '项目名称': case.project_name,
                       '模块名称': case.model_name,
                       '子模块名称': case.sub_model_name,
                       '功能': case.function_name,
                       '用例名称': key,
                       '前置条件': case.precondition,
                       '版本号': '',
                       '步骤': value[1],
                       '预期结果': value[0]}
            self.df.loc[self.case_numbers] = example
            self.case_numbers = self.case_numbers+1
        # print (self.df)
    def writeCases(self,cases):
        if isinstance(cases,list) or isinstance(cases,set):
            for case in cases:
                self.writeCase(case)
        else:
            self.writeCase(cases)
    def saveCaseToExcel(self,name):
        self.df.to_excel(name)

if __name__ == "__main__":
    cases = Input_Case.Input_Text("测试")
    cases.precondition = "登陆adx,进入审核"
    s = SaveCaseToExcel()
    s.writeCases(cases)
    s.saveCaseToExcel('Testcase.xlsx')