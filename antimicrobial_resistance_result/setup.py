import setuptools
from distutils.core import setup, Extension

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='antimicrobial_resistance_result',
    version='v0.1.0',
    author=['Dan Fornika'], 
    author_email='dfornika@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfornika/antimicrobial_resistance_result",
    packages=['AntimicrobialResistance'],
)
