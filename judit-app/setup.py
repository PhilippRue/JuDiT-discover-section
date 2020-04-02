#!/usr/bin/env python

from __future__ import absolute_import
from setuptools import setup

if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically
    setup(packages=["plots_host_system", "plots_overview", "plots_imp_detail"],
          name="judit-discover-section",
          author="Philipp Rüßmann",
          author_email="p.ruessmann@fz-juelich.de",
          description="DISCOVER section for the JuDiT database.",
          license="MIT",
          classifiers=["Programming Language :: Python"],
          version="0.1.0",
          install_requires=[
              "aiida-core~=1.1.1",
              "panel~=0.9.4",
              "tornado==5.1.1",
              "matplotlib==3.2.0",
              "requests~=2.21.0",
              "jupyter",
              "aiida-kkr==1.1.10",
              "ase-notebook==0.3.1",
              "pandas==1.0.1",
          ],
          extras_require={
              "pre-commit":
              ["pre-commit==1.17.0", "prospector==0.12.11", "pylint==1.9.3"]
          })
