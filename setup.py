#!/usr/bin/env python
"""PDDL parser setup file."""

from distutils.core import setup

setup(name='planning',
      version='1.0',
      description='Planning library with PDDL/HDDL Parser',
      author='Charles Lesire',
      author_email='charles.lesire@onera.fr',
      packages=['oara.planning', 'oara.planning.hddl', 'oara.planning.hddl.parser'],
      )
