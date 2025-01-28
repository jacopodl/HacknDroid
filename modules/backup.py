from modules import utility
import subprocess
import os
import zlib
import tarfile
from modules.tasks_management import Task

def app_backup(user_input : str):
    """
    Backup an application on the mobile device.

    Args:
        user_input (str): The App ID of the application to backup.
    """
    # Retrieve App ID from user input
    app_id = utility.app_id_from_user_input(user_input)

    # Create Backup file for the App ID specified as user input
    # adb backup -apk -f backup_<app_id>.ab <app_id>
    backup_name = "backup_"+app_id
    command = ['adb','backup',"-apk","-f", backup_name+".ab", app_id]
    print(command)
    output, error = Task().run(command, is_shell=True)

    # Convert backup file (comppressed file) as TAR file backup_<app_id>.tar 
    # and unpack it to a folder with name backup_<app_id>
    ab_to_tar_extract(backup_name)


def device_backup(user_input : str):
    """
    Backup the entire mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Backup of the device, including all data and apps
    backup_name = "backup_device"
    command = ['adb','backup',"-apk","-shared", "-all", "-f", backup_name+".ab"]
    print(command)
    output, error = Task().run(command, is_shell=True)

    # Convert backup file (comppressed file) as TAR file backup_<app_id>.tar 
    # and unpack it to a folder with name backup_<app_id>
    ab_to_tar_extract(backup_name)

def tar_extract(user_input : str):
    """
    Extract a TAR file from an Android Backup file.

    Args:
        user_input (str): The path to the Android Backup file.
    """
    # Ask again the AB file path if it doesn't exist or it hasn't AB extension
    if (not os.path.isfile(user_input)) or (not user_input.endswith(".ab")):
        user_input = input("Write the path of a valida Android Backup on your PC to be extracted:\n")
    
    # Collect the password of the Android Backup file from stdin
    password = input("Insert the password used on the mobile device for the backup:\n")
    # Unpack the Android Backup file using ABE and save it to <backup_name>.tar file
    tar_file = user_input.replace(".ab", ".tar")
    command = ['abe', 'unpack', user_input, tar_file, password]
    print(command)
    output, error = Task().run(command, is_shell=True)

    # Create the directory for the unpacked TAR file
    folder = user_input.replace(".ab", "")
    if not os.path.exists(folder):
        os.mkdir(folder)

    # Extract the TAR file in the destination folder 
    with tarfile.open(tar_file, "r") as tar:
        tar.extractall(path=folder)

    print(f"\nTAR Extracted in: {folder}")

def ab_to_tar_extract(backup_name):
    """
    Convert an Android Backup file to a TAR file and extract it.

    Args:
        backup_name (str): The name of the backup file.
    """
    # Collect the password of the Android Backup file from stdin
    password = input("Insert the password used on the mobile device for the backup:\n")
    # Unpack the Android Backup file using ABE and save it to <backup_name>.tar file
    command = ['abe', 'unpack', backup_name+".ab", backup_name+".tar", password]
    print(command)
    output, error = Task().run(command, is_shell=True)

    # Create the directory for the unpacked TAR file
    if not os.path.exists(backup_name):
        os.mkdir(backup_name)

    # Extract the TAR file in the destination folder 
    with tarfile.open(backup_name+".tar", "r") as tar:
        tar.extractall(path=backup_name)

    print(f"\nTAR Extracted in: {backup_name}")

def restore_backup(user_input):
    """
    Restore an Android Backup file on the mobile device.

    Args:
        user_input (str): The path to the Android Backup file.
    """
    # Ask again the AB file path if it doesn't exist or it hasn't AB extension
    if (not os.path.isfile(user_input)) or (not user_input.endswith(".ab")):
        user_input = input("Write the path of a valida Android Backup on your PC to be restored:\n")
    
    # Restore the AB file specified from the user 
    command = ['adb','restore',user_input]
    print(command)
    output, error = Task().run(command, is_shell=True)


def app_data_reset(user_input):
    """
    Reset the data of an application on the mobile device.

    Args:
        user_input (str): The App ID of the application to reset.
    """
    # Retrieve App ID from user input
    app_id = utility.app_id_from_user_input(user_input)
    
    # Reset App data for the application with App ID <app_id>
    command = ['adb','shell',"pm","clear",app_id]
    print(command)
    output, error = Task().run(command, is_shell=True)