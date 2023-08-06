
import json
import python_jsonschema_objects as pjs
from six import with_metaclass
from vppopt.schemas import WORKFLOW_SCHEMA
import os
from loguru import logger

def import_json_workflow(workflow_obj,imported_json):

    with open(imported_json,'r+') as f:
        imported_data = json.load(f)
    print(imported_data)

    return "import data from json file and update vppopt json workflow"


def workflow_path_update(workflow_path,workflow_obj,path_update):
    """
    update the path information in workflow file
    ===========================
    workflow_path, str
        path of workflow file, e.g. 
    workflow_obj, workflow object
        vppopt workflow object
    path_update, bool
        whether update path information in workflow or not
    """

    ################# Update Project dir###############
    #if not os.path.dirname(os.path.abspath(workflow_path)) == workflow_obj.workflow_for_json["ProjDir"]:
    if not path_update:
        err_msg = "ERROR: Mistmach between dirname of vppopt json workflow ({0}) and ProjDir ({1}). Please consider to update the following json keys (from vppopt json workflow) using {0}: ".format(
            os.path.dirname(os.path.abspath(workflow_path)),
            workflow_obj.workflow_for_json["ProjDir"]
        )
        logger.error(err_msg)
        for key, val in workflow_obj.workflow_for_json.items():
            if workflow_obj.workflow_for_json["ProjDir"] in (val):
                print(key)
        logger.info(
            "vppopt json workflow could be automatically updated by adding --path_update argument, e.g.\n vppopt run -wf vppopt.json --path_update"
            )
        return 1
    else:
        with open(os.path.abspath(workflow_path), 'r+') as file:
            content = file.read()
            content = content.replace(
                str(workflow_obj.workflow_for_json["ProjDir"]).encode('unicode_escape').decode('ASCII'),
                str(os.path.dirname(os.path.abspath(workflow_path))).encode('unicode_escape').decode('ASCII')
                )
            file.seek(0)
            file.write(content)
            "###!!!!!! DOES NOT WORK WITHOUT FILE TRUNCATE !!!!!!###"
            file.truncate()
        
        logger.info("vppopt json workflow is updated. Please check json file, especially the following json keys before relaunch the command:")
        for key, val in workflow_obj.workflow_for_json.items():
            if workflow_obj.workflow_for_json["ProjDir"] in (val):
                print(key,": ",val)
        return

def version_check(workflow_obj):
    import vppopt
    if not workflow_obj.workflow_for_json["Version"] == vppopt.__version__:
        logger.warning(
            "json workflow created by vppopt version '{}' and the current vppopt version is {}".format(
                workflow_obj.workflow_for_json["Version"],
                vppopt.__version__
            )
        )

def version_updater(workflow_obj):
    return "update old vppopt json workflow to current vppopt version"

class WorkFlow(object):
    """
    VPPOPT workflow class
    """
    def __init__(self) -> None:
        super().__init__()

        builder = pjs.ObjectBuilder(WORKFLOW_SCHEMA)
        ns = builder.build_classes()
        self.workflow = ns.VppoptWorkflowSchema()
        self.filepath = None

    @property
    def workflow_for_json(self):
        """
        workflow object to json
        """
        return self.workflow.for_json()

    def load_workflow(self,jsonWorkflow):
        """
        docstring
        """
        try:
            with open(jsonWorkflow,"r") as jsonFile:
                currentWF = json.load(jsonFile)
        except:
            try:
                currentWF = json.loads(jsonWorkflow)
            except:
                err_msg="ERROR: json workflow must be json file or string not {}".format(type(jsonWorkflow))
                raise Exception(err_msg)
        for key, val in currentWF.items():
            self.workflow[key] = val
    
    def saveAs(self,filepath):
        """
        save workflow as a json file
        ----------------------------
        filepath: string, file path including file name and extension
        """
        with open(filepath,'w') as jsonFile:
            json.dump(self.workflow.for_json(),jsonFile,indent=4)
        self.filepath = filepath
    
    def save(self):
        """
        docstring
        """
        if not self.filepath:
            err_msg = "ERROR: filepath attribute of JsonWorkflow instance is not set, saveAs function should be use"
            raise Exception(err_msg)
        
        with open(self.filepath,'w') as jsonFile:
            json.dump(self.workflow.for_json(),jsonFile,indent=4)

        #self.saveAs(self.filepath)     

