from setuptools import setup, find_packages


setup(
    name='competitivetracker',
    version='1.0.1',
    author='Darren Smith',
    author_email='darren.smith@sparkpost.com',
    packages=find_packages(),
    url='https://github.com/darrensmith223/CompetitiveTracker',
    license='Apache 2.0',
    description='Competitive Tracker Python API Library',
    install_requires=['requests>=2.20.1']
)