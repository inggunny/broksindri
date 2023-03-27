# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 21:56:20 2023

@author: elbia
"""

import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import matplotlib as mpl
import matplotlib.pyplot as plt
import getpass
import time

DB_user = input("Please enter MySQL username: ")
Pass_user = getpass.getpass("Please enter MySQL Password: ") #getpass para que no se visualize la contraseña
Grade_pol = int(input("Please enter the degree of the polynomal prediction: ")) #grado del polinomio


start_time = time.time() #define tiempo de inicio de ejecución de programa

SQLconfig = {
  'user': DB_user,
  'password': Pass_user,
  'host': '10.243.0.96',
  'database': 'test123',
  'raise_on_warnings': True
}

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
    mycursor = cnx.cursor()
    sql = "SELECT * FROM semana1"
    df_week1 = pd.read_sql(sql,cnx)
    sql = "SELECT * FROM semana2"
    df_week2 = pd.read_sql(sql,cnx)    
    sql = "SELECT * FROM semana3"
    df_week3 = pd.read_sql(sql,cnx)
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'test123'" #obtiene cantidad de tablas
    mycursor.execute(sql)
    x_temp = mycursor.fetchone()


mycursor.close()
cnx.close()


df_predict = pd.DataFrame(columns=["ID","IPcount"]) #arma el DF de predicción

print("Working...")
for ind in df_week1["ID"]: #bucle for por índice
    try:
        y_temp=[]
        index_week1 = df_week1.loc[ind, "IPcount"]   
        index_week2 = df_week2.loc[ind, "IPcount"]
        index_week3 = df_week3.loc[ind, "IPcount"]   
        y_temp.append(index_week1)
        y_temp.append(index_week2)
        y_temp.append(index_week3)
        #obtiene todos los valores para un mismo índice
    
        x_train = list(range(0,x_temp[0])) #el valor a predecir es función de la cantidad de tablas. range crea una lista
        y_train = y_temp
        
        x_test = len(y_temp) #los indices empiezan en 0, entonces len siempre estará uno arriba
    
        try:
            model2 = np.poly1d(np.polyfit(x_train,y_train,Grade_pol)) #predicción
            y_test = model2(x_test)
            df_predict.loc[len(df_predict.index)] = [ind,y_test] #añade al df de predicción la predicción en el índice del bucle for
        except:
            print("No enough data")
            y_test = 0
    except KeyboardInterrupt:
        print("Salida Manual")
    except Exception:
        pass

print("Code Execution Time: %s seconds"%(time.time()-start_time))
df_week1.plot(x="ID",title="Week 1")
df_week2.plot(x="ID",title="Week 2")
df_week3.plot(x="ID",title="Week 3")
df_predict.plot(x="ID",title="Next Week Prediction")
plt.show()
