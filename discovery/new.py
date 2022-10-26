import time
import dwf


t_start = time.process_time()

print('ggg')

data1 = [1 for i in range(64)]
data2 = [0 for i in range(64)]

datanew=[0 for i in range(64)]
for i in range(64):
    if i%2==0: datanew[i] = 1
    else: datanew[i] = 0
time.sleep(1)

print(time.process_time() - t_start)
