# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nsdpy']
install_requires = \
['certifi>=2020.12.5,<2021.0.0',
 'chardet>=4.0.0,<5.0.0',
 'idna>=2.10,<3.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['nsdpy = nsdpy:main']}

setup_kwargs = {
    'name': 'nsdpy',
    'version': '0.2.0',
    'description': 'Automatize the download of DNA sequences from NCBI, sort them according to their taxonomy and filter them with a gene name (provided as a regular expression)',
    'long_description': '# nsdpy\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![pypi](https://img.shields.io/pypi/v/nsdpy)](https://pypi.org/project/nsdpy/)\n\n\n\n- [Introduction](#introduction)\n- [Workfolw](#workflow)\n- [Quick start](#quick-start)\n- [Usage](#usage)\n  - [Google Colab](#google-colab)\n  - [Command line](#command-line)\n- [Authors and acknowledgment](#authors-and-acknowledgment)\n- [Support](#support)\n- [Licence](#license)\n- [More Documentation](#more-documentation)\n\n## Introduction\n\nnsdpy (nucleotide or NCBI sequence downloader) aims to ease the download and sort of big bacth of DNA sequences from the NCBI database. \nIt can also be usefull to filter the sequences based on their annotations.\nUsing nsdpy the user can:\n\n- **Search** NCBI nucleotide database\n- **Download** the fasta files or the cds_fasta files corresponding to the result of the search\n- **Sort** the sequences based on their taxonomy\n- **Select** coding sequences from cds files based on the gene names using one or more regular expressions. \nThis can help the user retrieve some sequences for which the gene name is annotated in another field.\n- **Retrieve** the taxonomic information and add it to the output sequences.  \n\n## Quick start\n\n- Clone the repo from Github: \n```bash \ngit clone https://github.com/RaphaelHebert/nsdpy.git\n  ```\n- pip:  \n_depending on the user environment pip may be replaced by pip3 if pip3 is used_\n```bash \npip install nsdpy\n```  \n*minimum python version for nsdpy: 3.8.2* \n\n- Google Colab: save a copy of [this notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing) in your drive.\n\n## Workflow\n\n<img src="https://docs.google.com/drawings/d/e/2PACX-1vRD4h7l0S57op_4j-5xsz8iv1j1XBliw-jEdtnWOIq-JAU2l8kSV6d1NmkHd5Q4zhUmZCA3SHUSuHJw/pub?w=801&amp;h=744" width="600" />\n\n## Usage\n### Google colab\n\n[nsdpy colab notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing)\n\n### Command line\n\n```bash\nnsdpy -r "USER\'S REQUEST" [OPTIONS] \n```\n\n## Authors and acknowledgment  \n\n[Raphael Hebert](https://github.com/RaphaelHebert)\n\n## Support\n\n## License\n\nCode and documentation copyright 2021 the nsdpy Authors. Code released under the MIT License.\n\n## More Documentation\n\nOfficial documentation:  \n[Readthedocs](https://nsdpy.readthedocs.io/en/latest/main.html#overview)\n  \n\n\n\n',
    'author': 'RaphaelHebert',
    'author_email': 'raphaelhebert18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RaphaelHebert/nsdpy',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
