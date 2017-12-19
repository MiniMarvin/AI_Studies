## Author:Caio M. Gomes
## Date: 28/01/2017
## Location: Abreu e Lima - Pernambuco
## Description: Exercise 5 of chapter 3 from A Systematic Introduction to Neural Networks
## Objective: Make an edge detection program, capable of compute the edges in a real image
# and them return an image just with the edges in the binary image
## Extra: Make the neurons compute parallel.


from math import *
import numpy as np
import random
import sys
import cv2

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
			return 1
		else:
			return 0


def __main__():
	original = cv2.imread(sys.argv[1], 0)
	h = original.shape[0]-2
	w = original.shape[1]-2
	edges = original.copy()
	#percep = [[Neuron([-1,-1,-1,-1, 8,-1,-1,-1,-1], -0.5) for i in range(0,w)] for j in range(0,h)]
	percep = Neuron([-1,-1,-1,-1, 8,-1,-1,-1,-1], -0.5)
	original = cv2.inRange(original, 200, 255)

	for i in range(0, h-1):
		for j in range(0, w-1):
			arr = original[i:i+3, j:j+3].ravel()
			#arr = []
			#for k in range(0, 3):
			#	for l in range(0,3):
			#		arr.append(original[i+l][j+k])

			#edges[i+1][j+1] = 255*percep[i-1][j-1].active( arr )
			try:
				#buff = 255*percep[i-1][j-1].active( arr )
				buff = 255*percep.active( arr )
				edges[i+1][j+1] = buff
				pass
			except Exception, e:
				print("error at : "+str(i+1)+","+str(j+1))
				raise

	cv2.imshow("original", original)
	cv2.imshow("edges", edges)
	cv2.waitKey(1)
	cv2.destroyAllWindows()
			

__main__()