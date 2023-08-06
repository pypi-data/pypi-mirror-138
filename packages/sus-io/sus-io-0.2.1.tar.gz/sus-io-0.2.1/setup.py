# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sus']

package_data = \
{'': ['*']}

install_requires = \
['base36>=0.1.1,<0.2.0',
 'dataclasses-json>=0.5.6,<0.6.0',
 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['test = tests.test:main']}

setup_kwargs = {
    'name': 'sus-io',
    'version': '0.2.1',
    'description': 'A SUS (Sliding Universal Score) parser and generator.',
    'long_description': '# sus-io\n\nA SUS (Sliding Universal Score) parser and generator.\n\n[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n\n## Functionality\n- Parse sus into tick-based objects.\n- Allow json output.\n\n## Usage\n\n### ``sus.loads(data: str)``\n```python\nimport sus\n\nprint(sus.loads("#00002: 4\\n#BPM01: 120\\n#00008: 01"))\n```\n\n### ``sus.load(fp: TextIO)``\n```python\nimport sus\n\nwith open("score.sus", "r") as f:\n    score = sus.load(f)\n    print(score)\n```\n\n### ``Score(...).to_json(...)``, ``Score.from_json(...)``\n```python\nimport sus\nfrom sus import Score\n\nwith open("score.sus", "r") as fi, open("score.json", "w") as fo:\n    score = sus.load(fi)\n    json = score.to_json(indent=4)\n    fo.write(json)\n\n    print(Score.from_json(json))\n```\n\n### ``sus.dump(score: Score)``, ``sus.dumps(score: Score)``\n```python\nimport sus\n\nwith open("score.sus", \'r\') as fi, open(sus_file.with_suffix(\'.dumped.sus\'), \'w\') as fd:\n    score = sus.load(fi)\n    print(sus.dumps(score))\n    sus.dump(score, fd, comment=\'Custom comment.\', space=False)\n```\n\n## Todo\n\n- Acknowledgement\n- Add example I/O\n- Contribution Guide\n- High Speed\n- etc.\n\n## Links\n\n### Javascript\n- [``sus-io (npm)``](https://www.npmjs.com/package/sus-io)\n- [``sus-parse (npm)``](https://www.npmjs.com/package/sus-parse)\n- [``sus-stringify (npm)``](https://www.npmjs.com/package/sus-stringify)\n\n## License\n\nMIT © 2021 mkpoli\n',
    'author': 'mkpoli',
    'author_email': 'mkpoli@mkpo.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkpoli/sus-io#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
