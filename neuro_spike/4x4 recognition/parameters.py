### Parameters of the given model


# initial learning par
num_in_neu = 784  # 4x4 size image
epochs = 1

num_out_neu =30


#  neuron par
R = 100
C = 1.

refrac_time = 0.03
init_refrac = 0
noise = 0


thresh = 0.01

# encoding
firing_delimeter =20


# STDP
A_plus = 0.01
A_minus = 0.95

tau_plus = 6
tau_minus = 15


range_stdp = 6