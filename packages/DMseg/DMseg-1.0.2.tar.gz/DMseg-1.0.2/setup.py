from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'Python package for DMseg: detecting differential methylation regions in DNA methylome data'

# Setting up
setup(
  name="DMseg",
  version=VERSION,
  author="James Dai, Kevin Wang",
  author_email="<jdai@fredhutch.org>",
  license='MIT',
  description=DESCRIPTION,
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  packages=find_packages(),

  install_requires=['pandas', 'numpy'], # add any additional packages that 
  
  keywords=['python', 'DNA methylation', 'Differentially methylated regions'],
  classifiers=["Topic :: Scientific/Engineering :: Bio-Informatics"]
)
