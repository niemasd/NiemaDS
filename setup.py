"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='niemads',  # Required
    version='1.0.16',  # Required
    description='NiemaDS: Non-standard data structures for Python 3',  # Required
    long_description='NiemaDS is a Python library that implements useful non-standard data structures.',  # Optional
    long_description_content_type='text/plain',  # Optional (see note above)
    url='https://github.com/niemasd/NiemaDS',  # Optional
    author='Niema Moshiri',  # Optional
    author_email='niemamoshiri@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    keywords='data structures fast',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    extras_require={  # Optional
        'dev': ['check-manifest'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/niemasd/NiemaDS/issues',
        'Source': 'https://github.com/niemasd/NiemaDS',
    },
)
