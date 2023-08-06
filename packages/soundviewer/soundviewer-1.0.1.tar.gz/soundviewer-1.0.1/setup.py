from setuptools import find_packages ,setup
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

#reuirements txt list from requirements.txt
with open('requirements.txt','r') as f:
    requirements = f.readlines()
    requirements = [r.strip() for r in requirements if r.strip() ]


setup(
    name='soundviewer', 

     #  List of packages to install with this one read it from requirements.txt dynamically
    install_requires=requirements,

    # Packages to include into the distribution
    packages=find_packages(include=['soundviewer']),

    # Start with a small number and increase it with every change you make
    # https://semver.org
    version='1.0.1',

    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    # For example: GPL
    license='GPL',

    # Short description of your library
    description='Python package for visualizing sound data',

    # Long description of your library
    long_description = long_description,
    long_description_context_type = 'text/markdown',

    # Your name
    author='', 

    # Your email
    author_email='',     

    # Either the link to your github or to your website
    url='https://github.com/emingenc/soundviewer',

    # Link from which the project can be downloaded
    download_url='',

    # List of keyword arguments
    keywords=[],

    # https://pypi.org/classifiers/
    classifiers=[]  )