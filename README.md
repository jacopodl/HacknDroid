# HacknDroid
The script is used for automate some MAPT activities and the interaction with the mobile Android device. The script was created to solve many problems:
- the command `adb root` is not enabled after device rooting on many mobile devices;
- the files need to be shared before on the external SD Card and then on the device;
- the retrieving of the application data (APKs, Shared preferences, Stored data) needs to be found and retrieved with several commands;
- the unpacking process of the application APK need a merge phase for application with multiple APKs in `/data/app/{app_id}_{base64_unique_id}` for efficency purpouses

## Pre-requisites
Install the following programs and add their folder with binary files in the `PATH` environment variable:
- [***ADB***](https://developer.android.com/tools/adb) for interaction with the mobile device in Developer Mode;
- [***scrcpy***](https://github.com/Genymobile/scrcpy) for mirroring and remote control of the mobile device over ADB connection;

Install python requirements using the following command:
```bash
pip install -r requirements.txt
```