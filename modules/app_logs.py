import os
import subprocess
from modules.utility import app_id_from_user_input, active_app_id_from_user_input, current_date
import time
from modules.tasks_management import Task, DAEMONS_MANAGER, list_daemons
from modules.adb import get_session_device_id

def logs_from_running_process(user_input):
    """
    Logs all types of logs from a running process.

    Args:
        user_input (str): The user input containing the app ID.
    """

    # Get the app ID from user input
    app_id = active_app_id_from_user_input(user_input)
    # Get the process ID for the app
    pid = get_pid(app_id)

    # Get the next available ID from the DAEMONS_MANAGER
    id = DAEMONS_MANAGER.get_next_id()
    # Add a new logging task to the DAEMONS_MANAGER
    DAEMONS_MANAGER.add_task('logging', track_running_logs, args=(app_id, pid, False, id))

    # Print the process ID if it's valid
    if pid != -1:
        print(f"\nProcess running with PID: {pid}")

    # Add additional information about the logging task
    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'ALL'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)


def crash_logs_from_running_process(user_input):
    """
    Logs crash logs from a running process.

    Args:
        user_input (str): The user input containing the app ID.
    """
    # Get the app ID from user input
    app_id = active_app_id_from_user_input(user_input)
    # Get the process ID for the app
    pid = get_pid(app_id)

    # Get the next available ID from the DAEMONS_MANAGER
    id = DAEMONS_MANAGER.get_next_id()
    # Add a new logging task to the DAEMONS_MANAGER
    DAEMONS_MANAGER.add_task('logging', track_running_logs, args=(app_id, pid, True, id))

    # Print the process ID if it's valid
    if pid != -1:
        print(f"\nProcess running with PID: {pid}")

    # Add additional information about the logging task
    additional_info = {'App ID':app_id, 'Mobile PID': pid, 'Logs Type': 'CRASH'}
    DAEMONS_MANAGER.add_info('logging', id, additional_info)


def track_running_logs(app_id, pid, crash_logs, id):
    """
    Tracks running logs and writes them to a file.

    Args:
        app_id (str): The application ID.
        pid (int): The process ID.
        crash_logs (bool): Whether to log only crash logs.
        id (int): The task ID.
    """

    logs_folder = os.path.join('results', app_id, 'logs')
    os.makedirs(logs_folder, exist_ok=True)

    # Default log file name
    file_name = f"{current_date()}_{id}_all.log"
    
    # Log file name for crash logs
    if crash_logs:
        file_name = f"{current_date()}_{id}_crash.log"

    file_path = os.path.join(logs_folder, file_name)
    
    # Collect logs and write to the file
    with open(file_path, "w") as f:
        # Default adb logcat command
        command = ['adb', '-s', get_session_device_id(), 'logcat', f'--pid={pid}']

        # adb logcat command for crash logs
        if crash_logs:
            command = ['adb', '-s', get_session_device_id(), 'logcat', f'--pid={pid}','*:E']

        # Start the adb logcat process
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.DEVNULL)
        
        cycle_pid = pid
        # Print the process ID
        
        while cycle_pid==pid:
            cycle_pid = get_pid(app_id)
            time.sleep(2)


        # Terminate the process
        process.terminate()
        process.wait()

    DAEMONS_MANAGER.stop_task('logging', id)


def run_and_crash_logs(user_input):
    """
    Runs the application and logs crash logs.

    Args:
        user_input (str): The user input containing the app ID or keywords to identify the application.
    """
    # Flush logs
    command = ['adb', '-s', get_session_device_id(), 'logcat', '-c']
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
    """
    Runs the application and logs all types of logs.

    Args:
        user_input (str): The user input containing the app ID or keywords to identify the application.
    """
    # Flush logs
    command = ['adb', '-s', get_session_device_id(), 'logcat', '-c']
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
    """
    Tracks crash logs or all the logs for an application with a specific App ID.

    Args:
        app_id (str): The application ID.
        crash_logs (bool): Whether to log only crash logs.
        id (int): The task ID.
    """
    pid=-1

    logs_folder = os.path.join('results', app_id, 'logs')
    os.makedirs(logs_folder, exist_ok=True)

    # Default log file name
    file_name = f"{current_date()}_{id}_all.log"
    
    # Log file name for crash logs
    if crash_logs:
        file_name = f"{current_date()}_{id}_crash.log"

    file_path = os.path.join(logs_folder, file_name)

    # Collect logs and write to the file
    with open(file_path, "w") as f:
        command = ['adb', '-s', get_session_device_id(), 'logcat']

        if crash_logs:
            command = ['adb', '-s', get_session_device_id(), 'logcat', '*:E']

        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f)

        pid = run_app_and_wait(app_id)

        # Terminate the process
        process.terminate()
        process.wait()

    lines = []

    # Filter logs by PID
    with open(file_path, "r") as fd:
        lines = fd.readlines()

    with open(file_path, "w") as fd:
        for l in lines:
            if pid in l:
                fd.write(l)

    DAEMONS_MANAGER.stop_task('logging', id)


def get_pid(app_id):
    """
    Gets the process ID of an application.

    Args:
        app_id (str): The application ID.

    Returns:
        int: The process ID or -1 if not found.
    """
    command = ['adb', '-s', get_session_device_id(), 'shell','pidof', app_id]
    output, error = Task().run(command)

    if output:
        return output.splitlines()[0]
    else:
        return -1

def run_app_and_wait(app_id):
    """
    Runs the application and waits for it to start.

    Args:
        app_id (str): The application ID.

    Returns:
        int: The process ID of the running application.
    """
    # Run command on Android device using the default pre-installed monkey command
    command = ['adb', '-s', get_session_device_id(), 'shell','monkey', f"-p '{app_id}'", '-v 1']
    output, error = Task().run(command)

    pid = get_pid(app_id)

    while True:
        cycle_pid = get_pid(app_id)

        if cycle_pid == -1:
            break

    return pid

def log_sessions(user_input):
    """
    List all running log sessions.

    Args:
        user_input (str): User input (not used in this function).
    """
    row_list = list_daemons('logging')