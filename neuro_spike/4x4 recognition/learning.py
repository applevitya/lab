from neuron import LIF_simple
from parameters import num_in_neu,num_out_neu
from encoding import Poisson_generator, read_img
import numpy as np



############ Random Weights #####################

W = np.random.uniform(0,0.5,size = [17,2])

#################################
# time series

T = 200 #ms
dt = 0.1
time = np.arange(0,T+dt,dt)

x = read_img()

### input/output spikes #########################
in_spikes = np.empty(shape=(num_in_neu,len(time)))
for i in range(num_in_neu):
  in_spikes[i]=Poisson_generator(T,dt,10+x[i],1)

out_spikes = np.zeros(shape=(num_out_neu,len(time)))

# creating the output layer of neurons
out_neurons = []
for i in range(num_out_neu):
	a = LIF_simple()
	out_neurons.append(a)

