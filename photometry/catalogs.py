"""
Panstarrs catalog class. 
"""

from functools import cached_property
import pandas as pd
import numpy as np


def read_sex_keywords(sex_file_name:str) -> list[str]:
    """
    Reads the header of the given sextractor catalog and returns the header keywords
    as a list.
    """
    with open(sex_file_name, encoding='utf8') as sex_file:
        lines = sex_file.readlines()

    keywords = [line.split()[2] for line in lines if line[0] == '#']
    return keywords

def clean_catalog(catalog_name: str, value: str) -> None:
    """Remove rows from thecatalog which have the given (error) value in them. Then write to file.
    For panstarss this would be -999, for sextractor it's 99."""
    with open(catalog_name, encoding='utf8') as cat:
        lines = cat.readlines()

    good_lines = [line for line in lines if value  not in line]

    good_file = open(catalog_name, 'w', encoding='utf8')
    for line in good_lines:
        good_file.write(line)

class PanstarrsCatalog:
    """
    Main class representing the panstarrs catalog. The catalog can be created by using the 
    website: https://catalogs.mast.stsci.edu/panstarrs/search-results.html
    """
    def __init__(self, file_name: str) -> None:
        self.original_file_name = file_name
        clean_catalog(file_name, '-999')
        self.data_base = pd.read_csv(file_name)

class SextractorCatalog:
    """Main sextractor catalog."""
    def __init__(self, file_name: str) -> None:
        self.original_file_name = file_name
        clean_catalog(file_name, '99.0000')

    @cached_property
    def data_base(self) -> pd.DataFrame:
        """Converts sextractor cat into a pandas dataframe."""
        data = np.loadtxt(self.original_file_name)
        keywords = read_sex_keywords(self.original_file_name)

        pandas_data = []
        for row in data:
            pandas_data.append(
                {keyword: row[i] for i, keyword in enumerate(keywords)}
            )
        return pd.DataFrame(pandas_data)


if __name__ == '__main__':
    file_name = '../sextractor_run/imacs.cat'
    test = SextractorCatalog(file_name)
    db = test.data_base

    pan_file = '../panstarrs_catalog/PS-5_22_2023.csv'
    pan_cat = PanstarrsCatalog(pan_file)
