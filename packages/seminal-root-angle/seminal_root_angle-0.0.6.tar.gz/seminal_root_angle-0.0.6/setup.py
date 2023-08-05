from setuptools import setup
from pathlib import Path

current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

setup(
  name = 'seminal_root_angle',
  packages = ['seminal_root_angle'],
  version = '0.0.6',
  license = 'GPLv3', 
  description = 'Extract seminal root angle from rhizobox images',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'Abraham George Smith',
  author_email = 'abe@abesmith.co.uk',
  url = 'https://github.com/Abe404/seminal_root_angle',
  download_url = 'https://github.com/Abe404/seminal_root_angle/archive/refs/tags/0.0.6.tar.gz',
  keywords = ['ROOT', 'ANGLE', 'PHENOTYPING'],
  install_requires=[
      "numpy ==1.22.2",
      "scikit-image ==0.19.1",
      "humanize ==3.14.0",
      "matplotlib ==3.5.1"
  ],
  classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent'
  ]
)
