#! /usr/bin/env python
import sys
#from multiprocessing import Process, current_process, freeze_support, Pool
#import argparse
import numpy as np

input = open(sys.argv[1],'r')
testData = open(sys.argv[2],'r')
##output = open(sys.argv[3],'w')
threads = 16

outDomains = []
majorityClass = []
instances = []
classes = [] ##List of dictionary of classes pointing to position in instances list
for line in input:
	info = line.strip().upper().split(',')
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

print "here"

correct = 0
wrong = 0
default = outDomains[majorityClass.index(max(majorityClass))]
for line in testData:
	info = line.strip().upper().split(',')
	features = info[0:-1]
	outClass = info[-1]
	scores =[]
	for out in xrange(len(instances)):
		total = 0.0
		for feat in xrange(len(features)):
			char = features[feat]
			if char in classes[out][feat]:
				pos = classes[out][feat][char]
				total +=instances[out][feat][pos]
				continue
		scores.append(total)
	for i in xrange(len(scores)):
		scores[i] = scores[i] / majorityClass[i]

	prediction = default
	if max(scores)>0:
		prediction = outDomains[scores.index(max(scores))]
	if prediction==outClass:
		#print "correct",scores
		correct +=1
		continue
	wrong +=1
	#print "wrong",scores

print "Correct",correct,"Wrong",wrong,round((100*float(correct))/(correct+wrong)),"%"
testData.close()






