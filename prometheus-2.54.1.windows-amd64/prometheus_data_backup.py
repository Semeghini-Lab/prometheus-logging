import os
import shutil
import time
from datetime import datetime, timedelta

source = r"C:\\Users\data-analysis\\prometheus-logging\\prometheus-2.54.1.windows-amd64\\data"  # Local directory
target = r"\\192.168.0.174\\exp-data\\prometheus-data"  # NAS directory

def copy_to_nas(source_dir, nas_dir):
    """
    Copies files and directories from the last 24 hours from a local directory to a NAS directory.
    
    Args:
        source_dir (str): Local directory with files and directories.
        nas_dir (str): NAS directory (e.g., network path or mapped drive).
    """
    # Get the current time and time 24 hours ago
    now = time.time()
    cutoff_time = now - 24 * 60 * 60  # 24 hours in seconds

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory does not exist: {source_dir}")
        return  # Exit the function

    # Check if destination directory exists, create it if not
    if not os.path.exists(nas_dir):
        try:
            print(f"NAS directory does not exist, creating it: {nas_dir}")
            os.makedirs(nas_dir)
        except Exception as e:
            print(f"Failed to create NAS directory: {e}")
            return  # Exit the function if NAS directory cannot be created

    # Walk through the source directory
    for dirpath, dirnames, filenames in os.walk(source_dir):
        # Create corresponding destination directory structure
        relative_path = os.path.relpath(dirpath, source_dir)
        destination_dir = os.path.join(nas_dir, relative_path)
        
        if not os.path.exists(destination_dir):
            try:
                os.makedirs(destination_dir)
            except Exception as e:
                print(f"Error creating directory {destination_dir}: {e}")
                continue  # Skip this directory and continue to the next one

        # Copy files in this directory
        for file_name in filenames:
            full_file_name = os.path.join(dirpath, file_name)
            file_mod_time = os.path.getmtime(full_file_name)

            # Copy only files modified within the last 24 hours
            if file_mod_time >= cutoff_time:
                print(f"Copying {full_file_name} to {destination_dir}")
                try:
                    shutil.copy2(full_file_name, destination_dir)  # shutil.copy2 to preserve metadata
                except Exception as e:
                    print(f"Error copying {full_file_name}: {e}")
            else:
                print(f"Skipping {full_file_name}, it is older than 24 hours")
    
    # Indicate that the task is completed
    print("File copy operation completed successfully.")

# Run the function
copy_to_nas(source, target)

# Indicate that the program has ended
print("Program has finished executing.")
