# mopa
Library for interactive multi-objective power amplifier design

# I. Installation
A virtual environment manager is recommended. This example will use miniconda.
1. Download [miniconda](https://docs.conda.io/en/latest/miniconda.html) and ensure you can activate it from your terminal by running `$ conda activate` 
2. Create an environment for mopa by running `$ conda create --name mopa_env python=3.9`
3. Activate the environment using `$ conda activate mopa_env`
4. Install the test verson of mopa using `$ pip install -i https://test.pypi.org/simple/ mopa==0.2.2`
5. To check that installation is successful `$ pip show mopa`

# II. Dashboard
mopa now includes the ability to be used as an interactive dashboard!
1. Activate the mopa environment using `$ conda activate mopa_env`
2. Run python on the command line by running `$ python`
3. Import mopa `>>> import mopa`
4. Create a dashboard `>>> app = mopa.app.create_dashboard()`
5. Run the dashboard `>>> app.run_server()`

# III. Contents
```
mopa
│   .gitattributes
│   .gitignore
│   config.ini
│   environment.yml: Conda environment
│   LICENSE
│   pyproject.toml
│   README.md
│   setup.cfg
│   setup.py
│
├───.github: Continuous integration
│   └───workflows
│           python-package-conda.yml
│
├───examples: Examples for using mopa
│   │   create_dashboard.py: Creating a dashboard
│   │   example_multi_device.py: Comparing multiple devices
│   │   example_single_device.py: Comparing a single device
│   │
│   └───io: Pre-computed inputs and outputs
│       ├───awr_runs
│       │       PAE_Qorvo_Sample_Data.txt
│       │       PAE_WIN_Sample_Data.txt
│       │       Pout_Qorvo_Sample_Data.txt
│       │       Pout_WIN_Sample_Data.txt
│       │
│       └───figures
│               multi_nondom.html
│               multi_robustness_metrics.html
│               single_nondom.html
│               single_objectives_only.html
│               single_robustness_metrics.html
│
└───src: Source code
    └───mopa
            analysis.py: Analysis code
            analysis_testing.py: Testing for analysis
            app.py: Dash app
            viz.py: Visualization
            __init__.py: Initialization
```
