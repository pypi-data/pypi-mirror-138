# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fretlabel']

package_data = \
{'': ['*'], 'fretlabel': ['UI/*', 'demo/*', 'dyes/*', 'skripts/*']}

install_requires = \
['biopandas>=0.2.9,<0.3.0', 'numpy>=1.21.4,<2.0.0', 'pandas>=1.3.5,<2.0.0']

entry_points = \
{'console_scripts': ['continue_run = fretlabel.console:continue_run',
                     'fretlabel = fretlabel.console:fretlabel',
                     'multi_run = fretlabel.console:multi_run',
                     'resp_fit = fretlabel.console:resp_fit',
                     'single_run = fretlabel.console:single_run',
                     'solvate = fretlabel.console:solvate']}

setup_kwargs = {
    'name': 'fretlabel',
    'version': '0.2.0',
    'description': 'PyMOL plugin to interactively label nucleic acids with fluorophores in silico',
    'long_description': '[![Docs Status](https://github.com/fdsteffen/fretlabel/workflows/FRETlabel%20docs/badge.svg)](https://github.com/fdsteffen/fretlabel/actions)\n[![PyPI](https://img.shields.io/pypi/v/fretlabel)](https://pypi.org/project/fretlabel/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<img src="https://raw.githubusercontent.com/fdsteffen/fretlabel/master/docs/images/fretlabel_banner.png" width=750px>\n\n*FRETlabel* is a **PyMOL plugin** to label nucleic acids with explicit fluorescent dyes. It aims to facilitate the workflow of setting up, running and evaluating **molecular dynamics simulations with explicit organic fluorophores** for *in silico* FRET calculations.\n\nSpecifically, *FRETlabel* includes the following features:\n- **PyMOL plugin for fluorescent labeling**: Label your nucleic acid of interest with the click of a button. The PyMOL plugin extends the AMBERDYES package (Graen et al. *JCTC* 2014) geometries and force field parameters of common nucleic acid linker chemistries.\n- **Build new fragments interactively**: Tutorials guide you step-by-step through the process of creating new base, linker and dye fragments by integrating with established pipelines for topology generation such as *Antechamber* and *Acpype*.\n- **FRET prediction**: Calculate FRET distributions from MD simulation with all-atom organic dyes. *FRETlabel* integrates with *FRETraj* to compute photon bursts based on distance *R*<sub>DA</sub>(*t*) and orientation trajectories *κ*<sup>2</sup>(*t*) of the fluorophores. \n\n<img src="https://raw.githubusercontent.com/fdsteffen/fretlabel/master/docs/images/graphical_abstract.png" width=700px>\n\n**Fig.** Schematic of *FRETlabel*: (i) A fluorescent dye (here Cy3) is coupled to a nucleic acid via a PyMOL plugin. (ii) An existing force field (e.g. AMBERDYES) is patched with parameters for linker fragments to enable MD simulations with explicit fluorophores (dots represent the spatial distribution of the dye).\n\n\n## Installation and Documentation\nFollow the instructions for your platform [here](https://rna-fretools.github.io/fretlabel/getting_started/installation)\n\n\n## FRETlabel and FRETraj\n*FRETlabel* attaches explicit fluorophores on a custom nucleic acid. If you instead like to use an implicit, geometrical dye model that relies on **accessible-contact volumes (ACV)** then have a look our sister project [*FRETraj*](https://rna-fretools.github.io/fretraj/intro.html) (Steffen, *Bioinformatics*, 2021)\n\n\n## References\nIf you use *FRETlabel* in your work please refer to the following paper:\n\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Phys. Chem. Chem. Phys.* **2016**, *18*, 29045-29055. [![](https://img.shields.io/badge/DOI-10.1039/C6CP04277E-blue.svg)](https://doi.org/10.1039/C6CP04277E)\n\n\n### Additional readings\n- T. Graen, M. Hoefling, H. Grubmüller, *J. Chem. Theory Comput.* **2014**, *10*, 5505-5512.\n- B. Schepers, H. Gohlke, *J. Chem. Phys.* **2020**, *152*, 221103.\n- R. Shaw, T. Johnston-Wood, B. Ambrose, T. D. Craggs, and J. G. Hill, *J. Chem. Theory Comput.*, **2020**, *16*, 7817–7824.\n- M. Zhao, F.D. Steffen R. Börner, M. Schaffer, R.K.O. Sigel, E. Freisinger, *Nucleic Acids Res.* **2018**, *46*, e13.\n- F.D. Steffen, R. Börner, E. Freisinger, R.K.O. Sigel, *CHIMIA* **2019**, *73*, 257-261.\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Bioinformatics* **2021**, *37*, 3953–3955.\n\n----\n\n<sup><a name="pymol">1</a></sup> PyMOL is a trademark of Schrödinger, LLC.\n',
    'author': 'Fabio Steffen',
    'author_email': 'fabio.steffen@chem.uzh.ch',
    'maintainer': 'Fabio Steffen',
    'maintainer_email': 'fabio.steffen@chem.uzh.ch',
    'url': 'https://rna-fretools.github.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
