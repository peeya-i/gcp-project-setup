def set_billing(bac_id, project_id)
    from googleapiclient import discovery
    from subprocess import PIPE, Popen
    import os

    name = 'projects/' + project_id 
    service = discovery.build('cloudbilling', 'v1',  cache_discovery=False)
    billing_request = service.projects().updateBillingInfo(name=name,
                              body={"billingAccountName": "billingAccounts/"+bac_id, 
                                    "billingEnabled": True})
    billing_response = billing_request.execute()

    return billing_response
