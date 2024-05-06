import boto3
import time

def wait_for_snapshot_completion(snapshot_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    while True:
        response = ec2.describe_snapshots(SnapshotIds=[snapshot_id])
        snapshot_status = response['Snapshots'][0]['State']
        if snapshot_status == 'completed':
            break
        print("Snapshot is still pending. Waiting...")
        time.sleep(30)  

def create_snapshot(volume_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    try:

        response = ec2.create_snapshot(
            Description=f'Snapshot of instance {volume_id}',
            VolumeId=volume_id
        )
        snapshot_id = response['SnapshotId']
        print("Snapshot created:", snapshot_id)
        return snapshot_id
    except Exception as e:
        print("Error creating snapshot:", e)

def create_volume_from_snapshot(snapshot_id, region, availability_zone):
    ec2 = boto3.client('ec2', region_name=region)

    wait_for_snapshot_completion(snapshot_id, region)

    try:
        response = ec2.create_volume(
            SnapshotId=snapshot_id,
            AvailabilityZone=availability_zone,
            Encrypted=True,
            KmsKeyId='2a697cea-a4d2-4434-bbcd-124369ec3481'
        )
        volume_id = response['VolumeId']
        print("Volume created from snapshot:", volume_id)
        return volume_id
    except Exception as e:
        print("Error creating volume from snapshot:", e)


def instance_stop(instance_id, region):
    ec2_client = boto3.client('ec2')
    ec2_client.stop_instances(InstanceIds=[instance_id])
    print("Instance is stopping...")
    waiter = ec2_client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])




def attach_volume(instance_id, volume_id, device_name, region, availability_zone, volume_id_new):
    ec2_client = boto3.client('ec2')
 
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    if state == 'stopped':
        try:
            
            print(volume_id)
            response = ec2_client.describe_volumes(VolumeIds=[volume_id])
            attachments = response['Volumes'][0]['Attachments']
            
            instance_info = ec2_client.describe_instances(InstanceIds=[instance_id])

            if attachments:
                root_volume = [volume for volume in instance_info['Reservations'][0]['Instances'][0]['BlockDeviceMappings'] if volume['DeviceName'] == '/dev/xvda'][0]
                root_volume_id = root_volume['Ebs']['VolumeId']
                ec2_client.detach_volume(VolumeId=root_volume_id)
                
                print("Volume detached successfully.")
            while True:
                response = ec2_client.describe_volumes(VolumeIds=[volume_id])
                volume_state = response['Volumes'][0]['State']
                if volume_state == 'available':
                    break
                print("Volume is not available. Waiting...")
                time.sleep(30)

            response = ec2_client.attach_volume(
                Device=device_name,
                InstanceId=instance_id,
                VolumeId=volume_id_new,
            )
            print("Volume attached successfully:", response)
        except Exception as e:
            print("Error attaching volume:", e)
   
def main():
    instance_id = 'i-0ed4ac5b495eac69e'
    device_name = '/dev/xvda'  
    volume_id = 'vol-067d413e4bc8fcae7'
    region = 'ap-southeast-1'
    availability_zone = 'ap-southeast-1b'
    


    snapshot_id = create_snapshot(volume_id, region)
    print(snapshot_id)

    if snapshot_id:
        volume_id_new = create_volume_from_snapshot(snapshot_id, region, availability_zone)
        if volume_id_new:
            print("Volume created successfully:", volume_id_new)
        else:
            print("Failed to create volume from snapshot.")
    else:
        print("Failed to create snapshot.")


    instance_stop(instance_id, region)
    
    
    attach_volume(instance_id, volume_id, device_name, region, availability_zone,volume_id_new)


if __name__ == "__main__":
    main()
