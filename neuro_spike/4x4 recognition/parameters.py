### Parameters of the given model


# initial learning par
num_in_neu = 16  # 4x4 size image
epochs = 1

num_out_neu = 2


#  neuron par
R = 10
C = 0.05

refrac_time = 0.11
init_refrac = 0
noise = 0

thresh = 0.15

# encoding
firing_delimeter =300

# STDP
A_plus = 0.2
A_minus = 0.3

tau_minus = 10
tau_plus = 3

range_stdp = 40