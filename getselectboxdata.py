# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 19:15:56 2015

@author: Administrator
"""


from selenium import webdriver

def save_options(lst, n, string):
    filename = 'listoption'+str(n)+'.txt'
    f = open(filename, 'w')
    for option in lst:
        if (option.get_attribute("value") == ''):
            continue
        else:
            if (string == 'year'):
                f.write(option.text+'\n')
                #lstres_year.append(option.text)
            elif (string== 'brand'):
                f.write(str(option.get_attribute("value"))+'\n')
                #lstres_brand.append(option.text)
            else:
                f.write(option.text+'\n')
                #lstres_probarea.append(option.text)
    f.close()

if __name__ == '__main__':
    truedelta_url = 'http://www.truedelta.com/problems'
    
    driver = webdriver.Firefox()
    driver.get(truedelta_url)
    driver.implicitly_wait(10)
    
    element_year = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[2]/td/select[@name='year']")
    element_brand = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[3]/td/select[@name='brand']")
    # element_model = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[4]/td/select[@name='model']")
    element_probarea = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/form/fieldset/table/tbody/tr[5]/td/select[@name='problem_area']")
    
    list_year = [x for x in element_year.find_elements_by_tag_name("option")]
    list_brand = [x for x in element_brand.find_elements_by_tag_name("option")]
    # list_model = [x for x in element_model.find_elements_by_tag_name("option")]
    list_probarea = [x for x in element_probarea.find_elements_by_tag_name("option")]
    # print range(1,4)
    
    save_options(list_year,1,'year')
    save_options(list_brand,2,'brand')
    save_options(list_probarea,3,'probarea')
    
    driver.close()
# print(str(list_year))