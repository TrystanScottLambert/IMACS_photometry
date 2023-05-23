""" Testing module for catalogs.py """


import sys
import unittest
import numpy as np
from pandas import DataFrame

sys.path.insert(1, '../photometry/')

from catalogs import read_sex_keywords, SextractorCatalog, PanstarrsCatalog, clean_catalog


class TestReadingSexKeywords(unittest.TestCase):
	"""
	Testing that the sex catalog class is reading in the 
	catalog correctly.
	"""

	def test_read_keywords(self):
		"""Testing that read_sex_keywords function is working correctly"""
		correct_keywords = [
			'ALPHAPEAK_J2000','DELTAPEAK_J2000','X_IMAGE','Y_IMAGE','MAG_APER',
			'MAGERR_APER', 'MAG_AUTO', 'MAGERR_AUTO', 'FLUX_AUTO', 'FLUXERR_AUTO',
			'FLUX_APER','FLUXERR_APER','CLASS_STAR'
			]
		keywords = read_sex_keywords('test_sex.cat')
		self.assertListEqual(keywords, correct_keywords)

class TestReadingSexCatalog(unittest.TestCase):
	"""Testing that the sex catalogs are being read in correctly into data frames."""

	def test_sextractor_database(self):
		"""testing the Sextractor catalog class with the test catalog."""
		sex_cat = SextractorCatalog('test_sex.cat')
		self.assertIsInstance(sex_cat.data_base, DataFrame)
		self.assertEqual(len(sex_cat.data_base.columns), 13)
		self.assertEqual(np.mean(sex_cat.data_base['ALPHAPEAK_J2000']), 357.1597327857143)

class TestReadingPanCatalog(unittest.TestCase):
	"""Testing that the pan catalogs are being read in correctly into data frames."""
	def test_panstars_database(self):
		pan_cat = PanstarrsCatalog('test_pan.csv')
		self.assertIsInstance(pan_cat.data_base, DataFrame)
		self.assertEqual(np.mean(pan_cat.data_base['raMean']), 357.52621118499997)
		self.assertEqual(len(pan_cat.data_base.columns), 8)

class TestCleaningCatalogs(unittest.TestCase):
	"""Testing that cleaning of both sexcatalogs and pan catalogs is working correctly."""

	def create_test_catalog(self, error_value):
		"""Creates a test catalog that can be used to see if bad values are being removed."""
		with open('test_clean.txt', 'w', encoding='utf8') as test_file:
			for i in range(4):
				test_file.write(f'{i ** 2} \n')
			test_file.write(f'{error_value}')
		
	def test_clean(self):
		"""Tests that the lines of a file that contain a value are removed."""
		self.create_test_catalog(-999)
		clean_catalog('test_clean.txt', '-999')
		with open('test_clean.txt', encoding='utf8') as test_file:
			lines = test_file.readlines()
		self.assertEqual(len(lines), 4)

		self.create_test_catalog(99)
		clean_catalog('test_clean.txt', '99')
		with open('test_clean.txt', encoding='utf8') as test_file:
			lines = test_file.readlines()
		self.assertEqual(len(lines), 4)
		



if __name__ == '__main__':
    unittest.main()
