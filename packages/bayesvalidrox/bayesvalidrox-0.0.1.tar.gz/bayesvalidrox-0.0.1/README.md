# BayesValidRox

An open-source, object-oriented Python package for surrogate-assisted Bayesain Validation of computational models.
This framework provides an automated workflow for surrogate-based sensitivity analysis, Bayesian calibration, and validation of computational models with a modular structure.

## Authors
- [@farid](https://git.iws.uni-stuttgart.de/farid)

## Installation
Install my project with pip
```bash
  pip install bayesvalidrox
```
## Features
* Surrogate modeling with Polynomial Chaos Expansion
* Global sensitivity analysis using Sobol Indices
* Bayesian calibration with MCMC using `emcee` package
* Bayesian validation with model weights for multi-model setting

## Requirements
* numpy==1.22.1
* pandas==1.2.4
* joblib==1.0.1
* matplotlib==3.4.2
* seaborn==0.11.1
* scikit-learn==0.24.2
* tqdm==4.61.1
* chaospy==4.3.3
* emcee==3.0.2
* tables==3.6.1
* corner==2.2.1
* h5py==3.2.1
