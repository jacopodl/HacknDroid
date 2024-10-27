import config

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

