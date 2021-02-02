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
    packages=['hAMRonization'],
    version=version,
    license="LGPLv3",
    description="Tool to convert and summarize AMR gene detection outputs "
                "using the hAMRonization specification",
    author='Finlay Maguire',
    author_email='finlaymaguire@gmail.com',
    url="https://github.com/pha4ge/hAMRonization",
    download_url=f"https://github.com/pha4ge/archive/v{version}.tar.gz",
    keywords=["Genomics", "Antimicrobial resistance", "Antibiotic",
              "Standardization"],
    python_requires='>=3.7',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            'hamronize = hAMRonization.hamronize:main'
            ],
        },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
        ],
    zip_safe=True,
    )
