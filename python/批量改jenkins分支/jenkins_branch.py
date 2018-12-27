#coding=utf-8

from selenium import webdriver
import os
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#设置浏览器驱动
driver = webdriver.Chrome('/Users/mac/Downloads/chromedriver')

#最大化窗口
driver.maximize_window()

jenkinsPage = 'http://192.168.199.120:8080/job/uat5/'

projectFileName = 'jenkinsProject_uat5.xls'

def getProjects(driver):
    projects = []
    project_tr_list =  driver.find_element_by_id('projectstatus').find_elements_by_tag_name("tr")
    file = open(projectFileName,'w')
    for i in range(len(project_tr_list)):
        project_tr = project_tr_list[i]
        
        print (project_tr.text)
        text = project_tr.text
        project_td_list = [str(n) for n in text.split()]  
        if len(project_td_list) > 0 and i!=0:
            file.write(project_td_list[0] +'\n')
            print (project_td_list[0])
    file.close()

print("+++++++++++++++++++++++++++++++++++++++1")

driver.get(jenkinsPage)
time.sleep(10)
getProjects(driver)
print("+++++++++++++++++++++++++++++++++++++++2")
driver.quit()
