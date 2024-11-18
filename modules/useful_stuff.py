from modules import utility
import subprocess

def screenshot(user_input):
    pass

def record_video(user_input):
    pass

def reboot(user_input):
    # adb reboot
    pass

def reboot_recovery(user_input):
    # adb reboot recovery
    pass

def reboot_bootloader(user_input):
    # adb reboot bootloader
    pass

def screen_lock_disabled(user_input):
    pass

def screen_lock_enabled(user_input):
    pass

def send_sms(user_input):
    """
    adb shell am start -a android.intent.action.SENDTO -d sms:+1234567890 --es sms_body "Hello, this is a test message" --ez exit_on_sent true
    """
    pass

def get_device_info(user_input):
    """
    Device model
    adb shell getprop ro.product.model
    Android version
    adb shell getprop ro.build.version.release
    """
    pass

def force_app_stop(user_input):
    app_id = utility.active_app_id_from_user_input(user_input)

    # Open ADB shell
    command = ['adb', 'shell', 'am', 'force-stop', app_id]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Print the external storage path
    output, error = process.communicate()
    print(f"{app_id} STOPPED")