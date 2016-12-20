#Libraries imports
import time
import os
import gc
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import sklearn.neighbors as nb
import sklearn.cross_validation as cv
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt


def normalizeAttribute(attr1):
	a = np.array(attr1)
	#PROBLEMA NO PODEM LLEGIR STRING
	a_norm = normalize(a.astype(np.float), norm='l2')
	#al fer np.array et genera una matriu.. encara que tingui dimensio 1
	return (a_norm.tolist())[0]

def transformGetData(df): #esta funcion debe devolver los datos en un np.array()
	#First Normalize numerical
	AAGE = normalizeAttribute(df['AAGE'])
	WKSWORKYEAR = normalizeAttribute(df['WKSWORKYEAR'])
	CHILDS = normalizeAttribute(df['CHILDS'])
	#MARSUPWT = normalizeAttribute(df['MARSUPWT']) NO FERLA SERVIR
	#then categorical
	F_ACLSWKR =  np.array(pd.get_dummies(df['F_ACLSWKR'])).tolist()
	F_EDUCATION = np.array(pd.get_dummies(df['F_EDUCATION'])).tolist()
	F_STATUSMARIT = np.array(pd.get_dummies(df['F_STATUSMARIT'])).tolist()
	F_AMJIND = np.array(pd.get_dummies(df['F_AMJIND'])).tolist()
	F_AMJOCC = np.array(pd.get_dummies(df['F_AMJOCC'])).tolist()
	F_RACE = np.array(pd.get_dummies(df['F_RACE'])).tolist()
	F_ORIGIN = np.array(pd.get_dummies(df['F_ORIGIN'])).tolist()
	F_ASEX = np.array(pd.get_dummies(df['F_ASEX'])).tolist()
	F_AWKSTAT = np.array(pd.get_dummies(df['F_AWKSTAT'])).tolist()
	F_FILESTATUS = np.array(pd.get_dummies(df['F_FILESTATUS'])).tolist()
	F_HHDFMX = np.array(pd.get_dummies(df['F_HHDFMX'])).tolist()
	F_HHDREL = np.array(pd.get_dummies(df['F_HHDREL'])).tolist()
	F_CONBIRTHFATH = np.array(pd.get_dummies(df['F_CONBIRTHFATH'])).tolist()
	F_CONBIRTHMOTH = np.array(pd.get_dummies(df['F_CONBIRTHMOTH'])).tolist()
	F_PENATVTY = np.array(pd.get_dummies(df['F_PENATVTY'])).tolist()
	F_PRCITSHP = np.array(pd.get_dummies(df['F_PRCITSHP'])).tolist()
	res = []
	for i in range(len(AAGE)):
		res.append(F_ACLSWKR[i]+F_EDUCATION[i]+F_STATUSMARIT[i]+F_AMJIND[i]+F_AMJOCC[i]+F_RACE[i]+F_ORIGIN[i]+F_ASEX[i]+F_AWKSTAT[i]+F_FILESTATUS[i]+F_HHDFMX[i]+F_HHDREL[i]+F_CONBIRTHFATH[i]+F_CONBIRTHMOTH[i]+F_PENATVTY[i]+F_PRCITSHP[i]+[AAGE[i],WKSWORKYEAR[i],CHILDS[i]])
	return res

def main():
    if os.path.isfile('census.csv'):
        csv = pd.read_csv('census.csv')
        print("---Rows of csv: {}---".format(len(csv)))
    else:
        print("---census.csv not found----")
        os._exit(1)
    #treat it
    X = transformGetData(csv)
    del csv
    gc.collect()
    X = pd.DataFrame(X)
    for i in range(10):
        print("---Iteration number: %s---"%i)
        train, test = train_test_split(X, test_size=0.33)
        train.to_csv('train_{}.csv'.format(i), index=False)
        test.to_csv('test_{}.csv'.format(i), index=False)

main()