# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hurdle']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'hurdle',
    'version': '1.0.0',
    'description': 'Scikit hurdle estimator',
    'long_description': '\n# Hurdle\n\n![tests status](https://github.com/prio-data/cc_backend_lib/actions/workflows/test.yml/badge.svg)\n\nThis package contains an implementation of Hurdle Regression, based in part on\n[Geoff Ruddocks implementation](https://geoffruddock.com/building-a-hurdle-regression-estimator-in-scikit-learn/)\nand Håvard Hegres 2022 adaption of his implementation.\n\n## Usage\n\n```\nfrom hurdle import HurdleEstimator\nfrom sklearn import linear_model\n\nest = HurdleEstimator(linear_model.LogisticRegression(), linear_model.LinearModel())\n\nest.fit(...)\n```\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/prio-data/hurdle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
