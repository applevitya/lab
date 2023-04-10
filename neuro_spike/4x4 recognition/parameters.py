### Parameters of the given model


# initial learning par
num_in_neu = 16  # 4x4 size image
epochs = 1

num_out_neu =6


#  neuron par
R = 100
C = 1.

refrac_time = 0.05
init_refrac = 0
noise = 0


thresh = 0.01

# encoding
firing_delimeter =100


# STDP
A_plus = 0.02
A_minus = 0.9

tau_plus = 6
tau_minus = 15


range_stdp = 5