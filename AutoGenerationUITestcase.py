#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import os
import time
import re
from selenium import webdriver
import Input_Case,Button_Case
from SaveCaseToExcel import SaveCaseToExcel
class Input():
    def __init__(self,element):
        self.input = element
        self.input_type = None
        self.input_statue = None
        self.input_selects = []
    def get_label(self):
        type = self.input_type if self.input_type else self.get_type()
        label = None
        if type == 1:
            label = self.input.find_elements_by_xpath('../../preceding-sibling::label')
            end = "文本框"
        elif type ==2:
            label = self.input.find_elements_by_xpath('../../../preceding-sibling::label')
            end = "单下拉选框"
        elif type ==31 or type ==32:
            label = self.input.find_elements_by_xpath('../../../preceding-sibling::label')
            end = "多下拉选框"
        elif type == 4:
            label = self.input.find_elements_by_xpath('../../../preceding-sibling::label')
            end = "数字框"
        elif type == 5:
            label = self.input.find_elements_by_xpath('../../../preceding-sibling::label')
            end = "复选框"
        elif type == 6:
            label = self.input.find_elements_by_xpath('../../../preceding-sibling::label')
            end = "单选框"
        elif type == 11:
            label = self.input.find_elements_by_xpath('../../preceding-sibling::label')
            end = ""
        else:
            print ("未处理类型",type)
        if label:
            print (label[0].text,type)
            return (label[0].text+end)
        else:
            return None
    def get_attribute(self, name):
        try:
            a = self.input.get_attribute(name)
        except Exception:
            print ("没有找到属性",name)
            a = None
        return a
    def get_type(self):
        if self.input_type:
            return self.input_type
        tp = self.get_attribute('type')
        disabled = self.get_attribute('disabled')
        if (tp == "text"or tp == "number") and disabled != "true":
            x = self.input.find_elements_by_xpath('./following-sibling::span')
            if x:#可能是单选框或者多选框
                y = self.input.find_elements_by_xpath('../../span')
                if y.__len__() > 1:#多选
                    self.input_statue = self.input.find_elements_by_xpath('..//i')
                    if input_statue:#多选框的选择框
                        self.input_type = 31
                    else:#多选框的显示框
                        self.input_type = 32
                else:#单选
                    self.input_type = 2
            else:#没有的话有可能是纯文本或者数字选择框
                y = self.input.find_elements_by_xpath('./../../span')
                if y:#数字选择框
                    self.input_type = 4
                else:#纯文本框
                    j = self.input.find_elements_by_xpath('../input')
                    if j.__len__()>1: #区间选择
                        self.input_type = 11
                    else:
                        self.input_type = 1
        elif tp=="checkbox" and disabled != "true":
            self.input_type =5
        elif tp == "radio"and disabled != "true":
            self.input_type = 6
        else:
            self.input_type = tp
        return self.input_type
    def get_case(self):
        gl = self.get_label()
        if gl:
            gt = self.get_type()
            if gt == 1:
                return Input_Case.Input_Text(gl)
            elif gt == 2:
                return Input_Case.Input_Select(gl)
            elif gt == 31:
                return Input_Case.Input_Select(gl)
            elif gt == 4:
                return Input_Case.Input_Number(gl)
            elif gt == 5:
                return Input_Case.Input_Checkbox(gl)
            elif gt == 6:
                return Input_Case.Input_Radio(gl)
            elif gt == 11:
                return Input_Case.Input_Date("日期")
            else:
                return None
        else:
            return None
    def get_selects(self):
        type = self.input_type if self.input_type else self.get_type()
        if type == 2 or type == 31:
            i_s = self.input_statue if self.input_statue else self.input.find_elements_by_xpath('..//i')
            if "is-reverse" not in i_s[0].get_attribute("class"):
                try:
                    self.input.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", i)
                time.sleep(1)
            divs = self.driver.find_elements_by_xpath('//div[@x-placement="bottom-start" or @x-placement="up-start"]')
            if divs.__len__() > 0:
                lis = divs[0].find_elements_by_tag_name("li")
                for li in lis:
                    self.input_selects.append(li.text)
            try:
                self.input.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", i)
            return self.input_selects
        return self.input_selects


class Operation_Platform():
    def __init__(self,url='http://duop.imgo.tv/#/login'):
        self.driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        self.driver.get(url)
        self.controls = set()

    def set_up(self):
        pass

    def tear_down(self):
        self.driver.close()

    def login(self,patform_name='AMP'):
        self.patform_name = patform_name
        need_login = self.driver.find_elements_by_xpath('//span[text()="登 录"]')
        if need_login.__len__()==0:
            print ("不需要登陆")
            return
        self.driver.find_element_by_xpath('//input[@placeholder="请输入OA邮箱"]').send_keys('shuangsheng')
        self.driver.find_element_by_xpath('//input[@placeholder="请输入密码"]').send_keys('Css861007/')
        self.driver.find_element_by_xpath('//span[text()="登 录"]').click()
        self.driver.set_page_load_timeout(3)
        self.driver.find_element_by_xpath('//div[text()="%s"]/preceding-sibling::div[2]' % patform_name).click()

    def switch_page(self,page_list=[]):
        self.page_name = page_list
        for p in page_list:
            #判断是否可以展开
            wb = self.driver.find_element_by_xpath('//span[text()="%s"]'%p)
            i_numbers = wb.find_elements_by_xpath('following-sibling::i')
            if i_numbers.__len__()!=0:#能展开
                cs = wb.find_element_by_xpath('../..').get_attribute('class')
                if "is-opened" in cs:
                    pass
                else:
                    wb.click()
                # print (cs)
            else:
                wb.click()

    def find_all_inputs(self,element='',precondition=''):
        inputs = element.find_elements_by_tag_name("input") if element != '' else self.driver.find_elements_by_tag_name("input")
        for i in inputs:
            i = Input(i)
            case = i.get_case()
            if case:
                case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s" % (
                self.patform_name, '->'.join(self.page_name)))
                case.set_platform_name("统一运营平台")
                case.set_project_name(self.patform_name)
                case.set_model_name(self.page_name[0])
                case.set_sub_model_name(self.page_name[-1])
                # case.set_function_name(case.)
                self.controls.add(case)
            else:
                print (i.get_type(),"没有处理")

    def find_all_buttons(self,element='',precondition=''):
        #过滤表格中的button
        bts = element.find_elements_by_xpath('div[not(contains(@class, "cell"))]/button') if element != '' else self.driver.find_elements_by_xpath('//div[not(contains(@class, "cell"))]/button')
        for bt in bts:
            spans = bt.find_elements_by_tag_name('span')
            if spans.__len__() != 0 and spans[0].text != '':
                if re.search("新(建|增).*",spans[0].text):
                    # bt.click()
                    self.driver.execute_script("arguments[0].click();", bt)
                    time.sleep(1)
                    dialogs = self.driver.find_elements_by_xpath('//div[@role="dialog"]')
                    if dialogs:
                        st = dialogs[-1].find_element_by_xpath('./..').get_attribute('style')
                        if "display: none" not in st:
                            self.find_all_inputs(dialogs[-1],precondition="登陆%s,进入%s,点击%s"% (self.patform_name, '->'.join(self.page_name), spans[0].text))
                        else:
                            self.find_all_inputs('', precondition="登陆%s,进入%s,点击%s" % (
                            self.patform_name, '->'.join(self.page_name), spans[0].text))
                    try:
                        bt = dialogs[-1].find_element_by_xpath('.//button[@aria-label="Close"]')
                        self.driver.execute_script("arguments[0].click();", bt)
                        # dialogs[-1].find_element_by_xpath('//button[@aria-label="Close"]').click()
                    except Exception:
                        dialogs[-1].find_element_by_xpath('.//button/span[text()="取 消"]').click()
                    time.sleep(1)
                case = Button_Case.Button(spans[0].text+"按钮")
                case.set_platform_name("统一运营平台")
                case.set_project_name(self.patform_name)
                case.set_model_name(self.page_name[0])
                case.set_sub_model_name(self.page_name[-1])
                case.set_function_name(spans[0].text)
                case.set_precondition(precondition if precondition != '' else "登陆%s,进入%s" % (self.patform_name, '->'.join(self.page_name)))
                self.controls.add(case)

    def find_table_header_body(self):
        body = self.driver.find_elements_by_tag_name('tbody')
        header = self.driver.find_elements_by_tag_name('thead')
        return header,body

    def click_select(self,value):
        selects_element = self.driver.find_element_by_xpath('//div[@x-placement="bottom-start" or @x-placement="up-start"]')
        self.driver.execute_script("arguments[0].click();", selects_element.find_element_by_xpath('.//span[text()="%s"]'%value))
        time.sleep(1)
        # self.driver.execute('arguments[0]',selects_element.find_element_by_xpath('.//span[text()="%s"]'%value))

    def input_search_partition(self,label,values,style='text'):
        label_element = self.driver.find_element_by_xpath('//label[text()="%s"]'%label)
        input_element = label_element.find_element_by_xpath('following-sibling::div[1]//input')
        open_flag = False
        if isinstance(values,list):
            for v in values:
                if style == 'text':
                    input_element.send_keys(v)
                elif style == 'select':
                    if not open_flag:
                        open_flag=True
                        input_element.click()
                    self.click_select(v)
                    time.sleep(1)
                else:
                    print ("style","输入错误")
        else:
            if style == 'text':
                input_element.send_keys(values)
            elif style == 'select':
                input_element.click()
                self.click_select(values)
            else:
                print ("style", "输入错误")


    def search_result(self,label,value):
        find_numbers = 0
        header,body = self.find_table_header_body()
        if body and header:
            ths = header[0].find_elements_by_tag_name('th')
            index = None
            for th in ths:
                lb = th.find_element_by_tag_name('div').text
                if lb in label and lb != '':
                    index = th.get_attribute('class')
                    break
            trs = body[0].find_elements_by_tag_name('tr')
            find_numbers = trs.__len__()
            print (label,"找到",find_numbers)
            if index:
                for tr in trs:
                    div = tr.find_element_by_xpath('td[contains(@class,"%s")]/div'%index.split(" ")[0])
                    if isinstance(value,list):
                        if div.text not in value:
                            return False
                    else:
                        if value not in div.text:
                            return False
        if find_numbers == 0:
            return None
        else:
            return True

    def all_controls(self):
        return self.controls

if __name__=="__main__":
    target = "http://test-admin.da.imgo.tv/adx/creative/pre"
    op = Operation_Platform()
    op.login('AMP')
    op.switch_page(["素材管理", "广告素材"])
    time.sleep(1)
    op.input_search_partition('创意类型','AI图片','select')
    op.input_search_partition('名称/ID', '513889', 'text')
    time.sleep(1)
    print (op.search_result('名称/ID','513889'))
    print (op.search_result('创意类型', 'AI图片'))
    # op.find_all_inputs()
    # op.find_all_buttons()
    s = SaveCaseToExcel()
    s.writeCases(op.all_controls())
    s.saveCaseToExcel("Testcase.xlsx")