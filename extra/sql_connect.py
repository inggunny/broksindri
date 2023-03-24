# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:53:33 2023

@author: elbia
"""

import mysql.connector
from mysql.connector import errorcode


SQLconfig = {
  'user': 'bruno',
  'password': 'nano123',
  'host': '10.243.0.96',
  'database': 'test123',
  'raise_on_warnings': True
}
i=0
try:
  cnx = mysql.connector.connect(**SQLconfig)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    #lectura
    #mycursor = cnx.cursor()
    #sql_lectura = "SELECT * FROM table WHERE columnC LIKE '%09:00:00'"
    print ("se conecto a la bd") 
    #escritura
    #esto asume diccionario:
    mycursor = cnx.cursor()
    with open('rojoS.txt', 'r') as file:
        for line in file:
            i+= 1
            sql_escritura = "INSERT INTO semana3 (ID, IPcount) VALUES (%s, %s)"
            val = (i, line)
            mycursor.execute(sql_escritura, val)
            cnx.commit()       

mycursor.close()
cnx.close()
