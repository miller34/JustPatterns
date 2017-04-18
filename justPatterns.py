#! /usr/bin/env python
import sys
#from multiprocessing import Process, current_process, freeze_support, Pool
import argparse
import numpy as np

def parseArgs():
	parser = argparse.ArgumentParser(description='Find Orthologs in MultiSpecies FASTA file.')
	parser.add_argument("-i",help="Input CSV File",action="store", dest="input",required=True)
	parser.add_argument("-c",help="Cross Validation",action="store",type=int, dest="cross",default=10,required=False)
	parser.add_argument("-o",help="Output Pattern File",action="store",dest="output", required=False)
	#parser.add_argument("-t",help="Number of Cores",action="store",dest="threads",default=1,type=int, required=False)
	parser.add_argument("-p",help="Threshold of Excellent Pattern",action="store",dest="patternThreshold",default=0.99,type=float, required=False)
	parser.add_argument("-s",help="Minimum Difference in Output Scores",action="store",dest="scoreSep",default=0.0,type=float, required=False) ##how many layers of hidden nodes
	args = parser.parse_args()
	return args

def predict(info,  allInstances,  allOutDomains, allMajorityClasses,patternThresh,scoreSep):
	noGuess = True
	features = info[0:-1]
	outClass = info[-1]
	bestScore = 0
	prediction = ""
	bestScores =[]
	for x in xrange(len(allInstances)):
		scores=[0.0]*len(allMajorityClasses[x])
		default = allOutDomains[x][allMajorityClasses[x].index(max(allMajorityClasses[x]))]
		prediction = default
		outListReason = []
		for out in xrange(len(allMajorityClasses[x])):
			outListReason.append([])
			total = 0.0
			for i in xrange(len(features)):
				char = features[i]
				if char in allInstances[x][i]:
					if out<len(allInstances[x][i][char]):
						total += allInstances[x][i][char][out]/(sum(allInstances[x][i][char])+0.00000001)
						outListReason[out].append(allInstances[x][i][char][out]/(sum(allInstances[x][i][char])+0.00000001))
			scores[out] += total
		if max(scores)>bestScore:
			bestScore = max(scores)
			prediction = allOutDomains[x][scores.index(bestScore)]
			bestA=0
			for i in xrange(len(outListReason)):
				maxed = max(outListReason[i])
				if maxed >patternThresh and maxed>bestA:
					bestA = maxed
					prediction= allOutDomains[x][i]
			noGuess = True
			oScores = sorted(scores)
			bestScores = scores[:]
			if len(oScores)==1 or oScores[-1]-oScores[-2]>scoreSep: ##0.2 for Breast data
				noGuess = False
			if not noGuess:	
				return prediction==outClass,noGuess
	return prediction==outClass,noGuess

def makeClassesAndInstances(input, allInstances,allOutDomains,allMajorityClasses,patternThresh,scoreSep):
	outDomains = []
	majorityClass = []
	instances = dict()
	numRemaining = 0
	for line in input:
		info = line.strip().upper().split(',')
		if len(allInstances)>0:
			isCorrect,noGuess = predict(info,allInstances,allOutDomains,allMajorityClasses,patternThresh,scoreSep)
			if isCorrect and not noGuess:
				continue
		numRemaining +=1
		features = info[0:-1]
		outClass = info[-1]
		if not outClass in outDomains:
			outDomains.append(outClass)
			majorityClass.append(0)
		outPos = outDomains.index(outClass)
		majorityClass[outPos] +=1
		for i in xrange(len(features)):
			char = info[i]
			if not i in instances:
				instances[i] = dict()
			if not char in instances[i]:
				instances[i][char]=[1]*len(outDomains) #1 used here for normalization. This pattern alg.
			if outPos>=len(instances[i][char]):
				while len(majorityClass)>len(instances[i][char]):
					instances[i][char].append(1) #1 used here for normalization. This pattern alg.
			instances[i][char][outPos] +=1
	for i in instances:
		for char in instances[i]:
			for x in xrange(len(majorityClass)):
				z = float(majorityClass[x] +len(instances[i][char]))
				if x<len(instances[i][char]):
					instances[i][char][x] = instances[i][char][x] / z
				else:
					instances[i][char].append(1.0/z)
		for char in instances[i]:
			sumTotal = float(sum(instances[i][char]) + len(majorityClass)) #+ len(instances[i][char]) used for normalization. Think pattern tree alg.
			for x in xrange(len(majorityClass)):
				if x < len(instances[i][char]):
					newVal = instances[i][char][x] / sumTotal
					instances[i][char][x] = newVal
				else:
					instances[i][char].append(1.0/sumTotal)
	return instances,outDomains,majorityClass,numRemaining

if __name__ =='__main__':
	args = parseArgs()
	
	allLines = open(args.input,'r').readlines()
	
	sizeTest = len(allLines)/args.cross
	output=""
	if args.output:
		output = open(args.output,'w')
	correct = 0
	wrong = 0
	#args.patternThreshold = float(p)/100
	for x in range(args.cross):
		start = x*sizeTest
		testData = allLines[start:start+sizeTest]
		train = allLines[start + sizeTest:len(allLines)] + allLines[0:start]
	
		oldNumRemain = sys.maxint
		allInstances = []
		allOutDomains = []
		allMajorityClasses = []
		while oldNumRemain:
			i,d,m,nR = makeClassesAndInstances(train,allInstances,allOutDomains,allMajorityClasses,args.patternThreshold,args.scoreSep)
			if nR>=oldNumRemain:
				break
			allInstances.append(i)
			allOutDomains.append(d)
			allMajorityClasses.append(m)
			oldNumRemain = nR
		for line in testData:
			info = line.strip().upper().split(',')
			isCorrect,noGuess = predict(info,allInstances,allOutDomains,allMajorityClasses,args.patternThreshold,args.scoreSep)
			if isCorrect:
				correct+=1
				continue
			wrong +=1
	print "Correct",correct,"Wrong",wrong,round((100*float(correct))/float(correct+wrong),2),"%"
	#print correct,',',wrong,',',round((100*float(correct))/float(correct+wrong),2),"%"
	if args.output:
		output.close()
		

