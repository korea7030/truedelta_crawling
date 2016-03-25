# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:51:08 2015

@author: Sang
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 23:08:39 2015

@author: Sang
"""

import lxml.html as xhtml
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select


truedelta_url = 'http://www.truedelta.com/problems'
    
driver = webdriver.Firefox()
driver.get(truedelta_url)
driver.implicitly_wait(10)

year = Select(driver.find_element_by_name('year'))
year.select_by_visible_text('2015')

brand = Select(driver.find_element_by_name('brand'))
brand.select_by_value('33')
 
model = Select(driver.find_element_by_name('model'))
model.select_by_visible_text('Outback')

area = Select(driver.find_element_by_name('problem_area'))
area.select_by_value('4')

submit = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/div/input[2]")
submit.click()

html = driver.page_source
p = re.compile('No Results')


if (re.findall(p, html)):
    driver.close()
else:
    # print(html)
    soup = BeautifulSoup(html)
    header_lst = soup.find_all('div', class_='header')
    #container_lst = soup.find_all('div', class_='table-container')
    
    # print (str(header_lst))
    
    for head in header_lst :
        car_nm = head.find('h2').text 
        car_dtl = head.find('p').text
        table_con = head.find_next_sibling()
        
        #print table_con.find_all('tr')
        tr_lst = table_con.find_all('tr')
        for tr in tr_lst:
            td_lst = tr.find('td', class_='data-column')
            data_columns =  str(td_lst).replace('<br/><br/>', '|').replace('<td class="data-column">', '').replace('</td>','')
            # print data_columns
            if data_columns.find("|") != -1 :
                 data_lst = data_columns.split("|")
                 if len(data_lst) == 2:
                    tmp1 = data_lst[0]
                    tmp2 = data_lst[1]
                    print "tmp1 : "+tmp1 
                    print "tmp2 : "+tmp2 
                 elif len(data_lst) == 3:
                    tmp1 = data_lst[0]
                    tmp2 = data_lst[1]
                    tmp3 = data_lst[2]
            else :
                print data_columns
                
            td_desc= tr.find('td', class_='desc-column').text
            # print td_desc
            # print td_lst
            
        # data_con = table_con.find_all('td',class_='data-column')
        # desc_con = table_con.find_all('td',class_='desc-column')
            
        # print data_con
        
#    for contain in container_lst:
#        data_con = contain.find_all('td', class_='data-column')
#        desc_con = contain.find_all('td', class_='desc-column')
        
#        for data in data_con :
#            data_lst = data.find_all(text=True)
#            if len(data_lst) == 1:
#                car_km = data_lst[0]
#            elif len(data_lst) == 2:
#                car_km = data_lst[0]
#/                car_cst = data_lst[1]
#            else:
#                car_km = data_lst[0]
#                car_cst = data_lst[1]
                