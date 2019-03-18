from setuptools import find_packages, setup

setup(
    name='lem_sim',
    packages=find_packages('src'),
    version='0.0.1',
    description='A blockchain-based LEM simulation',
    author='Niklas R.',
    package_dir={"": "src"},
)
