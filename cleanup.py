import subprocess

def prune_docker_system():
    try:
        subprocess.run(["docker", "system", "prune", "-af"], check=True)
        print("Docker system prune completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Docker system prune failed.")

if __name__ == "__main__":
    prune_docker_system()
