from stacking import *
import matplotlib.pyplot as plt
import os

############ INSTRUCTIONS ##############
# Comment al the code in whichever example is not executed.
# Run this module.

#-------------------------- Example 1: Saturn TIFF images, using mean stacking method ----------------------------------
#Prepare a list of Saturn TIFF images
dir_path = 'venv/images/Saturn_tests'
file_list = []
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        file_list.append('venv/images/Saturn_tests/' + path)

#Arguments in img_stack:
#file list: a list of strings
#file_format: 'fits' or 'tiff'
#stacking_method: 'mean' or 'binapprox'
#roi: a region of interest centered in the image. Must be smaller than the image size. 2 element list, e.g. [300, 300]
#(Optional) Number of bins, if binapprox method is selected
stacked_img = img_stack(file_list, 'tiff', 'mean', [300,300])
plt.imshow(stacked_img.T, cmap='gray', vmin=0, vmax=44000)
plt.colorbar()
plt.show()
#-----------------------------------------------------------------------------------------------------------------------





#------------------ Example 2: Triangulum Galaxy (M33) FITS images, using binapprox stacking method --------------------
# #Prepare a list of M33 FITS images
# file_list = ['venv/images/M33_tests/b_00{}.fits'.format(str(i)) for i in range(1, 4)]
# stacked_img = img_stack(file_list, 'fits', 'binapprox', [300,300], 10)
# plt.imshow(stacked_img.T, cmap='gray', vmin=0, vmax=44000)
# plt.colorbar()
# plt.show()
#-----------------------------------------------------------------------------------------------------------------------

