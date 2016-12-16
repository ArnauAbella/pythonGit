#Libraries imports
import csv
#myImports

#Code

#getting data
with open('exemple.csv','rb') as csvfile:
	lines = csv.reader(csvfile, delimiter=",")
	empties = {}
	nRowsMissing = 0
	nRows = 0;
	for row in lines:
		has_missing = False
		nRows += 1
		for idx, column in enumerate(row):
			if not column:
				#Column of the row is empty
				has_missing = True
				if empties.get(idx):
					empties[idx] = empties[idx] + 1
				else:
					empties[idx] = 1
			'''
			elif column is '': 
				#Column of the row is empty
				has_missing = True
				if empties.get(idx):
					empties[idx] = empties[idx] + 1
				else:
					empties[idx] = 1 
			'''    
		if has_missing:
			nRowsMissing += 1
	print 
	print "number of rows : {}".format(nRows)
	print "rows with missing data: {}".format(nRowsMissing)
	print "Missing rows {}%".format(round((float(nRowsMissing)/nRows)*100,2))
	print empties
