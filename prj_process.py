# Check and create project as needed. Return the status of the project
# Failed => Fail to setup project
# Sandbox => The environment is a sandbox project creation is not needed
# Created => Project was created
# Existing => Existing project that will require resources removal at the end
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from subprocess import PIPE, Popen
import os
from pprint import pprint

def prj_setup( project_id='prj_id' ):
    # Set environment variables for the project
    os.environ['DEVSHELL_PROJECT_ID'] = project_id
    os.environ['PROJECT'] = project_id

    ret_msg = 'Failed'       # return message set to failed before processing

#    stdout, stderr = Popen("gcloud config set project {}".format(project_id),
#                           shell=True, stdout=PIPE, stderr=PIPE).communicate()
#    set_prj = (stderr + stdout).decode(encoding="utf-8")

    # Check whether the user has authenticated with GCP
    stdout, stderr = Popen("gcloud alpha billing accounts list",
                           shell=True, stdout=PIPE, stderr=PIPE).communicate()
    billing = (stderr + stdout).decode(encoding="utf-8")

#    if "WARNING" in set_prj:
#        print(set_prj)

#    elif "ERROR" in billing:
    if "ERROR" in billing:
        print("You need to authenticate with GCP first. Do not proceed until login is done.\n")

    elif "Listed 0 items." in billing:
        print("The GCP environment is a sandbox or lab environment. Project creation is not needed.\n")
        ret_msg = 'Sandbox'

    else:
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

        # Check whether the project exists. If it isn't, create it.
        try: response = service.projects().get(projectId=project_id).execute()
        except:
            try: response = service.projects().create(
                               body= { "projectId": project_id,
                                       "name": project_id }).execute()
                # The wait allows the creation to propagate through before proceeding to the next step
            except:
                print("Failed to create project. Please check the 'project_id' to make sure it is unique.\n")
            else:
                response = service.projects().get(projectId=project_id).execute()
                print("Project creation completed.\n")
                Popen("sleep 2", shell=True).communicate()
                ret_msg = 'Created'

        else:
            ret_msg = 'Existing'

        pprint( response )

    return ret_msg

from datetime import datetime
# Get the UTC time in the format used by 'gcloud alpha resources
def get_utc():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
