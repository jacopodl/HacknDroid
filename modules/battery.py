import subprocess
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import config.menu as menu
import config.style as tool_style
from modules.tasks_management import Task

def battery_saver_on(user_input):
    """
    Enable battery saver mode on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'broadcast' ,'-a' ,'android.intent.action.ACTION_POWER_SAVE_MODE_CHANGED' ,'--ez' ,'"mode"' ,'true']
    output, error = Task().run(command)
    print(output)


def battery_saver_off(user_input):
    """
    Disable battery saver mode on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'broadcast' ,'-a' ,'android.intent.action.ACTION_POWER_SAVE_MODE_CHANGED' ,'--ez' ,'"mode"' ,'false']
    output, error = Task().run(command)
    print(output)

def check_battery_status(user_input):
    """
    Check the battery status of the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    # Open ADB shell
    command = ['adb' ,'shell', 'dumpsys', 'battery']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()


    style = Style.from_dict(tool_style.STYLE)
    
    lines = output.splitlines()
    
    print('')
    print_formatted_text(HTML(f"<option>{lines[0]}</option>"), style=style)
    
    line = '-'*len(lines[0])
    print_formatted_text(HTML(f"<option>{line}</option>"), style=style)

    for l in lines[1:]:
        key_value = l.strip().split(":")
        print_formatted_text(HTML(f"<descr>{key_value[0]}:</descr> {key_value[1]}"), style=style)

    print_formatted_text(HTML(f"<option>{line}</option>"), style=style)

    print("", end="\n\n")