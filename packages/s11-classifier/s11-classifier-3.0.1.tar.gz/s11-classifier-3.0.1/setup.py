# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.
# pylint: skip-file
from setuptools import setup
import setuptools
import os

version = '3.0.1'

long_description = open('README.md').read()

test_requirements = [
    'pytest'
]

setup(
    name='s11-classifier',
    version=version,
    description="Classifier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Satelligence",
    author_email='team@satelligence.com',
    url='https://gitlab.com/satelligence/classifier',
    packages=setuptools.find_packages(),
    package_dir={
        'classifier': 'classifier'
    },
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.0.3, <4.0.0',
        'numpy>=1.17.5, <2.0.0',
        'pylint>=2.12.0, <3.0.0',
        'pytest>=5.2.0, <6.0.0',
        'rasterio>=1.1.8, <2.0.0',
        'scikit_learn==1.0.2',
        'xgboost>=1.1.1, <2.0.0',
        'boto3>=1.16.63, <2.0.0',
        'folium>=0.12.1, <1.0.0',
        'geopandas>=0.8.2, <1.0.0',
        'geojson>=2.5.0, <3.0.0',
        'click>=7.1.2, <8.0.0',
        'rasterstats>=0.15.0, <1.0.0',
        'rtree>=0.9.7, <1.0.0',
        'xarray>=0.12.3, <1.0.0',
        'python-dateutil>=2.8.1, <3.0.0',
        'jinja2>=2.11.3, <3.0.0'

    ],
    license="Apache-2.0",
    zip_safe=False,
    python_requires='>=3.5'
)
