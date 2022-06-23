#!/usr/bin/env python3
''' setup file for installation of fzj_weather prometheus exporter '''
from setuptools import setup, find_packages

setup(
    name='prometheus_fzj_weather_exporter',
    version='1.1.0',
    description='prometheus exporter for weather data from FZJ',
    author='Oskar Druska',
    author_email='o.druska@fz-juelich.de',
    packages=find_packages(),
    license='ISC',
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'prometheus_client'
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'prometheus_fzj_weather_exporter=prometheus_fzj_weather_exporter.main:main'
        ],
    },

)
