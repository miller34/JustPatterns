#! /usr/bin/env python

import sys
import os
import subprocess

input = open(sys.argv[1],'r')

allLines = input.readlines()
input.close()
numCrossValidation = 10

sizeTest = len(allLines)/numCrossValidation
for x in range(numCrossValidation):
	#x=7
	start = x*sizeTest
	test = allLines[start:start+sizeTest]
	train = allLines[start + sizeTest:len(allLines)] + allLines[0:start]
	print x	
	tempTest = open("tempTest2",'w')
	for y in test:
		tempTest.write(y)
	tempTest.close()
	tempTrain = open("tempTrain2",'w')
	for y in train:
		tempTrain.write(y)
	tempTrain.close()
	#out = "tempOut"
	#command = [ 'python', "../revisedFuzzy.py", "tempTrain", "tempTest", out]
	#command = [ 'python', "../fuzzyPartition.py", "tempTrain", "tempTest", out]
	##command = [ 'python', "../testSecondOrder.py", "tempTrain", "tempTest", out]
	######command = [ 'python', "../zipTest.py", "tempTrain2", "tempTest2","tempOut"]
	#command = [ 'python', "newAlgorithmManyIterations.py", "tempTrain2", "tempTest2","tempOut"]
	command = [ 'python', "combinationAlgorithm.py", "tempTrain2", "tempTest2","tempOut"]
	##command = [ 'python', "newAlgorithm.py", "tempTrain2", "tempTest2","tempOut"]
	#command = [ 'python', "../zipTest.py", "tempTrain", "tempTest", out]
	#prog=  subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	prog=  subprocess.Popen(command)
	prog.communicate()




