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

def attach_volume(instance_id, snapshot_id, device_name, region, availability_zone):
    ec2_client = boto3.client('ec2')
    volume_id = create_volume_from_snapshot(snapshot_id, region, availability_zone)
    try:
        response = ec2_client.describe_volumes(VolumeIds=[volume_id])
        attachments = response['Volumes'][0]['Attachments']
        if attachments:
            print("Volume is already attached. Detaching...")
            ec2_client.detach_volume(VolumeId=volume_id)
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
            VolumeId=volume_id,
        )
        print("Volume attached successfully:", response)
    except Exception as e:
        print("Error attaching volume:", e)



def main():
    volume_id = 'vol-067d413e4bc8fcae7'
    region = 'ap-southeast-1'
    availability_zone = 'ap-southeast-1b'

    snapshot_id = create_snapshot(volume_id, region)

    if snapshot_id:
        volume_id = create_volume_from_snapshot(snapshot_id, region, availability_zone)
        if volume_id:
            print("Volume created successfully:", volume_id)
        else:
            print("Failed to create volume from snapshot.")
    else:
        print("Failed to create snapshot.")

    instance_id = 'i-0ed4ac5b495eac69e	'
    device_name = '/dev/xvdf'  
    attach_volume(instance_id, snapshot_id, device_name, region, availability_zone)

if __name__ == "__main__":
    main()
