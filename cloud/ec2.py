import csv
import boto3

region_name = 'af-south-1'

def get_ec2_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.all()
    
    return instances

def get_target_groups():
    elbv2 = boto3.client('elbv2')
    target_groups = elbv2.describe_target_groups()['TargetGroups']
    
    return target_groups

def main():
    # Get EC2 instances
    ec2_instances = get_ec2_instances()

    # Get Target Groups
    target_groups = get_target_groups()

    # Create a CSV file to store the results
    with open('aws_resources.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Resource Type', 'ID', 'Name', 'Protocol', 'Port', 'VPC ID'])

        # Write EC2 instances to CSV
        for instance in ec2_instances:
            instance_id = instance.id
            instance_name = ''
            
            # Get the instance name (if it has a 'Name' tag)
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break

            writer.writerow(['EC2', instance_id, instance_name, '', '', ''])

        # Write Target Groups to CSV
        for tg in target_groups:
            tg_arn = tg['TargetGroupArn']
            tg_name = tg['TargetGroupName']
            tg_protocol = tg['Protocol']
            tg_port = tg['Port']
            tg_vpc_id = tg['VpcId']

            writer.writerow(['Target Group', tg_arn, tg_name, tg_protocol, tg_port, tg_vpc_id])

    print('CSV file created: aws_resources.csv')

if __name__ == '__main__':
    main()
