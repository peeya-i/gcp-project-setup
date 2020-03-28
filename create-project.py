from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

project_body = {
    "projectId": project_id,
  "name": project_id,
}

# Check whether the project exists. Create if it isn't.
try: response = service.projects().get(projectId=project_id).execute()
except:
  request = service.projects().create(body=project_body).execute()
  # The wait allows the creation to propagate through before proceeding to the next step
  !sleep 2
  response = service.projects().get(projectId=project_id).execute()
pprint( response )
