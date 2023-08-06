# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esqa', 'esqa.asserts']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.0,<7.0', 'elasticsearch==7.10.1']

entry_points = \
{'console_scripts': ['esqa = esqa.cli:main']}

setup_kwargs = {
    'name': 'esqa',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Table of Contents\n\n* [Overview](#Overview)\n* [Install](#Install)\n* [Behavior](#Behavior)\n* [Usage](#Usage)\n* [Configurations](#Configurations)\n\n## Overview\n\n**Esqa** automates the checks the qualities of the Elasticsearch indices\nas the unit test frameworks such as RSpec or PyTests. Users add the test cases\ninto the setting files and checks if the target indices is build as expected running the command `esqa`. \n\n## Install\n\n```bash\n$ poetry install\n$ poetry build\n$ pip install dist/esqa-0.0.1.tar.gz\n```\n\n## Behavior\n\nWhen we run Esqa, the following steps are executed. \n\n1. Submit Es query to an Elasticsearch cluster \n2. Get the result ranking from Elasticsearch\n3. Check if the rankings from Es cluter satisfiy the conditions described in configuration file\n\nThe following is the image.\n\n![Esqa overiew](doc/esqa-behavior.png "overivew")\n\n## Usage\n\nEsqa provides the `esqa` command which check if the queries gets the expected search rankings from Elasticsearch indices.\n\nWe run the `esqa` command specifying the configuration file and target index.\n\n```shell\n$ esqa  --config sample_config.json --index document-index --host localhost --port 9200\n```\n\n## Configurations\n\nEsqa has the settings file in which we add the test cases. \nThe test cases consist of two blocks *query* and *validations*.\n*query* is an Elasticsearch query and *validation* is the expected behavior\nwhen we run the defined query to the specified index.\n\nThe following is an example of the setting file of esqa.\nThe setting file means that results from Elasticsearch must satisfy the conditions defined in\n`asserts` block when we run the defined query (searching `engineer` to the `message` field) to the target index.\n\n```json\n{\n  "cases": [\n    {\n      "name": "match query",\n      "query": {\n        "query": {\n          "match": {\n            "message": {\n              "query": "engineer"\n            }\n          }\n        }\n      },\n      "asserts": [\n        {\n          "type": "equal",\n          "rank": 0,\n          "item": {\n            "field": "document_id",\n            "value": "24343"\n          }\n        }\n      ]\n    }\n  ]\n}\n```\n\nWe add all the test cases into `cases` block.\nEach test cases have three elements `name`, `query` and `asserts`.\n`name` is the name of the test case. `query` is the target query which we want to validate.\nWe add a set of expected behaviors to the `asserts` block.  \n\nThe `asserts` block contains the conditions that search results from\nElasticsearch cluster must satisfy. Each condition\ncontains several elements `type`, `rank` and `item`. \n\n| Element | Summary |\n| :--- | :--- |\n| type | condition types (`equal`、`higher`、`lower`） |\n| rank | rank of the specified item |\n| item | item stored in Elasticsearch indices specified in rank element must satisfy |\n\n`item` element specifies the document in Es indices. The item is specified with the field value.\n\n| Element | Summary |\n| :--- | :--- |\n| field | field name |\n| value | value of the field specified in `field` element |\n\n## Templates\n\nSometimes queries in the test cases are almost the same.\nIn such cases, esqa provides *templates* in the configuration files.\n\nTemplate files are JSON file which contains an Elasticsearch query\nwith **variables**.\n\nThe following is an example of template file. As we can see, `query`\nblock contains a variable `${query_str}`. The variables are injected\nfrom the Esqa configuraiton file.\n\n```json\n{\n  "query": {\n    "match": {\n      "message": {\n        "query": "${query_str}"\n      }\n    }\n  }\n}\n```\n\nThe following is a configuration file which specifies the template file.\nTo uses template files in the configuration file, we add `template` element in `query` block.\nThe variables in the specified template file need to be added in the `query` block.\nFor example the configuration file added a variable `query_str` defined in template file.\n\n```json\n{\n  "cases": [\n    {\n      "name": "match identical",\n      "query": {\n        "template": "tests/fixtures/default_template.json",\n        "query_str": "engineer"\n      },\n      "asserts": [\n        {\n          "type": "equal",\n          "rank": 0,\n          "item": {\n            "field": "id",\n            "value": "2324"\n          }\n        }\n      ]\n    }\n  ]\n}\n```',
    'author': 'Takahiko Ito',
    'author_email': 'takahiko.ito@dr-ubie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
