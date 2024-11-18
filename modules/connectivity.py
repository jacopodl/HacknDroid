import subprocess

def enable_wifi(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'svc', 'wifi', 'enable']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)

    choice = 'x'
    while choice != 'y' and choice != 'n':
        choice = input("Do you want to open Wifi settings (y/n)? ")
        choice = choice.strip().lower()
        print(choice)

    if choice == 'y':
        # Open ADB shell
        command = ['adb', 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        output, error = process.communicate()
        print(output)


def disable_wifi(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'svc', 'wifi', 'disable']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)

def enable_airplane_mode(user_input):
    # Open ADB shell
    command = ['adb','shell','settings','put','global','airplane_mode_on','1']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)


def disable_airplane_mode(user_input):
    # Open ADB shell
    command = ['adb','shell','settings','put','global','airplane_mode_on','0']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)

def donotdisturb_total_silence(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '3']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)


def donotdisturb_alarms_only(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '2']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)


def donotdisturb_priority_only(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '1']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)


def donotdisturb_disabled(user_input):
    # Open ADB shell
    command = ['adb', 'shell', 'settings', 'put', 'global', 'zen_mode', '0']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output, error = process.communicate()
    print(output)
