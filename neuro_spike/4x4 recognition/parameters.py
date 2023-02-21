### Parameters of the given model


# initial learning par
num_in_neu = 16  # 4x4 size image
epochs = 1

num_out_neu = 2


#  neuron par
R = 0.10
C = 1

refrac_time = 0.12
init_refrac = 0
noise = 0

thresh = 0.001

# encoding
firing_delimeter =100

# STDP
A_plus = 2
A_minus = 1

tau_minus = 2
tau_plus = 2

range_stdp = 50