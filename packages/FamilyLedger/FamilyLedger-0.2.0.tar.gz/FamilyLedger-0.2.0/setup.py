"""
setuptools entry point

Copyright (C) 2020, fondlez, fondlez at protonmail.com
"""
import os
import sys

from setuptools import setup, find_packages


def read(relative_filepath, strip=None, **kwargs):
    this_filedir = os.path.dirname(__file__)
    with open(
        os.path.join(this_filedir, relative_filepath),
        encoding=kwargs.get('encoding', 'utf8'),
    ) as fh:
        content = fh.read()
        if strip:
            content.strip()
        return content


setup(
    name='FamilyLedger',
    version=read('familyledger/VERSION', strip=True),
    author='fondlez',
    author_email='fondlez@protonmail.com',
    url='https://github.com/fondlez/familyledger',
    description='Family Ledger is an application for collecting and viewing '
        'in-game item data held in World of Warcraft accounts.',
    long_description = read('README.rst'),
    download_url='https://github.com/fondlez/familyledger',
    packages=[
        'familyledger', 
        'familyledger.utils', 
        'familyledger.slpp',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ledger = familyledger.ledger:setup',
            'ledger_web = familyledger.ledger_web:setup',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Games/Entertainment :: Role-Playing',
    ],
    install_requires=[
        'remi==2019.11',
        'tqdm',
        'XlsxWriter',
    ],
)