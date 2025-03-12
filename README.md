# HacknDroid
The script is used for the automation of some MAPT activities and the interaction with the mobile Android device. The script was created to solve many problems:
- the command `adb root` is not enabled after device rooting on many production mobile devices;
- the files need to be shared before on the external SD Card and then on the device;
- the retrieving of the application data (APKs, Shared preferences, Stored data) needs to be found and retrieved with several commands;
- the unpacking process of the application APK need a merge phase for application with multiple APKs in `/data/app/{app_id}_{base64_unique_id}` for efficency purpouses

Detailed list of available functionalities can be found [here](#script-features).

---

## Install
Install python requirements using the following command:
```bash
pip install -r requirements.txt
```
Install other binary requirements:
```bash
python3 hackndroid.py --install
```

---

## Run the program
```bash
python hackndroid.py
```
![Run Example](.img/run_example_0.png)
![Run Example](.img/run_example_1.png)
![Run Example](.img/run_example_2.png)

### Proxy via DNS Spoofing (on Windows)
To run DNS Server using the tool, ensure that the Windows Firewall is disabled on the PC where the script will be run:
![Run Example](.img/disable_windows_firewall_0.png)
![Run Example](.img/disable_windows_firewall_1.png)

If everything was set successfully, you can intercept the traffic on ports 80, 443 in Burp Suite as follows:
![Run Example](.img/dns_proxy_intercept.png)

---


## Script features
### Task Manager
  - [x] *Daemon tasks*
    - [x] logcat
    - [x] mirroring
    - [x] proxy with dns spoofing
    - [x] video recoding
  - [x] *Sequential tasks*

### Functionalities
- [x] `apk_analysis`<br>Analysis of the APKs (apk decompiling, search for common Root Detection, Certificate Pinning, SHA1-SHA256 strings in the files)
  - [x] `from_apk_on_pc`
  - [x] `from_mobile_device`
- [x] `apk_compiling`<br>Compile an APK file from the folder with decompiled and modified code
  - [x] `compile`: Compile an apk file from the folder with decompiled and modified code
  - [x] `compile_and_sign`: Compile and sign an apk file from the folder with decompiled and modified code
- [x] `apk_decompiling`<br>Decompile an APK file
  - [x] `from_apk_on_pc`: 
  - [x] `from_mobile_device`: 
- [x] `apk_to_jar`<br>Convert the apk to a jar file
  - [x] `from_apk_on_pc`: 
    - [x] `create_jar_file`: 
    - [x] `jadx_create_and_open_file`: 
  - [x] `from_mobile_device`: 
    - [x] `create_jar_file`: 
    - [x] `jadx_create_and_open_file`: 
- [x] `backup_and_data`<br>Backup the mobile device or an application
  - [x] `backup_device`: Backup the mobile device
  - [x] `backup_specific_app`: Backup a specific app specifing its app ID
  - [x] `backup_restore`: Specify the backup file path on your system
  - [x] `backup_to_folder`: Convert the AB file to an unpacked folder
  - [x] `reset_app_data`: Reset App data
- [x] `download_from_mobile`<br>Download file from the mobile device
- [x] `install_uninstall`<br>Install/Uninstall an app on the mobile device
  - [x] `install_from_apk`
  - [x] `install_from_playstore`
  - [x] `uninstall`
- [x] `merge_apks`<br>Merge several APKs using APKEditor
  - [x] `from_directory`
  - [x] `from_list`
- [x] `mirroring`<br>Launch scrcpy for mobile device mirroring
- [x] `proxy`<br>Set global proxy on the mobile device
  - [x] `system_proxy`
    - [x] `get_current_proxy`
    - [x] `set_proxy_with_current_ip`
    - [x] `set_proxy_with_other_ip`
    - [x] `del_proxy`
  - [x] `invisible_proxy`
    - [x] `ip_tables`
      - [x] `get_current_proxy`
      - [x] `set_proxy_with_current_ip`
      - [x] `set_proxy_with_other_ip`
      - [x] `del_proxy`
    - [x] `dns`
      - [x] `get_current_proxy`
      - [x] `dns_server_with_current_ip`
      - [x] `dns_server_with_another_ip`
- [x] `sign_apk`<br>Sign an apk on your PC. Write the path of the apk you want to test
- [x] `track_logs`<br>Logs gathering
  - [x] `all_logs`
  - [x] `all_crash_logs`
- [x] `upload_to_mobile`<br>Upload a file from PC to mobile device
- [x] `useful_staffs`
  - [x] `device_info`
    - [x] `apps_list`
      - [x] `3rd_party_apps`: Get list of all the installed 3rd-party apps
      - [x] `system_apps`: Get list of all the installed system apps
    - [x] `cpu_info`: Get CPU information
    - [x] `general_info`: Get mobile device general information
    - [x] `ram_info`: Get RAM information
    - [x] `storage_info`: Get Storage information
  - [x] `battery_saver`: Battery Saver mode (ON/OFF)
  - [x] `do_not_disturb_mode`: Do Not Disturb mode (ON/OFF)
  - [x] `connectivity`: Connectivity options management
    - [x] `wifi`: Wifi option Management (ON/OFF)
    - [x] `airplane`: Airplane mode Management (ON/OFF)
  - [x] `screenshot_video`: Screenshot/Video on the mobile device
    - [x] `screenshot`
    - [x] `video`
  - [x] `shutdown`<br>Shutdown/Reboot the device with several options
    - [x] `shutdown`: Shutdown the mobile device
    - [x] `reboot`: Reboot the mobile device
    - [x] `reboot_recovery`: Reboot the mobile device in recovery mode
    - [x] `reboot_bootloader`: Reboot the mobile device in bootloader mode

### Future functionalities
- [ ] `apk_analysis`
  - [ ] `signature_scheme_analysis`
  - [ ] `specific_technology`
    - [ ] Cordova
    - [ ] Flutter
- [ ] `system_mount_for_root`: Device rooting
  - [ ] Android <=10
  - [ ] Android 10+
- [ ] `install_certificates`
    - [ ] install depending on android
      - [ ] Android <=10
      - [ ] Android 10+
    - [ ] Install without Rooted device
      - [ ] MDM install 
      - [ ] install certificates on user land and modify android manifest
      - [ ] VPN certificate in userland
- [ ] `frida`: Use Frida for several functionalities
  - [ ] `function_hooking`
  - [ ] `script`

### Tested on
- [x] Windows
- [ ] Linux
- [ ] MacOS