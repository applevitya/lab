from neuron import LIF_simple
from parameters import num_in_neu,num_out_neu
from encoding import Poisson_generator, read_img
from STDP import update
import numpy as np



############ Random Weights #####################

W = np.random.uniform(0,0.5,size = [17,2])

#################################
# time series

T = 200 #ms
dt = 0.1
time = np.arange(0,T+dt,dt)


### input/output spikes #########################
in_spikes = np.empty(shape=(num_in_neu,len(time)))
out_spikes = np.zeros(shape=(num_out_neu,len(time)))

# creating the output layer of neurons
out_neurons = []
for i in range(num_out_neu):
	a = LIF_simple()
	out_neurons.append(a)


##### learning ########

for i in range(2,3):
	img = read_img(str(i)+".png")


	I = np.zeros(shape=(num_in_neu,))
	for t in range(len(time)):

		for j,neu in enumerate(out_neurons):
			for i in range(num_in_neu):
				I[j] = 0
				I[j] += np.dot(W[i][j],in_spikes[i][t])


				if t>=neu.initRefrac:

					v = neu.vprev + (-neu.vprev + I[j] * neu.R) / neu.tau_m * dt  # LIF
					# v= neu.vprev + np.dot(W[i][j],in_spikes[i][t])
					if (v > neu.v_base):
						# v -= 0.01
						if v < neu.v_base:
							v = neu.v_base

					if v >= neu.v_thresh:
						neu.num += 1
						out_spikes[j][t] = 1
						v += neu.v_spike
						neu.initRefrac = t + neu.refracTime
						v = neu.v_base
						neu.v_thresh += 0.0001
						break

					neu.vprev = v



