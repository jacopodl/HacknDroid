# HacknDroid
The script is used for the automation of some MAPT activities and the interaction with the mobile Android device. The script was created to solve many problems:
- the command `adb root` is not enabled after device rooting on many production mobile devices;
- the files need to be shared before on the external SD Card and then on the device;
- the retrieving of the application data (APKs, Shared preferences, Stored data) needs to be found and retrieved with several commands;
- the unpacking process of the application APK need a merge phase for application with multiple APKs in `/data/app/{app_id}_{base64_unique_id}` for efficency purpouses
- management of invisible proxy setup 

# Main functionalities
- ***apk:*** Several APKs related operations (apk analysis for root detection/certificate pinning hints, apk decompiling/compiling, JADX-GUI launch, etc.)
- ***app_data_and_logs:*** Access to app data (e.g. backups) and logs
- ***device_info:*** Get mobile device information 
- ***devices:*** Select one of the available mobile devices
- ***file_transfer:*** Transfer files from/to mobile devices 
- ***install_uninstall:*** Install/Uninstall an app on the mobile device.
- ***interactive_shell:*** Interactive shell for the mobile device
- ***mirroring:*** Mirroring management (screenshot, video recording and scren mirroring)
- ***mobile_settings:*** Management of mobile device modes (battery saver, do not disturb, connectivity)
- ***processes_list:*** List all the processes
- ***proxy:*** Set proxy on the mobile device using the current PC IP or another IP (e.g. regular proxy, invisible proxy via iptables or dns spoofing)
- ***shutdown_reboot:*** Reboot/shutdown the device with several options

---

## Install
Install python requirements using the following command:
```bash
pip install -r requirements.txt
```

Install all the binary requirements with the following command:
```bash
python3 hackndroid.py --install
```

> ***Note:***
> Before installing, ensure that the latest version of the Java JDK is installed on your system.
> 
> Additionally, make sure to configure the `JAVA_HOME` environment variable to point to the *JDK installation directory*, and update the `PATH` variable to include the `<jdk-path>/bin` directory.

---

## Run the program
```bash
python hackndroid.py
```

# More details
For further details, visit the documentation [here](https://raffadndm.gitbook.io/toolkit/hackndroid).