# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 20:54:14 2015

@author: Administrator
"""


import requests
import re
import json
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import pymysql

list_year = []
list_brand = []
list_probarea = [] 

# par_year,par_brand,car_nm,car_dtl,car_rpr_dt,car_km,car_desc.strip()
def insert_data(year, brand, model,area,ca_nm, ca_dtl, ca_km, ca_cst, ca_desc) :
    
    connection = pymysql.connect(host='localhost',
                             user='leejh',
                             password='leejh',
                             db='pythondb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)            
    try :
        with connection.cursor() as cursor:
            cursor.execute('SET autocommit = 0')
            sql = "INSERT INTO T_TRUEDELTA (T_YEAR, T_BRAND, T_MODEL, T_PR_AREA, T_CAR_NM,T_CAR_DTL, T_CAR_KM, T_CAR_CST, T_CAR_DESC)values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (year, brand, model, area,  ca_nm, ca_dtl, ca_km, ca_cst, ca_desc))
            connection.commit()
    finally:
        connection.close()
    
    
        
def make_optionlist() :
    for i in range(2,4):
        filename = 'listoption'+str(i)+'.txt'
        f = open(filename , 'r')
        
        # print(filename)
        for line in f.readlines():
            if (filename == 'listoption1.txt'):
                list_year.append(line.strip())
            if (filename == 'listoption2.txt'):
                list_brand.append(line.strip())
            if (filename == 'listoption3.txt'):
                list_probarea.append(line.strip())

#==============================================================================
#
# 제목 : div class='header'
# 전체내용 : div class='table-container'
#           내용 : 날짜(월 년), km수, 가격 - data-column
#                 수리내용 - desc-column
# search btn : /html/body/div[3]/div[2]/div/div[1]/form/fieldset/div/input[2]
#==============================================================================
    
def delta_craw(par_year, par_brand, par_model, par_area):
    
    print ("==============================")
    print ("year : "+par_year)
    print ("brand : "+par_brand)
    print ("model : "+par_model)
    print ("area : "+par_area)
    print ("==============================")
    
    car_nm = ''
    car_dtl = ''
    car_km = ''
    car_cst = ''
    car_desc = ''
        
    truedelta_url = 'http://www.truedelta.com/problems'
    
    driver = webdriver.Firefox()
    driver.get(truedelta_url)
    driver.implicitly_wait(10)
    driver.switch_to_default_content()
    
    year = Select(driver.find_element_by_name('year'))
    year.select_by_visible_text(par_year)
    driver.implicitly_wait(5)
    
    brand = Select(driver.find_element_by_name('brand'))
    brand.select_by_value(par_brand)
    driver.implicitly_wait(5)
     
    model = Select(driver.find_element_by_name('model'))
    model.select_by_visible_text(par_model)
    driver.implicitly_wait(5)
    
    area = Select(driver.find_element_by_name('problem_area'))
    area.select_by_value(par_area)
    driver.implicitly_wait(5)
    
    submit = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/div/input[2]")
    submit.click()
    
    driver.implicitly_wait(10)
    
    html = driver.page_source
    p = re.compile('No Results')
    
    if (re.findall(p, html)):
        driver.close()
    else:
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        
        header_lst = soup.find_all('div', class_='header')
        print ("header : "+str(header_lst))        
#==============================================================================
#       h2 : T_CAR_NM/  p : T_CAR_DTL
#       data-column :         
#==============================================================================
        
        for head in header_lst :
            try :
                car_nm = head.find('h2').text 
                car_dtl = head.find('p').text
                
                table_con = head.find_next_sibling()
                
                tr_lst = table_con.find_all('tr')
                print ("tr_lst : "+str(tr_lst))
                
                for tr in tr_lst:
                    td_lst = tr.find('td', class_='data-column')
                    data_columns =  str(td_lst).replace('<br/><br/>', '|').replace('<td class="data-column">', '').replace('</td>','')
                    
                    print "data_columns : "+data_columns
                    
                    if data_columns.find("|") != -1 :
                         data_lst = data_columns.split("|")
                         car_km = data_lst[0]
                         car_cst = data_lst[1]
                    else :
                         car_km= data_columns
                
                
                car_desc= tr.find('td', class_='desc-column').text
            
                print ("==================================\n")
                print ("car_nm : "+car_nm+"\n")
                print ("car_dtl : "+car_dtl+"\n")
                print ("car_km : "+car_km+"\n")                
                print ("car_cst : "+car_cst+"\n")
                print ("car_desc : "+car_desc.strip()+"\n")
                print ("==================================\n")
                print ("!!!!!!!!!!!!!!!Insert 시작!!!!!!!!!!!!!!!!!!!")
                insert_data(par_year,par_brand,par_model,par_area,car_nm,car_dtl,car_km,car_cst,car_desc.strip())
            
            except Exception:
                continue
            
        driver.close()
        
        
if __name__ == '__main__':
    arg1 = int(sys.argv[1])
    arg2 = int(sys.argv[2])
    
    make_optionlist()
    
    print str(range(arg1, arg2))
    
    for year in range(arg1, arg2):
        str_year = str(year)
        for brand in list_brand:
            
            print ("=================")
            print ("brand : "+brand)
            print ("year : "+str_year)
            print ("=================")
            
            url = "http://www.truedelta.com/inc/add_models_rh.php?brand="+brand+"&year="+str_year
            print url
            
            lst_model = requests.get(url)
                        
            json_dat = json.loads(lst_model.text)
            try :
                len_dat = len(json_dat)
            except TypeError:
                continue
                
            for i in range(0,len_dat):
                model = json_dat[i]['model']
                for area in list_probarea:
                    # print area
                    delta_craw(str_year, brand, model, area)