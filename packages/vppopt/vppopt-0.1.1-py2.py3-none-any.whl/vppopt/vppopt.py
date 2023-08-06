
import logging
from vppopt.workflow import WorkFlow
from loguru import logger
from oemof import solph
import pandas as pd
import datetime
import os
import sys
import importlib
from oemof.solph.views import convert_keys_to_strings


def run_external_script(
    workflow_obj,
    nodes = None,
    esys=None,
    om = None,
    script_type="reporting"
    ):

    """
    run external python script for run_vppopt and vppopt run 
    ========================================================
    workflow_obj, 
        vppopt workflow object
    esys, 
        energy system, None by default
    om,
        optimization model
    script_type, str
        model or reporting
    """
    workflow_for_json = workflow_obj.workflow_for_json
    if not workflow_for_json:
        err_msg = "ERROR: vppopt json workflow not found"
        raise Exception(err_msg)
    
    # script type must be either 'inputgen' or 'model' or 'reporting'
    if not script_type or not any(script_type==el for el in ["inputgen", "model","reporting"]):
        err_msg = "ERROR: script_type is missed or not equal to either 'inputgen', 'mode' or 'reporting'"
        logger.error(err_msg)
        return 1
    
    externalScript = workflow_for_json["ExternalScript"]
    scriptDir = str(externalScript["script_dir"])
    if not os.path.exists(scriptDir):
        err_msg = "ERROR: No such file or directory {}".format(scriptDir)
        raise Exception(err_msg)
    
    # should check if path already exisist
    if not os.path.dirname(scriptDir) in sys.path:
        sys.path.append(os.path.dirname(scriptDir))
    
    script_count = 0
    # TODO if externalScript empty
    for script in externalScript["scripts"]:
        print(script)
        if not script:
            continue
        if (not script["tag"]) or (not script["name"]):
            script_count+=1
            logger.warning(
                "Script name and tag must be specified for all external python script. Name and/or tag of script [{}] ({}) is/are missed".format(script_count,script["name"])
                )
            continue

        if not os.path.isfile(os.path.join(scriptDir,"{}.py".format(script["name"]))):
            err_msg = "ERROR: {}.py not found in {}. Please check the consistency between external script file name and data from workflow".format(script["name"],scriptDir)
            raise Exception(err_msg)

        if str(script["tag"]).lower()==script_type.lower():
            imported_module = importlib.import_module("scripts.{}".format(script["name"]))
            kwargs = script["arguments"]
            kwargs["workflow_obj"] = workflow_obj

            eval("imported_module.main(nodes, esys, om,**kwargs)")

def run_vppopt(nodes,**kwargs):
    """
    :param model - pyomo abstract model
    nodes: dict,
        nodes
    workflow_obj:
        workflow object
    """
    workflow_obj = kwargs.get("workflow_obj")
    # TODO: timeindex could be gotten from vppopt.json, timeseries data
    # simulation settings
    try:
        simu_settings = workflow_obj.workflow_for_json["SimulationStep"]
        start_date = simu_settings["start_date"]
        end_date = simu_settings["end_date"]
        timestep_per_hour = float(simu_settings["time_step"])
        if not all([start_date,end_date,timestep_per_hour]):
            logger.error("'start_date', 'end_date' and 'timestep_per_hour' must be specified in vppopt json workflow. Simulation will stop, please check workflow file and start simulation again")
            return

        solver_settings = simu_settings["solver_settings"]
        solver = solver_settings["solver"]
        solver_io = solver_settings["solver_io"]
        executable = solver_settings["executable"]
        solve_kwargs = solver_settings["solve_kwargs"]
        solver_cmd_options = solver_settings["cmdline_options"]

    except KeyError as err:
        raise Exception("{} not found in vppopt json workflow. Please check or update vppopt json workflow".format(err))
    
    timeindex = pd.date_range(
        start=start_date,
        end=end_date,
        freq='{}H'.format(1/timestep_per_hour)
        )
    logger.info("timeindex contains {} periods from {} to {}".format(timeindex.shape[0],timeindex.min(),timeindex.max()))

    # TODO: skip last row of time index or check with row number from data
    
    # optimizer setting
    # solver could be gotten from vppopt also
    # solver = kwargs.get('solver','cbc')
    # solver_io = kwargs.get('solver_io',"lp")
    # executable = kwargs.get('executable',"")
    # solve_kwargs = kwargs.get('solve_kwargs',{})
    # solver_cmd_options = kwargs.get("cmdline_options",{})

    # periods = kwargs.get('periods',8760)
    # if not timeindex:
    #     logger.info("No timeindex is specified, only 24 hours will be considered as simulation time")
    #     start_date = datetime.datetime(datetime.datetime.now().year,1,1)
    #     timeindex = pd.date_range(start=start_date,periods=periods,freq='H')    

    # model creation and solving
    logger.info("Starting optimization")

    # initilisation of the energy system
    energy_system = solph.EnergySystem(timeindex=timeindex)

    # TODO: all external script with tag of 'nodes' or 'energy_system' must be run here

    # run external script for updating nodes before creating energysystem
    # at this moment there are only timeindex in energy_system
    # TODO: Why there is not data for variable_costs in nodes?????
    run_external_script(workflow_obj,nodes = nodes, esys=energy_system, script_type="model")

    # add nodes and flows to energy system
    energy_system.add(*nodes)    

    print("*********************************************************")
    print("The following objects have been added to energy system object:")
    for n in energy_system.nodes:
        oobj = str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        print(oobj + ":", n.label)
    print("*********************************************************")

    #####################################
    # Optimize the energy system
    #####################################
    om = solph.Model(energy_system)

    # TODO: all external script with tag of 'model' or 'energy_system' must be run here
    # at this moment the modification in nodes does not have any impact in energy_system and om
    run_external_script(workflow_obj,esys=energy_system, om=om, script_type="model")

    # TODO: Do not understand what is it for?
    om.receive_duals()

    # solving the linear problem using the given solver
    om.solve(
        solver=solver,
        solver_io=solver_io,
        executable=executable,
        solve_kwargs=solve_kwargs,
        cmdline_options = solver_cmd_options        
        )
    
    logger.info("Store the energy system with the results")
    # add results to the energy system to make it possible to store them.
    
    energy_system.results["main"] = solph.processing.results(om)
    energy_system.results['main'] = convert_keys_to_strings(energy_system.results['main'])
    energy_system.results["meta"] = solph.processing.meta_results(om)

    energy_system.dump(dpath=os.getcwd(),filename='esys.vppopt')
    if os.path.isfile(os.path.join(os.getcwd(),"esys.vppopt")):
        logger.info("energysystem is found at {}".format(os.path.join(os.getcwd(),'esys.vppopt')))

    return energy_system, om