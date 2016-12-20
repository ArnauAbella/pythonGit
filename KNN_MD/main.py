#Libraries imports
import time
import os
import gc
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import sklearn.neighbors as nb
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


#myImports

# headers = ["AAGE","F_ACLSWKR","F_EDUCATION","F_STATUSMARIT","F_AMJIND","F_AMJOCC","F_RACE","F_ORIGIN","F_ASEX","F_AWKSTAT","F_FILESTATUS","F_HHDFMX","F_HHDREL","MARSUPWT","CHILDS","F_CONBIRTHFATH","F_CONBIRTHMOTH","F_PENATVTY","F_PRCITSHP","WKSWORKYEAR","TARGET"]

#Code
def normalizeAttribute(attr1):
	a = np.array(attr1)
	#PROBLEMA NO PODEM LLEGIR STRING
	a_norm = normalize(a.astype(np.float), norm='l2')
	#al fer np.array et genera una matriu.. encara que tingui dimensio 1
	return (a_norm.tolist())[0]

def loadData(): #esta funcion debe devolver los datos en un np.array()
	csv = pd.read_csv('train.csv')
	# turn categoricals to new column with 0 or 1 (except TARGET)
	train = pd.get_dummies(csv, columns=['F_ACLSWKR', 'F_EDUCATION', 'F_STATUSMARIT', 'F_AMJIND', 'F_AMJOCC', 'F_RACE',
										 'F_ORIGIN', 'F_ASEX', 'F_AWKSTAT', 'F_FILESTATUS', 'F_HHDFMX', 'F_HHDREL',
										 'F_CONBIRTHFATH', 'F_CONBIRTHMOTH', 'F_PENATVTY', 'F_PRCITSHP'])
	target = train['TARGET']
	train_wo_target = train.drop('TARGET', 1)
	test_csv = pd.read_csv('test.csv')
	test_wo_label = test_csv.drop('TARGET', 1)
	test = pd.get_dummies(test_wo_label)
	missing_columns = [item for item in list(train_wo_target.keys()) if item not in list(test.keys())]
	print("test dataset was missing {}; adding them with values 0".format(missing_columns))
	for mc in missing_columns:
		test[mc] = pd.Series(0, index=test.index)
	return (train_wo_target,target,test,test_csv['TARGET'])


def computeBestK(knn, dTrain, labTrain, dTest, labTest):
    #Code to calculate the best k
    scoreK = []
    for neighbor in range(1,30,2):
        knn = nb.KNeighborsClassifier(n_neighbors=neighbor,weights='uniform',algorithm='auto',leaf_size=30, metric='minkowski',metric_params=None,p=2, n_jobs=8)
        knn.fit(dTrain, labTrain)
        scoreK.append(knn.score(dTest, labTest))
    plt.plot(range(1,30,2),scoreK,'b')
    plt.show()

def datasetInMemory(): #Load census.csv in RAM
	if os.path.isfile('census.csv'):
		df = pd.read_csv('census.csv')
	else:
		print("---census.csv not found----")
		os._exit(1)
	return df

def doKNNandFit(X,y,mode):
	print("---Create k-NN----")
	knn = nb.KNeighborsClassifier(n_neighbors=23, weights='uniform', algorithm='auto', leaf_size=30,
								  metric='minkowski',
								  metric_params=None, p=2, n_jobs=4)
	print("---Train k-NN----")
	knn.fit(X, y)
	''' MEMORY ERROR...
	if mode == 'CV':
		print("---Read from local k-NN----")
		if os.path.isfile('KNN_Classifier'):
			with open('KNN_Classifier', 'rb') as file:
				knn = pickle.load(file) #Import KNN classifier
		else:
			print("---Create k-NN----")
			knn = nb.KNeighborsClassifier(n_neighbors=23, weights='uniform', algorithm='auto', leaf_size=30, metric='minkowski',
										  metric_params=None, p=2, n_jobs=4)
			print("---Train k-NN----")
			knn.fit(X, y)
			print('---Storing KNN_Classifier---')
			pickle.dump(knn, open("KNN_Classifier", "wb"))
	else:
		print("---Create k-NN----")
		knn = nb.KNeighborsClassifier(n_neighbors=23, weights='uniform', algorithm='auto', leaf_size=30,
									  metric='minkowski',
									  metric_params=None, p=2, n_jobs=4)
		print("---Train k-NN----")
		knn.fit(X, y)
	'''
	return knn

def doKfoldCrossValidation():
	print("---k-Fold Cross Validation----")
	print("---Doing preprocessing----")
	df = datasetInMemory()
	# turn categoricals to new column with 0 or 1 (except TARGET)
	train = pd.get_dummies(df, columns=['F_ACLSWKR', 'F_EDUCATION', 'F_STATUSMARIT', 'F_AMJIND', 'F_AMJOCC', 'F_RACE',
										 'F_ORIGIN', 'F_ASEX', 'F_AWKSTAT', 'F_FILESTATUS', 'F_HHDFMX', 'F_HHDREL',
										 'F_CONBIRTHFATH', 'F_CONBIRTHMOTH', 'F_PENATVTY', 'F_PRCITSHP'])
	X = train.drop('TARGET', 1)
	y = train['TARGET']
	knn = doKNNandFit(X, y, 'KCV')
	print("---Start cross_val_score----")
	scores = cross_val_score(knn, X=X, y=y, cv=5, scoring='f1_macro')
	print("Scores: {}".format(scores))
	print("Median of scores: {}".format(np.mean(scores)))

def doCrossValidation():
	print("---Cross Validation----")
	(train_X, train_y, test_X, test_y) = loadData()
	knn = doKNNandFit(train_X,train_y,'CV')
	print('---Storing KNN_Classifier---')
	predicted_label = knn.predict(test_X)
	print(classification_report(test_y,predicted_label))

#MAIN
if __name__ == '__main__':
	start = time.time()
	# Chose one
	doCrossValidation()
	#doKfoldCrossValidation()
	end = time.time()
	print("Global exec time: {}".format(end-start))