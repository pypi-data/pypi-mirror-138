========
Tutorial
========

As VPPopt is developed on top of `oemof-solph package <https://github.com/oemof/oemof-solph>`_ 
which is based on `pyomo <http://www.pyomo.org/>`_ for creating and solving 
`linear <https://www.gurobi.com/resource/linear-programming-basics/>`_ or 
`mixed-integer linear <https://www.gurobi.com/resource/mip-basics/>`_ optimization problems. 
It is (highly) recommended to read `solph <https://oemof-solph.readthedocs.io/en/latest/usage.html>`_ and 
`pyomo <https://pyomo.readthedocs.io/en/stable/>`_ user's guide for more comprehension about LP or MIP model 
as well as oemof-solp energy system.

Introduction of oemof energy system and its components
------------------------------------------------------

oemof energy system whose topological representation is found in the image below 
will be the main container for the model and contain different 
`nodes <https://github.com/oemof/oemof-network/blob/dev/src/oemof/network/network.py#L107>`_ and 
`flow <https://oemof-solph.readthedocs.io/en/latest/reference/oemof.solph.html#module-oemof.solph.network.flow>`_.

.. image:: https://oemof-solph.readthedocs.io/en/latest/_images/oemof_solph_example.svg
    :scale: 50 %
    :alt: alternate text
    :align: center

source: oemof-solph

- There are two types of nodes in oemof energy system - components and buses.
- Every component has to be connected with one or more buses
- The connection between a component and a bus is represented by a flow

VPPopt project
--------------

The basic idea for vppopt tool is to facilitate the energy system generation and 
optimization formulation. A vppopt could be initialized by the following command:

.. code-block:: bash

    vppopt init -pdir <vppopt project directory path> -s <scenario name>

The structure of a vppopt project is as follow

.. code-block:: bash
    
    vppopt_project
        |__vppopt.json
        |__vppopt.xlsx
        |__scripts

vppopt json workflow
^^^^^^^^^^^^^^^^^^^^

vppopt json (editable) workflow file will be used to give vppopt program the necessary information about

    - file and directory paths
    - simulation settings
    - external user scripts being used
    - etc.

Below an example of a vppopt json workflow file

.. code-block:: json

    {
        "Version": "2021.01",
        "ProjName": "Untitled Project",
        "ProjDir": "G:\\Workspace\\Cenaero\\Git\\vppopt-examples\\examples\\opnieuw",
        "WorkflowFile": "G:\\Workspace\\Cenaero\\Git\\vppopt-examples\\examples\\opnieuw\\vppopt.json",
        "NodesDataExcelFile": "G:\\Workspace\\Cenaero\\Git\\vppopt-examples\\examples\\opnieuw\\vppopt.xlsx",
        "Scenario": {},
        "Nodes": {},
        "SimulationStep": {
            "start_date": "2016-01-01",
            "end_date": "2016-12-31",
            "time_step": 4,
            "solver_settings": {
                "solver": "cbc",
                "executable": "",
                "solver_io": "lp",
                "solve_kwargs": {},
                "cmdline_options": {}
            }
        },
        "ExternalScript": {
            "script_dir": "G:\\Workspace\\Cenaero\\Git\\vppopt-examples\\examples\\opnieuw\\scripts",
            "scripts": [
                {
                    "name":"reporting_create_graph",
                    "tag":"reporting",
                    "arguments":{}
                },
                {
                    "name":"model_test_updating_nodes",
                    "tag":"model",
                    "arguments":{}
                }
            ]
        }
    }

.. note::

    ``Scenario`` and ``Nodes`` fields from vppopt json workflow file 
    are currently not used for the scurrent version of vppopt.


vppopt Excel input file
^^^^^^^^^^^^^^^^^^^^^^^

After initializing a project using ``vppopt init`` an Excel file 
(being served as an Excel Input Template) containing different empty 
sheets (e.g. INFO, buses, demand, renewables, etc.) will be created. 
This Excel file willl be used to fill all necessary input for creating an 
(oemof-solph) energy system.

After completing Excel file with all neccessary data for creating oemof-solph 
energy system, all these data will be parsed by ``vppopt`` and stored in list 
of oemof-solph nodes. The latters will be then fed in an oemof-solph 
energy system object for creating an (pyomo) optimization problem.

The optimization problem created will be solved using an optimizer specified 
within ``SimulationStep.solver_settings`` from ``vppopt json workflow``.

At this stage, the vppopt could be already executed using ``vppopt run`` sub-command 
for obtaining basic outputs as described in `Outputs section targets`_

More information on how to initializing and completing an Excel Input File of a vppopt 
project could be found `here <excel_input_template.html>`_

python (user) external scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For updating/modifying nodes, energy system and/or optimization model, external python scripts 
could be used. These scripts must be placed within ``scripts`` directory of a vppopt project. 
Currently two types of scripts could be used with vppopt.

- ``model`` scripts which are used for updating/modifying nodes, energy system and or optimization model before being solved
- ``reporting`` scripts which are used for post-processing step and automatically creating the report

The metadata of all python external scripts must be provided in vppopt json workflow at ``ExternalScript`` as below

.. code-block::

    "ExternalScript": {
            "script_dir": "G:\\Workspace\\Cenaero\\Git\\vppopt-examples\\examples\\opnieuw\\scripts",
            "scripts": [
                {
                    "name":"reporting_create_graph",
                    "tag":"reporting",
                    "arguments":{}
                },
                {
                    "name":"model_test_updating_nodes",
                    "tag":"model",
                    "arguments":{}
                }
            ]
        }

Two examples for ``model`` and ``reporting`` external script are found below.

- Example of a ``model`` python external script

.. code-block:: python

    from oemof import solph
    import numpy as np
    import matplotlib.pyplot as plt

    def main(nodes,esys,om,**kwargs):
        """
        nodes: list of node objects created by vppopt created by vppopt with data from Excel file
        esys: energy system object created by vppopt with data from Excel file
        om: optimization model created by vppopt with data from Excel file
        """

        def heat_demand(d):
            """
            basic model for heat demand, solely based on the day of the year
            """
            return 0.6 + 0.4*np.cos(2*np.pi*d/356)
        
        def solar_thermal(d):
            """
            basic model for solar thermal yield, solely based on the day of the year
            """
            return 0.5 - 0.5 * np.cos(2 * np.pi * d / 356)
        
        # always check if nodes/esys/om
        if nodes:
            for node in nodes:
                if isinstance(node,solph.Bus):
                    if node.label=='b_heat': b_heat=node

            for node in nodes:
                # Set up demand_heat
                if node.label=='demand_heat':
                    print("demand_heat: ",node.inputs[b_heat].nominal_value)
                    node.inputs[b_heat].fix = [heat_demand(day) for day in range(0,len(esys.timeindex))]
                
                # Set up fireplace
                # variable cost is already set up but we don't see in nodes data
                if node.label=='fireplace' and isinstance(node,solph.Source):
                    node.outputs.data[b_heat].nominal_value=10
                    node.outputs[b_heat].max = [1.0]*len(esys.timeindex)
                    node.outputs[b_heat].min = [0.4]*len(esys.timeindex)
                    node.outputs[b_heat].nonconvex=solph.NonConvex(minimum_uptime=2,initial_status=1)
                    
                if node.label=='boiler':
                    node.outputs[b_heat].nominal_value=10
                    
                if node.label=='b_heat_excess':
                    node.inputs[b_heat].nominal_value=10

                if node.label=='thermal_collector':
                    node.outputs[b_heat].fix=[solar_thermal(day) for day in range(0,len(esys.timeindex))]
        return

- Example of a ``reporting`` python external script

.. code-block:: python

    from oemof import solph
    from oemof.network.graph import create_nx_graph
    from oemof.solph.processing import results
    from vppopt.utils import draw_graph
    from loguru import logger
    import os
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go


    def main(nodes,esys, om, **kwargs):

        workflowObj = kwargs.get("workflowObj")

        output_file = kwargs.get("output_file","out.xlsx")

        if not esys:
            es = solph.EnergySystem()        
            es.restore(dpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))), filename = "esys.oemof")
        else:
            es = esys
        # print the solver results

        import pprint as pp
        print("********* Meta results *********")
        pp.pprint(es.results["meta"])
        print("")

        results = es.results["main"]

        data = solph.views.node(results, "b_heat")["sequences"]
        
        graph_data = []
        for col in data.columns:
            graph_data.append(go.Scatter(x=data.index, y=data[col],name=str(col)))
        
        fig = go.Figure(graph_data)
        fig.write_html("graph.html")
        
        logger.info("Create graph of energy system")
        graph_name = kwargs.get("graph_name")
        if not graph_name:
            graph_name = "esys.graphml"

        graph = create_nx_graph(es,filename=graph_name)

        if os.path.isfile(graph_name):
            print("Graph created at {}".format(os.path.abspath(graph_name)))
        else:
            print("Graph is not found at {}".format(os.path.abspath(graph_name)))
        
        draw_graph(
            grph=graph,
            plot=True,
            node_size=1000,
            node_color={
                "b_heat":"red"
            }
        )

        # check and plot results
        results=esys.results["main"]
        invest = solph.views.node(results, "b_heat")["scalars"][(("thermal_collector", "b_heat"), "invest")]
        print("Invested in {} solar thermal power.".format(invest))

        if plt is not None:
            # plot heat bus
            data = solph.views.node(results, "b_heat")["sequences"]
            exclude = ["b_heat_excess", "status"]
            columns = [
                c
                for c in data.columns
                if not any(s in c[0] or s in c[1] for s in exclude)
            ]
            data = data[columns]
            ax = data.plot(kind="line", drawstyle="steps-post", grid=True, rot=0)
            ax.set_xlabel("Date")
            ax.set_ylabel("Heat (arb. units)")
            plt.show()

Basic run
---------

Using vppopt command line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    vppopt run -wf <vppopt json workflow, e.g. vppopt.json>

.. note::

    vppopt run could be executed from any place, but some output files could be saved in 
    current workding directory.

Running from a python script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Possible to running vppopt project from python script

.. code-block:: python
    
    import vppopt


Outputs
^^^^^^^

From a basic run without any python external script two output files will be created

- out.xlsx
- esys.vppopt

Advanced
--------

How to create a new component
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

How to add new constraint, new attribute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`example <https://forum.openmod.org/t/adding-an-attribute-to-flow/976/8>`_

multi-objective optimization with pymoo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Examples
--------

`vppopt-examples <https://github.com/cenaero-enb/vppopt-examples>`_

`oemof-solph examples <https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph>`_