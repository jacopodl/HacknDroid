from modules.utility import app_id_from_user_input, active_app_id_from_user_input
from modules.tasks_management import Task
from modules.adb import get_session_device_id

def run_app_meminfo(user_input):
    """
    Return memory information commands for a specified Android application.
    1. Extract the app ID from the user input.
    2. Run the 'monkey' command on the Android device to interact with the specified app.
    3. Dump memory information for the current package using the 'dumpsys meminfo' command.

    Args:
        user_input (str): The user input containing the app identifier.

    Returns:
        None
    """

    # Get the app ID from user input
    app_id = app_id_from_user_input(user_input)
    # Run command on Android device using the default pre-installed monkey command
    command = ['adb', '-s', get_session_device_id(), 'shell','monkey', f"-p '{app_id}'", '-v 1']
    output, error = Task().run(command)
    # Dump memory for the current package
    command = ['adb', '-s', get_session_device_id(), 'shell', 'dumpsys', 'meminfo', ]
    output, error = Task().run(command)
    print(output)

def running_app_meminfo(user_input):
    """
    Return memory information commands for a specified Android application.
    1. Extract the running app ID from the user input.
    2. Dump memory information for the current package using the 'dumpsys meminfo' command.

    Args:
        user_input (str): The user input containing the app identifier.

    Returns:
        None
    """

    # Get the app ID from user input
    app_id = active_app_id_from_user_input(user_input)
    # Dump memory for the current package
    command = ['adb', '-s', get_session_device_id(), 'shell', 'dumpsys', 'meminfo', ]
    output, error = Task().run(command)
    print(output)
