=========
Changelog
=========

Ideas for futur features
------------------------

- add workflow and Excel Input Interface version updater (update vppopt.json)
- packaging vppopt with the help of `Cookiecutter template <https://github.com/audreyfeldroy/cookiecutter-pypackage>`_
- evaluate ``script_only`` argument for sub-command ``vppopt run``
- add ``out_dir`` argument for ``vppopt run`` sub-command
- add ``es_graph`` option for ``vppopt run`` sub-command with automatic assign node color
- create customized constraints
- modify objective function
- import json-format input
- initialize external python script snippet
- evaluate the way to feed in timeseries data for consumption and production profiles
- `multi-objective optimization <https://stackoverflow.com/questions/50742999/multi-objective-optimization-example-pyomo>`_
- `Effective implementation of the epsilon-constraint method in Multi-Objective Mathematical Programming problems <https://www.sciencedirect.com/science/article/abs/pii/S0096300309002574>`_

v2021.01 
--------

- first release
- command line interface for
    - initializing a vppopt project ``vppopt init -pdir /path/for/project/directory`` using ``oemof.solph`` package
    - runing a vppopt project ``vppopt run -wf <workflow_json_file.json>``
- basic run with an Excel input interface, e.g. vppopt.xlsx
- advanced run with python (user) external scripts
- different types of python external script could be used
    - external script for modifying nodes, energy system or optimization model
    - external script for post-processing process
        - create graph for energy system
        - result visualization
- automatic saving all results to Excel file, i.e. out.xlsx
- json workflow schema for different metadata for running vppopt project
    - simulation step
    - solver settings