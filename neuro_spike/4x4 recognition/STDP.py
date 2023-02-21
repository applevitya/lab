from parameters import A_plus,A_minus, tau_plus, tau_minus


def rl(t):
    if t >= 0:
        return -A_plus * np.exp(-float(t) / tau_plus)
    if t < 0:
        return A_minus * np.exp(float(t) / tau_minus)


# STDP weight update rule
def update(w, t):
    del_w = rl(t)
    if del_w < 0:
        return w + del_w
    elif del_w > 0:
        return w + del_w