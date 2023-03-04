### Parameters of the given model


# initial learning par
num_in_neu = 16  # 4x4 size image
epochs = 1

num_out_neu =4


#  neuron par
R = 100
C = 1

refrac_time = 2
init_refrac = 0
noise = 0

thresh = 0.1

# encoding
firing_delimeter = 500
# STDP
A_plus = 0.9
A_minus = 1.6

tau_plus = 0.5
tau_minus = 3

range_stdp = 20