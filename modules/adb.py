import os
from tabulate import tabulate
from termcolor import colored
from modules.error import ADBConnectionException, OptionNotAvailable
import subprocess
import configparser

def check_connection(adb_shell_output):
    """
    Check if the device is connected to ADB.

    Returns:
        bool: True if the device is connected to ADB, False otherwise.
    """

    if "no devices/emulators found" in adb_shell_output:
        raise ADBConnectionException("No device connected", code=1)
    
def get_current_device():
    """
    Get the current device ID.

    Returns:
        str: The device ID.
    """
    


def select_device(user_input):
    """
    List the devices connected to ADB.

    Args:
        user_input (str): The user input string.

    Returns:
        str: The output of the ADB devices command.
    """

    # Create an instance of ConfigParser

    adb_devices = adb_devices_list()

    try:
        choice = int(input(colored("Select the device ID you want to use:\n", 'green')))
        print("")
        
        if choice >= 0 and choice < len(adb_devices):
            config = configparser.ConfigParser()
    
            if not os.path.exists('config.ini'):
                config.read('config.ini')

            # Add a new section if it doesn't exist
            if not config.has_section('General'):
                config.add_section('General')
            
            config.set('General', 'adb_session_device', adb_devices[choice][1])

            # Write the configuration to a file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

        else:
            raise ValueError("")

    except ValueError:
        raise OptionNotAvailable("")


def adb_devices_list():
    while True:
        command = ['adb', 'devices', '-l']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output, error = process.communicate()

        headers = ["Device ID", "Device Name", "Status", "Model"]

        row_list = []
        table_rows = []
        id = 0
        for row in output.replace("List of devices attached\n","").strip().splitlines():
            device_row = row.split()

            for info in device_row[2:]:
                if info.startswith('model:'):
                    model = info.replace('model:', '').replace('_',' ')

                    if get_session_device_id() == device_row[0]:
                        selected_id = f" {id} ".center(len(headers[0]))
                        table_rows.append([colored(f" {id} ".center(len(headers[0])), 'black', 'on_red'), 
                                           colored(f" {device_row[0]} ".center(len(headers[1])), 'black', 'on_white'), 
                                           colored(f" {device_row[1]} ".center(len(headers[2])), 'black', 'on_white'), 
                                           colored(f" {model} ".center(len(headers[2])), 'black', 'on_white')])
                    else:
                        table_rows.append([colored(f" {id} ", 'red'), colored(f" {device_row[0]} ", 'yellow'), f" {device_row[1]} ", f" {model} "])

                    row_list.append([id, device_row[0], device_row[1], model])

            id += 1

        color_headers = [colored(h, 'blue') for h in headers]

        if len(row_list)>0:
            print(tabulate(table_rows, headers=color_headers, tablefmt='fancy_grid', colalign=('center', 'center', 'center', 'center')), end='\n\n')
        else:
            print(tabulate(table_rows, headers=color_headers, tablefmt='fancy_grid'), end='\n\n')
        
        print(colored("device\t\t", "cyan")+"Connected and ready")
        print(colored("offline\t\t", "cyan")+"Device not responsive")
        print(colored("unauthorized\t", "cyan")+"Connection not authorized by the device", end="\n\n")

        if len(row_list) == 0:
            raise ADBConnectionException("")

        else:
            return row_list

def get_session_device_id():
    """
    Get the device ID from the configuration file.

    Returns:
        str: The device ID.
    """
    if os.path.exists('config.ini'):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('General', 'adb_session_device')
    else:
        return None