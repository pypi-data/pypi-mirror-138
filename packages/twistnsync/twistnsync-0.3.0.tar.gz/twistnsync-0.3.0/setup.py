# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twistnsync']

package_data = \
{'': ['*']}

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.16.0,<0.17.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'twistnsync',
    'version': '0.3.0',
    'description': 'Twist-n-Sync is time synchronization algorithm that employs IMU gyroscope data.',
    'long_description': '# Twist-n-Sync. Time synchronization algorithm that employs IMU gyroscope data\n\nImagine that you want to synchronize [two smartphones](https://www.mdpi.com/1424-8220/21/1/68)<sup>1</sup> for stereoscopic (or multiscopic) photo or video shutting with _microseconds accuracy and precision_.\nOr you need to synchronize Azure Kinect DK [depth frames](https://arxiv.org/abs/2111.03552)<sup>2</sup> with smartphone frames.\n\nTwist-n-Sync is a time synchronization algorithm that can solve the time sync issues by employing gyroscope chips widely available in millions of comsumer gadgets.\n\nAnother benefical usage of the package is synchronization of diverse motion capture (mocap) systems (OptiTrack, Vicon) that provide ground truth data for robot navigation and state estimation algorithms (Wheeled, Visual, Visual-Inertial Odometry and SLAM).\n\n## Installation\n\n`pip install twistnsync`\n\n## Usage examples\n\nWIP: The python notebook examples in [`examples`](https://github.com/MobileRoboticsSkoltech/twistnsync-python/examples) folder provide comprehensive mini-tutorials how to use the code:\n- [two systems sync by gyroscope data](https://github.com/MobileRoboticsSkoltech/twistnsync-python/blob/master/examples/Smartphone_and_MCU-board_data_sync.ipynb);\n- TODO mocap data (position orientation) and robot data sync;\n- TODO clock drift evaluation of two independent systems;\n\n## References\nIn case of usage of the materials, please, refer to the source and/or publications:\n\n<sup>1</sup>\n```\n@article{faizullin2021twist,\n  title={Twist-n-Sync: Software Clock Synchronization with Microseconds Accuracy Using MEMS-Gyroscopes},\n  author={Faizullin, Marsel and Kornilova, Anastasiia and Akhmetyanov, Azat and Ferrer, Gonzalo},\n  journal={Sensors},\n  volume={21},\n  number={1},\n  pages={68},\n  year={2021},\n  publisher={Multidisciplinary Digital Publishing Institute}\n}\n```\n\n<sup>2</sup>\n```\n@ARTICLE{9709778,\n  author={Faizullin, Marsel and Kornilova, Anastasiia and Akhmetyanov, Azat and Pakulev, Konstantin and Sadkov, Andrey and Ferrer, Gonzalo},\n  journal={IEEE Sensors Journal}, \n  title={SmartDepthSync: Open Source Synchronized Video Recording System of Smartphone RGB and Depth Camera Range Image Frames with Sub-millisecond Precision}, \n  year={2022},\n  volume={},\n  number={},\n  pages={1-1},\n  doi={10.1109/JSEN.2022.3150973}\n}\n```\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Marsel Faizullin',
    'author_email': 'marsel.faizullin@skoltech.ru',
    'maintainer': 'Marsel Faizullin',
    'maintainer_email': 'marsel.faizullin@skoltech.ru',
    'url': 'https://github.com/MobileRoboticsSkoltech/twistnsync-python',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
