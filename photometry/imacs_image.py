"""
Main IMACS image class
"""

from functools import cached_property
from numpy import ndarray
from astropy.io import fits
from astroquery.mast import Catalogs
from astropy.wcs import WCS


def get_center_pix(array_2d: ndarray):
    """
    Works out the central pixels (rounded if need be) of a 2d array.
    """
    center_x = int(round(array_2d.shape[1]/2))
    center_y = int(round(array_2d.shape[0]/2))
    return center_x, center_y

IMACS_FOV = 0.4 # Radius in degrees

class ImacsImage:
    """
    Representation of IMACS observations.
    """
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.hdul = fits.open(file_name)
        self.wcs = WCS(self.header)

    @property
    def header(self):
        """Header of the image."""
        return self.hdul[0].header

    @property
    def data(self):
        """Data of the image"""
        return self.hdul[0].data


if __name__ == '__main__':
    infile = '../imacs_data/night_1_theli.fits'
    night_1 = ImacsImage(infile)
