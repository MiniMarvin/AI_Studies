##sources:
##http://www.mrc.uidaho.edu/~rwells/techdocs/Biological%20Signal%20Processing/Chapter%2003%20The%20Hodgkin-Huxley%20Model.pdf
##http://www.math.mcgill.ca/gantumur/docs/reps/RyanSicilianoHH.pdf

# file HHSquid.m Hodgkin-Huxley model using Euler's method
# This script allows up to two current pulses to be injected
# into the membrane to excite a response. The widths can
# be independently set, but the pulses cannot overlap. If pulse
# 2 is turned on before pulse 1 ends it replaces pulse 1.

# maximal conductances (mS/cm^2); 1=K, 2=Na, 3=lk;
# membrane capacitance is 1 uF/cm^2
import numpy as np
import * from math

#condutances based on original model
g = np.zeros(3)
g[1]=36
g[2]=120
g[3]=0.3

# battery voltage (mV) relative to resting potential; 1=K, 2=Na; 3=lk
E[1]=-12
E[2]=115
E[3]=10.613

# variable initialization I_ext is in microamps/cm^2
I_ext=0
V=-10
x=np.zeros(3)
x[3]=1
t_rec=0
t_final=50 # t_final sets the time span of the simulation

# applied pulses parameters; T1=on time for pulse 1, T2=on time for pulse 2
# Tw1 is the width of pulse 1, Tw2 is the width of pulse 2. I_on1 is the
# amplitude of pulse 1 in microamps/square cm, I_on2 is the amplitude of
# pulse 2. All times are in milliseconds. If T2>t_final the
# second pulse is not applied.
I_on1=2.5
I_on2=2.5
T1=10
T2=70
Tw1=5
Tw2=5

# time step for integration in milliseconds
dt=0.01

# integration by Euler's method
# computations for t < 0 establish initial conditions at t = 0.
for t in range(-30, t_final, dt):
	if t==T1: 
		I_ext=I_on1
		pass #turns on external current at
	t=T1
	if t==T1+Tw1:
		I_ext=0
		pass #turns off external current
	if t==T2:
		I_ext=I_on2
		pass #turns on second pulse
	if t==T2+Tw2:
		I_ext=0
		pass #turns off second pulse

	#alpha parameters in H-H model
	alpha = np.zeros(3)
	alpha[1]=(10-V)/(100*(exp((10-V)/10)-1))
	alpha[2]=(25-V)/(10*(exp((25-V)/10)-1))
	alpha[3]=0.07*exp(-V/20)

	#beta parameters in H-H model
	beta = np.zeros(3)
	beta[1]=0.125*exp(-V/80)
	beta[2]=4*exp(-V/18)
	beta[3]=1/(exp((30-V)/10)+1)

	#time constants (msec) and asymptotic values
	tau=1./(alpha+beta)
	x_0=alpha*tau

	#Euler integration
	x=(1-dt/tau)*x+dt/tau*x_0

	#conductance calculations
	gnmh = np.zeros(3)
	gnmh[1]=g[1]*x[1]^4
	gnmh[2]=g[2]*x[2]^3*x[3]
	gnmh[3]=g[3]

	#membrane voltage update
	I=gnmh*(V-E)
	V=V+dt*(I_ext-sum(I))

	#plotting records
	if t >= 0:
		t_rec=t_rec+1
		x_plot(t_rec)=t
		y_plot(t_rec)=V
		G(t_rec,1)=gnmh(1) # GK
		G(t_rec,2)=gnmh(2) # GNa
		end
	pass

##plot the data

#plot(x_plot,y_plot); xlabel('Time (ms)'); ylabel('Relative Membrane Voltage (mV)');
#figure;
#plot(x_plot,G); xlabel('Time (ms)'); ylabel('Conductance(mS/cm^2)');
