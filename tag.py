import boto3



ec2 = boto3.client('ec2')
s3 = boto3.client('s3')


def tag_resources(service, resources, tags):
    for resource in resources:
        try:
            service.create_tags(Resources=[resource], Tags=tags)
            