import numpy as np

wasserboden = np.array([2.6, 2.5, 3.3, 3.5])
h1 = np.array([24.65, 24.4, 25.2, 25.2])
h2 = np.array([19.85, 19.7, 20.4, 20.5])
delta_h = ( (h2 - wasserboden) +(h1 - wasserboden) ) / 2 
print(delta_h)


t1 = np.array([13.2, 23.1, 34.9, 48.8])
t2 = np.array([14.4, 23.1, 35.6, 50.8])
delta_t = (t1 + t2) / 2
print(delta_t)


delta_t_values = [10.59, 11.29, 11.21, 10.97, 11.16,
                  11.11, 11.16, 11.17, 11.29, 11.23]

delta = np.array(delta_t_values)
mittelwert = np.mean(delta)
print(mittelwert)