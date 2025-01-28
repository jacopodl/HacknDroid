import subprocess
import re
import os
from modules import utility
from modules.tasks_management import Task

def install_from_apk(user_input):
    """
    Install an APK file on the mobile device.

    Args:
        user_input (str): The path to the APK file.
    """
    # Verify if the apk path is valid and related to an existing APK file
    apk_path = utility.valid_apk_file(user_input)

    # Install the APK on the mobile device
    command = ['adb' ,'install' , user_input]
    output, error = Task().run(command)
    print(output)


def install_from_playstore(user_input):
    """
    Install an application from the Google Play Store on the mobile device.

    Args:
        user_input (str): The App ID of the application to install.
    """
    # Verify if the App ID provided by user is valid
    app_id = utility.get_valid_playstore_app_id(user_input)

    # Create intent to open Play Store
    command = ['adb' ,'shell' ,'am' ,'start' ,'-a' ,'android.intent.action.VIEW' ,'-d' , f"market://details?id={app_id}"]
    output, error = Task().run(command)


def uninstall_app(user_input):
    """
    Uninstall an application from the mobile device.

    Args:
        user_input (str): The App ID of the application to uninstall.
    """
    # Verify if the App ID is related to an installed application 
    app_id = utility.app_id_from_user_input(user_input)

    # Uninstall the application on the mobile device
    command = ['adb' ,'uninstall' , app_id]
    output, error = Task().run(command)