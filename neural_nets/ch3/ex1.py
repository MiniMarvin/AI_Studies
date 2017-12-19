##Author:Caio M. Gomes
##Date: 21/01/2017
##Location: Abreu e Lima - Pernambuco
##Description: Exercise 1 of chapter 3 from A Systematic Introduction to Neural Networks
#AObjective: Define the number of linear separable functions for a certain number of inputs.


from math import *
import numpy as np
import random
import sys

class Neuron(object):
	"""Clasical Neuron Model with threshold and binary output"""

	##generate the neuron weights and BIAS.
	def __init__(self, wmap, BIAS):
		super(Neuron, self).__init__()
		self.mapval = wmap
		self.th = BIAS
		#print(wmap)
		pass

	##Check if the weighted sum computes more than 1
	def active(self, mi):
		ms = 0
		
		for x in range(0, len(self.mapval)):
			ms += self.mapval[x]*mi[x]
			#print("-> "+str(mi[x]))
			pass
		ms += self.th
		#print(self.th)

		if ms >= 0.0:
		#print(ms, -self.th)
		#if ms >= -self.th:
			return 1
		else:
			return 0


def compute(n):
	random.seed()
	weights = np.zeros(n)
	#setup neuron weights
	for i in range(0, n):
		w = int((2*random.random()-1)*100)
		#weights[i] = 2*random.random()-1
		weights[i] = w/100.0

	#if(weights[0] == -weights[1]):
	#	print("EQUAL!!")

	#BIAS = -random.random()
	BIAS = 2*random.random()-1
	if(BIAS >= -0.01 and BIAS <= 0.01):
		BIAS = 0


	neuron = Neuron(weights,  BIAS)
	#if(BIAS == 0): 
	#	print("ZERO!!")

	msum = 0 
	#make the input excitation -> 2 binary digits per cycle
	for i in range(0, 2**n):
		buff = i
		inputarr = [int(x) for x in bin(buff)[2:]]

		if(len(inputarr) < n):
			#we invert the array to make it become wrong 
			#and add the necessary part them we invert it again
			#to make it become correct
			inputarr = list(reversed(inputarr))
			buffarr = np.zeros(n - len(inputarr))
			inputarr.extend(buffarr)
			inputarr = list(reversed(inputarr))

		msum += neuron.active(inputarr)*(2**i)

	if(msum == int('0110',2) or msum == int('1001',2)):
		print("XOR!")

	return msum

def comp(n):

	neuron = Neuron([-0.5,0.5], 0)
	pos = 0

	for i in range(0, 4):
		inputarr = [int(x) for x in bin(i)[2:]]
		if(len(inputarr) < 2):
			inputarr = list(reversed(inputarr))
			buffarr = np.zeros(2 - len(inputarr))
			inputarr.extend(buffarr)
			inputarr = list(reversed(inputarr))

		
		print(neuron.active(inputarr))

	return pos

def __main__():
	n = int(sys.argv[1])
	print(n)
	arr = np.zeros(2**2**n)

	print(arr)

	for i in range(0, 1000000):
		val = compute(n)

		try:
			arr[val] += 1
			pass
		except Exception, e:
			print("summed: "+str(val))
			raise

	print(arr)

	lsf = 0
	for i in arr:
		if i != 0:
			lsf += 1

	print("With "+str(n)+" variables we have "+str(lsf)+" linearly separable functions")

__main__()