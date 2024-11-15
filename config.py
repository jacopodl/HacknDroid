from modules import apk_analyzer, apk_install, app_logs, backup, file_transfer, merge_apks, mirroring, mobsf, proxy, signature, useful_stuff, utility

OPTIONS =   {
                'main': { 
                    "description":['',],
                    'children':{
                        "apk_analysis": { 
                            'description': [
                                'Analysis of the APKs related to the application:', 
                                ' > signature schema verifier', 
                                ' > apk decompiled with apktool',
                                ' > search for common Root Detection strings in smali files', 
                                ' > search for common Certificate Pinning strings or SHA1-SHA256 hash string in smali files'
                                ],
                            'children': {
                                "from_apk_on_pc" : { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                    " > the path of the folder where the apk will be decompiled"
                                                    ],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function' : apk_analyzer.apk_analysis_from_file
                                },
                                "from_mobile_device" : { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the app id or a part of the app name to be extracted and analysed"
                                                    " > the path of the folder where the apk will be decompiled"
                                                    ],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': apk_analyzer.apk_analysis_from_device
                                },
                                'back' : dict()
                            }
                        },
                        "apk_compiling": { 
                            'description': ['Compile an apk file from the folder with decompiled and modified code',],
                            'children': {
                                "compile": { 
                                    'description': ['Compile an apk file from the folder with decompiled and modified code',],
                                    'children': {
                                        'back' : dict(),
                                    },
                                    'function' : apk_analyzer.apk_compile_from_folder
                                },
                                "compile_and_sign": { 
                                    'description': ['Compile and sign an apk file from the folder with decompiled and modified code',],
                                    'children': {
                                        'back' : dict(),
                                    },
                                    'function' : apk_analyzer.apk_compile_and_sign_from_folder
                                },
                                'back' : dict(),
                            },
                        },
                        "apk_decompiling": { 
                            'description': ['Decompile an apk file',],
                            'children': {
                                "from_apk_on_pc" : { 
                                    'description': ["Decompile the apk file into smali code. Write the following two strings (separated by space):",
                                                    " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                    " > the path of the folder where the apk will be decompiled"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function' : apk_analyzer.apk_decompiler_from_file
                                },
                                "from_mobile_device" : { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the app id or a part of the app name to be extracted and analysed"
                                                    " > the path of the folder where the apk will be decompiled"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': apk_analyzer.apk_decompiler_from_device
                                },
                                'back' : dict()
                            }
                        },
                        "apk_to_jar": {
                            'description': ['Convert the apk to a jar file',],
                            'children': {
                                "from_apk_on_pc" : { 
                                    'description': ["Convert an apk file on the PC to a jar file"],
                                    'children': {
                                        "create_jar_file":{
                                            'description': ["Convert the apk to a jar file. Write the following two strings (separated by space):",
                                                            " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                            " > the path of the folder where the JAR file will be stored"],
                                            'children':{
                                                "back":dict(),
                                            },
                                            'function': apk_analyzer.jar_from_file
                                        },
                                        "jadx_create_and_open_file":{
                                            'description': ["Open the reversed apk in JADX-GUI. Write the path of the apk on your PC (or the folder with all the APKs related to the app)",],
                                            'children':{
                                                "back":dict(),
                                            },
                                            'function': apk_analyzer.jar_from_file
                                        },
                                        "back" : dict(),
                                    },
                                    'function' : apk_analyzer.apk_decompiler_from_file
                                },
                                "from_mobile_device" : { 
                                    'description': ["Convert am apk from the mobile device to a jar file"],
                                    'children': {
                                        "create_jar_file":{
                                            'description': ["Convert the apk to a jar file. Write the following two strings (separated by space):",
                                                            " > the app id or a part of the app name to be extracted and analysed",
                                                            " > the path of the folder where the apk will be decompiled"],
                                            'children':{
                                                "back":dict(),
                                            },
                                            'function': apk_analyzer.jar_from_device
                                        },
                                        "jadx_create_and_open_file":{
                                            'description': ["Open the reversed apk in JADX-GUI. Write the app id or a part of the app name to be extracted and analysed",],
                                            'children':{
                                                "back":dict(),
                                            },
                                            'function': apk_analyzer.jar_from_device
                                        },
                                        "back" : dict(),
                                    },
                                },
                                'back' : dict()
                            }
                        },
                        "backup_and_data" : {
                            'description': ['Backup the mobile device or an application',],
                            'children': {
                                "backup_device" : { 
                                    'description': ["Backup the mobile device"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function' : backup.device_backup
                                },
                                "backup_specific_app" : { 
                                    'description': ["Backup a specific app, writing its app id or a keyword to identify it"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': backup.app_backup
                                },
                                "backup_restore" : { 
                                    'description': ["Specify the backup file path on your system to be restored on the mobile device"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': backup.restore_backup
                                },
                                "backup_to_folder" : { 
                                    'description': ["Specify the backup file path on your system to be extracted"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': backup.tar_extract
                                },
                                "reset_app_data" : { 
                                    'description': ["Reset App data"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': backup.app_data_reset
                                },
                                'back' : dict()
                            }
                        },
                        "download_from_mobile" :  { 
                            'description': ["Write the following two strings (separated by space):",
                                            " > the path of the file/folder on the mobile device",
                                            " > the PC folder (where the file will be downloaded)"],
                            'children': {
                                "back" : dict(),
                            },
                            'function': file_transfer.download_from_user_input
                        },
                        "force_app_stop" :  { 
                            'description': ["Write the app id of the mobile app or some keywords to identify it"],
                            'children': {
                                "back" : dict(),
                            },
                            'function': useful_stuff.force_app_stop
                        },
                        "install_uninstall" : {
                            'description': ['Install an app on the mobile device.',],
                            'children': {
                                "from_apk_on_pc" : {
                                    'description' : ["Write the path of the apk on your PC to be installed",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': apk_install.install_from_apk
                                },
                                "from_play_store" : {
                                    'description' : ["Write the app id of the app to be installed (the command prompt will be open)",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': apk_install.install_from_playstore
                                },
                                "back" : dict()
                            }
                        },
                        "merge_apks": {
                            'description': ['Merge several APKs'],
                            'children': {
                                "from_directory" : {
                                    'description' : ["Write the path of the directory with APKs to be merged",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': merge_apks.merge_from_dir
                                },
                                "from_list" : {
                                    'description' : ["Write the list of APKs paths to be merged (separated by spaces):",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': merge_apks.merge_from_list
                                },
                                "back" : dict(),
                            },
                        },
                        "mobsf" :  { 
                            'description': ["Static Analysis of the APK using MobSF"],
                            'children': {
                                "from_apk_on_pc" : { 
                                    'description': ["Write the path of the apk on your PC to be analysed (or the folder with all the APKs related to the app)"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function' : mobsf.mobsf_from_file
                                },
                                "from_mobile_device" : { 
                                    'description': ["Write the app id or a part of the app name to be analysed",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': mobsf.mobsf_from_device
                                },
                                "back" : dict(),
                            },
                            'function': file_transfer.download
                        },
                        "mirroring" : {
                            'description': ['Launch scrcpy for mobile device mirroring (Press any key to continue)',],
                            'children': {
                                "back" : dict(),
                            },
                            'function': mirroring.mirroring
                        },
                        "proxy" : {
                            'description': ['Set global proxy on the mobile device:',
                                            ' > using the current PC IP',
                                            ' > using another IP'],
                            'children': {
                                "get_current_proxy" : {
                                    'description' : ["Press ENTER to see current proxy settings"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': proxy.get_current_proxy_settings
                                },
                                "set_proxy_with_current_ip" : {
                                    'description' : ["Write the port number for the proxy on the current PC",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': proxy.set_current_pc_proxy
                                },
                                "set_proxy_with_other_ip" : {
                                    'description' : ["Write the following values:",
                                                     " > IP address of the proxy",
                                                     " > port number of the proxy"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': proxy.set_generic_proxy
                                },
                                "del_proxy" : {
                                    'description' : ["Press ENTER to reset proxy configuration"],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': proxy.del_proxy
                                },
                                "back" : dict(),
                            },
                            'function': mirroring.mirroring
                        },
                        "sign_apk":{
                            'description': ['Sign an apk on your PC. Write the path of the apk you want to test'],
                            'children': {
                                "back" : dict()
                            },
                            'function': signature.sign_apk
                        },
                        "track_logs" : {
                            'description': ['Process for logs gathering:',
                                            ' > automated mode: the application will be opened by the script',
                                            ' > manual mode: the application needs to be launched by the user'],
                            'children': {
                                "all_logs" : {
                                    'description' : ["Write the app id or a part of the app name to be launched",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': app_logs.all_logs
                                },
                                "app_logs" : {
                                    'description' : ["Write the app id or a part of the app name to be launched",],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': app_logs.app_logs
                                },
                                "back" : dict()
                            }
                        },
                        "upload_to_mobile" : { 
                            'description': ["Write the following two strings (separated by space):",
                                            " > the path of the file/folder on the PC",
                                            " > the mobile device folder (where the file will be uploaded)"],
                            'children': {
                                "back" : dict(),
                            },
                            'function': file_transfer.upload
                        },
                        "useful_staffs" : {
                            'description': ['Process for logs gathering:',
                                            ' > automated mode: the application will be opened by the script',
                                            ' > manual mode: the application needs to be launched by the user'],
                            'children': {
                                "battery_saver" : {
                                    'description' : ["Battery Saver mode",],
                                    'children': {
                                        "off" : {
                                            'description' : ["Turn off battery saver mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.battery_saver_off
                                        },
                                        "on" : {
                                            'description' : ["Turn on battery saver mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.battery_saver_on
                                        },
                                        "back" : dict(),
                                    }
                                },
                                "do_not_disturb_mode" : {
                                    'description' : ["Do Not Disturb mode",],
                                    'children': {
                                        "off" : {
                                            'description' : ["Turn off Do Not Disturb mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.donotdisturb_disabled
                                        },
                                        "on" : {
                                            'description' : ["Turn on Do Not Disturb mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.donotdisturb_enabled
                                        },
                                        "back" : dict(),
                                    }
                                },
                                "connectivity" : {
                                    'description' : ["Connectivity options management (Wifi, airplane mode)",],
                                    'children': {
                                        "wifi_off" : {
                                            'description' : ["Turn off Wifi option",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.disable_wifi
                                        },
                                        "wifi_on" : {
                                            'description' : ["Turn on Wifi option",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.enable_wifi
                                        },
                                        "airplane_off" : {
                                            'description' : ["Turn off Airplane mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.disable_airplane_mode
                                        },
                                        "airplane_on" : {
                                            'description' : ["Turn on Airplane mode",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.enable_airplane_mode
                                        },
                                        "back" : dict(),
                                    }
                                },
                                "screenshot_video" : {
                                    'description' : ["Screenshot/Video on the mobile device",],
                                    'children': {
                                        "screenshot" : {
                                            'description' : ["Screenshot.","Press enter to continue...",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.screenshot
                                        },
                                        "video" : {
                                            'description' : ["Video","Press enter to start recording...",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.record_video
                                        },
                                        "back" : dict(),
                                    },
                                    'function': app_logs.all_logs
                                },
                                "reboot" : {
                                    'description' : ["Reboot the device with several options",],
                                    'children': {
                                        "reboot" : {
                                            'description' : ["Reboot the mobile device.","Press enter to continue...",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.reboot
                                        },
                                        "reboot_recovery" : {
                                            'description' : ["Reboot the mobile device in recovery mode.","Press enter to continue...",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.reboot_recovery
                                        },
                                        "reboot_bootloader" : {
                                            'description' : ["Reboot the mobile device in bootloader mode.","Press enter to continue...",],
                                            'children': {
                                                "back" : dict(),
                                            },
                                            'function': useful_stuff.reboot_bootloader
                                        },
                                        "back" : dict(),
                                    },
                                },
                                "back" : dict()
                            }
                        },
                    }
                }
            }

STYLE = {
    'section': 'bg:#ffffff bold',
    'section1': 'bg:#dd0000 bold white',
    'section2': 'bg:#dd5500 bold white',
    'section3': 'bg:#dd8800 bold white',
    'option': 'ansigreen bold',
    'descr': 'ansiyellow bold',
    'error':'bg:#ff0000 bold white',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
    'space':'white'
}