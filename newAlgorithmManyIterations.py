#! /usr/bin/env python
import sys
#from multiprocessing import Process, current_process, freeze_support, Pool
#import argparse
import numpy as np

testData = open(sys.argv[2],'r')
##output = open(sys.argv[3],'w')
#threads = 16

def predict(info, allClasses, allInstances,  allOutDomains, allMajorityClasses):
	correct = False
	noGuess = False
	features = info[0:-1]
	outClass = info[-1]
	bestScore = 0
	prediction = ""
	bestScores =[]
	for x in xrange(len(allInstances)):
		default = allOutDomains[x][allMajorityClasses[x].index(max(allMajorityClasses[x]))]
		prediction = default
		scores =[]
		for out in xrange(len(allInstances[x])):
			total = 0.0
			for feat in xrange(len(features)):
				char = features[feat]
				if char in allClasses[x][out][feat]:
					pos = allClasses[x][out][feat][char]
					total +=allInstances[x][out][feat][pos]
					continue
			scores.append(total)
		for i in xrange(len(scores)):
			scores[i] = scores[i] / allMajorityClasses[x][i]
	
		if max(scores)>bestScore:
			prediction = allOutDomains[x][scores.index(max(scores))]
			bestScore = max(scores)
			noGuess = False
			#if (max(scores)/ float(sum(scores)))/(1.0/float(len(scores)))<1.2:
			oScores = sorted(scores)
			bestScores = scores[:]
			if oScores[-1]-oScores[-2]<1.5:
				noGuess = True
			if not noGuess:	
				return prediction==outClass,noGuess
	if prediction==outClass:
		correct = True
	#return correct,noGuess
	return correct,noGuess



def makeClassesAndInstances(inputFile, allClasses, allInstances,allOutDomains,allMajorityClasses):
	outDomains = []
	majorityClass = []
	input = open(inputFile,'r')
	instances = []
	classes = [] ##List of dictionary of classes pointing to position in instances list
	numRemaining = 0
	for line in input:
		info = line.strip().upper().split(',')
		if len(allInstances)>0:
			isCorrect,noGuess = predict(info,allClasses,allInstances,allOutDomains,allMajorityClasses)
			if isCorrect and not noGuess:
				continue
		numRemaining +=1
		features = info[0:-1]
		outClass = info[-1]
		if not outClass in outDomains:
			outDomains.append(outClass)
			outPos = outDomains.index(outClass)
			instances.append([[0] for i in xrange(len(features))])
			classes.append([dict() for i in xrange(len(features))])
			for i in xrange(len(features)):
				char = features[i]
				classes[outPos][i][char] =0
			majorityClass.append(0)
		outPos = outDomains.index(outClass)
		majorityClass[outPos] +=1
		for i in xrange(len(features)):
			char = info[i]
			if not char in classes[outPos][i]:
				classes[outPos][i][char] = len(classes[outPos][i])
				instances[outPos][i].append(0)
			pos = classes[outPos][i][char]
			instances[outPos][i][pos] +=1
	input.close()
	for out in xrange(len(instances)):
		for feat in xrange(len(instances[out])):
			if len(instances[out][feat])>1:
				#median = np.median(instances[out][feat])
				mean = sum(instances[out][feat])/len(instances[out][feat])
				for i in xrange(len(instances[out][feat])):
					newVal = 0
					potential = instances[out][feat][i] - mean
					if potential >0:
						newVal = potential
					else:
						newVal = 2*potential
					#instances[out][feat][i] = instances[out][feat][i] -median
					instances[out][feat][i] = newVal

	return classes,instances,outDomains,majorityClass,numRemaining

oldNumRemain = sys.maxint
allClasses = []
allInstances = []
allOutDomains = []
allMajorityClasses = []
while oldNumRemain:
	c,i,d,m,nR = makeClassesAndInstances(sys.argv[1],allClasses,allInstances,allOutDomains,allMajorityClasses)
	allClasses.append(c)
	allInstances.append(i)
	allOutDomains.append(d)
	allMajorityClasses.append(m)
	if nR>=oldNumRemain:
		allClasses = allClasses[0:-1]
		allInstances = allInstances[0:-1]
		allOutDomains = allOutDomains[0:-1]
		allMajorityClasses = allMajorityClasses[0:-1]
		break
	oldNumRemain = nR


print "here"
#print allInstances

correct = 0
wrong = 0
print len(allOutDomains)
for line in testData:
	info = line.strip().upper().split(',')
	isCorrect,noGuess = predict(info,allClasses,allInstances,allOutDomains,allMajorityClasses)
	if isCorrect:
		correct+=1
		continue
	wrong +=1



print "Correct",correct,"Wrong",wrong,round((100*float(correct))/(correct+wrong)),"%"
testData.close()






