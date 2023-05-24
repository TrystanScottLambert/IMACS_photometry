"""
Determining the zero point of the photometric calibration.
"""

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u
from photcal.photometric_calibration import get_photometric_transformation, Color,\
      FilterMag, Settings

from determine_star_limits import UPPER_LIM, LOWER_LIM, SEARCH_TOLERANCE
from catalogs import SextractorCatalog, PanstarrsCatalog


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

i_obs = FilterMag(
    'i_imacs',
    np.array(list(reduced_sex_cat['MAG_AUTO'])),
    np.array(list(reduced_sex_cat['MAGERR_AUTO']))
    )

i_cat = FilterMag(
    'i_pan',
    np.array(list(reduced_pan_cat['iMeanPSFMag'])),
    np.array(list(reduced_pan_cat['iMeanPSFMagErr']))
    )

r_cat = FilterMag(
    'r_pan',
    np.array(list(reduced_pan_cat['rMeanPSFMag'])),
    np.array(list(reduced_pan_cat['rMeanPSFMagErr']))
    )

z_cat = FilterMag(
    'z_pan',
    np.array(list(reduced_pan_cat['zMeanPSFMag'])),
    np.array(list(reduced_pan_cat['zMeanPSFMagErr']))
    )

color_ri = Color('r-i', r_cat, i_cat)
color_iz = Color('i-z', i_cat, z_cat)

settings = Settings(i_obs, i_cat, [color_ri, color_iz])
transform = get_photometric_transformation(settings)
