import os
from setuptools import setup
from distutils.core import Command


setup(
    name='cpi',
    version='0.1.17',
    description="Quickly adjust U.S. dollars for inflation using the Consumer Price Index (CPI)",
    author='Ben Welsh',
    author_email='b@palewi.re',
    url='http://www.github.com/palewire/cpi',
    license="MIT",
    packages=("cpi",),
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    install_requires=(
        "requests>=2.20.0",
        "click>=6.7",
        "python-dateutil>=2.7.3",
        "pandas>=0.23.1",
    ),
    entry_points="""
        [console_scripts]
        inflate=cpi.cli:inflate
    """,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)
