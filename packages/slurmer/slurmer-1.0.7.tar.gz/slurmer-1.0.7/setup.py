# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurmer']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'slurmer',
    'version': '1.0.7',
    'description': 'A package to schedule different tasks in parallel with cluster support.',
    'long_description': '# Slurmer\n\nThis package is designed to run heavy loads in a computer cluster. Supported task schedulers are:\n\n- Running on a single node\n- [SLURM](https://slurm.schedmd.com/documentation.html)\n\nPRs to add more schedulers are welcome.\n\n## Features\n\n- Run multiple tasks in parallel.\n- Run tasks in randomised order but consistently in multiple computing nodes.\n- Consistent pipeline to work with heavy tasks (directory creation, handling errors, postprocessing...)\n\n## Example\n\nYou can find the documentation [here](https://jmigual.github.io/slurmer/). \n\nThe package can be used as follows:\n\n```python\nfrom dataclasses import dataclass\nfrom pathlib import Path\nfrom typing import Iterator\n\nimport slurmer\n\n\n@dataclass\nclass MyTaskParameters(slurmer.TaskParameters):\n    processing_id: int\n\n\n@dataclass\nclass MyTaskResult(slurmer.TaskResult):\n    good_result: bool\n\n\nclass MyTask(slurmer.Task):\n\n    def __init__(self, min_job: int, max_job: int):\n        super().__init__()\n        self.min_job = min_job\n        self.max_job = max_job\n\n    def generate_parameters(self) -> Iterator[MyTaskParameters]:\n        for i in range(self.min_job, self.max_job):\n            yield MyTaskParameters(processing_id=i)\n\n    def make_dirs(self):\n        # Dirs are created before the task is run\n        for i in range(self.min_job, self.max_job):\n            Path(f"out/result_{i}").mkdir(parents=True, exist_ok=True)\n\n    def process_function(self, parameters: MyTaskParameters) -> MyTaskResult:\n        # Run your heavy code here\n        for i in range(parameters.processing_id, parameters.processing_id + 10):\n            print(f"Processing {i}")\n\n        return MyTaskResult(good_result=True)\n\n    def process_output(self, result: MyTaskResult) -> bool:\n        # Postprocess output, this is NOT run in parallel and only handles the tasks run \n        # in the current node. If you want to postprocess everything wait for all the nodes\n        # to finsish computing.\n        #\n        # This function should check whether the output is the "expected" one and return True \n        # if something went wrong.\n        return not result.good_result\n```\n\nThen in your main script:\n```python\n>>> task = MyTask(min_job=1, max_job=10)\n>>> task.execute_tasks()\n```\n',
    'author': 'Joan Marcè i Igual',
    'author_email': 'J.Marce.i.Igual@tue.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jmigual.github.io/slurmer/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
