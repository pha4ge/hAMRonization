import setuptools
from distutils.core import setup, Extension

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='hAMRonization',
    version='v1.0.0alpha',
    author=['Dan Fornika', 'Finlay Maguire'],
    author_email='dfornika@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pha4ge/hAMRonization ",
    packages=['hAMRonization'],
)
