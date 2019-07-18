#!/usr/bin/python3
from setuptools import setup

exec(open('version.py').read())

setup(
    name='getsos',
    version=__version__,
    author='Kshithij Iyer',
    author_email='kshithij.ki@gmail.com',
    url='https://github.com/kshithijiyer/gluster-BulkVolumeCreate/',
    licens="BSD 2-Clause 'Simplified' License",
    description=("A tool to collect sosreports of multiple servers."),
    py_modules=['getsos', 'version'],
    entry_points="""
    [console_scripts]
    getsos = getsos:main
    """
)
