# -*- coding: utf-8 -*-
"""
Created on Fri May 27 10:41:02 2022

@author: elbia
"""

import logReader
import pandas as pd
import matplotlib.pyplot as plt

path1 = "/home/victor/tesis/python/last_gunny2.txt"
path2 = "/home/victor/tesis/python/delta_gunny2.txt"
path3 = "/home/victor/tesis/python/hist_gunny2.txt"

t0 = {}
pd_test_delta = pd.DataFrame()
pd_test_last = pd.DataFrame()
pd_test_hist = pd.DataFrame()

    
with open(path1) as f:
    for line in f:
       (key, val) = line.split(":")
       t0[key] = int(val)
f.close()

print(t0)

t1 = logReader.lectura('/var/log/nginx/access.log',
                       '/var/log/nginx/access.log.1',
                       '/home/victor/tesis/python/current_line.txt')

t1_0 = t1[0]
t1_1 = t1[1]

new_cur_lin = t1_1

t0_delta = t0.copy()
t1_delta = t1_0.copy()

t0_last = t0.copy()
t1_last = t1_0.copy()

t0_hist = t0.copy()
t1_hist = t1_0.copy()

"""    
print("t0")
print(t0)
print("\n")
print("t1")
print(t1_0)
print("\n")
"""    

for key in t1_delta.copy():
    print("key "+key)
    print(t0_delta)
    if key in t0_delta.copy():
        IP_updated = t1_delta[key] - t0_delta[key]
        print(IP_updated)
        t0_delta[key] = IP_updated
        t1_delta.pop(key)
    else:
        print("no existe")

t0_delta = {**t0_delta , **t1_delta}
print(t0_delta)
print("\n")

for key in t0_last.copy():
    if key in t1_last.copy():
        pass
    else:
        t0.pop(key)
        
t0_last = {**t0,**t1_0}


for key in t1_hist.copy():
    if key in t0_hist.copy():
        if t1_hist[key] > t0_hist[key]:
            t0_hist[key] = t1_hist[key]
            t1_hist.pop(key)
        else:
            t1_hist.pop(key)
    else:
        pass

t0_hist = {**t0_hist,**t1_hist}


#    print(t0_delta)
#    print(t1_last)
#    print(t0_hist)

t0_delta_pd = pd.DataFrame.from_dict(t0_delta.items())
t1_last_pd = pd.DataFrame.from_dict(t1_last.items())
t0_hist_pd = pd.DataFrame.from_dict(t0_hist.items())

pd_test_delta = pd_test_delta.append(t0_delta_pd,ignore_index=True)
pd_test_last = pd_test_last.append(t1_last_pd,ignore_index=True)
pd_test_hist = pd_test_hist.append(t0_hist_pd,ignore_index=True)

#t0_delta_ax = t0_delta_pd.plot.bar(x=0, y=1, rot=0,title="delta")
#t1_last_ax = t1_last_pd.plot.bar(x=0,y=1,rot=0,title="ultimo")
#t0_hist_ax = t0_hist_pd.plot.bar(x=0,y=1,rot=0,title="maximo")


with open(path2, 'w') as d: 
    for key, value in t0_delta.items(): 
        d.write('%s:%s\n' % (key, value))
d.close()        



with open(path1, 'w') as l: 
    for key, value in t1_last.items(): 
        l.write('%s:%s\n' % (key, value))
l.close()


with open(path3, 'w') as h: 
    for key, value in t0_hist.items(): 
        h.write('%s:%s\n' % (key, value))
h.close()
   
    

print(pd_test_delta)
#pd_test_delta.plot.bar(x=0,y=1,rot=0,title="delta")
#pd_test_last.plot.bar(x=0,y=1,rot=0,title="ultimo")
#pd_test_hist.plot.bar(x=0,y=1,rot=0,title="maximo")
print(new_cur_lin)

with open('/home/victor/tesis/python/current_line.txt', 'w') as c: 
    c.write(str(new_cur_lin))
c.close()


