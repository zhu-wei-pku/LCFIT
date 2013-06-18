import os
import sys
import functions
import fitting_functions
from numpy import *
import matplotlib.pyplot as plt
from scipy import optimize

def movingaverage(interval, window_size):
    window= ones(int(window_size))/float(window_size)
    return convolve(interval, window, 'same')

### Global constants
au = 1.496*10**11
msun = 1.988435*10**30
rsun = 6.955*10**8
mjup = 1.8988*10**27 
rjup = 6.9173*10**7
day = 60.*60.*24.
gconst = 6.67*10**(-11)


### Read from config file
### Load initial parameters and lightcurve

temp_param_names = []
temp_param_vals = []
temp_param_range = []

lc = functions.read_config_file("INPUT_LC")
lc = loadtxt(lc)

lc_ld1 = eval(functions.read_config_file("LC_LD1"))
lc_ld1_err = eval(functions.read_config_file("LC_LD1_ERR"))
lc_ld2 = eval(functions.read_config_file("LC_LD2"))
lc_ld2_err = eval(functions.read_config_file("LC_LD2_ERR"))
for i in range(len(lc_ld1)):
    temp_param_names.append("lc_ld1")
    temp_param_vals.append(lc_ld1[i])
    temp_param_range.append(lc_ld1_err[i])
    temp_param_names.append("lc_ld2")
    temp_param_vals.append(lc_ld2[i])
    temp_param_range.append(lc_ld2_err[i])

temp_param_names.append("period")
temp_param_vals.append(float(functions.read_config_file("PERIOD")))
temp_param_range.append(float(functions.read_config_file("PERIOD_ERR")))

temp_param_names.append("t0")
temp_param_vals.append(float(functions.read_config_file("T0"))-floor(float(functions.read_config_file("T0"))))
temp_param_range.append(float(functions.read_config_file("T0_ERR")))

temp_param_names.append("rsum")
temp_param_vals.append(float(functions.read_config_file("RSUM")))
temp_param_range.append(float(functions.read_config_file("RSUM_ERR")))

temp_param_names.append("rratio")
temp_param_vals.append(float(functions.read_config_file("RRATIO")))
temp_param_range.append(float(functions.read_config_file("RRATIO_ERR")))

temp_param_names.append("i_0")
temp_param_vals.append(float(functions.read_config_file("I0")))
temp_param_range.append(float(functions.read_config_file("I0_ERR")))

temp_param_names.append("ecosw")
temp_param_vals.append(float(functions.read_config_file("ECOSW")))
temp_param_range.append(float(functions.read_config_file("ECOSW_ERR")))

temp_param_names.append("esinw")
temp_param_vals.append(float(functions.read_config_file("ESINW")))
temp_param_range.append(float(functions.read_config_file("ESINW_ERR")))


### Distribute as free or fixed param, including associated brackets
free_param_names = []
free_param_vals = []
free_param_range = []
free_param_func = []

fixed_param_names = []
fixed_param_vals = []

for i in range(len(temp_param_names)):
    if temp_param_range[i] == 0:
        fixed_param_names.append(temp_param_names[i])
        fixed_param_vals.append(temp_param_vals[i])
    else:
        free_param_names.append(temp_param_names[i])
        free_param_vals.append(temp_param_vals[i])
        free_param_range.append(temp_param_range[i])
        free_param_func.append("b")

print "FREE PARAMS"
for i in range(len(free_param_names)):
    print free_param_names[i],free_param_vals[i],free_param_range[i]


print "FIXED PARAMS"
for i in range(len(fixed_param_names)):
    print fixed_param_names[i],fixed_param_vals[i]

x0 = zeros(len(free_param_names))

free_param_vals = [functions.read_ascii("best_param_mcmc")[1]]
free_param_vals = array(functions.read_table(free_param_vals))[0]

print free_param_vals

phase,flux,err,model = fitting_functions.lc_chisq(free_param_vals,free_param_names,fixed_param_names,fixed_param_vals,lc,False,True)

### Plot data
plt.clf()
plt.scatter(phase,flux,s=1,color="k")
plt.scatter(phase+1,flux,s=1,color="k")

plt.scatter(phase,model,s=2,color="r")
plt.scatter(phase+1,model,s=2,color="r")

plt.xlim(0.995,1.005)
plt.show()

### Plot residual
plt.clf()

residual = flux-model
residual_mvavg = movingaverage(residual,10)

plt.scatter(phase,residual,s=1,color="k")
plt.scatter(phase+1,residual,s=1,color="k")

plt.scatter(phase,residual_mvavg,s=10,color="r")
plt.scatter(phase+1,residual_mvavg,s=10,color="r")

plt.axhline(y=0,color="r")

plt.xlim(0.995,1.005)
plt.show()
