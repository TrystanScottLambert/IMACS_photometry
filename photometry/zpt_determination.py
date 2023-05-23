"""
Determining the zero point of the photometric calibration.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from determine_star_limits import UPPER_LIM, LOWER_LIM, SEARCH_TOLERANCE
from catalogs import SextractorCatalog, PanstarrsCatalog


def m_instrumental(m_panstars, color_ri, color_iz, c_0, c_1, c_2):
    """
    Function for fitting the data. Will need to do a fit in order to determine the 
    values for c_0, c_1, and c_2.

    color_ri mean the r-i color from panstars. 
    """
    return c_0 + m_panstars + c_1*color_ri + c_2*color_iz


if __name__ == '__main__':
    INFILE_SEX = '../sextractor_run/imacs.cat'
    INFILE_PAN = '../panstarrs_catalog/PS-5_22_2023.csv'
    sex_cat = SextractorCatalog(INFILE_SEX)
    pan_cat = PanstarrsCatalog(INFILE_PAN)

    sex_cat.data_base = sex_cat.data_base[
        sex_cat.data_base['MAG_APER'].between(LOWER_LIM, UPPER_LIM)
    ]

    catalog = SkyCoord(
        ra = sex_cat.data_base['ALPHAPEAK_J2000'] * u.deg,
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

    reduced_pan_cat['ri'] = reduced_pan_cat['rMeanPSFMag'] - reduced_pan_cat['iMeanPSFMag']
    reduced_pan_cat['iz'] = reduced_pan_cat['iMeanPSFMag'] - reduced_pan_cat['zMeanPSFMag']
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(reduced_pan_cat['iMeanPSFMag'], reduced_pan_cat['ri'], reduced_pan_cat['iz'])
    plt.show()