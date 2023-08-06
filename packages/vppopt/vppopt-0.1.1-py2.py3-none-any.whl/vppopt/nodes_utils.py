# -*- coding: utf-8 -*-
"""
General description
-------------------
Collection of functions for handling with oemof.solph nodes
"""

import os
import json
import numpy as np
import pandas as pd
from loguru import logger
from oemof import solph
from oemof.tools import economics

def get_node_from_list(node_list, node_type,label):
    """
    return oemof node from list using node type and label
    """

    res = [node for node in node_list if isinstance(node,node_type) and node.label==label]

    if len(res)>1:
        err_msg = "node label must be unique"
        logger.error(err_msg)
        return 1

    return res[0]

def nodes_data_excel_to_json(excel_path,json_path,**kwargs):
    """
    Convert excel to json

    Parameters
    ----------
    excel_path: str
        Excel path
    json_path: str
        json path

    possible keyword arguments
    --------------------------
    engine: str,
        default openpyxl
    """

    if not os.path.isfile(excel_path):
        err_msg = "File not found at {}".format(excel_path)
        logger.error(err_msg)
        return 1
    excel_parser_engine = kwargs.get("engine","openpyxl")
    nodes = nodes_data_excel_parser(excel_path,engine=excel_parser_engine)
    nodes_dict = dict()

    for key in nodes.keys():
        if key.lower() != 'timeseries':
            nodes_dict[key] = nodes[key].to_dict(orient='records')
        elif key.lower() == 'timeseries':
            nodes_dict[key] = nodes[key].to_dict(orient='list')

    with open(json_path,"w") as fp:
        json.dump(nodes_dict,fp,indent=4)

def nodes_data_json_to_excel():
    """
    convert nodes data
    """

    return

def nodes_data_excel_parser(excel_path,**kwargs):
    """
    Return a dictionary of pandas series from Excel sheet

    Parameters
    ----------
    excel_path : :obj:`str`
        Path to excel file

    Possible keyword arguments
    --------------------------
    engine: :obj: `str`
        Engine for parsing excel file using pandas, by default engine='xlrd'

    Returns
    -------
    :obj:`dict`
        Imported nodes data
    """
    excel_parser_engine = kwargs.get("engine","xlrd")

    # Check if excel file exists
    if not excel_path or not os.path.isfile(excel_path):
        raise FileNotFoundError(
            "Excel data file {} not found.".format(excel_path)
        )

    xls = pd.ExcelFile(excel_path,engine=excel_parser_engine)

    try:
        # TODO for sheet in xls.sheet_names:
        # nodes_data[sheet] = xls.parse(sheet)
        nodes_data = {
            "buses": xls.parse("buses").replace({np.nan:None}),
            "commodity_sources": xls.parse("commodity_sources").replace({np.nan:None}),
            "transformers": xls.parse("transformers").replace({np.nan:None}),
            "transformers_chp": xls.parse("transformers_chp").replace({np.nan:None}),
            "renewables": xls.parse("renewables").replace({np.nan:None}),
            "demand": xls.parse("demand").replace({np.nan:None}),
            "storages": xls.parse("storages").replace({np.nan:None}),
            "powerlines": xls.parse("powerlines").replace({np.nan:None}),
            "timeseries": xls.parse("time_series").replace({np.nan:None}),
            "financial":xls.parse("financial").replace({np.nan:None})
        }
    except KeyError:
        err_msg = "Excel file must contains: "
        err_msg+="buses, commodity_sources, transformers, renewables, demand, "
        err_msg+="storages, powerlines, financial and timeseries]. "
        err_msg+="The following sheets are found: {}".format(xls.sheet_names)
        raise Exception(err_msg)

    # set datetime index
    nodes_data["timeseries"].set_index("timestamp", inplace=True)
    nodes_data["timeseries"].index = pd.to_datetime(
        nodes_data["timeseries"].index
    )

    logger.info("Data from Excel file {} imported in as nodes data.".format(excel_path))

    return nodes_data

def nodes_from_dict(nd=None,**kwargs):
    """
    Return a list of nodes (oemof objects) from nodes dict

    Parameters
    ----------
    nd : :obj:`dict`
        Nodes data

    Returns
    -------
    nodes : `obj`:dict of :class:`nodes <oemof.network.Node>`
    """

    if not nd:
        err_msg = "ERROR: No nodes data provided"
        print(err_msg)
        return 1

    nodes = []

    ###################
    # Create BUS objects
    ###################
    busd = {}
    for i, row in nd["buses"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):
            logger.info("bus {} will be created".format(row["label"]))
            bus = solph.Bus(label=row["label"])
            nodes.append(bus)
            busd[row["label"]] = bus

            if row["excess"] and not pd.isnull(row["excess"]):
                # Automatically add Sink for curtailment (excess)
                # Add variable cost for excess cost --> minimise curtailment
                nodes.append(
                    solph.Sink(
                        label=row["label"] + "_excess",
                        inputs={
                            busd[row["label"]]:solph.Flow(
                                variable_costs = row["excess costs"]
                            )
                        },
                    )
                )
            # Automatically add Source for shortage
            # Add variable cost for shortage --> minimize shortage
            if row["shortage"] and not pd.isnull(row["shortage"]):
                nodes.append(
                    solph.Source(
                        label = row["label"] + "_shortage",
                        outputs={
                            busd[row["label"]]:solph.Flow(
                                variable_costs=row["shortage costs"]
                            )
                        },
                    )
                )
    #######################
    # Create Source objects
    #######################
    for i, row in nd["commodity_sources"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):
            nodes.append(
                solph.Source(
                    label=row["label"],
                    outputs={
                        busd[row["to"]]: solph.Flow(
                            variable_costs = row["variable costs"]
                        )
                    },
                )
            )
    #########################
    # Create Source objects
    # with fixed time series
    # from 'renewables' table
    #########################

    # A source can represent a pv-system, a wind power plant, an import of natural gas 
    # or a slack variable to avoid creating an in-feasible model. While a wind power plant
    # will have an hourly feed-in depending on the weather conditions the natural_gas 
    # import might be restricted by maximum value (nominal_value) and an annual limit 
    # (summed_max). As we do have to pay for imported gas we should set variable costs. 
    # Comparable to the demand series an fix is used to define a fixed the normalised
    # output of a wind power plant. Alternatively, you might use max to allow for easy 
    # curtailment. The nominal_value sets the installed capacity.

    for i, row in nd["renewables"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):
            # set static outflow values
            outflow_args = {}

            # get time series data from timeseries Excel sheet for node and parameter
            for col in nd["timeseries"].columns.values:
                if col.split(".")[0] == row["label"]:
                    outflow_args[col.split(".")[1]]=nd["timeseries"][col]
                    # outflow_args["fix"]=nd["timeseries"][col]
            
            # TODO add NON-CONVEX to outflow_args
            if row["capex"] and not pd.isnull(row["capex"]):
                # with investment mode, nominal_value must be None
                logger.info("Invest {} capacity".format(row["label"]))
                invest_args = {}
                if not row["epc_invest"] or pd.isnull(row["epc_invest"]):
                    epc_invest = economics.annuity(row["capex"],20,0.08)
                else:
                    epc_invest=row["epc_invest"]
                invest_args["ep_costs"] = epc_invest

                if row["max"] and not pd.isnull(row["max"]):
                    invest_args["maximum"] = row["max"]

                if row["min"] and not pd.isnull(row["min"]):
                    invest_args["minimum"]=row["min"]

                if row["existing"] and not pd.isnull(row["existing"]):
                    invest_args["existing"]=row["existing"]
                
                outflow_args["investment"] = solph.Investment(**invest_args)                
            else:
                outflow_args["nominal_value"] = row["capacity"]
            
            # create source object and append to nodes list
            nodes.append(
                solph.Source(
                    label=row["label"],
                    outputs = {
                        busd[row["to"]]:solph.Flow(**outflow_args)
                    }
                )
            )
    #####################
    # Create Sink objects
    #####################
    """
    A sink is normally used to define the demand within an energy model but it can also be used to detect excesses.

    The example shows the electricity demand of the electricity_bus defined above.
    - 'nd['timeseries'][col]' should be sequence of normalised values
    - 'nominal_value' is the maximum demand the normalised sequence is multiplied with.
    - Giving 'nd['timeseries'][col]' as parameter 'fix' means that the demand cannot be changed by the solver.    
    
    In contrast to the 'demand sink' the 'excess sink' has normally less restrictions but is open to take the whole excess.
    """
    for i, de in nd["demand"].iterrows():
        if de["active"] and not pd.isnull(de["active"]):
            # set static inflow values
            inflow_args = {
                "nominal_value":de["nominal value"]
            }
            # get time series for node and parameter
            for col in nd["timeseries"].columns.values:
                if col.split(".")[0]==de["label"]:
                    # inflow_args[col.split(".")[1]]=nd["timeseries"][col]
                    # TODO: verify other key than 'fix'?????
                    inflow_args["fix"]=nd["timeseries"][col] 
            
            # Create Sink object and append to nodes list
            nodes.append(
                solph.Sink(
                    label=de["label"],
                    inputs={
                        busd[de["from"]]:solph.Flow(**inflow_args)
                    }
                )
            )
    ###########################
    # Create Transformer object
    ###########################
    """
    An instance of the Transformer class can represent a node with multiple input and output flows such as:
    - a power plant
    - a transport line 
    - or any kind of a transforming process as electrolysis, a cooling device or a heat pump. 
    The efficiency has to be constant within one time step to get a linear transformation.
    You can define a different efficiency for every time step (e.g. the thermal powerplant efficiency according 
    to the ambient temperature) but this series has to be predefined and cannot be changed within the optimisation.

    A condensing power plant can be defined by a transformer with one input (fuel) and one output (electricity)
    ```
    b_gas = solph.Bus(label='natural_gas')
    b_el = solph.Bus(label='electricity')
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={b_el: solph.Flow(nominal_value=10e10)},
        conversion_factors={electricity_bus: 0.58})
    ```

    A CHP power plant would be defined in the same manner but with two outputs:
    ```
    b_gas = solph.Bus(label='natural_gas')
    b_el = solph.Bus(label='electricity')
    b_th = solph.Bus(label='heat')

    solph.Transformer(
        label='pp_chp',
        inputs={b_gas: Flow()},
        outputs={b_el: Flow(nominal_value=30),
                b_th: Flow(nominal_value=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4})
    ```
    A CHP power plant with 70% coal and 30% natural gas can be defined with two inputs and two outputs:
    ```
    b_gas = solph.Bus(label='natural_gas')
    b_coal = solph.Bus(label='hard_coal')
    b_el = solph.Bus(label='electricity')
    b_th = solph.Bus(label='heat')

    solph.Transformer(
        label='pp_chp',
        inputs={b_gas: Flow(), b_coal: Flow()},
        outputs={b_el: Flow(nominal_value=30),
                b_th: Flow(nominal_value=40)},
        conversion_factors={b_el: 0.3, b_th: 0.4,
                            b_coal: 0.7, b_gas: 0.3})
    ```
    """
    for i, row in nd["transformers"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):
            # set static inflow values
            inflow_args = {
                "variable_costs":row["variable input costs"]
            }
            # inflow_args = {}
            outflow_args = {}
            # get time series for inflow transformer
            for col in nd["timeseries"].columns.values:
                if col.split(".")[0]==row["label"]:
                    # inflow_args[col.split(".")[1]] = nd["timeseries"][col]
                    inflow_args["fix"] = nd["timeseries"][col]
            
            #TODO: multi inputs/outputs and add investment

            if row["capex inflow"] and not pd.isnull(row["capex inflow"]):
                logger.info("Invest {} inflow capacity".format(row["label"]))                
                invest_args = {}
                invest_args["ep_costs"] = economics.annuity(row["capex inflow"],20,0.08)

                if row["max inflow"] and not pd.isnull(row["max inflow"]):
                    invest_args["maximum"] = row["max inflow"]

                if row["min inflow"] and not pd.isnull(row["min inflow"]):
                    invest_args["minimum"] = row["min inflow"]

                if row["existing inflow"] and not pd.isnull(row["existing inflow"]):
                    invest_args["existing"] = row["existing inflow"]

                inflow_args["investment"] = solph.Investment(**invest_args)
            else:                
                outflow_args["nominal_value"] = row["capacity"] # should be specify capacity inflow or outflow

            # create Transformer object and append to nodes list
            nodes.append(
                solph.Transformer(
                    label=row["label"],
                    inputs = {
                        busd[row["from"]]:solph.Flow(**inflow_args)
                    },
                    outputs={
                        busd[row["to"]]:solph.Flow(**outflow_args)
                    },
                    conversion_factors = {
                        busd[row["to"]]:row["efficiency"]
                    }
                )
            )
    ################################
    # Create Transformer CHP objects
    ################################
    for i, row in nd["transformers_chp"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):

            inflow_args = {}
            outflow_elec_args = {}
            outflow_heat_args = {}

            inflow_args["variable_costs"] = row["variable input costs"]

            if row["capex elec"] and not pd.isnull(row["capex elec"]):
                logger.info("Invest {} inflow capacity".format(row["label"])) 
                invest_args = {}
                invest_args["ep_costs"] = economics.annuity(row["capex elec"],20,0.08)
                if row["max elec"] and not pd.isnull(row["max elec"]):
                    invest_args["maximum"] = row["max elec"]
                if row["min elec"] and not pd.isnull(row["min elec"]):
                    invest_args["minimum"] = row["min elec"]
                if row["existing elec"] and not pd.isnull(row["existing elec"]):
                    invest_args["existing"] = row["existing elec"]
                
                outflow_elec_args["investment"] = solph.Investment(**invest_args)
                investment = solph.Investment(**invest_args)
            else:
                # inflow_args["nominal_value"] = row["capacity_el"]
                outflow_elec_args["nominal_value"] = row["capacity_el"]
                outflow_heat_args["nominal_value"] = row["capacity_heat"]

            # Create Transformer CHP object and append to nodes list
            nodes.append(
                solph.Transformer(
                    label = row["label"],
                    inputs ={
                        busd[row["from"]]:solph.Flow(**inflow_args)
                    },
                    outputs={
                        busd[row["to_el"]]:solph.Flow(**outflow_elec_args),
                        busd[row["to_heat"]]:solph.Flow(**outflow_heat_args)
                    },
                    conversion_factors={
                        busd[row["to_el"]]:row["efficiency_el"],
                        busd[row["to_heat"]]:row["efficiency_heat"]
                    }
                )
            )

    ########################
    # Create Storage objects
    ########################
    for i, row in nd["storages"].iterrows():
        if row["active"] and not pd.isnull(row["active"]):

            inflow_args = {}
            outflow_args = {}

            if row["capex"] and not pd.isnull(row["capex"]):
                logger.info("Invest {} storage capacity".format(row["label"]))

                invest_args = {}
                invest_args["ep_costs"] = economics.annuity(row["capex"],20,0.08)
                if row["max"] and not pd.isnull(row["max"]):
                    invest_args["maximum"] = row["max"]
                if row["min"] and not pd.isnull(row["min"]):
                    invest_args["minimum"] = row["min"]
                if row["existing"] and not pd.isnull(row["existing"]):
                    invest_args["existing"] = row["existing"]

                investment=solph.Investment(
                    **invest_args
                )
                nominal_capacity=None
            
            #TODO add if row["capex inflow"] and if row["capex outflow"]
            #TODO read relation_capacity_inflow/outflow from excel
                
            else:
                investment = None
                nominal_capacity = row["nominal capacity"]            
            
            if row["capacity inflow"] and row["capacity inflow ratio"]:
                logger.error("{} is overdetermined, only capacity inflow or capacity inflow ratio shoul be set".format(row["label"]))
                return 1
            if row["capacity inflow"]:
                inflow_args["nominal_value"] = row["capacity inflow"]
            if row["capacity inflow ratio"]:
                capacity_inflow_ratio = row["capacity inflow ratio"]
            else:
                capacity_inflow_ratio = None
            inflow_args["variable_costs"] = row["variable input costs"]
            
            if row["capacity outflow"] and row["capacity outflow ratio"]:
                logger.error("{} is overdetermined, only capacity outflow or capacity outflow ratio shoul be set".format(row["label"]))
                return 1
            if row["capacity outflow"]:
                outflow_args["nominal_value"] = row["capacity outflow"]
            if row["capacity outflow ratio"]:
                capacity_outflow_ratio = row["capacity outflow ratio"]
            else:
                capacity_outflow_ratio = None

            outflow_args["variable_costs"] = row["variable output costs"]

            ###################CHECK INPUT###############
            if all([row["capacity min"],row["initial capacity"]]):
                if row["initial capacity"]<row["capacity min"]:
                    err_msg = "ERROR: Initial capacity cannot be lower than minimum capacity. Please update your input file"
                    raise Exception(err_msg)

            nodes.append(
                solph.components.GenericStorage(
                    label=row["label"],
                    inputs = {
                        busd[row["bus"]]:solph.Flow(**inflow_args)
                    },
                    outputs = {
                        busd[row["bus"]]:solph.Flow(**outflow_args)
                    },
                    investment=investment,
                    nominal_storage_capacity=nominal_capacity,
                    loss_rate = row["capacity loss"],
                    initial_storage_level = row["initial capacity"],
                    max_storage_level=row["capacity max"],
                    min_storage_level=row["capacity min"],
                    invest_relation_input_capacity = capacity_inflow_ratio,
                    invest_relation_output_capacity = capacity_outflow_ratio,
                    inflow_conversion_factor = row["efficiency inflow"],
                    outflow_conversion_factor = row["efficiency outflow"]
                )
            )
    #####################
    # Create Link objects
    #####################
    """
    A Link object with 1...2 inputs and 1...2 outputs
    Note: This component is experimental. Use it with care
    """
    for i, p in nd["powerlines"].iterrows():
        if p["active"] and not pd.isnull(p["active"]):
            bus1 = busd[p["bus_1"]]
            bus2 = busd[p["bus_2"]]
            nodes.append(
                solph.custom.Link(
                    label = "powerline" + "_" + p["bus_1"] + "_" + p["bus_2"],
                    inputs = {
                        bus1:solph.Flow(),
                        bus2:solph.Flow()
                    },
                    outputs = {
                        bus1: solph.Flow(nominal_value = p["capacity"]),
                        bus2: solph.Flow(nominal_value=p["capacity"]),
                    },
                    conversion_factors={
                        (bus1,bus2):p["efficiency"],
                        (bus2,bus1):p["efficiency"]
                    }
                )
            )    
    return nodes
