import numpy as np
from parameters import firing_delimeter
import cv2

def Poisson_generator(time,dt,rate, n, myseed=False):
  """
  Generates poisson trains

  Args:
    rate            : noise amplitute [Hz]
    n               : number of Poisson trains
    myseed          : random seed. int or boolean

  Returns:
    pre_spike_train : spike train matrix, ith row represents whether
                      there is a spike in ith spike train over time
                      (1 if spike, 0 otherwise)
  """

  # Retrieve simulation parameters
  range_t = np.arange(0, time+dt, dt)  # Vector of discretized time points [ms]
  Lt = range_t.size

  # set random seed
  if myseed:
      np.random.seed(seed=myseed)
  else:
      np.random.seed()

  # generate uniformly distributed random variables
  u_rand = np.random.rand(n, Lt)

  # generate Poisson train
  poisson_train = 1. * (u_rand < rate * (dt /firing_delimeter))

  return poisson_train

def read_img(name_file):

	img = cv2.imread(name_file, 0)
	img2 = cv2.imread(name_file,0)

	img = np.ndarray.flatten(img)
	return img


