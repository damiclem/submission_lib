# submission-lib
Scheduling libraries for submission server @BioCompUP

## Requirements
- Slurm or SGE installed
- ``libslurm-dev`` library for Slurm or ``gridengine-dev`` for SGE, both downloadable with apt
- ``libdrmaa`` C bindings for Slurm or SGE
- ``drmaa-python`` python library (from pip or conda)

## ENV variables
Set the env variables for the drmaa-python library. With PyCharm you can set this env variables in the run configuration.

### SGE
```shell
export SGE_ROOT=/path/to/gridengine
export SGE_CELL=default
```
### SLURM
Set the path to the libdrmaa library C binding
```shell
export DRMAA_LIBRARY_PATH=/usr/lib/slurm-drmaa/libdrmaa.so
```
