# Check and create project as needed. Return the status of the project
# Failed => Fail to setup project
# Sandbox => The environment is a sandbox project creation is not needed
# Created => Project was created
# Existing => Existing project that will require resources removal at the end
def prj_setup( project_id='prj_id' ):
    from pprint import pprint

    from googleapiclient import discovery
    from oauth2client.client import GoogleCredentials
    import os

    ret_msg = 'Failed'       # return message set to failed before processing

    response = os.popen("gcloud config set project {}".format(project_id)).read()
    # Check whether the user has authenticated with GCP
    billing = os.popen("gcloud alpha billing accounts list").read()

    if "WARNING" in response:
        print(response)

    elif "ERROR" in billing:
        print("You need to authenticate with GCP first.\n")

    elif "Listed 0 items." in billing:
        print("The GCP environment is a sandbox or lab environment. Project creation is not needed.\n")
        ret_msg = 'Sandbox'

    else:
        os.environ['DEVSHELL_PROJECT_ID'] = project_id
        os.environ['PROJECT'] = project_id

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
                os.popen("sleep 2")
                ret_msg = 'Created'

        else:
            ret_msg = 'Existing'

        pprint( response )

    return ret_msg

# Get the UTC time in the format used by 'gcloud alpha resources
def get_utc():
    from datetime import datetime

    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
