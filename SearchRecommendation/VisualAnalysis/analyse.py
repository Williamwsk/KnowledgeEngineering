# -*- coding: utf-8 -*-  
import numpy as np    
import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt    

f = open('search_temp.txt','r')  
a = f.read()  
sr_txt = eval(a)  
f.close() 

labels=sr_txt.keys()
total = sum(sr_txt.values())
X = [float(val)/float(total) for val in sr_txt.values()]
  
fig = plt.figure()  
plt.pie(X,labels=labels,autopct='%1.2f%%') 
plt.title("Searched words chart")  
    
  
#plt.show()    
plt.savefig("sw_Chart.jpg")
plt.show("sw_Chart.jpg")

