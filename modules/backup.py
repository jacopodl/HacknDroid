from modules import utility
import subprocess
import os

def app_backup(user_input):
    app_id = utility.app_id_from_user_input(user_input)

    backup_name = "backup_"+app_id+".ab"
    command = ['adb','backup',"-apk","-f", backup_name, app_id]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process.communicate()


def device_backup(user_input):
    backup_name = "backup_device.ab"
    command = ['adb','backup',"-apk","-shared", "-all", "-f", backup_name]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process.communicate()


def restore_backup(user_input):
    if (not os.path.isfile(user_input)) or (not user_input.endswith(".ab")):
        user_input = input("Write the path of a valida Android Backup on your PC to be restored:\n")
    
    command = ['adb','restore',user_input]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process.communicate()


def app_data_reset(user_input):
    pass