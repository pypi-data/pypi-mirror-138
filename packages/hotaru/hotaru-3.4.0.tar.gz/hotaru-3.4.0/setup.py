# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hotaru',
 'hotaru.console',
 'hotaru.footprint',
 'hotaru.image',
 'hotaru.image.filter',
 'hotaru.optimizer',
 'hotaru.train',
 'hotaru.util']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8,<0.9',
 'matplotlib>=3.5,<4.0',
 'scipy>=1.8,<1.9',
 'tensorflow-addons>=0.15.0,<0.16.0',
 'tensorflow>=2.6.1,<2.8',
 'tifffile>=2022,<2023',
 'tqdm>=4.62,<5.0']

entry_points = \
{'console_scripts': ['hotaru = hotaru.console:main']}

setup_kwargs = {
    'name': 'hotaru',
    'version': '3.4.0',
    'description': 'High performance Optimizer to extract spike Timing And cell location from calcium imaging data via lineaR impUlse',
    'long_description': '# HOTARU\n\nHigh performance Optimizer to extract spike Timing And cell location from calcium imaging data via lineaR impUlse\n\n### Author\nTAKEKAWA Takashi <takekawa@tk2lab.org>\n\n### Reference\n- Takekawa., T, et. al.,\n  Automatic sorting system for large scale calcium imaging data, bioRxiv (2017).\n  https://doi.org/10.1101/215145\n\n\n## Install\n\n### Require\n- python >= 3.8\n- tensorflow >= 2.6.1\n\n### Install Procedure (using venv)\n- Create venv environment for hotaru\n  - `python3.x -m venv hotaru`\n- Activate hotaru environment\n  - `source hotaru/bin/activate`\n- Install hotaru\n  - `pip install hotaru`\n\n\n## Usage\n\n### Apply Method\n- (in hotaru venv)\n- `mkdir work`\n- `cd work`\n- `cp somewhere/TARGET.tif imgs.tif`\n- `hotaru config`\n- `hotaru run`\n- (see outs directory)\n\n### Config Option\n- Set sampling rate of movie  \n  `hotaru config --hz 20.0`\n- Set mask file (tif or npy)  \n  `hotaru config --mask-type mask.tif`\n- Set calcium dynamics  \n  `hotaru config --tau-rise 0.08 --tau-fall 0.16`\n- Set cell size candidate  \n  `hotaru config --radius-type log --radius "2.0,40.0,13"`  \n  `hotaru config --radius-type linear --radius "2.0,11.0,10"`  \n  `hotaru config --radius-type manual --radius "2,3,4,5,6,7,8,9,10"`    \n  \n### Check Resutls\n- (in hotaru venv and in work dir)\n- `tensorboard --logidr logs`\n- open in web browser `http://localhost:6006`\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tk2lab/HOTARU',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
