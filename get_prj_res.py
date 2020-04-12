def get_prj_res( fname ):
    import json
    from subprocess import PIPE, Popen

    !gcloud services enable cloudresourcemanager.googleapis.com
    !gcloud alpha resources list --format=json > {fname}

    # Enables the cloud resource manager API
    stdout, stderr = Popen("gcloud services enable cloudresourcemanager.googleapis.com",
                           shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if sterr != "
    en_crm = (stderr + stdout).decode(encoding="utf-8")

    # Test loading the JSON contents from the file
    with open( fname ) as file:
      rsc_json = json.load( file )

    return rsc_json
