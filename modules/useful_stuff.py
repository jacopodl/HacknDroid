"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from modules import utility
import subprocess
from prompt_toolkit import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import config.style as tool_style
from tabulate import tabulate
from modules.tasks_management import Task
import re
from termcolor import colored
from modules.adb import get_session_device_id

def reboot(user_input):
    """
    Reboot the mobile device after user confirmation.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Ask confirmation to the user
    choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    while choice != 'n' and choice != 'y':
        print('Please, select a valid option...')
        choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    if choice == 'y':
        # Reboot using ADB
        command = ['adb', '-s', get_session_device_id(), 'shell', 'reboot']
        output, error = Task().run(command, is_shell=True)


def reboot_recovery(user_input):
    """
    Reboot the mobile device into recovery mode after user confirmation.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Ask confirmation to the user
    choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    while choice != 'n' and choice != 'y':
        print('Please, select a valid option...')
        choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    if choice == 'y':
        # Reboot in recovery mode using ADB
        command = ['adb', '-s', get_session_device_id(), 'reboot', 'recovery']
        output, error = Task().run(command, is_shell=True)


def reboot_bootloader(user_input):
    """
    Reboot the mobile device into bootloader mode after user confirmation.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Ask confirmation to the user
    choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    while choice != 'n' and choice != 'y':
        print('Please, select a valid option...')
        choice = input(colored("Are you sure you want to reboot the mobile device (y/n)? ", "green"))

    if choice == 'y':
        command = ['adb', '-s', get_session_device_id(), 'reboot', 'bootloader']
        output, error = Task().run(command, is_shell=True)


def shutdown(user_input):
    """
    Shutdown the mobile device after user confirmation.

    Args:
        user_input (str): User input (not used in this function).
    """
    choice = input(colored("Are you sure you want to shutdown the mobile device (y/n)? ", "green"))

    while choice != 'n' and choice != 'y':
        print('Please, select a valid option...')
        choice = input(colored("Are you sure you want to shutdown the mobile device (y/n)? ", "green"))

    if choice == 'y':
        command = ['adb', '-s', get_session_device_id(), 'shell', 'reboot', '-p']
        output, error = Task().run(command, is_shell=True)


def screen_lock_enabled(user_input):
    """
    Enable screen lock on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Click LOCK button (26) (Specific for Motorola with PIN unlock)
    command = ['adb', '-s', get_session_device_id(), 'shell', 'input', 'keyevent','26']
    output, error = Task().run(command, is_shell=True)


def general_info(user_input):
    """
    Retrieve and display general information about the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    """
    Device model
    adb shell getprop ro.product.model
    Android version
    adb shell getprop ro.build.version.release
    """

    style = Style.from_dict(tool_style.STYLE)
    
    print('')
    print_formatted_text(HTML(f"<option>Device Information</option>"), style=style)
    # Get model via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.product.model']
    output, error = Task().run(command)
    print(f"Device Model: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.product.brand']
    output, error = Task().run(command)
    print(f"Brand: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.product.manufacturer']
    output, error = Task().run(command)
    print(f"Manufacturer: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.build.version.release']
    output, error = Task().run(command)
    print(f"Android Version: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.build.id']
    output, error = Task().run(command)
    print(f"Build ID: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.build.version.sdk']
    output, error = Task().run(command)
    print(f"SDK Version: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.build.date']
    output, error = Task().run(command)
    print(f"Build Date: {output.strip()}")

    # Get brand information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'getprop', 'ro.serialno']
    output, error = Task().run(command)
    print(f"Device Serial Number: {output.strip()}", end='\n\n')


def cpu_info(user_input):
    """
    Retrieve and display CPU information of the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Get CPU information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'cat', '/proc/cpuinfo']
    output, error = Task().run(command)
    print(output.strip(), end='\n\n')


def network_info(user_input):
    """
    Retrieve and display network information of the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Get network information via ADB shell
    command = ['adb', '-s', get_session_device_id(), 'shell', 'dumpsys', 'connectivity']
    output, error = Task().run(command)
    print(output.strip(), end='\n\n')


def ram_info(user_input):
    """
    Retrieve and display RAM information of the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    command = ['adb', '-s', get_session_device_id(), 'shell', 'cat', '/proc/meminfo']
    output, error = Task().run(command)
    rows = output.strip().split("\n")
    
    rows = [re.split(r'\s{2,}', r) for r in rows]

    for r in rows:
        r[0] = colored(r[0], 'blue')

    print(tabulate(rows, tablefmt='fancy_grid'))

def storage_info(user_input):
    """
    Retrieve and display storage information of the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Get brand information via df command
    command = ['adb', '-s', get_session_device_id(), 'shell', 'df']
    print(command)
    output, error = Task().run(command)
    print(output.strip(), end='\n\n')


def system_apps(user_input):
    """
    Retrieve and display the list of system applications on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Get the list of system apps
    command = ['adb', '-s', get_session_device_id(), 'shell', 'pm', 'list', 'packages', '-s']
    print(command)
    output, error = Task().run(command)

    # Print all the apps IDs in a table with 2 columns
    packages_in_output_table(output, 2)

def third_party_apps(user_input):
    """
    Retrieve and display the list of third-party applications on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Get the list of 3rd-party apps
    command = ['adb', '-s', get_session_device_id(), 'shell', 'pm', 'list', 'packages', '-3']
    print(command)
    output, error = Task().run(command)

    # Print all the apps IDs in a table with 3 columns
    packages_in_output_table(output, 3)


def packages_in_output_table(output : str, num_cols : int):
    """
    Retrieve the list of app IDs and format them in a table with the specified number of columns.

    Args:
        output (str): Output of the command adb shell pm list packages [-3|-s].
        num_cols (int): The number of columns to be used.
    """
    # List of rows with packages IDs 
    packages_list = []
    # List of all the packages IDs
    packages = [l.replace("package:", '') for l in output.strip().splitlines()]

    # A list for each row     
    row_list = []
    # Read all the packages IDs
    for i, p in enumerate(packages):
        # If the index is a multiple of num_cols or 0
        if i%num_cols == 0:
            if len(row_list)>0:
                # If the index of the package is a multiple of num_cols
                # Add the row to the list of rows
                packages_list.append(row_list)

            # Reset the row content
            row_list = []
        
        # Add the package ID in the current row
        row_list.append(p)

    # Print the entire table
    print(tabulate(packages_list, tablefmt='fancy_grid'))

def force_app_stop(user_input):
    """
    Force stop an application on the mobile device based on user input.

    Args:
        user_input (str): User input containing the app ID or keywords to search for the app.
    """
    # Read app ID from user input or retrieve it from the words specified by the user
    # (the search is performed in the list of the running apps) 
    app_id = utility.active_app_id_from_user_input(user_input)

    # Force the stop of the app with identified app ID
    command = ['adb', '-s', get_session_device_id(), 'shell', 'am', 'force-stop', app_id]
    print(command)
    output, error = Task().run(command)
    print(f"{app_id} STOPPED")