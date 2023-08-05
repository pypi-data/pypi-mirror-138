# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xblobs']

package_data = \
{'': ['*']}

install_requires = \
['dask-image>=0.2.0', 'numpy>=1.22.2', 'scipy>=1.2.0', 'xarray>=0.11.2']

setup_kwargs = {
    'name': 'xblobs',
    'version': '1.0.2',
    'description': 'Python tool to detect and analyse coherent structures in turbulence, powered by xarray.',
    'long_description': "# xblobs\nPython tool to detect and analyse coherent structures in turbulence, powered by xarray. \n\nThe algorithm has been developed originally to detect and track coherent structures (blobs) in plasma turbulence simulations but it can be applied on any 2D xarray Dataset with a cartesian grid and constant spacing `dx`,`dy` and `dt`. An example is shown below:\n\n\n![Density evolution](example_gifs/turbulence_blobs.gif ) \n\n\n## Requirements\n- Python >= 3.5\n- xarray >= 0.11.2\n- scipy >= 1.2.0\n- dask-image >= 0.2.0\n- numpy >= 1.14\n\n## Installation\n\nDev install:\n```\ngit clone https://github.com/gregordecristoforo/xblobs.git\ncd xblobs\npip install -e .\n```\n\n## Usage\nThe algorithm is based on the threshold method, i.e. all structures exceeding a defined threshold are labeled as blobs. In order to track blobs over time they have to spatially overlap in two consecutive frames. \n\nApplying `find_blobs` function on xarray dataset returns the dataset with a new variable called `blob_labels`. The number of blobs is added as an attribute to `blob_labels` as `number_of_blobs`. The parameters of single blobs can then be calculated with the `Blob` class. \n### xstorm\nThe default implementation is done for a xstorm dataset.\n```Python\nfrom xblobs import Blob\nfrom xblobs import find_blobs\nfrom xstorm import open_stormdataset\n\nds = open_stormdataset(inputfilepath='./BOUT.inp')\nds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\n                threshold = 5e18 ,region = 0.0, background = 'flat')\n\nblob1 = Blob(ds,1)\n\n# call blob methods you are interested in\nprint(blob1.lifetime())\n#etc\n```\n### xbout\nFor [BOUT++ simulations](https://github.com/boutproject/BOUT-dev) using [xbout](https://github.com/boutproject/xBOUT) one has to specify the dimensions in addition.\n```Python\nfrom xblobs import Blob\nfrom xblobs import find_blobs\nfrom xbout import open_boutdataset\n\nds = open_boutdataset()\nds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\n                threshold = 1.3 ,region = 0.0, background = 'flat', \n                n_var = 'n', t_dim = 't', rad_dim = 'x', pol_dim = 'z')\n                \nblob1 = Blob(ds,1, n_var = 'n', t_dim = 't', rad_dim = 'x',pol_dim = 'z')\n```\n### generic xarray dataset\nFor a generic xarray dataset adjust the dimensions to your needs, for example:\n```Python\nfrom xblobs import Blob\nfrom xblobs import find_blobs\n\nds = load_your_dataset()\n\nds = find_blobs(da = ds, scale_threshold = 'absolute_value' ,\n                threshold = 1.3 ,region = 0.0, background = 'flat', \n                n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')\n                \nblob1 = Blob(ds,1, n_var = 'density', t_dim = 'time', rad_dim = 'radial', pol_dim = 'poloidal')\n```\n## Input parameters\n### `find_blobs()`\n- `da`: xbout Dataset  \n\n- `threshold`: threshold value expressed in terms of the chosen scale_threshold\n\n- `scale_threshold`: following methods implemented\n  - `absolute_value`: threshold is scalar value\n  - `profile`: threshold is time- and poloidal-average profile\n  - `std`: threshold is standard deviation over all three dimensions\n  - `std_poloidal`: threshold is standard deviation over poloidal dimension\n  - `std_time`: threshold is standard deviation over time dimension\n\n- `region`: blobs are detected in the region with radial indices greater than `region`\n\n- `background`: background that is subtracted. Options:\n  - `profile`: time- and poloidal-averaged background\n  - `flat`: no background subtracted\n\n- `n_var`: xarray variable used for blob tracking\n    \n- `t_dim`: xarray dimension for time\n\n- `rad_dim`: xarray dimension for radial dimension\n\n- `pol_dim`: xarray dimension for poloidal dimension \n\n### `Blob()`\n- `variable`: xbout Dataset containing blob_labels\n- `id`: integer between 0 and number of detected blobs \n  - 0: refers to the background\n  - 1-n: detected blobs  \n- other parameters equivalent to `find_blobs`\n\n\n## Blob methods\nthe following blob parameters are implemented:\n- `t_init`: time when blob is detected \n- `lifetime`: lifetime of blob\n- `com`: center of mass, over time\n- `velocity`: absolute velocity of centre of mass of blob, over time\n- `velocity_x`: radial velocity of centre of mass of blob, over time\n- `velocity_y`: poloidal velocity of centre of mass of blob, over time\n- `amplitude`: maximum of the signal within the blob above background, over time\n- `max_amplitude`: maximum of the signal within the blob above background\n- `mass`: integral of signal in area where background is exceeded, over time\n- `average_mass`: average blob mass\n- `size`: integral of area above background, over time\n\nother blob parameters are straightforward to implement\n\n## Parallelization \nBlob detection is parallelised across any number of dimensions by [`dask-image`](https://docs.dask.org/en/latest/).\n\n## Contact\nIf you have questions, suggestions or other comments you can contact me under gregor.decristoforo@uit.no\n",
    'author': 'gregordecristoforo',
    'author_email': 'gregor.decristoforo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uit-cosmo/xblobs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
