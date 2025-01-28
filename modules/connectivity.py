import subprocess
from modules.tasks_management import Task 

def enable_wifi(user_input):
    """
    Enable WiFi on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'svc', 'wifi', 'enable']
    output, error = Task().run(command)
    print(output)

    choice = 'x'
    while choice != 'y' and choice != 'n':
        choice = input("Do you want to open Wifi settings (y/n)? ")
        choice = choice.strip().lower()
        print(choice)

    if choice == 'y':
        # Open ADB shell
        command = ['adb', 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
        output, error = Task().run(command)
        print(output)


def disable_wifi(user_input):
    """
    Disable WiFi on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'svc', 'wifi', 'disable']
    output, error = Task().run(command)
    print(output)

def enable_airplane_mode(user_input):
    """
    Enable airplane mode on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb','shell','settings','put','global','airplane_mode_on','1']
    output, error = Task().run(command)
    print(output)


def disable_airplane_mode(user_input):
    """
    Disable airplane mode on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb','shell','settings','put','global','airplane_mode_on','0']
    output, error = Task().run(command)
    print(output)

def donotdisturb_total_silence(user_input):
    """
    Enable 'Do Not Disturb' mode with total silence on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '3']
    output, error = Task().run(command)
    print(output)


def donotdisturb_alarms_only(user_input):
    """
    Enable 'Do Not Disturb' mode with alarms only on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '2']
    output, error = Task().run(command)
    print(output)


def donotdisturb_priority_only(user_input):
    """
    Enable 'Do Not Disturb' mode with priority only on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '1']
    output, error = Task().run(command)
    print(output)


def donotdisturb_disabled(user_input):
    """
    Disable 'Do Not Disturb' mode on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '0']
    output, error = Task().run(command)
    print(output)
