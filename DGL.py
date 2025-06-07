import numpy as np
import matplotlib.pyplot as plt
# Physical constants

g = 9.18  # m/s^2
L = 2 # m
mu = 0.1 

THETA_0 = np.pi /3
THETA_DOT_0 = 0 #No initial velocity


def get_theta_double_dot(theta, theta_dot):
    return -mu * theta_dot - (g/L) * np.sin(theta)

def theta(t):
    # Initialize changing values
    theta = THETA_0
    theta_dot = THETA_DOT_0
    delta_t = 0.01
    for time in np.arange(0, t, delta_t):
        theta_double_dot = get_theta_double_dot(theta, theta_dot)
        theta_dot += theta_double_dot * delta_t
        theta += theta_dot * delta_t
    return theta


for t in np.arange(0, 10, 0.1):
    print(theta(t))


# plot result
t = np.arange(0, 10, 0.1)
theta_values = [theta(time) for time in t]
plt.plot(t, theta_values)
plt.xlabel('Time (s)')
plt.ylabel('Theta (rad)')
plt.title('Pendulum Motion')
# Save the plot to a file instead of showing it interactively
plt.savefig('pendulum_motion.png')
plt.close()
print("Plot saved as 'pendulum_motion.png'")
