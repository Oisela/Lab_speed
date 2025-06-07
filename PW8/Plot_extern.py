import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Provided data
U_C = np.array([1.132, 1.194, 1.265, 1.331, 1.379, 1.403, 1.397, 1.36, 1.291, 1.19,
                1.062, 0.919, 0.788, 0.677, 0.588, 0.518, 0.46, 0.413, 0.372, 0.338, 0.309])
U_0 = np.array([0.975, 0.948, 0.906, 0.846, 0.772, 0.688, 0.612, 0.55, 0.513, 0.506,
                0.531, 0.587, 0.652, 0.708, 0.752, 0.785, 0.809, 0.827, 0.842, 0.853, 0.862])
omega = np.array([3141.592654, 3769.911184, 4398.229715, 5026.548246, 5654.866776,
                  6283.185307, 6911.503838, 7539.822369, 8168.140899, 8796.45943,
                  9424.777961, 10053.09649, 10681.41502, 11309.73355, 11938.05208,
                  12566.37061, 13194.68915, 13823.00768, 14451.32621, 15079.64474, 15707.96327])

# Calculate U_C / U_0
U_ratio = U_C / U_0

# Define the model function
def U_C_U_0_model(omega, omega_0, delta):
    return (omega_0**2) / np.sqrt((omega_0**2 - omega**2)**2 + 4 * delta**2 * omega**2)

# Perform the fit
initial_guess = [10000, 500]  # Initial guess for omega_0 and delta
params, covariance = curve_fit(U_C_U_0_model, omega, U_ratio, p0=initial_guess)

# Extract fitted parameters
omega_0_fit, delta_fit = params
omega_0_fit_error, delta_fit_error = np.sqrt(np.diag(covariance))

# Generate data for plotting the fit
omega_fit = np.linspace(min(omega), max(omega), 1000)
U_fit = U_C_U_0_model(omega_fit, omega_0_fit, delta_fit)

# Plot the data and the fit
plt.figure(figsize=(10, 6))
plt.scatter(omega, U_ratio, label="Measured Data", color="blue", alpha=0.7)
plt.plot(omega_fit, U_fit, label=f"Fit: $\\omega_0 = {omega_0_fit:.2f} \\pm {omega_0_fit_error:.2f}$, "
                                 f"$\\delta = {delta_fit:.2f} \\pm {delta_fit_error:.2f}$", color="red")
plt.xlabel(r"$\omega$ ($s^{-1}$)")
plt.ylabel(r"$U_C / U_0$")
plt.legend()
plt.grid(True)
plt.savefig("Plot_U_C_U_0_fit.png")
plt.show()
