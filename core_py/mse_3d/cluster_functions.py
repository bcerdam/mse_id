import os
import paramiko

'''
download_folder_from_server(): Downloads contents from a given folder in PUC cluster.
    - username: Self explanatory
    - ssh_path: Self explanatory
    - password: Self explanatory
    - remote_folder: Path of folder on the cluster.
    - local_path: Path where to store it.
'''
def download_folder_from_server(username, ssh_path, password, remote_folder, local_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=ssh_path, username=username, password=password)
        sftp_client = ssh_client.open_sftp()
        sftp_client.chdir(remote_folder)
        files = sftp_client.listdir()
        local_folder = os.path.join(local_path, os.path.basename(remote_folder))
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        for file in files:
            remote_file = os.path.join(remote_folder, file)
            local_file = os.path.join(local_folder, file)
            sftp_client.get(remote_file, local_file)

        sftp_client.close()
        ssh_client.close()

        print(f"Folder '{remote_folder}' downloaded to '{local_folder}'")
    except Exception as e:
        print(f"Error: {e}")


'''
upload_folder_to_server(): Uploads CONTENT of local folder to a given path (folder) on the cluster.
    - username: Username for SSH connection.
    - ssh_path: SSH address of the cluster.
    - password: Password for SSH connection.
    - local_folder: Path of the local folder that has the CONTENT to upload.
    - remote_path: Path of folder where to upload the CONTENTS on the cluster.
'''


def upload_folder_to_server(username, ssh_path, password, local_folder, remote_path):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=ssh_path, username=username, password=password)
        sftp_client = ssh_client.open_sftp()

        # Create the remote directory if it doesn't exist
        try:
            sftp_client.chdir(remote_path)
        except IOError:
            sftp_client.mkdir(remote_path)
            sftp_client.chdir(remote_path)

        # Upload the entire folder recursively
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_file = os.path.join(root, file)
                remote_file = os.path.join(remote_path, os.path.relpath(local_file, local_folder))
                sftp_client.put(local_file, remote_file)

        sftp_client.close()
        ssh_client.close()

        print(f"Folder '{local_folder}' uploaded to '{remote_path}' on the cluster")
    except Exception as e:
        print(f"Error: {e}")

        print(f"Folder '{local_folder}' uploaded to '{remote_path}' on the cluster")
    except Exception as e:
        print(f"Error: {e}")
