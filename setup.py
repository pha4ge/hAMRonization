import os
import re
import runpy
from setuptools import setup
from setuptools.command.build_py import build_py

with open('README.md') as fh:
    long_description = fh.read()

with open('hAMRonization/__init__.py') as fh:
    info = fh.read()
    version = re.search('^__version__\\s*=\\s*"(.*)"',
                        info, re.M).group(1)

# stdlib-only module with the pinned chamredb/argNorm data to download
data_sources = runpy.run_path(os.path.join('hAMRonization', 'data_sources.py'))


class BuildWithData(build_py):
    """Download the database mapping data into the package when building"""

    def run(self):
        super().run()
        if os.environ.get(data_sources['SKIP_DOWNLOAD_ENV']):
            print("hAMRonization: skipping database mapping data download")
            return
        if getattr(self, 'editable_mode', False):
            # editable installs use the source tree
            data_dir = data_sources['DATA_DIR']
        else:
            data_dir = os.path.join(self.build_lib, 'hAMRonization', 'data')
        data_sources['download_data'](data_dir)


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
    python_requires='>=3.10',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas'],
    cmdclass={'build_py': BuildWithData},
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
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
        ],
    zip_safe=False,
    )
