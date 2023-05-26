"""
Script for determining the depth of the IMACS image.
"""

import numpy as np
import pylab as plt
from scipy.stats import gaussian_kde

from catalogs import SextractorCatalog
from zpt_determination import imacs_zpt

INFILE_SEX = '../sextractor_run/imacs.cat'
sex_cat = SextractorCatalog(INFILE_SEX)

sex_cat.data_base['CAL_MAGS'] = sex_cat.data_base['MAG_AUTO'] + imacs_zpt
sex_cat.data_base['SNR'] = (2.5/np.log(10))/sex_cat.data_base['MAGERR_AUTO']
reduced_data = sex_cat.data_base[sex_cat.data_base['SNR'] < 15]

mag = np.array(reduced_data['CAL_MAGS'])
signal_to_noise = np.array(reduced_data['SNR'])

n_bins = 100
kernal = gaussian_kde((mag, signal_to_noise))
x_i, y_i = np.mgrid[
    mag.min():mag.max():n_bins*1j, signal_to_noise.min():signal_to_noise.max():n_bins*1j]
z_i = kernal(np.vstack([x_i.flatten(), y_i.flatten()]))

plt.pcolormesh(x_i, y_i, z_i.reshape(x_i.shape), shading='auto')
plt.xlabel('Measured Mags')
plt.ylabel('SNR')
plt.ylim(0,15)
plt.xlim(24, 30)
plt.axhline(5, ls='--', lw=1.5, color='r', alpha=0.4)
plt.show()
