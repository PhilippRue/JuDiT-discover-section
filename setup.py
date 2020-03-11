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
              "bokeh~=1.3.4",
              "pandas~=0.24.2",
              "requests~=2.21.0",
              "jupyter",
          ],
          extras_require={
              "pre-commit":
              ["pre-commit==1.17.0", "prospector==0.12.11", "pylint==1.9.3"]
          })
