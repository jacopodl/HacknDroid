"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import os
from modules import utility
import shutil
from modules.tasks_management import Task

def merge_from_dir(user_input):
    """
    Merge APK files from a specified directory.

    Args:
        user_input (str): The path to the directory containing APK files.

    Returns:
        str: The name of the merged APK file.
    """
    # Check if the directory exists
    while not os.path.exists(user_input):
        user_input = input("Insert an existing folder path:\n")

    # Generate the name for the merged APK file
    apk_name = "merged_"+utility.rsc_from_path(user_input)+".apk"

    # Command to merge APK files
    # -f: force overwrite of output APK file
    command = [f'APKEditor','m',"-f","-i", user_input, "-o", apk_name]
    print(command)
    output, error = Task().run(command, is_shell=True)

    return apk_name

def merge_from_list(user_input):
    """
    Merge a list of APK files.

    Args:
        user_input (str): A space-separated list of APK file paths.

    Returns:
        str: The name of the merged APK file.
    """
    check = True
    apks = user_input.split(" ")       

    # Check if the APK files exist on the system
    check = utility.is_apk_on_system(apks)

    while not check:
        user_input = input("Provide a valid list of apks paths on your system:\n")
        apks = user_input.split(" ")
        check = utility.is_apk_on_system(apks)

    # Create a temporary directory for merging APK files
    os.makedirs(".tmp_merge_apks", exist_ok=True)

    # Copy APK files to the temporary directory
    for f in apks:
        shutil.copy(f,".tmp_merge_apks")

    # Merge APK files from the temporary directory
    apk_name = merge_from_dir(".tmp_merge_apks")

    # Remove the temporary directory
    shutil.rmtree(".tmp_merge_apks")
    return apk_name