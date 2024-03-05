from setuptools import setup, find_packages

setup(
    name='ena-CLI',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'pandas',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'ena-CLI = ena_CLI.__main__:main',
        ],
    },
    author='Khadim GUEYE',
    author_email='gueye.kgy@gmail.com',
    description='This script facilitates the submission of projects, samples, runs, assemblies, and other analyses to the public repository ENA (European Nucleotide Archive). It also assists in validating AMR (Antimicrobial Resistance) antibiograms before submission.',
    url='https://github.com/KhadimGueyeKGY/ena-CLI',
)
