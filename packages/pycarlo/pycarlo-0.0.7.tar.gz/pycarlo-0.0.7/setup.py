import distutils.text_file
from pathlib import Path
from typing import List, Optional

from setuptools import setup, find_packages

__VERSION__ = '0.0.7'


def parse_requirements(file_name: Optional[str] = 'requirements.txt') -> List[str]:
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(file_name))).readlines()


def get_long_description():
    with open('README.md', 'r') as fh:
        return fh.read()


setup(
    name='pycarlo',
    version=__VERSION__,
    license='Apache Software License (Apache 2.0)',
    description='Monte Carlo\'s Python SDK',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Monte Carlo Data, Inc',
    author_email='info@montecarlodata.com',
    url='https://www.montecarlodata.com/',
    packages=find_packages(exclude=['tests*', 'utils*', 'examples*']),
    include_package_data=True,
    install_requires=parse_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.7'
)
