from parameters import A_plus,A_minus, tau_plus, tau_minus
import numpy as np



def rl(t):
    if t >= 0:
        return -A_plus * np.exp(-float(t) / tau_plus)
    if t < 0:
        return A_minus * np.exp(float(t) / tau_minus)


# STDP weight update rule
def update(w, t):
    del_w = rl(t)
    if del_w < 0:
        if w+del_w>0:
            if w+del_w>1:
                return 1
            else: return w + del_w
        else:
            return 0.2

    elif del_w > 0:
        if w + del_w > 0:
            if w + del_w > 1:
                return 1
            else:
                return w + del_w
        else:
            return 0.2




