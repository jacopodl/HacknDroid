import subprocess
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import config

def battery_saver_on(user_input):    
    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'broadcast' ,'-a' ,'android.intent.action.ACTION_POWER_SAVE_MODE_CHANGED' ,'--ez' ,'"mode"' ,'true']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)


def battery_saver_off(user_input):
    # Open ADB shell
    command = ['adb' ,'shell' ,'am' ,'broadcast' ,'-a' ,'android.intent.action.ACTION_POWER_SAVE_MODE_CHANGED' ,'--ez' ,'"mode"' ,'false']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)

def check_battery_status(user_input):
    """
    adb shell dumpsys battery
    """
    # Open ADB shell
    command = ['adb' ,'shell', 'dumpsys', 'battery']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()


    style = Style.from_dict(config.STYLE)
    
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