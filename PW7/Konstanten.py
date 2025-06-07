import matplotlib.pyplot as plt
import numpy as np
import math
## bolzemann constant
k = 1.38064852e-23
## speed of light
c = 299792458
## planck constant
h = 6.62607015e-34
## Wellenlänge in nm
l = 580e-9


constante = h * c / (l * k)



U_1 =  6
U_2 =  4
I_1 =  4.546
I_2 =  3.6

IL_1 = 9.102447569 
IL_2 = 7.77459711




P1 =  U_1 * I_1
P2 =  U_2 * I_2

P1_P_2 = P1 / P2

T_1 =  ( ( ((P1/P2)**(1/4))-1 )* constante) /np.log(IL_1/IL_2) 
print(T_1)

T_2 = (((T_1**4) * P2) / P1)**(1/4)

print(T_2)

