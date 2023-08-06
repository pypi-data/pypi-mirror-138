import os
from distutils.core import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def version():
    setupDir = os.path.dirname(os.path.realpath(__file__))
    versionFile = open(os.path.join(setupDir, 'gtdb_validation_tk', 'VERSION'))
    return versionFile.readline().strip()


setup(
    name='gtdb_validation_tk',
    version=version(),
    author='Donovan Parks',
    author_email='donovan.parks@gmail.com',
    packages=['gtdb_validation_tk'],
    package_data={'gtdb_validation_tk': ['VERSION']},
    entry_points={
        'console_scripts': [
            'gtdb_validation_tk = gtdb_validation_tk.__main__:main'
        ]
    },
    url='https://pypi.org/project/gtdb-validation-tk/',
    license='GPL3',
    description='A toolbox for validating the GTDB taxonomy.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    install_requires=[
        "numpy >= 1.8.0",
        "biolib >= 0.1.8",
        "dendropy >= 4.0.0",
        'fuzzywuzzy'],
)
