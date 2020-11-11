import setuptools
import re
from distutils.core import setup

with open('README.md') as fh:
    long_description = fh.read()

with open('hAMRonization/__init__.py') as fh:
    info = fh.read()
    version = re.search('^__version__\s*=\s*"(.*)"',
                        info, re.M).group(1)

setup(
    name='hAMRonization',
    version=version,
    author=['Finlay Maguire', 'Dan Fornika'],
    python_requires='>=3.7',
    author_email='finlaymaguire@gmail.com',
    description='hAMRonization AMR gene detection implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pha4ge/hAMRonization",
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            'hamronize = hAMRonization.hamronize:main'
            ],
        },
    packages=['hAMRonization'],
)
