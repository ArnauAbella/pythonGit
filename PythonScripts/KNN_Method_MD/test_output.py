#Libraries imports
import csv
import random
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import sklearn.neighbors as nb
import sklearn.cross_validation as cv

headers=['1','2','3','4','class']
df = pd.read_csv('iris.csv',header=None,names=headers)
print(np.array(df['1']))
a = np.array(df[['1','2', '3', '4']]).tolist() 
b = np.array(pd.get_dummies(df['class'])).tolist()
'''
print(a)
print("----------")
print(b)
'''
print(a[0])
c = []
for i in range(len(a)-1):
	c.append(a[i]+b[i])
	if i == 2:
		break
print(a)	
print(c)	
'''
for x in np.nditer(a):
	print(x) 
'''



