#!/usr/bin/env python

from distutils.core import setup


# Requirements.
setup_requires = []

install_requires = []


setup(name='Kraken',
      version='1.1.0',
      description='Kraken Rigging Framework',
      author='Eric Thivierge, Phil Taylor',
      author_email='ethivierge@gmail.com',
      url='http://fabric-engine.github.io/Kraken//',
      license='BSD 3-clause "New" or "Revised" License',
      packages = ['kraken'],
      package_dir = {'': 'Python'},
      setup_requires = setup_requires,
      install_requires = install_requires,
     )