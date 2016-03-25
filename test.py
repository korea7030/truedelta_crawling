# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:33:19 2015

@author: Administrator
"""

import pymysql

connection = pymysql.connect(host='localhost'
                             ,user='leejh'
                             ,password='leejh'
                             ,db='pythondb'
                             ,charset='utf8mb4'
                             ,cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql="INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org','very-secret' ))
        
    connection.commit()
    
    with connection.cursor() as cursor:
        sql="SELECT email, password FROM users WHERE email=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result=cursor.fetchone()
        print(result)
finally:
    connection.close()
    