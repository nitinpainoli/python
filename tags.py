import boto3
import openpyxl
# def ec2():
#     ec2_client = boto3.client('ec2', region_name='ap-southeast-1')
#     response = ec2_client.describe_instances()
#     untagged_instances = []
#     for reservation in response['Reservations']:
#         for instance in reservation['Instances']:
#             if 'Tags' not in instance:
#                 untagged_instances.append(instance['InstanceId'])
#             else:
#                 required_tag = False
#                 for tag in instance['Tags']:
#                     if tag['Key'] == 'Created By' and tag['Value'] == 'Terraform':
#                         required_tag = True
#                         break
#                 if not required_tag:  
#                     print("es")
#                     untagged_instances.append(instance['InstanceId'])
#     print(untagged_instances)

# ec2()



def ec2():
    ec2_client = boto3.client('ec2', region_name='ap-southeast-1')
    response = ec2_client.describe_instances()
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    print("all")
    print(instance_ids)
    response = ec2_client.describe_instances(Filters=[
        {'Name': 'tag:Environment', 'Values': ['test']}
    ])
    instance_tag = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_tag.append(instance['InstanceId'])
    print("tagged")
    print(instance_tag)

    for instance_id in  instance_ids:
        if instance_id not in instance_tag:
            print(instance_id)
    

ec2()
