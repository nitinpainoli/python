import boto3

def get_instances_and_root_volumes(key, value):
    ec2 = boto3.client('ec2')

    response = ec2.describe_instances(Filters=[
        {'Name': f'tag:{key}', 'Values': [value]}
    ])

    instances_and_volumes = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            root_volume_id = None
            for block_device in instance['BlockDeviceMappings']:
                if block_device['DeviceName'] == instance['RootDeviceName']:
                    root_volume_id = block_device['Ebs']['VolumeId']
                    break
            
            instances_and_volumes.append({'InstanceID': instance_id, 'RootVolumeID': root_volume_id})

    return instances_and_volumes

key = 'Environment'
value = 'test'
instances_and_volumes = get_instances_and_root_volumes(key, value)
print(instances_and_volumes)
