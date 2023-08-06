# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macro_counter',
 'macro_counter.adapters',
 'macro_counter.app',
 'macro_counter.core',
 'macro_counter.repositories.components']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=2.1.0,<3.0.0',
 'prompt-toolkit>=3.0.18,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pymongo>=3.11.4,<4.0.0',
 'pyparsing>=2.4.7,<3.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['macro_counter = macro_counter:main']}

setup_kwargs = {
    'name': 'macro-counter',
    'version': '0.2.2',
    'description': 'Python macro nutrient counter.',
    'long_description': "# Macro Counter\n\nConvenient terminal application to keep track of calories/macros with a simple prompt\n\n## Installation\n\nMacro counter can be installed from test PyPI using a little bit customized `pip` command:\n\n```\npip3 install --upgrade -i https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple macro_counter\n```\n\n## Usage\n\n### CLI\n\n**Register a component**\n\n```\n>>> register tomato_100gr\nRegistering tomato_100gr\nType (L)iquid/(S)olid: Solid\nType units (100.0) :\nHow much Calories : 18\nHow much Protein : 0.9\nHow much Carb : 3.9\nHow much Fiber : 1.2\nHow much Sugar : 2.6\nHow much Fat : 0.2\nHow much Saturated fat :\nHow much Mono insaturated fat :\nHow much Poly insaturated fat : 0.1\nHow much Trans fat :\nCreated: tomato_100gr\n>>> register coco_milk_100ml\nRegistering coco_milk_100ml\nType (L)iquid/(S)olid: Liquid\nType units (100.0) :\nHow much Calories : 185\nHow much Protein : 1.6\nHow much Carb : 2\nHow much Fiber :\nHow much Sugar : 2\nHow much Fat : 19\nHow much Saturated fat : 17\nHow much Mono insaturated fat :\nHow much Poly insaturated fat :\nHow much Trans fat :\nCreated: coco_milk_100ml\n```\n\n**Checking component infos**\n\n```\n>>> tomato_100gr\n----------------------  --------  -----\nCalories                18.0\nUnits                   100.0 gr\nProtein                 0.9       18.0%\nCarb                    3.9       78.0%\nFiber                   1.2\n- Sugar                 2.6       52.0%\nFat                     0.2       4.0%\n- Poly insaturated fat  0.1       2.0%\n----------------------  --------  -----\n>>> coco_milk_100ml\n---------------  --------  -----\nCalories         185.0\nUnits            100.0 ml\nProtein          1.6       7.1%\nCarb             2.0       8.8%\n- Sugar          2.0       8.8%\nFat              19.0      84.1%\n- Saturated fat  17.0      75.2%\n---------------  --------  -----\n```\n\n**Multiplying operations**\n\nTo check the nutritional facts of 2 liters of Coco milk.\n\n```\n>>> coco_milk_100ml * 20\n---------------  ---------  -----\nCalories         3700.0\nUnits            2000.0 ml\nProtein          32.0       7.1%\nCarb             40.0       8.8%\n- Sugar          40.0       8.8%\nFat              380.0      84.1%\n- Saturated fat  340.0      75.2%\n---------------  ---------  -----\n```\n\nTo check the nutritional facts of 2 liters of Coco milk using normalizing-to-one operation.\n\n```\n>>> coco_milk_100ml % 2000\n---------------  ---------  -----\nCalories         3700.0\nUnits            2000.0 ml\nProtein          32.0       7.1%\nCarb             40.0       8.8%\n- Sugar          40.0       8.8%\nFat              380.0      84.1%\n- Saturated fat  340.0      75.2%\n---------------  ---------  -----\n```\n\n**Adding operations**\n\n```\n>>> tomato_100gr + coco_milk_100ml\n----------------------  --------  -----\nCalories                203.0\nUnits                   200.0 gr\nProtein                 2.5       9.1%\nCarb                    5.9       21.4%\nFiber                   1.2\n- Sugar                 4.6       16.7%\nFat                     19.2      69.6%\n- Saturated fat         17.0      61.6%\n- Poly insaturated fat  0.1       0.4%\n----------------------  --------  -----\n```\n\n**Updating existing components**\n\nYou can remove actual fields using 'r' or 'reset' keyword.\n\n```\n>>> register tomato_100gr\nUpdating tomato_100gr\nType (L)iquid/(S)olid (Solid) :\nType units (100.0) :\nHow much Calories (18.0/Reset):\nHow much Protein (0.9/Reset):\nHow much Carb (3.9/Reset):\nHow much Fiber (1.2/Reset):\nHow much Sugar (2.6/Reset):\nHow much Fat (0.2/Reset):\nHow much Saturated fat :\nHow much Mono insaturated fat :\nHow much Poly insaturated fat (0.1/Reset):\nHow much Trans fat :\nNothing changed\n```\n\n**Assign a single component**\n\nYou can also update the unit field, for example cooked chicken won't be as heavy as the raw one, but will still contains the macros.\n\n```\n>>> chicken_cooked = chicken_raw\nType (L)iquid/(S)olid (Solid) :\nType units (200.0) : 160\nCreated: chicken_cooked\n```\n\n**Assign a recipe**\n\nWeight the product at the end of the recipe to fine tune further macro counting, corresponding to weight gain according to cooking, evaporating water, ect...\n\n```\n>>> tiramisu = eggs * 4 + almond_flour % 66 + mascarpone % 500 + erythritol * 66 * 22 + fresh_cream % 200\nType (L)iquid/(S)olid (Solid) :\nType units (1000.0) : 900\nCreated: tiramisu\n```\n\n**Delete a component**\n\n```\n>>> delete tomato\nComponent tomato deleted\n```\n\n**Display components details**\n\nThis will display each components data with their percentages over all the other.\n\n```\n>>> detail tomato_100gr + coco_milk_100ml\nName             Units    Cal    Prot    Carb    Fiber    Sugar    Fat    Sat     Poly\n---------------  -------  -----  ------  ------  -------  -------  -----  ------  ------\ntomato_100gr     100.0gr  18.0   0.9     3.9     1.2      2.6      0.2            0.1\n                 50.0%    8.9%   36.0%   66.1%   100.0%   56.5%    1.0%           100.0%\ncoco_milk_100ml  100.0ml  185.0  1.6     2.0              2.0      19.0   17.0\n                 50.0%    91.1%  64.0%   33.9%            43.5%    99.0%  100.0%\n\nTotal            200.0    203.0  2.5     5.9     1.2      4.6      19.2   17.0    0.1\n```\n",
    'author': 'Laurent Arthur',
    'author_email': 'laurent.arthur75@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ludwig778/macro_counter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
