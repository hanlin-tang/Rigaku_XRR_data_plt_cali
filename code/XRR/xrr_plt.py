# -*-coding:utf-8-*-
import os
import shutil
import re
import matplotlib.pyplot as plt
import numpy as np
import math
slit_size = 0.35 # 0.05 mm
sample_size  = 5 # 5mm
sin_theta = slit_size/sample_size
Angle_correct_upper_limit  = np.arcsin(sin_theta) # in rads
Angle_limit_degree = math.degrees(Angle_correct_upper_limit) # in degree

def normall(A):
    I0 = np.max(A) #get rid of first few data points
    for i, a in enumerate(A):

        A[i] = A[i] / I0

    return A

def transform_arrays(A, B, x):

    for i, a in enumerate(A):   # a is 2theta

        #B[i] = B[i] / I0
        if a < 2*x:
            B[i] = B[i] / (math.sin(math.radians(a/2)))


    return B

# Example usage:

x = Angle_limit_degree




plt.rcParams["font.family"] = "Times New Roman"

# Set the source path of the files you want to copy
source_path = "C:\\Users\\12243\\Desktop\\CWO_XRD\\XRR"  # source data file path

# Set the destination path for the copied files
destination_path = "C:\\Users\\12243\\Desktop\\CWO_XRD\\xrr_temp"  # all copied ras data files

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

# Loop through each file in the source directory
for file_name in os.listdir(source_path):

    # Check if the file is a ras file (.ras extension)
    if file_name.endswith(".ras"):
        # Build the full path of the file
        file_path = os.path.join(source_path, file_name)

        # Copy the file to the destination directory
        shutil.copy(file_path, destination_path)

    # print(f"File {file_name} copied to {destination_path}")  #copy all ras file to data process folder

files = os.listdir(destination_path)  # obtain all file name in the specific folder

offset = 0  # measurement offset
# phi_step = int(input('phi interval :'))
import xrayutilities as xu
# data = xu.io.rigaku_ras.RASFile('YBT005_103_RSM.ras', path ="C:\\Users\\12243\\Desktop\\file name change" )
from matplotlib.pylab import *

f = figure(figsize=(7, 5))
i = 0
phi_list = []
omega_list_real = []
for file_name in files:

    match = re.findall(r'\b\w+\b', file_name.replace('_', '.'))
    #print(match)

    label = match[-2]  # should return ras
    sample_name = match[0]  # should return sample name if the file is samplename_XRD.ras
    if label == 'reflectivity':
        # phi = phi_step *i
        # phi_list.append(phi)
        d = xu.io.RASFile(file_name, path=source_path)
        scan = d.scans[-1]
        tt = scan.data[scan.scan_axis] - offset  # scan angle
        plt.yscale("log")
        #plt.ylim([0.0000000001, 1])
        plt.xlim([0, 6])
        theta_start_index = 80
        tt_0 = tt[theta_start_index:] #get rid of first few data points
        intensity_0 = scan.data['int'][theta_start_index:]
        #print(scan.data['int'])

        transformed_B = transform_arrays(tt_0,intensity_0 , Angle_limit_degree)
        reflectivity = normall(transformed_B)
        #sample_number = int(list(sample_name)[-1])
        if sample_name == 'CWOI9':#or sample_name =='CWOI11' or sample_name=='sub': #select which file to plot
            plt.plot(tt_0, reflectivity, label='XRR')

            #np.savetxt('C:\\Users\\12243\\Desktop\\CWO_XRD\\XRR\\processed_txt_file\\{}.txt'.format(sample_name), np.c_[tt_0, reflectivity])   # write processed txt file to the current folder

    # print(tt) sampnp.savetxt('myfile.txt', np.c_[x,y,z])le_name == 'CWOI6' or or sample_name == 'CWOI1'
    # print(scan.data['int']) #scan data
    # max_intensity = max(scan.data['int'])  # find the highest intensity
    # inter = max_intensity/2
    # max_index = np.where(scan.data['int']==max_intensity)[0][0]  # find the index of the highest intensity
    # max_position = tt[max_index]  # find the position corresponding to the highest intensity
    # omega_list_real.append(max_position)
    i = i + 1

    # print(max_position)
    # semilogy(tt, scan.data['int'], 'o-', ms=3, label='data')
    # show()
# print(type(omega_list_real))
# print(phi_list)


plt.xlabel('$2\\theta$[\xb0]', fontsize=18)
plt.ylabel('Reflectivity', fontsize=18)
# plt.yticks([])
# plt.minorticks_off()

# semilogy(phi_list, omega_list_real, 'o-', ms=3, label='data')
data = np.loadtxt('CWOI9_fit.txt')


fit_theta = data[:, 0]
y = data[:, 1]
fit_ref = normall(y)
plt.plot(fit_theta, y,'-.', label = 'calculation')
plt.legend(prop={"size": 18})
plt.show()
