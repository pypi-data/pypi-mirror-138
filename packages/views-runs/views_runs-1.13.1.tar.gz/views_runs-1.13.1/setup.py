# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['views_runs']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.0.2,<2.0.0',
 'stepshift>=2.2.1,<3.0.0',
 'views-partitioning>=3.0.0,<4.0.0',
 'views-schema>=2.2.0,<3.0.0',
 'viewser>=5.12.0,<6.0.0']

setup_kwargs = {
    'name': 'views-runs',
    'version': '1.13.1',
    'description': 'Tools for doing model runs with views',
    'long_description': '# views-runs \n\nThis package is meant to help views researchers with training models, by\nproviding a common interface for data partitioning and stepshift model\ntraining. It also functions as a central hub package for other classes and\nfunctions used by views researchers, \nincluding [stepshift](https://github.com/prio-data/stepshift) (StepshiftedModels)\nand [views_partitioning](https://github.com/prio-data/views_partitioning) (DataPartitioner).\n\n## Installation\n\nTo install `views-runs`, use pip:\n\n```\npip install views-runs\n```\n\nThis also installs the vendored libraries `stepshift` and `views_partitioning`.\n\n## Usage\n\nThe library offers a class imported at `views_runs.ViewsRun`, that wraps the to\ncentral components of a ViEWS 3 run: A partitioning scheme expressed via a\n`views_partitioning.DataPartitioner` instance, and a stepshifted modelling\nprocess expressed via a `stepshift.views.StepshiftedModels` instance. \nFor documentation on the data partitioner, see \n[views_partitioning](https://www.github.com/prio-data/views_partitioning). For documentation on stepshifted modelling, see \n[views.StepshiftedModels](https://github.com/prio-data/viewser/wiki/Stepshift).\n\n\nThe wrapper takes care of applying these two classes to your data, in order to\nproduce predictions in a familiar and predictable format, as well as ensuring\nthat there is no overlap between training and testing partitions.\nInstantiating a run requires instances of both of these classes, like so:\n\n```\nrun = ViewsRun(\n   DataPartitioner({"A":{"train":(1,100),"test":(101,200)}}),\n   StepshiftedModels(LogisticRegression,[1,2,3,4,5,6],"my_dependent_variable"),\n)\n```\n\nThis instance can then be applied to a [time-unit indexed\ndataframe](https://github.com/prio-data/viewser/wiki/DataConventions#time-unit-indexed-pandas-dataframes)\nto train the models, and produce predictions for the timespans defined in the data partitioner:\n\n```\nrun.fit("A","train",dataframe)\npredictions = run.predict("A","test",dataframe)\n```\n\n## Examples\n\nThere are notebooks that show various workflows with `views_runs` and the\nvendored libraries:\n\n* [BasicExample.ipynb](examples/BasicExample.ipynb)\n',
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/prio-data/views_runs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
