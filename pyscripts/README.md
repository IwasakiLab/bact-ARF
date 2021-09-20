# Python scripts for import

This directory contains useful Python scripts. 
They can be imported from jupyter notebook. (The path to this dirctory is added to `PYTHONPATH` in the jupyter lab docker.)

## layouts

```
pyscripts/
├── config.py                       : Codes to simplify handling of paths. 
├── datasets.py                     : Scripts to download datasets, load them from storage, and manage their metadata.
├── genomeutil.py                   : Snippets useful for genome sequence analysis.
├── iupred2a_data                   : Parameters of IUPred2A* 
│   ├── anchor2_energy_matrix
│   ├── anchor2_interface_comp
│   ├── iupred2_long_energy_matrix
│   ├── iupred2_short_energy_matrix
│   ├── long_histogram
│   └── short_histogram
├── iupred2a_lib_mod.py             : IUPred2A script modified by S. Yamanouchi*
├── README.md                       : This file.
└── visualization.py                : Codes related to visualization.
```

\* Files related to IUPred2A Will not be released due to the IUPred2A license.

