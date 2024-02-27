import os
import sys
import subprocess

'''
def submit_jobs(folder_path):
    - folder_path: folder of job.sh's
'''
def submit_jobs(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate through each file
    for file in files:
        # Check if the file is a job script (ends with .sh)
        if file.endswith('.sh'):
            # Construct the full path to the job script
            job_script_path = os.path.join(folder_path, file)

            # Execute sbatch on the job script
            subprocess.run(['sbatch', job_script_path])

if __name__ == "__main__":
    # Check if the path argument is provided
    if len(sys.argv) != 2:
        print("Usage: python3 submit_jobs.py <folder_path>")
        sys.exit(1)

    # Extract the folder path from command-line arguments
    folder_path = sys.argv[1]

    # Verify if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    # Submit jobs
    submit_jobs(folder_path)

'''
1. Set up 3 local folders:
    - Folder containing csv's.
    - Folder containing job.sh's: create_job_scripts()
    - Folder for resulting out's
    
2. Set up 3 remote folders:
    - Folder to contain csv's
    - Folder to contain job.sh's
    - Folder for resulting out's

3. Upload folder containing csv's to server: upload_folder_to_server()
4. Upload folder containing job.sh's: upload_folder_to_server()
5. SBATCH all job.sh's: submit_jobs.py
6. Download resulting out's: download_folder_from_server()
'''