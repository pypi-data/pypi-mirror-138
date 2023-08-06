# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapa']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'geojson>=2.5.0,<3.0.0',
 'haversine>=2.5.1,<3.0.0',
 'ipyleaflet>=0.15.0,<0.16.0',
 'notebook>=6.4.8,<7.0.0',
 'numba>=0.55.1,<0.56.0',
 'numpy-stl>=2.16.3,<3.0.0',
 'numpy>=1.21,<2.0',
 'pystac-client>=0.3.2,<0.4.0',
 'rasterio>=1.2.10,<2.0.0']

entry_points = \
{'console_scripts': ['dem2stl = mapa.cli:dem2stl', 'mapa = mapa.cli:mapa']}

setup_kwargs = {
    'name': 'mapa',
    'version': '0.4.0',
    'description': '🌍 Create 3d-printable STLs from satellite elevation data 🌏',
    'long_description': '# mapa 🌍\n\n[![PyPI](https://badge.fury.io/py/mapa.svg)](https://badge.fury.io/py/mapa)\n[![Python](https://img.shields.io/pypi/pyversions/mapa.svg?style=plastic)](https://badge.fury.io/py/mapa)\n[![Downloads](https://pepy.tech/badge/mapa/month)](https://pepy.tech/project/mapa)\n[![Python Tests](https://github.com/fgebhart/mapa/actions/workflows/test.yml/badge.svg)](https://github.com/fgebhart/mapa/actions/workflows/test.yml)\n\n`mapa` let\'s you create 3d-printable [STL](https://en.wikipedia.org/wiki/STL_(file_format)) files from satellite\nelevation data (using [DEM](https://en.wikipedia.org/wiki/Digital_elevation_model) data).\n\nUnder the hood `mapa` uses:\n* [numpy](https://numpy.org/) and [numba](https://numba.pydata.org/) to crunch large amounts of data in little time\n* [ALOS DEM](https://planetarycomputer.microsoft.com/dataset/alos-dem) satellite data (max resolution of 30m) provided by\n  [Planetary Computer](https://planetarycomputer.microsoft.com/)\n\n\n## Installation\n```\npip install mapa\n```\n\n## Usage\n`mapa` provides the following approaches for creating STL files:\n\n### 1. Using the `mapa` interactive map\nThe easiest way is using the `mapa` cli. Simply type\n```\nmapa\n```\nA [jupyter notebook](https://jupyter.org/) will be started with an interactive map. Follow the described steps by\nexecuting the cells to create a 3d model of whatever place you like.\n\n Choose bounding box    | Create STL file\n:-------------------------:|:-------------------------:\n![](https://i.imgur.com/76hcx9N.jpg)  |  ![](https://i.imgur.com/llvxlrk.png)\n\n Slice STL file         | 3D print\n:-------------------------:|:-------------------------:\n![](https://i.imgur.com/AKSRHbK.jpg)  |  ![](https://i.imgur.com/WQn9nwY.png)\n\n### 2. Using the dem2stl cli\nThe `dem2stl` cli lets you create a 3d-printable STL file based on your tiff file. You can run a demo computation to get\na feeling of how the output STL will look like:\n```\ndem2stl demo\n```\nIf you have your tiff file ready, you may run something like\n```\ndem2stl --input your_file.tiff --output output.stl --model-size 200 --z-offset 3.0 --z-scale 1.5\n```\nThe full list of options and their intention can be found with `dem2stl --help`:\n```\nUsage: dem2stl [OPTIONS]\n\n  🌍 Convert DEM data into STL files 🌏\n\nOptions:\n  --input TEXT                Path to input TIFF file.\n  --output TEXT               Path to output STL file.\n  --as-ascii                  Save output STL as ascii file. If not provided,\n                              output file will be binary.\n  --model-size INTEGER        Desired size of the generated 3d model in\n                              millimeter.\n  --max-res                   Whether maximum resolution should be used. Note,\n                              that this flag potentially increases compute\n                              time dramatically. The default behavior (i.e.\n                              max_res=False) should return 3d models with\n                              sufficient resolution, while the output stl file\n                              should be < ~400 MB.\n  --z-offset FLOAT            Offset distance in millimeter to be put below\n                              the 3d model. Defaults to 4.0. Is not influenced\n                              by z-scale.\n  --z-scale FLOAT             Value to be multiplied to the z-axis elevation\n                              data to scale up the height of the model.\n                              Defaults to 1.0.\n  --demo                      Converts a demo tif of Hawaii into a STL file.\n  --cut-to-format-ratio TEXT  Cut the input tiff file to a specified format.\n                              Set to `1` if you want the output model to be\n                              squared. Set to `0.5` if you want one side to be\n                              half the length of the other side. Omit this\n                              flag to keep the input format. This option is\n                              particularly useful when an exact output format\n                              ratio is required for example when planning to\n                              put the 3d printed model into a picture frame.\n                              Using this option will always try to cut the\n                              shorter side of the input tiff.\n  --version                   Show the version and exit.\n  --help                      Show this message and exit.\n```\n\n### 3. Using `mapa` as python library\nIn case you are building your own application you can simply use `mapa`\'s functionality as a within your application by importing the modules functions.\n```python\nfrom mapa import convert_tiff_to_stl\n\npath_to_stl = convert_tiff_to_stl(\n    input_file: "path/to/your/input_file.tiff",\n    as_ascii: False,\n    model_size: 200,\n    output_file: "path/to/your/output_file.stl",\n    max_res: False,\n    z_offset: 3.0,\n    z_scale: 1.5,\n    cut_to_format_ratio: None,\n)\n```\n\n## Changelog\n\nSee [Releases](https://github.com/fgebhart/mapa/releases).\n\n\n## Contributing\n\nContributions, feedback or issues are welcome.\n',
    'author': 'Fabian Gebhart',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fgebhart/mapa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
