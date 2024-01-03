import pulumi
from pulumi_aws import s3
from pulumi_aws import *
import pulumi_aws as aws
# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)


bucketObject = s3.BucketObject('index.html', bucket=bucket.id,source=pulumi.FileAsset('./index.html'))  

print("ec2")
ubuntu = aws.ec2.get_ami(most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])
web = aws.ec2.Instance("web",
    ami=ubuntu.id,
    instance_type="t3.micro",
    tags={
        "Name": "HelloWorld",
    })
