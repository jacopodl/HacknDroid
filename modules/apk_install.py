"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import sys
from modules import utility
from modules.tasks_management import Task
from modules.adb import get_session_device_id
from modules.app_info import app_id_from_apk

def install_from_apk(user_input):
    """
    Install an APK file on the mobile device.

    Args:
        user_input (str): The path to the APK file.
    """
    # Verify if the apk path is valid and related to an existing APK file
    apk_path = utility.valid_apk_file(user_input)

    app_id = app_id_from_apk(apk_path)

    if utility.is_app_id(app_id):
        uninstall_app(app_id)
    else:
        return

    # Install the APK on the mobile device
    print(f"Installing {apk_path} on the device...", end=' ')
    sys.stdout.flush()
    command = ['adb', '-s', get_session_device_id(), 'install' , apk_path]
    output, error = Task().run(command)
    
    if "success" in output.lower():
        print("DONE")
    else:
        print("FAILED")


def install_from_playstore(user_input):
    """
    Install an application from the Google Play Store on the mobile device.

    Args:
        user_input (str): The App ID of the application to install.
    """
    # Verify if the App ID provided by user is valid
    app_id = utility.get_valid_playstore_app_id(user_input)

    if utility.is_app_id(app_id):
        print(f"Uninstalling {app_id} from the device...", end=' ')
        sys.stdout.flush()
        uninstall_app(app_id)
        print("DONE")
    else:
        return

    # Create intent to open Play Store
    print(f"Opening {app_id} on PlayStore...", end=' ')
    sys.stdout.flush()
    command = ['adb', '-s', get_session_device_id(), 'shell' ,'am' ,'start' ,'-a' ,'android.intent.action.VIEW' ,'-d' , f"market://details?id={app_id}"]
    output, error = Task().run(command)
    print("DONE")


def uninstall_app(user_input):
    """
    Uninstall an application from the mobile device.

    Args:
        user_input (str): The App ID of the application to uninstall.
    """
    # Verify if the App ID is related to an installed application 
    app_id = utility.app_id_from_user_input(user_input)

    # Uninstall the application on the mobile device
    print(f"Uninstalling {app_id} from the device...", end=' ')
    sys.stdout.flush()
    command = ['adb', '-s', get_session_device_id(), 'uninstall' , app_id]
    output, error = Task().run(command)
    print("DONE")