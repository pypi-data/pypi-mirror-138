# make setup.pu for package building
from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'My first Python package，probably the final version'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="hw_3", 
        version=VERSION,
        author="Bingcheng Qing",
        author_email="bc.qing@berkeley.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Bingcheng Qing', 'AY250', '2022Spring'],
)
