import subprocess
import signal
from modules.utility import app_id_from_user_input
import time
import re
import os
import config

def app_crash_logs(user_input):
    pass


def all_crash_logs(user_input):
    '''
        Retrieve log from the application for further analysis
        Flush adb logcat content
        adb logcat -c
        Start ADB logcat (No restriction of the logs to the application because there can be other useful logs to be analysed)
        adb logcat  
        Run command on Android device using the default pre-installed monkey command
        adb shell monkey -p 'your package name' -v 500
        Check when the App was shutdown (if empty string, the app is not running)
        while True:
            adb shell pidof package_name
    '''
    # User input is an app ID or a list of keywords to identify the application 


    # Flush logs
    command = ['adb', 'logcat', '-c']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Take App ID
    app_id = app_id_from_user_input(user_input)

    pid=-1

    # Collect logs
    with open(f"{app_id}.log", "w") as f:
        command = ['adb', 'logcat', '*:E']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=f, text=True, shell=True)

        stdout, stderr = process.communicate()
    
    print(f"{app_id}.log")
    return app_id, pid


def app_logs(user_input):
    app_id, pid = all_logs(user_input)

    lines = []
    with open(f"{app_id}.log", "r") as fd:
        lines = fd.readlines()

    with open(f"{app_id}-bis.log", "w") as fd:
        for l in lines:
            if pid in l:
                fd.write(l)

    print('END')

        
def all_logs(user_input):
    '''
        Retrieve log from the application for further analysis
        Flush adb logcat content
        adb logcat -c
        Start ADB logcat (No restriction of the logs to the application because there can be other useful logs to be analysed)
        adb logcat  
        Run command on Android device using the default pre-installed monkey command
        adb shell monkey -p 'your package name' -v 500
        Check when the App was shutdown (if empty string, the app is not running)
        while True:
            adb shell pidof package_name
    '''
    # User input is an app ID or a list of keywords to identify the application 


    # Flush logs
    command = ['adb', 'logcat', '-c']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Take App ID
    app_id = app_id_from_user_input(user_input)

    pid=-1

    # Collect logs
    with open(f"{app_id}.log", "w") as f:
        command = ['adb', 'logcat']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=f, text=True, shell=True)

        pid = run_app_and_wait(app_id)

        #os.kill(process.pid, signal.SIGTERM)
        process.terminate()
        process.wait()
    
    print(f"{app_id}.log")
    return app_id, pid


def get_pid(app_id):
    command = ['adb', 'shell','pidof', app_id]
    process = subprocess.run(command, capture_output=True, text=True)

    if process.returncode == 0:
        return process.stdout.splitlines()[0]
    else:
        return -1

def run_app_and_wait(app_id):
    #Run command on Android device using the default pre-installed monkey command
    command = ['adb', 'shell','monkey', f"-p '{app_id}'", '-v 1']
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)
    pid = get_pid(app_id)

    if pid != -1:
        print(f"Process created with PID: {pid}")

    while True:
        cycle_pid = get_pid(app_id)

        if cycle_pid == -1:
            break

    return pid