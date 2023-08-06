# File: setup.py
# Date: 20-Sep-2018
#
# Update:
#
import re

from setuptools import find_packages, setup


thisPackage = 'fakepdftk'
#requires = ['pdfrw']


with open('fakepdftk/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name=thisPackage,
    version=version,
    description='fake replacement for pdfTK to implement watermarks',
    long_description="See:  README.md",
    author='Ezra Peisach',
    author_email='ezra.peisach@rcsb.org',
    url='https://github.com/epeisach/py-fakePDFtk',
    #
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ),
    entry_points={
        'console_scripts': [
            'fakepdftk=fakepdftk.command_line:main',
        ]
    },
    install_requires=['pdfrw'],
    packages=find_packages(exclude=['fakepdftk.tests', 'tests.*']),
    #package_data={
    #    # If any package contains *.md or *.rst ...  files, include them:
    #    '': ['*.md', '*.rst', "*.txt"],
    #},
    #

    #
    test_suite="fakepdftk.tests",
    tests_require=['tox'],
    #
    # Not configured ...
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},
    # Added for
    #command_options={
    #    'build_sphinx': {
    #        'project': ('setup.py', thisPackage),
    #        'version': ('setup.py', version),
    #        'release': ('setup.py', version)
    #    }
    #},
    zip_safe=True,
)
