import matplotlib.pyplot as plt
import numpy as np

'''Linear calibration for gamma-ray spectra. ''' 
# x contains the channel numbers of the selected features. 
x = [386.62, 436.98, 916.00, 1034.92]
# y contains the corresponding accepted energies. 
y = [0.5110, 0.6617, 1.173, 1.332]
# Linear fit. a and b are the gain and the offset. 
(a,b) = np.polyfit(x, y, 1)
print("The gain a = " + str(a) + " MeV/channel number. The offset b = " + str(b) + " MeV")
# Plotting the fitted line. 
plt.figure()
plt.scatter(x, y, label='Raw data points')
plt.ylabel("Energy (MeV)")
plt.xlabel("CN")
# y_l contains the calculated energies using the calibration. 
y_l = []
for i in range(len(x)):
    y_l.append(a * x[i] + b)
plt.plot(x, y_l, label='Fitted line')
plt.legend()

# Calculating the energies using the calibration. cn is the channel number and uncert is 
def getEnergy(a, b, cn, uncert):
    return (a * cn + b, a * uncert)
# The third and fourth parameter
(energy, uncertainty) = getEnergy(a, b, 916, 21.31)
# print("The energy is " + str(energy) + " MeV, the uncertainty is " + str(uncertainty))

# Plotting the linear calibration and all the spectrum features with uncertainties. 
# x_all has all the data for measured channel numbers. 
x_all = [941.37, 386.62,  916.00, 177.76, 1034.92, 720.85, 436.98, 293.45, 129.83, 363.45, 122.33, 662.94]
# y_all has all the data for calculated experimental energies using the calibration. 
y_all = [1.215, 0.553, 1.185, 0.304, 1.326, 0.952, 0.613, 0.442, 0.247, 0.526, 0.238, 0.883]
# y_accepted has all the data for accepted energies. 
y_accpeted = [1.274, 0.5110, 1.173, 0.210, 1.332, 1.117, 0.661, 0.477, 0.184, 0.570, 0.176, 1.064]
# uncer has all the data for the uncertainties of the calculated experimental energies. 
uncer = [0.023, 0.015, 0.025, 0.014, 0.029, 0.026, 0.016, 0.018, 0.010, 0.014, 0.014, 0.016]
plt.figure()
#Plotting them. 
for i in range(len(x_all)): 
    plt.errorbar(x_all[i], y_all[i], yerr=uncer[i])
plt.errorbar(941.37, 1.215, yerr=0.023, label = 'Experimental data points')
plt.plot(x_all, y_all, label='Fitted line', linewidth = 0.5)
plt.scatter(x_all, y_accpeted, label = 'Raw data points')
plt.ylabel("Energy (MeV)")
plt.xlabel("CN")
plt.legend()

'''Calculating the energy resolution, A^2, C^2, and Npe. '''
# The measured FWHMs in channel numbers. 
FWHMs = [46.150, 30.380, 50.030, 27.020, 56.227, 51.820, 30.760, 36.000, 19.081, 26.821, 28.041, 31.244]
# Calculating the energy resolutions squared. 
Energy_resl_squared = []
for i in range(len(FWHMs)):
    Energy_resl_squared.append(((FWHMs[i] * a + b)/y_all[i]) ** 2)
# Calculating the inverses of the energies. 
Energy_inverse = []
for i in range(len(FWHMs)):
    Energy_inverse.append(1/y_all[i])
(A_squared,C_squared) = np.polyfit(Energy_inverse, Energy_resl_squared, 1)
Energy_resl_squared_fitted = []
for i in range(12):
    Energy_resl_squared_fitted.append(A_squared * Energy_inverse[i] + C_squared)
print("A^2 = " + str(A_squared) + " MeV, C^2 = " + str(C_squared))
print("Npe = " + str(1/A_squared) + " photoelectrons/MeV")
# Plotting the fitted equation [5] and the data points of Energy_resl_squared and Energy_inverse. 
plt.figure()
plt.scatter(Energy_inverse, Energy_resl_squared)
plt.plot(Energy_inverse, Energy_resl_squared_fitted, label = 'Fitted line for equation [5]')
plt.ylabel("Energy resolution squared")
plt.xlabel("Energy inverted (MeV^(-1))")
plt.legend()

'''Determining c and d in equation [11].'''
ener = [37.016, 23.829, 22.359]
ener_sqrt = []
for i in ener: 
    ener_sqrt.append(np.sqrt(i))
Z_value = [83, 66, 64]
(c, d) = np.polyfit(Z_value, ener_sqrt, 1)
plt.figure()
ener_sqrt_fitted = []
for i in Z_value: 
    ener_sqrt_fitted.append(c * i + d)
plt.scatter(Z_value, ener_sqrt, label = 'Raw data points')
plt.plot(Z_value, ener_sqrt_fitted, label = 'Fitted line')
plt.ylabel("Square-root energy (KeV^(1/2))")
plt.xlabel("Atomic number (Z)")
plt.legend()
print("c = " + str(c) + ", d = " + str(d))
plt.show()