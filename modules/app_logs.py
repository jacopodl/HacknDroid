import config
import subprocess
import signal

# Retrieve log from the application for further analysis
# Flush adb logcat content
# adb logcat -c
# Start ADB logcat (No restriction of the logs to the application because there can be other useful logs to be analysed)
# adb logcat  
# Run command on Android device using the default pre-installed monkey command
# adb shell monkey -p 'your package name' -v 500
# Check when the App was shutdown (if empty string, the app is not running)
# while True:
#   adb shell pidof package_name
def app_logs():
    pass

def all_logs(user_input):
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
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Collect logs
    with open("logcat.log", "w") as f:
        command = ['adb', 'logcat']
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=f, text=True)

        x = input()
        process.send_signal(signal.CTRL_BREAK_EVENT)

def main():
    all_logs()

if __name__=="__main__":
    main()