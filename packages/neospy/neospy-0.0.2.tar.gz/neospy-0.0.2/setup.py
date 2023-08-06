from setuptools import setup

setup(
    name = 'neospy',
    version = '0.0.2',    
    description = 'A Python module to interface with the NEOS optimization servers.',
    url = 'https://github.com/scythetrigger/neospy',
    author = 'Nicholas Parham',
    author_email = 'nick-99@att.net',
    license = 'Apache Software License',
    packages = ['neospy'],
    install_requires = [
        'bs4', 
        'requests',
        'amplParser'
        ],

    classifiers = [],
)