# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_durations']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=4.6']

entry_points = \
{'pytest11': ['pytest-durations = pytest_durations']}

setup_kwargs = {
    'name': 'pytest-durations',
    'version': '1.0.0',
    'description': 'Pytest plugin reporting fixtures and test functions execution time.',
    'long_description': '## Introduction\n\nA pytest plugin to measure fixture and test durations.\n\nIn order to get the pure test setup/teardown durations, plugin subtracts time taken by fixtures which scope is larger than "function".\n\n## Installation\n\n```shell\n$ pip install pytest-durations\n```\n\n## Example or report\n\n```\n============================= fixture duration top =============================\ntotal          name          num avg            min            max           \n0:00:00.063821 fake_reporter   4 0:00:00.015300 0:00:00.014831 0:00:00.018389\n0:00:00.068513   grand total  22 0:00:00.000117 0:00:00.000110 0:00:00.000132\n============================ test call duration top ============================\ntotal          name                          num avg            min            max           \n0:00:00.527693      test_plugin_with_options   4 0:00:00.041085 0:00:00.040256 0:00:00.405267\n0:00:00.041535           test_plugin_disable   1 0:00:00.041535 0:00:00.041535 0:00:00.041535\n0:00:00.018607 test_get_current_ticks_frozen   1 0:00:00.018607 0:00:00.018607 0:00:00.018607\n0:00:00.590297                   grand total  10 0:00:00.000706 0:00:00.000706 0:00:00.000706\n=========================== test setup duration top ============================\ntotal          name                                     num avg            min            max           \n0:00:00.018670                 test_report_measurements   1 0:00:00.018670 0:00:00.018670 0:00:00.018670\n0:00:00.015979 test_report_measurements_with_rows_limit   1 0:00:00.015979 0:00:00.015979 0:00:00.015979\n0:00:00.015100 test_report_measurements_with_time_limit   1 0:00:00.015100 0:00:00.015100 0:00:00.015100\n0:00:00.015079   test_report_measurements_empty_results   1 0:00:00.015079 0:00:00.015079 0:00:00.015079\n0:00:00.005076                 test_plugin_with_options   4 0:00:00.001138 0:00:00.001030 0:00:00.001770\n0:00:00.071377                              grand total  10 0:00:00.015079 0:00:00.015079 0:00:00.015079\n========================== test teardown duration top ==========================\ntotal          name        num avg            min            max           \n0:00:00.001990 grand total  10 0:00:00.000128 0:00:00.000128 0:00:00.000128\n============================== 10 passed in 0.71s ==============================\n```\n\n## Development\n\nProject uses [poetry](https://python-poetry.org/) for dependencies management, [pytest](https://pytest.org/) for testing and [pre-commit](https://pre-commit.com/) for coding standard checks.\n\n```shell\n$ pip install poetry\n$ poetry install\n$ pre-commit install\n$ pytest tests\n```\n\n## Change Log\n\n### 1.0.0 (Feb 14, 2022)\n \n* First Release\n',
    'author': 'Oleg Blednov',
    'author_email': 'oleg.codev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blake-r/pytest-durations',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
