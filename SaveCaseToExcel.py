#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import pandas as pd
import re
import Input_Case
class SaveCaseToExcel(object):
    def __init__(self):
        heads = ('项目类型','项目','模块','子模块','功能点','用例标题','优先级','是否准入用例','是否自动化','关联需求','版本标签','前置条件','测试步骤','期望结果','附件图片','测试结果','备注','用例作者')
        self.df = pd.DataFrame(columns=heads)
        self.case_numbers = 1
    def writeCase(self,case):
        if not isinstance(case.all_cases(), dict):
            print ("用例集错误")
            return 1
        for key, value in case.all_cases().items():
            example = {'项目类型': case.platform_name,
                       '项目': case.project_name,
                       '模块': case.model_name,
                       '子模块': case.sub_model_name,
                       '功能点': case.function_name,
                       '用例标题': key,
                       '优先级': case.priority,
                       '是否准入用例': case.is_access,
                       '是否自动化': case.is_auto,
                       '关联需求': case.relative_need,
                       '前置条件': case.precondition,
                       '版本标签': case.version,
                       '测试步骤': value[1],
                       '期望结果': value[0],
                       '附件图片': case.image,
                       '测试结果': case.test_result,
                       '备注': case.remarks,
                       '用例作者': case.author
                       }
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