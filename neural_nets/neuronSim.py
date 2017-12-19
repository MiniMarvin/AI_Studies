##sources:
##http://www.mrc.uidaho.edu/~rwells/techdocs/Biological%20Signal%20Processing/Chapter%2003%20The%20Hodgkin-Huxley%20Model.pdf
##http://www.math.mcgill.ca/gantumur/docs/reps/RyanSicilianoHH.pdf

#!/usr/bin

import random
import math

##new random seed
random.seed()

##Potentials
Vo = -random.randrange(0, 100, 0.01)
V = 0

##Constants
h = random.random()
m = 0
n = 0

##Diff Values
dn = 0
dm = 0
dh = 0
dv = 0

while():

	##Secondary
	an = (10-V)/(100.0*math.exp((10-V)/10-1))
	am = (25-V)/(10.0*math.exp((25-V)/10-1))
	ah = 0.07*math.exp(-V/20.0)
	bn = 0.125*math.exp(-V/80.0)
	bm = 4*math.exp(-V/18.0)
	bh = 1/(exp((30-V)/10 + 1))

	##Condutances
	gk = gk_max*n**4
	gNa = gNa_max*m**3*h

	##DiffEquations
	dn = an*(1-n)- bn
	dm = am*(1-m)- bm
	dh = ah*(1-h)- bh

	dV = gNa*(V - ENa) + gk*(V - Ek) + gvaz*(V - Evaz) + Iinj

	buff_n = n
	buff_m = m
	buff_h = h
	buff_V = V

	n = n+dn*dt
	m = m+dm*dt
	h = h+dh*dt
	V = V+dV*dt