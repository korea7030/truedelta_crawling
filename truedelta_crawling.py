# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 11:10:10 2015

@author: Administrator
"""

import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver

truedelta_url = 'http://www.truedelta.com/problems'

## All Years Id :rh-model-year, xpath :  /html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[2]/td/select
## Select make Id : rh-make , xpath : /html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[3]/td/select
## Select model Id : rh-model, xpath : /html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[4]/td/select 
## Search Xpath : /html/body/div[3]/div[2]/div/div[1]/form/fieldset/div/input[2]

driver = webdriver.Firefox()
driver.get(truedelta_url)
driver.implicitly_wait(10)

# get id
# element_year = driver.find_element_by_id('rh-model-year')
# element_make = driver.find_element_by_id('rh-make')
# element_model = driver.find_element_by_id('rh-model')

# get xpath
element_year = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[2]/td/select[@name='year']")
element_brand = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[3]/td/select[@name='brand']")
element_model = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[4]/td/select[@name='model']")

# get list 
list_year = [x for x in element_year.find_elements_by_tag_name("option")]

# print("brand = "+str(list_brand))

# print("model = "+str(list_model))
element_year.find_elements_by_tag_name
for year in list_year:
    if (year.get_attribute("value") == "") :
        continue
    else :
        year.click()
        list_brand = [x for x in element_brand.find_elements_by_tag_name("option")]
        for brand in list_brand:
            # brand.text - option text 값
            # brand.get_attribute("value") - option value값            
            if (brand.get_attribute("value") == ""):
                continue
            else:
                brand.click()
                list_model = [x for x in element_model.find_elements_by_tag_name("option")]
                for model in list_model:
                    if (model.text=="Select model"):
                        continue
                    elif (model.get_attribute("value") == ""):
                        break                        
                    else:                        
                        model.click()
                        html = driver.page_source
                        print(html)
#==============================================================================
#                       div class="header" , h2 , p  
#                       table-container
#                       
#==============================================================================
                    # html = driver.page_source
                    # print(html)
    #print year.get_attribute("value")
           
# for option_year in element_year.find_elements_by_tag_name('option'):
#     option_year.click()
#     for option_make in element_make.find_elements_by_tag_name('option'):
#        option_make.click()
#        for option_model in element_model.find_elements_by_tag_name('option'):
#            option_model.click()
#            element_btn.click() 
#            html = driver.page_source
#            print(html)
    
#    driver.back()        
        
    


