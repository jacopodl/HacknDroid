import subprocess
import signal
from modules.utility import app_id_from_user_input, active_app_id_from_user_input
import time
import re
import os
import config.menu as menu
from modules.tasks_management import Task, DAEMONS_MANAGER, list_daemons
        
def logs_from_running_process(user_input):
    app_id = active_app_id_from_user_input(user_input)
    pid = get_pid(app_id)

    id = DAEMONS_MANAGER.get_next_id()
    DAEMONS_MANAGER.add_task('logging', track_running_logs, args=(app_id, pid, False, id))

    if pid != -1:
        print(f"\nProcess running with PID: {pid}")

    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'ALL'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)


def crash_logs_from_running_process(user_input):
    app_id = active_app_id_from_user_input(user_input)
    pid = get_pid(app_id)

    id = DAEMONS_MANAGER.get_next_id()
    DAEMONS_MANAGER.add_task('logging', track_running_logs, args=(app_id, pid, True, id))

    if pid != -1:
        print(f"\nProcess running with PID: {pid}")

    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'CRASH'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)


def track_running_logs(app_id, pid, crash_logs, id):
    file_name = f"{app_id}_{id}_all.log"
    
    if crash_logs:
        file_name = f"{app_id}_{id}_crash.log"

    # Collect logs
    with open(file_name, "w") as f:
        command = ['adb', 'logcat', f'--pid={pid}']

        if crash_logs:
            command = ['adb', 'logcat', f'--pid={pid}','*:E']

        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.DEVNULL)
        
        cycle_pid = pid
        print(cycle_pid)
        while cycle_pid==pid:
            cycle_pid = get_pid(app_id)
            time.sleep(2)


        #os.kill(process.pid, signal.SIGTERM)
        process.terminate()
        process.wait()

    DAEMONS_MANAGER.stop_task('logging', id)


def run_and_crash_logs(user_input):
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
    output, error = Task().run(command)

    # Take App ID
    app_id = app_id_from_user_input(user_input)
    id = DAEMONS_MANAGER.get_next_id()
    DAEMONS_MANAGER.add_task('logging', track_logs, args=(app_id, True, id))

    pid = get_pid(app_id)

    while get_pid(app_id) == -1:
        time.sleep(1)
        pid = get_pid(app_id)

    if pid != -1:
        print(f"\nProcess created with PID: {pid}")

    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'CRASH'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)

def run_and_logs(user_input):
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
    output, error = Task().run(command)

    # Take App ID
    app_id = app_id_from_user_input(user_input)
    id = DAEMONS_MANAGER.get_next_id()
    DAEMONS_MANAGER.add_task('logging', track_logs, args=(app_id, False, id))

    pid = get_pid(app_id)

    while get_pid(app_id) == -1:
        time.sleep(1)
        pid = get_pid(app_id)

    if pid != -1:
        print(f"\nProcess created with PID: {pid}")

    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'ALL'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)


def track_logs(app_id, crash_logs, id):
    pid=-1

    file_name = f"{app_id}_{id}_all.log"
    
    if crash_logs:
        file_name = f"{app_id}_{id}_crash.log"

    # Collect logs
    with open(file_name, "w") as f:
        command = ['adb', 'logcat']

        if crash_logs:
            command = ['adb', 'logcat', '*:E']

        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f)

        pid = run_app_and_wait(app_id)

        #os.kill(process.pid, signal.SIGTERM)
        process.terminate()
        process.wait()

    lines = []

    with open(file_name, "r") as fd:
        lines = fd.readlines()

    with open(file_name, "w") as fd:
        for l in lines:
            if pid in l:
                fd.write(l)

    DAEMONS_MANAGER.stop_task('logging', id)


def get_pid(app_id):
    command = ['adb', 'shell','pidof', app_id]
    output, error = Task().run(command)

    if output:
        return output.splitlines()[0]
    else:
        return -1

def run_app_and_wait(app_id):
    #Run command on Android device using the default pre-installed monkey command
    command = ['adb', 'shell','monkey', f"-p '{app_id}'", '-v 1']
    output, error = Task().run(command)

    pid = get_pid(app_id)

    while True:
        cycle_pid = get_pid(app_id)

        if cycle_pid == -1:
            break

    return pid

def log_sessions(user_input):
    row_list = list_daemons('logging')