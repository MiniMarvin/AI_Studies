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
from functools import partial
from multiprocessing import Pool

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

class MyImg(object):
	##generate the neuron weights and BIAS.
	def __init__(self, wmap, BIAS):
		super(MyImg, self).__init__()
		self.img = img
		#print(wmap)
		pass

	def update(val, x, y):
		self.img[x][y] = val
		pass


def __main__():
	#global members
	global original
	global edges
	original = cv2.imread(sys.argv[1], 0)
	edges = original.copy()
	#percep = Neuron([-1,-1,-1,-1, 8,-1,-1,-1,-1], -0.5)

	h = original.shape[0]-2
	w = original.shape[1]-2

	original = cv2.inRange(original, 200, 255)

	#p = Pool(8)
	#print( p.map(calcEdges, np.arange(w-2).all, np.arange(h-2).all ) )
	#print( p.map(calcEdges, [1], [1] ) )
	for i in range(h-2):
		p = Pool(8)
		func = partial(calcEdges, i)
		p.map(func, np.arange(w-2))
		p.close()
		p.join()
		print(i)

	cv2.imshow("original", original)
	cv2.imshow("edges", edges)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def calcEdges(i, j):
#def calcEdges(myarr):
#	i = myarr[0]
#	j = myarr[1]

	arr = original[i:i+3, j:j+3].ravel()
	percep = Neuron([-1,-1,-1,-1, 8,-1,-1,-1,-1], -0.5)
	global edges
	

	try:
		global edges
		buff = 255*percep.active( arr )
		edges[i+1][j+1] = buff
		pass
	#except Exception, e:
	except Exception:
		print("error at : "+str(i+1)+","+str(j+1))
		raise

	return buff

			
__main__()