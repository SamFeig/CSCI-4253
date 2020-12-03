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

def create_snapshot(compute, project, zone, existing_vm_name, snapshot_name, labelFingerprint):
    snapshot_body =     {
        "name": snapshot_name,
        "labelFingerprint": labelFingerprint,
        "storageLocations": [
            "us-west1"
        ]
    }
    return compute.disks().createSnapshot(project=project, zone=zone, disk=existing_vm_name, body=snapshot_body).execute()

def create_snapshot_image(compute, project, zone, snapshot_name, labelFingerprint):
    image_snapshot_body = {
        "name": snapshot_name,
        "sourceSnapshot": "global/snapshots/%s"%(snapshot_name),
        "labelFingerprint": labelFingerprint
    }
    return compute.images().insert(project=project, body=image_snapshot_body).execute()

# Pulled from GCP programming tutorial as suggested: compute/api/create_instance.py
# [START create_instance]
def create_instance(compute, project, zone, name, bucket):
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-1804-lts').execute()
    source_disk_image = "global/snapshots/base-snapshot-demo-instance"

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup_script.sh'), 'r').read()
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
                    'sourceSnapshot': source_disk_image,
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
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation, type="zone"):
    print('Waiting for operation to finish...')
    while True:
        result = None
        if type == "zone":
            result = compute.zoneOperations().get(
                project=project,
                zone=zone,
                operation=operation).execute()
        else:
            result = compute.globalOperations().get(
                project=project,
                operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)


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
    instances = list_instances(service, args.project_id, 'us-west1-b')
    no_of_clones = 3
    network_target="allow-5000"

    if instances:
        for instance in instances:
            print('Creating snapshot of compute VM :', instance['name'])

            snapshot_name = "base-snapshot-"+instance['name']
            operation = create_snapshot(service, args.project_id, args.zone, instance['name'], snapshot_name, instance['labelFingerprint'])
            wait_for_operation(service, args.project_id, args.zone, operation['name'])
            operation = create_snapshot_image(service, args.project_id, args.zone, snapshot_name, instance['labelFingerprint'])
            wait_for_operation(service, args.project_id, args.zone, operation['name'], "global")

            for i in range(0, no_of_clones):
                start_time = time.time()
                instance_name = "%s-%d" % (instance['name'], i)
                operation = create_instance(service, args.project_id, args.zone, instance_name, snapshot_name)
                wait_for_operation(service, args.project_id, args.zone, operation['name'])
                print("--- Clone %d took %s seconds ---" % (i, time.time() - start_time))
            result_instances = list_instances(service, args.project_id, args.zone)
            
            if result_instances:
                for result_instance in result_instances:
                    add_firewall_rule_to_compute_node(args.project_id, args.zone, result_instance['name'], network_target, result_instance['tags']['fingerprint'])
   
# [END run]