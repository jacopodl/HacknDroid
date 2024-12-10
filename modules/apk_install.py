import subprocess
import re
import os
from modules import utility
from modules.tasks_management import Task

def install_from_apk(user_input):
    apk_path = utility.valid_apk_file(user_input)

    # Open ADB shell
    command = ['adb' ,'install' , user_input]
    print(command)
    output, error = Task().run(command)
    print(output)


def install_from_playstore(user_input):
    app_id = utility.get_valid_playstore_app_id(user_input)

    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'start' ,'-a' ,'android.intent.action.VIEW' ,'-d' , f"market://details?id={app_id}"]
    output, error = Task().run(command)


def uninstall_app(user_input):
    app_id = utility.app_id_from_user_input(user_input)

    # Open ADB shell
    command = ['adb' ,'uninstall' , app_id]
    output, error = Task().run(command)