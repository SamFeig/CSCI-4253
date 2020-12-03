#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth

credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

# Pulled from GCP programming tutorial as suggested: compute/api/create_instance.py
# [START create_instance]
def create_instance(compute, project, zone, name, bucket):
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-1804-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup_script.sh'), 'r').read()
    startup_script_remote = open(
        os.path.join(
            os.path.dirname(__file__), 'startup_script_remote.sh'), 'r').read()
    service_credentials = open(
        os.path.join(
            os.path.dirname(__file__), 'service-credentials.json'), 'r').read()
    part3 = open(
        os.path.join(
            os.path.dirname(__file__), 'part3.py'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, { #Add metadata needed for part3 and transfer files to vm1
                'key': 'startup-script-remote',
                'value': startup_script_remote
            }, {
                'key': 'service-credentials',
                'value': service_credentials
            }, {
                'key': 'part3',
                'value': part3
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

def create_firewall_rule(project):
    target = "allow-5000"
    firewall_body =     {
        "name": target,
        "sourceRanges": [
            "0.0.0.0/0"
        ],
        "targetTags": [
            target
        ],
        "allowed": [
            {
            "IPProtocol": "tcp",
            "ports": [
                "5000"
            ]
            }
        ]
    }
    try:
        request = service.firewalls().insert(project=project, body=firewall_body)
        response = request.execute()
    except Exception as e:
        print('Count not create firewall rule. Check if the rule already exists')
        pass
    
    return target

def add_firewall_rule_to_compute_node(project, zone, instance, target_tag, fingerprint):
    tags_body = {
        "items": [
            target_tag
        ],
        "fingerprint": fingerprint
    }
    request = service.instances().setTags(project=project, zone=zone, instance=instance, body=tags_body)
    response = request.execute()


# [START run]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', default='csci-4253', help='Your Google Cloud project ID.')
    parser.add_argument('bucket_name', default='csci4253bucket', help='Your Google Cloud Storage bucket name.')
    parser.add_argument(
        '--zone',
        default='us-west1-b',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    args = parser.parse_args()

    operation = create_instance(service, args.project_id, args.zone, args.name, args.bucket_name)
    wait_for_operation(service, args.project_id, args.zone, operation['name'])
    print("Your running instances are:")
    network_target = create_firewall_rule(args.project_id)
    instances = list_instances(service, args.project_id, 'us-west1-b')
    if instances:
        for instance in instances:
            add_firewall_rule_to_compute_node(args.project_id, args.zone, instance['name'], network_target, instance['tags']['fingerprint'])
            print(instance['networkInterfaces'][0]['accessConfigs'][0]['natIP'])
            print("Firewall rule added to instance", instance['name'])
    else:
        print("No instances present")
    
# [END run]