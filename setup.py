# -*- coding: utf-8 -*-
"""Installer for the collective.isotope package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() + '\n' + 'Contributors\n'
    '============\n'
    + '\n'
    + open('CONTRIBUTORS.rst').read()
    + '\n'
    + open('CHANGES.rst').read()
    + '\n'
)


setup(
    name='collective.isotope',
    version='0.1',
    description="Plone view for folders and collections using the Isotope "
                "jquery plugin",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='cewing',
    author_email='cris@crisewing.com',
    url='http://pypi.python.org/pypi/collective.isotope',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.z3cform.datagridfield',
        'plone.api',
        'setuptools',
        'six',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
