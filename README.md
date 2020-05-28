# mskimpact_tp53_exploration
**Exploratory Analysis of the MSK IMPACT Cohort**

***

## Repository structure

## Working with this repository

### Clone the repository
To clone this repository on your local computer please run:
```shell
$ git clone https://github.com/emilecohen/mskimpact_tp53_exploration.git
```

### Step 1 - Setup your Python environment
The second part of the repository was written and tested under `Python 3.6`, working with JupyterNotebook. You can see the requirements under [`requirements.yml`](./requirements.yml). The main Python packages used are:

- `ipython`
- `numpy`
- `matplotlib`
- `seaborn`
- `pandas`

#### Step 2.1 - Setup a python conda-environment on your local computer

We assume you have conda installed on your computer, otherwise please see https://conda.io/docs/index.html (conda documentation) and https://conda.io/docs/_downloads/conda-cheatsheet.pdf (conda cheat sheet). You need to install `jupyter notenook` in your base conda environment if not done yet.

To create the conda-env, please run the following command:
```bash
# create the conda-env and install the appropriate libraries
$ conda env create --name mskimpact_env --file requirements.yml
```

Some useful command lines to work with this conda-env:
```bash
# activate the conda-env
$ source activate mskimpact_env

# deactivate the conda-env
$ source deactivate
```

> :warning: Please always activate the `mskimpact_env` conda-env before running any Python notebook, to make sure you have all the necessary dependencies and the good libraries version:
> ```bash
> # if you use jupyter notebook
> $ source activate mskimpact_env; jupyter notebook
> 
> # if you use jupyter lab
> $ source activate mskimpact_env; jupyter lab
> ```

In any Python Jupyter notebook, importing the file `utils/setup_environment.ipy` automatically checks that you're running the notebook under the `imp-ann_env` conda-env, you can check it yourself by running in the notebook:
```ipython
# prints the current conda-env used
!echo $CONDA_DEFAULT_ENV

# list all the conda-env on your computer, the one you're working on is indicated by a star
!conda env list
```

## Details on the notebooks

All Python notebooks will begin with the following lines, which load a set of custom function designed by us, and load appropriate libraries, it also makes sure that you're working on the `mskimpact_env` that you should have created earlier:
```ipython
%run ../../utils/setup_environment.ipy
```

## Supplementary
