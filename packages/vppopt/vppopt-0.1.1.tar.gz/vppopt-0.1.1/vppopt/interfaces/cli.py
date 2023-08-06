"""
Module docstring
"""
import os
import argparse
from loguru import logger

from vppopt.nodes_utils import nodes_data_excel_parser, nodes_from_dict
from vppopt.vppopt import run_vppopt, run_external_script
from vppopt.results import om_result_to_excel

from vppopt.workflow import WorkFlow
from vppopt.schemas import excel_scenario_init
from vppopt.workflow import workflow_path_update


def main():
    """
    command line interface

    Sub-commands
    ------------
    version
    init
    run
    excel_reader (deprecated)
    """
    parser = argparse.ArgumentParser(
        description='Script for initilazing vppopt scenario'
    )

    parser.add_argument(
        "--version",
        help="version of vppopt",
        action="store_true"
        )

    "Sub-commands arguments"
    subparsers = parser.add_subparsers(dest="subcmd", help="sub-command help")
    # ================
    # init sub-command
    # ================
    init_parser = subparsers.add_parser(
        "init",
        help="Initializing vppopt scenario and more"
        )
    init_parser.add_argument(
        '-pdir',
        '--proj_dir',
        type=str,
        help='vppopt project directory'
        )
    init_parser.add_argument(
        '-s',
        '--scenario',
        type=str,
        default="vppopt",
        help="name of vppopt scenario json file")

    # ==========================#
    # run sub-command
    run_parser = subparsers.add_parser(
        "run",
        help="run vppopt scenario and more"
        )
    run_parser.add_argument(
        '-wf',
        '--workflow',
        type=str,
        help='[REQUIRED] vppopt JSON Workflow',
        required=True
        )
    run_parser.add_argument(
        '--path_update',
        help='automatic update path of project directory',
        action="store_true"
        )

    # ==========================
    # excel_reader sub-command
    excel_reader_parser = subparsers.add_parser(
        "excel_reader",
        help="run vppopt with scenario read from excel file"
        )

    excel_reader_parser.add_argument(
        'excel_file',
        metavar='excel_file',
        type=str,
        help='[REQUIRED] Excel File for vppopt scenario')

    excel_reader_parser.add_argument(
        '--graph',
        help="Path for saving energy system graph",
        type=str
    )

    excel_reader_parser.add_argument(
        '--result_excel',
        help="Path for saving energy system graph",
        type=str
    )

    args = parser.parse_args()

    # main comment
    if args.version:
        import vppopt
        return vppopt.__version__

    "========================="
    if args.subcmd == 'init':
        import vppopt
        # Default vppopt json workflow
        jsonWorkflow = WorkFlow()
        workflow = jsonWorkflow.workflow
        workflow.Version = vppopt.__version__

        if not args.proj_dir:
            logger.info("No value is given for proj_dir argument, 'NewProject' directory will be created as project directory")
            projDir = os.path.join(os.getcwd(), "NewProject")
        else:
            projDir = os.path.abspath(args.proj_dir)
                    
        # Verifying if the project directory is created
        if not os.path.exists(projDir):
            os.mkdir(projDir)
        workflow.ProjDir = projDir

        workflow.ExternalScript.script_dir = os.path.join(projDir, "scripts")
        scriptDir = str(workflow.ExternalScript.script_dir)
        if not os.path.exists(scriptDir):
            os.mkdir(scriptDir)

        # workflow name or senario name
        workflowName = os.path.split(args.scenario)[-1].split('.')[0]
        jsonWorkflow.saveAs(os.path.join(
            projDir,
            "{}.json".format(workflowName))
            )
        workflow.WorkflowFile = os.path.join(
            projDir,
            "{}.json".format(workflowName)
            )

        # automatically generate excel input
        excel_path = os.path.join(projDir, "{}.xlsx".format(workflowName))
        excel_scenario_init(excel_path)
        workflow.NodesDataExcelFile = excel_path

        # TODO: addd restriction to json field

        jsonWorkflow.save()

    # ===========================
    if args.subcmd=='run':

        if not os.path.isfile(os.path.abspath(args.workflow)):
            err_msg = "ERROR: No such file or directory {}".format(
                os.path.abspath(args.workflow)
                )
            logger.error(err_msg)
            return 1

        workflow_obj = WorkFlow()
        workflow_obj.load_workflow(args.workflow)
        ################# Update Project dir#################
        # TODO: update project dir information in workflow file when move to another machine
        if not os.path.dirname(os.path.abspath(args.workflow)) == workflow_obj.workflow_for_json["ProjDir"]:
            workflow_path_update(args.workflow,workflow_obj,args.path_update)
            return
        #####################################################
        # get nodes data excel file from workflow file
        nodesExcelFile = workflow_obj.workflow_for_json["NodesDataExcelFile"]
        # read in nodes data from excel file into python dictionary
        nodes_data_dictionary = nodes_data_excel_parser(nodesExcelFile,engine='openpyxl')
        # create oemof nodes liste from nodes data dictionary
        nodes = nodes_from_dict(nd=nodes_data_dictionary)
        
        esys, om = run_vppopt(nodes, workflow_obj=workflow_obj)

        # dump om into pickle file or json file
        # with open("in.vppopt",'wb') as f:
        #     import pickle
        #     pickle.dump(om,f,-1)
        
        ############## Reporting external scripts would be run here############
        run_external_script(workflow_obj,esys=esys,om=om, script_type="reporting")        
        
        # automatically store all result in excel file or sql or pickle
        excel_path = os.path.join(workflow_obj.workflow_for_json["ProjDir"],"out.xlsx")        
        om_result_to_excel(om, excel_path)
        if os.path.isfile(excel_path):
            logger.info("Saved outputs to {}".format(excel_path))
        else:
            logger.warning("Excel output file not found at {}".format(excel_path))
    # ===========================
    if args.subcmd=='excel_reader':
        logger.warning("This sub-command will be deprecat")
        if not os.path.isfile(os.path.abspath(args.excel_file)):
            err_msg = "ERROR: No such file or directory {}".format(os.path.abspath(args.excel_file))
            print(err_msg)
        
        # should try with xlrd first?
        nodes_data_dictionary = nodes_data_excel_parser(args.excel_file,engine='openpyxl')
        nodes = nodes_from_dict(nd=nodes_data_dictionary)
        esys,om = run_vppopt(nodes)

        ##############POST PROCESSING############
        # Energy System Graph
        if args.graph:
            from oemof.network.graph import create_nx_graph
            logger.info("Create graph of energy system")
            graph_name = args.graph
            graph = create_nx_graph(esys,filename=graph_name)
            if os.path.isfile(graph_name):
                print("Graph created at {}".format(os.path.abspath(graph_name)))
            else:
                print("Graph is not found at {}".format(os.path.abspath(graph_name)))
            
            from vppopt.utils import draw_graph
            draw_graph(
                grph=graph,
                plot=True,
                node_size=1000,
                node_color={
                    "bel":"yellow",
                    "bh2":"green",
                    "bheat":"red"
                }
            )
        ####################################################
        # Result excel file (could be automatically created)
        if args.result_excel:
            excel_path = args.result_excel
            om_result_to_excel(om, excel_path)


if __name__=='__main__':
    main()
