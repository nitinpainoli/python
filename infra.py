import os
import subprocess
import sys

print("Installing eksctl")
cmd = 'ls -la'
os.system(cmd)




def install_eksctl():
    install_dir = "/usr/local/bin"
    cmd2_result = subprocess.run(["uname", "-s"], stdout=subprocess.PIPE, text=True)
    cmd2_stdout = cmd2_result.stdout.strip()  

    eksctl_url = f"https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_{cmd2_stdout}_amd64.tar.gz"
 
    eksctl_path = os.path.join(install_dir, "eksctl")

    try:
        subprocess.run(["curl", "-Lo", eksctl_path, eksctl_url], check=True)

        subprocess.run(["tar", "-xvzf", eksctl_path], check=True)

        subprocess.run(["chmod", "+x", eksctl_path], check=True)

        subprocess.run(["mv", "eksctl", eksctl_path], check=True)

        print("eksctl installed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def install_kubectl():
    install_dir = "/usr/local/bin"

    kubectl_url = "https://dl.k8s.io/release/v1.28.2/bin/linux/amd64/kubectl" 
    kubectl_path = os.path.join(install_dir, "kubectl")
    print(kubectl_path)
    try:
        subprocess.run(["curl", "-Lo", kubectl_path, kubectl_url], check=True)


        subprocess.run(["chmod", "+x", kubectl_path], check=True)


        print("kubectl installed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def install_aws():
    try:

    # Install AWS CLI v2 using the official installer script
        install_command = ["curl", "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip", "-o", "awscliv2.zip"]
        subprocess.run(install_command, check=True)

        # Unzip the installer
        unzip_command = ["unzip", "awscliv2.zip"]
        subprocess.run(unzip_command, check=True)

        # Run the installation script
        install_script = ["./aws/install"]
        subprocess.run(install_script, check=True)

        # Verify the installation
        verify_command = ["aws", "--version"]
        result = subprocess.run(verify_command, stdout=subprocess.PIPE, text=True)

        # Print the AWS CLI version
        print("AWS CLI v2 has been successfully installed.")
        print("AWS CLI Version:", result.stdout.strip())

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# def configure_aws_auth():
#     if len(sys.argv) != 3:
#         print("Usage: python script.py <cluster_name> <region>")
#         return

#     cluster_name = sys.argv[1]
#     region = sys.argv[2]

#     arn = "arn:aws:iam::825727885535:role/internal_aws_media_production_3762_TTN-AdminUser"
#     username = "cicd"
#     group = "system:masters"

#     cmd = [
#         "eksctl",
#         "create",
#         "iamidentitymapping",
#         "--cluster",
#         cluster_name,
#         "--region",
#         region,
#         "--arn",
#         arn,
#         "--username",
#         username,
#         "--group",
#         group,
#         "--no-duplicate-arns",
#     ]
    
#     cmd2 = [
#         "aws",
#         "eks",
#         "update-kubeconfig",
#         "--name",
#         cluster_name,
#         "--region",
#         region,
#     ]

#     try:
#         subprocess.run(cmd, check=True)
#         print("AWS authentication configured successfully.")

#         subprocess.run(cmd2, check=True)
#         print("kubectl configured successfully.")

#     except subprocess.CalledProcessError as e:
#         print(f"Error configuring AWS authentication: {e}")


install_eksctl()
install_kubectl()
install_aws()
# configure_aws_auth()

mongodb:x:114:65534::/home/mongodb:/usr/sbin/nologin