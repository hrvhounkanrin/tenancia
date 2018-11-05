import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='meslimmo',
    version='1.0.0',
    packages=['meslimmo'],
    include_package_data=True,
    description='Django data api for mesley immo app',
    long_description=README,
    author='Hervé HOUNKANRIN',
    author_email='hrvhounkanrin@gmail.com',
    url='',
    license='MIT'
)
