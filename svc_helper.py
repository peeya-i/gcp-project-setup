# Dictionary of services as key and commands to list out the names of the instances
# of the servicesand delete the services in the project.
# TO DO: Add more services that costs money to the list
# Legends: ### I don't think there is anything to do
#          #$$ Control by enabling or disabling API
#          #?? I don't know
#          #** Special cases

from subprocess import PIPE, Popen

svc_cmds = {
  #??  'ANTHOS': ['list', 'delete'],

  #?? App Engine: domain-mappings, firewall-rules, region, services, ssl-certificates
  'APPENG': ['gcloud app instances list',
             #gcloud app instances delete INSTANCE --service=SERVICE, -s SERVICE --version=VERSION, -v VERSION
             ''],

  # Compute Engine: These are some of the common services. There are more to be explored.
  # Try to cover some of those in the Assets listing
  'INST_GRPM': ['gcloud compute instance-groups managed list',
                'gcloud compute instance-groups managed delete {1} --{3}={2} --quiet'],
  'INST_GRPU': ['gcloud compute instance-groups unmanaged list',
                'gcloud compute instance-groups unmanaged delete {1} --zone={2} --quiet'],
  'INST_TEMP': ['gcloud compute instance-templates list',
                'gcloud compute instance-templates delete {1} --quiet'],
  'INST_HLTH': ['gcloud compute health-checks list',
                'gcloud compute health-checks delete {1} --global --quiet'],

  # TPUs does not appear in Assets or Resources listing. It requires us to specify the zone to get a response.
  # currently only available in zones: us-central1-a,b,c europe-west1-a and asia-east1-c
  'TPUS': ['gcloud compute tpus list --zone=us-central1-a',
           'gcloud copmute tpus delete {1} --zone={2} --quiet'],

  # Kubernetes Engine: services that do not require deletion
  #     images [can be obtained using repositories]
  #     node-pools [to manipulate node-pools in a cluster]
  #     subnets list-usable [list usable subnets to create clusters]
  'GKE': ['gcloud container clusters list',
          'gcloud container clusters delete {1} --zone {2} --quiet'],

  # Cloud Functions
  'FUNCTION': ['gcloud functions list',
               'gcloud functions delete {1} --quiet'],
  
  # Cloud run:
    'CLOUDRUNF': ['gcloud run services list --platform=managed --region={0}',
                'gcloud run services delete {2} --platform=managed --region={3} --quiet'],
  # Below are cloud run for GKE and Anthos. They are not tested
#  'CLOUDRUNG': ['gcloud run services list --platform=gke --cluster={} #NEED CLUSTER DEFINED',
#                'gcloud run services delete {x} --platform=gke --cluster={} --quiet'],
#  'CLOUDRUNK': ['gcloud run services list --platform=kubernetes #NEED TO read file [/root/.kube/config]',
#                'gcloud run services delete {x} --platform=kubernetes --quiet'],

  # Bigtable: instances,
  #	  not needed: clusters specify specific clusters in an instances
  'BIGTABLE': ['gcloud bigtable instances list',
               'gcloud bigtable instances delete {1} --quiet'],

  #?? Datastore/Firestore
  # When trying to delete by disableing API, the following MSG:
  # FAILED_PRECONDITION: The service datastore.googleapis.com is depended on by the following active service: cloudapis.googleapis.com

  # Filestore
  'FILESTORE': ['gcloud filestore instances list',
                'gcloud filestore instances delete {1} --zone {2} --quiet'],

  # GCS: Get the list of buckets before the code makes any changes.
  'STORAGE': ['echo & gsutil ls',
              'gsutil rm -r {1}'],

  # Cloud SQL
  'SQL': ['gcloud sql instances list',
          'gcloud sql instances delete {1}'],

  # Spanner
  'SPANNER': ['gcloud spanner instances list',
              'gcloud spanner instances delete {1}'],

  #** Memorystore: To list the instances, you have to specify the region
  # gcloud config set redis/region us-central1 OR
  # gcoud redis instances list region --region=
  # This example fixed at us-central1
  'MEMSTORE': ['gcloud redis instances list region --region={0}',
               'gcloud redis instances delete {1} --quiet'],

  ### Data Transfer: This is a one-time transfer service 

  # VPC Network => External IP address reservation
  'ADDRESSES': ['gcloud compute addresses list',
                'gcloud compute addresses delete {1} --region={4} --quiet'],

  # Network Services: Load balancing, Cloud DNS, Cloud CDN, Traffic Director, Service Directory
  # Hybrid Connectivity: VPN, Interconnect, Cloud Routers
  # Network Service Tiers
  # Network Security: Cloud Armor, SSL Policies
  # Netowrk Intelligence: Network Topology, Connectivity Tests, Perf Dash, Firewall Insights

  ### Cloud Build: Build the following services: Functions, Run, App Engine, Kubernetes Engine,
  #   Compute Engine, Firebase, Cloud KMS, Service Accounts
  # It appears that once built is completed, there is no on-going charges

  #?? Cloud Tasks: App Engine task creation and monitoring tool

  #?? Container Registry
  'CNTREG': ['',
             ''],

  # Artifact Registry
  # Cloud Scheduler
  # Deployment Manager
  # Endpoints
  # Identity Platform
  # Source Repositories
  # Privat Catalog: Catalog of approved services.
  # Composer


  # Dataproc: Use Region as part of the command, but the reply comes back with
  # zone information.
  'DATAPROC': ['gcloud dataproc clusters list --region={0}',
               'gcloud dataproc clusters delete {1} --region={0} --quiet'],

  # Pubsub: Topics and subscriptions must be deleted separately.
  'PUBSUB_T': ['gcloud pubsub topics list --flatten=name --format=list',
               'gcloud pubsub topics delete {2} --quiet'],
  'PUBSUB_S': ['echo & gcloud pubsub subscriptions list --flatten=name --format=list',
               'gcloud pubsub subscriptions delete {2}'],

  # Dataflow

  #?? IoT Core: The devices in the iot registries must be deleted first before the 
  # can be deleted.
  'IOTCORE': ['gcloud iot registries list --region={0}',
              'gcloud iot registries delete {1} --region={0} --quiet'],

  # BigQuery
  # *** Data Catalog: Data Catalog allows you to discover, manage, and understand data assets across Google Cloud Platform.
  #     Data Catalog API natively indexes Cloud BigQuery, Cloud Storage, and Cloud Pub/Sub data assets.
  # Cloud Data Fusion is a fully-managed, cloud native, enterprise data integration service
  #     for quickly building and managing data pipelines.

  # Dataprep

  # AI Platform: AI Hub, Notebooks, Jobs, Models

  #$$ Natural Language: When AutoML is used, Google is only charging for training time
  # and number of translation requested. Control by disabling API

  #$$ Recommendations AI: recommendationengine.googleapis.com Disable API

  # Tables: Datasets, Models

  #$$ Talent Solution: Control by disabling API

  #$$ Translation: Datasets, Models charges? Google is only charging for training time
  # and number of translation requested. Control by disabling API

  #$$ Vision: Datasets, Models. hen AutoML is used, Google is only charging for training time
  # and number of translation requested. Control by disabling API

  #$$ Video Intelligence: It is a callable servie. Nothing to delete

  # API: APIs enabled at the time of this scan. We want to put API last. If disabled
  # too soon, commands to cleanup newly created resources may not work
  'APIS': ['gcloud services list --enabled',
           'gcloud services disable {1} --async']
}

# Parameter:
#  svc_cmds => Dictionary of service names, commands to list the instances,
#              and commands to delete the instances
#  region   => Region for some of region bound instances
def get_svc_en( svc_cmds, region ):
  svc_list = {}

  for key in svc_cmds:
    print("LIST: ", key, "=> ", svc_cmds[key][0].format(region))
    response, stderr = Popen(svc_cmds[key][0].format(region), shell=True, stdout=PIPE, stderr=PIPE).communicate()
    names = [[l.split() for l in response.decode(encoding="utf-8").split('\n')[1:-1]]]
    svc_list.update({key : names})
    svc_list[key].append( [response.decode(encoding="utf-8"), stderr.decode(encoding="utf-8")] )

  return svc_list

# Parameter:
#  svc_cmds => Dictionary of service names, commands to list the instances,
#              and commands to delete the instances
#  region   => Region for some of region bound instances
#  svc_start => List of instances before the the code starts
#  svc_end   => List of instances after the code finishes executing          
def del_svc( svc_cmds, region, svc_start, svc_end ):
  # Iterate through different types services
  for key in svc_cmds:
    # Iterate through each instances of the service
    for inst in range(len(svc_end[key][0])):
      print("CHECK: ", key, "=> ", svc_cmds[key][1].format(region, *svc_end[key][0][inst]))
      if svc_end[key][0][inst] not in svc_start[key][0]:
        print('DEL: ', svc_cmds[key][1].format(region, *svc_end[key][0][inst]))
        response, stderr = Popen(svc_cmds[key][1].format(region, *svc_end[key][0][inst]), shell=True, stdout=PIPE, stderr=PIPE).communicate()
        svc_end[key].append( [response.decode(encoding="utf-8"), stderr.decode(encoding="utf-8")] )
  return svc_end
