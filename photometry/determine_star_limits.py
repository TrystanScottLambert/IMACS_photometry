"""
Determining the best stars to use for photometric calibration.

One cannot choose stars that are too brigh since they are saturating and 
thus cause non linearity on the brighter side of things. On the other hand 
too faint sources are not reliable. This plot is made so that 
we can determine reasonable limits.

Import the UPPER_LIM and LOWER_LIM from this module.
Set them based on the plot that is generated.
"""

import numpy as np
import pylab as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from catalogs import SextractorCatalog, PanstarrsCatalog

SEARCH_TOLERANCE = 1 * u.arcsec
UPPER_LIM = -6  # from the plot
LOWER_LIM = -9.5

if __name__ == '__main__':
    INFILE_SEX = '../sextractor_run/imacs.cat'
    INFILE_PAN = '../panstarrs_catalog/PS-5_22_2023.csv'
    sex_cat = SextractorCatalog(INFILE_SEX)
    pan_cat = PanstarrsCatalog(INFILE_PAN)

    catalog = SkyCoord(
        ra = sex_cat.data_base['ALPHAPEAK_J2000'] *u.deg,
        dec = sex_cat.data_base['DELTAPEAK_J2000'] * u.deg
    )

    c = SkyCoord(
        ra = pan_cat.data_base['raMean'] * u.deg,
        dec = pan_cat.data_base['decMean'] * u.deg
    )

    idx, d2d, _ = c.match_to_catalog_sky(catalog)
    cut = np.where(d2d < SEARCH_TOLERANCE)[0]
    idx = idx[cut]

    reduced_pan_cat = pan_cat.data_base.iloc[cut]
    reduced_sex_cat = sex_cat.data_base.iloc[idx]

    delta_mags = np.array(list(reduced_sex_cat['MAG_APER'])) - np.array(list(reduced_pan_cat['iMeanPSFMag']))
    plt.scatter(np.array(list(reduced_sex_cat['MAG_APER'])), delta_mags)
    plt.axvspan(xmin = LOWER_LIM, xmax=UPPER_LIM, alpha=0.2, color='r')
    plt.show()