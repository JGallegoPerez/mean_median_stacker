import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# Culls the original 2D array to a central region of interest
# Values must be even numbers
def center_roi(arr2d, roi):
    half = (np.array(roi) / 2).astype(int)
    center_i = int(arr2d.shape[0] / 2)
    center_j = int(arr2d.shape[1] / 2)
    return arr2d[(center_i - half[0]):(center_i + half[0]), (center_j - half[0]):(center_j + half[0])]

def image_reader(file, format):
    if format == 'tiff':
        data = plt.imread(file)
    elif format == 'fits':
        hdulist = fits.open(file)
        data = hdulist[0].data
    return data

def mean_stack(file_lst, format, roi):
    data0 = center_roi(image_reader(file_lst[0],format),roi)
    data_sum = np.zeros((data0.shape))  # create a 2D array with zeros
    for f in file_lst:
        data = center_roi(image_reader(f,format),roi)
        data_sum += data
    data_mean = data_sum / len(file_lst)
    return data_mean

#running_stats function taken from "Data-driven Astronomy" course
def running_stats(filenames, format, roi):
    '''Calculates the running mean and stdev for a list of FITS files using Welford's method.'''
    n = 0
    for filename in filenames:
        data = center_roi(image_reader(filename,format),roi)
        if n == 0:
            mean = np.zeros_like(data)
            s = np.zeros_like(data)
        n += 1
        delta = data - mean
        mean = mean + (delta / n)
        s = s + (delta * (data - mean))
    s /= n - 1
    np.sqrt(s, s)
    if n < 2:
        return mean, None
    else:
        return mean, s

def median_bins_fits(fits_lst, format, B, roi):
    mu, sigma = running_stats(fits_lst, format, roi)  # center_roi had been applied before
    minval = mu - sigma
    bin_width = 2 * sigma / B
    ignore_bin = np.zeros((mu.shape[0], mu.shape[1]), dtype=np.uint16)
    # 1st and 2nd dimensions indicate pixel pos. 3rd dim indicates bin
    bins = np.zeros((B, mu.shape[0], mu.shape[1]), dtype=np.uint16)
    bins_starts = np.zeros(((B, mu.shape[0], mu.shape[1])))
    for b in range(B):
        bins_starts[b, :, :] = minval + (b * bin_width)
    for f in fits_lst: #for each image:
        data = center_roi(image_reader(f,format),roi)
        data_flat = data.reshape(data.shape[0] * data.shape[1], 1)
        for p in range(len(data_flat)):  # pixel by pixel
            i = p // data.shape[0]
            j = p % data.shape[0]
            if data_flat[p] < minval[i][j]:
                ignore_bin[i][j] += 1
            elif data_flat[p] < (mu[i][j] + sigma[i][j]):
                bin1d = bins_starts[:, i, j]
                bin1d = list([x for x in bin1d if x <= data_flat[p]])
                max_list = max(bin1d)
                bins_starts_index = bin1d.index(max_list)
                bins[bins_starts_index][i][j] += 1
    return mu, sigma, ignore_bin, bins

def median_approx_fits(fits_lst, format, B, roi):
    mu, sigma, ignore_bin, bins = median_bins_fits(fits_lst, format, B, roi)  # BIG
    N = len(fits_lst)
    img1 = center_roi(image_reader(fits_lst[0], format), roi)
    total = ignore_bin
    total_all = ignore_bin
    exceed_index = np.zeros(img1.shape)
    arr_limit = np.ones(img1.shape) * ((N + 1) / 2)
    for b in range(B):
        exceed_index += ((total_all + bins[b, :, :]) < arr_limit).astype(int)
        total_all += bins[b, :, :]
        bins[b, :, :] = ((total + bins[b, :, :]) < arr_limit).astype(int) * bins[b, :, :]
        total = total + bins[b, :, :]  # all bins have been summed up
    bin_begin = mu - sigma + ((exceed_index) * 2 * (sigma) / B)  # vectorized
    exceeded_array = bin_begin + (sigma / B)
    return exceeded_array

def img_stack(file_lst, format, method, roi, bins=0):
    if method == 'mean':
        print("Mean stacking method used")
        stacked = mean_stack(file_lst, format, roi)
    elif method == 'binapprox':
        stacked = median_approx_fits(file_lst, format, bins, roi)
        print("Binapprox stacking method used")
    return stacked



