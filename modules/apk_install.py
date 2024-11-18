import subprocess
import re
import os
from modules import utility


def install_from_apk(user_input):
    apk_path = utility.valid_apk_file(user_input)

    # Open ADB shell
    command = ['adb' ,'install' , user_input]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)

def install_from_playstore(user_input):
    app_id = utility.get_valid_playstore_app_id(user_input)

    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'start' ,'-a' ,'android.intent.action.VIEW' ,'-d' , f"market://details?id={app_id}"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()

def uninstall_app(user_input):
    app_id = utility.app_id_from_user_input(user_input)

    # Open ADB shell
    command = ['adb' ,'uninstall' , app_id]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()