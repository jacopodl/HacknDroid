"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from modules import adb, apk_analyzer, apk_install, app_logs, backup, battery, connectivity, file_transfer, mem_info, merge_apks, mirroring, proxy, shell, signature, useful_stuff
import modules.tasks_management
from modules import utility

OPTIONS =   {
                'home': { 
                    "description":['',],
                    'children':{
                        "apk": {
                            'description': ['Several APKs related operations:',
                                            ' > Analysis',
                                            ' > APP info from APK/Android Manifest'
                                            ' > APK to JAR',
                                            ' > Compiling',
                                            ' > Decompiling',
                                            ' > Merge APKs',
                                            ' > Sign APK',],
                            'device_needed': False,
                            'children' : {
                                "apk_analysis": { 
                                    'description': [
                                        'Analysis of the APKs related to the application:', 
                                        ' > search for common Root Detection strings in smali files', 
                                        ' > search for common Certificate Pinning strings or SHA1-SHA256 hash string in smali files',
                                        ' > signature schema verifier'
                                        ],
                                    'device_needed': False,
                                    'children': {
                                        "from_apk_on_pc" : { 
                                            'description': ["Write the following two strings (separated by space):",
                                                            " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                            " > the path of the folder where the apk will be decompiled"
                                                            ],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            'function' : apk_analyzer.apk_analysis_from_file
                                        },
                                        "from_mobile_device" : { 
                                            'description': ["Write the following two strings (separated by space):",
                                                            " > the app id or a part of the app name to be extracted and analysed"
                                                            " > the path of the folder where the apk will be decompiled"
                                                            ],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            'function': apk_analyzer.apk_analysis_from_device
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    }
                                },
                                "app_info": { 
                                    'description': ['App info from the APK',],
                                    'device_needed': False,
                                    'children': {
                                        "from_apk_on_pc": { 
                                            'description': ['Write the path of the APK file on the PC to be analysed',],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            'function' : apk_analyzer.print_app_info_from_pc
                                        },
                                        "from_mobile_device": { 
                                            'description': ['Write the app id or a part of the app name to be analysed',],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function' : apk_analyzer.print_app_info_from_device
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                },
                                "compiling": { 
                                    'description': ['Compile an apk file from the folder with decompiled and modified code',],
                                    'device_needed': False,
                                    'children': {
                                        "compile": { 
                                            'description': ['Compile an apk file from the folder with decompiled and modified code',],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            'function' : apk_analyzer.apk_compile_from_folder
                                        },
                                        "compile_and_sign": { 
                                            'description': ['Compile and sign an apk file from the folder with decompiled and modified code',],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function' : apk_analyzer.apk_compile_and_sign_from_folder
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "decompiling": { 
                                    'description': ['Decompile an apk file',],
                                    'device_needed': False,
                                    'children': {
                                        "from_apk_on_pc" : { 
                                            'description': ["Decompile the apk file into smali code. Write the following two strings (separated by space):",
                                                            " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                            " > the path of the folder where the apk will be decompiled"],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function' : apk_analyzer.apk_decompiler_from_file
                                        },
                                        "from_mobile_device" : { 
                                            'description': ["Write the following two strings (separated by space):",
                                                            " > the app id or a part of the app name to be extracted and analysed"
                                                            " > the path of the folder where the apk will be decompiled"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home":dict()
                                            },
                                            
                                            'function': apk_analyzer.apk_decompiler_from_device
                                        },
                                        "back" : dict(),
                                        "home":dict()
                                    },
                                    
                                },
                                "apk_to_jar": {
                                    'description': ['Convert the apk to a jar file',],
                                    'device_needed': False,
                                    'children': {
                                        "from_apk_on_pc" : { 
                                            'description': ["Convert an apk file on the PC to a jar file"],
                                            'device_needed': False,
                                            'children': {
                                                "create_jar_file":{
                                                    'description': ["Convert the apk to a jar file. Write the following two strings (separated by space):",
                                                                    " > the path of the apk on your PC (or the folder with all the APKs related to the app)",
                                                                    " > the path of the folder where the JAR file will be stored"],
                                                    'device_needed': False,
                                                    'children':{
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': apk_analyzer.jar_from_file
                                                },
                                                "jadx_create_and_open_file":{
                                                    'description': ["Open the reversed apk in JADX-GUI. Write the path of the apk on your PC (or the folder with all the APKs related to the app)",],
                                                    'device_needed': False,
                                                    'children':{
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': apk_analyzer.jadx_from_file
                                                },
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                        },
                                        "from_mobile_device" : { 
                                            'description': ["Convert am apk from the mobile device to a jar file"],
                                            'device_needed': True,
                                            'children': {
                                                "create_jar_file":{
                                                    'description': ["Convert the apk to a jar file. Write the following two strings (separated by space):",
                                                                    " > the app id or a part of the app name to be extracted and analysed",
                                                                    " > the path of the folder where the apk will be decompiled"],
                                                    'device_needed': True,
                                                    'children':{
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },        
                                                    'function': apk_analyzer.jar_from_device
                                                },
                                                "jadx_create_and_open_file":{
                                                    'description': ["Open the reversed apk in JADX-GUI. Write the app id or a part of the app name to be extracted and analysed",],
                                                    'device_needed': True,
                                                    'children':{
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': apk_analyzer.jadx_from_device
                                                },
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "merge_apks": {
                                    'description': ['Merge several APKs'],
                                    'device_needed': False,
                                    'children': {
                                        "from_directory" : {
                                            'description' : ["Write the path of the directory with APKs to be merged",],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': merge_apks.merge_from_dir
                                        },
                                        "from_list" : {
                                            'description' : ["Write the list of APKs paths to be merged (separated by spaces):",],
                                            'device_needed': False,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': merge_apks.merge_from_list
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "sign_apk":{
                                    'description': ['Sign an apk on your PC. Write the path of the apk you want to test'],
                                    'device_needed': False,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': signature.sign_apk
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                        },
                        "app_data_and_logs" : {
                            'description' : ['Analysis of app data and logs:',
                                             ' > Backup and data',
                                             ' > Force App stop',
                                             ' > Track logs',],
                            'device_needed': True,
                            'children' : {
                                "backup_and_data" : {
                                    'description': ['Backup the mobile device or an application',],
                                    'device_needed': True,
                                    'children': {
                                        "backup_device" : { 
                                            'description': ["Backup the mobile device"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function' : backup.device_backup
                                        },
                                        "backup_specific_app" : { 
                                            'device_needed': True,
                                            'description': ["Backup a specific app, writing its app id or a keyword to identify it"],
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': backup.app_backup
                                        },
                                        "backup_restore" : { 
                                            'description': ["Specify the backup file path on your system to be restored on the mobile device"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': backup.restore_backup
                                        },
                                        "backup_to_folder" : { 
                                            'description': ["Specify the backup file path on your system to be extracted"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': backup.tar_extract
                                        },
                                        "reset_app_data" : { 
                                            'description': ["Reset App data"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': backup.app_data_reset
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                            
                                },
                                "dump_mem_info" : {
                                    'description': ['Dump the memory information for an application',],
                                    'device_needed': True,
                                    'children': {
                                        "run_app_meminfo" : { 
                                            'description': ["Run and dump the memory information for an application"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function' : mem_info.run_app_meminfo
                                        },
                                        "running_app_meminfo" : { 
                                            'description': ["Dump the memory information for a running application"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': mem_info.running_app_meminfo
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "force_app_stop" :  { 
                                    'description': ["Write the app id of the mobile app or some keywords to identify it"],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.force_app_stop
                                },
                                "track_logs" : {
                                    'description': ['Process for logs gathering:',
                                                    ' > automated mode: the application will be opened by the script',
                                                    ' > manual mode: the application needs to be launched by the user'],
                                    'device_needed': True,
                                    'children': {
                                        "run_and_log" : {
                                            'description' : ["Run the app and logs it using the tool",],
                                            'device_needed': True,
                                            'children': {
                                                "normal_logs" : {
                                                    'description' : ["Write the app id or a part of the app name to be launched and the log it",],
                                                    'device_needed': True,
                                                    'children': {
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': app_logs.run_and_logs
                                                },
                                                "crash_logs" : {
                                                    'description' : ["Write the app id or a part of the app name to be launched and the log its crashes",],
                                                    'device_needed': True,
                                                    'children': {
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': app_logs.run_and_crash_logs
                                                },
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                        },
                                        "running_app_log" : {
                                            'description' : ["Log a running app",],
                                            'device_needed': True,
                                            'children': {
                                                "normal_logs" : {
                                                    'description' : ["Write the app id or a part of the app name to be logged",],
                                                    'device_needed': True,
                                                    'children': {
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': app_logs.logs_from_running_process
                                                },
                                                "crash_logs" : {
                                                    'description' : ["Write the app id or a part of the app name to be logged",],
                                                    'device_needed': True,
                                                    'children': {
                                                        "back" : dict(),
                                                        "home" : dict()
                                                    },
                                                    
                                                    'function': app_logs.crash_logs_from_running_process
                                                },
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                        },
                                        "log_sessions" : {
                                            'description' : ["List logging sessions",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': app_logs.list_daemons
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                          
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                                      
                        },
                        "device_info": {
                            'description' : ["Get mobile device information",],
                            'device_needed': True,
                            'children': {
                                "apps_list": {
                                    'description' : ["Get list of all the installed apps",],
                                    'device_needed': True,
                                    'children': {
                                        "3rd_party_apps": {
                                            'description' : ["Get list of all the installed 3rd-party apps",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': useful_stuff.third_party_apps
                                        },
                                        "system_apps": {
                                            'description' : ["Get list of all the installed system apps",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': useful_stuff.system_apps
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "battery_status" : {
                                    'description' : ["Battery Status",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': battery.check_battery_status
                                },
                                "cpu_info": {
                                    'description' : ["Get CPU information",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.cpu_info
                                },
                                "general_info": {
                                    'description' : ["Get mobile device general information",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.general_info
                                },
                                "network_info": {
                                    'description' : ["Get Network information",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.network_info
                                },
                                "ram_info": {
                                    'description' : ["Get RAM information",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.ram_info
                                },
                                "storage_info": {
                                    'description' : ["Get Storage information",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.storage_info
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                        },
                        'devices':{
                            'description': ["Select one of the available mobile devices (the current one is highlighted with red/white background)"],
                            'device_needed': False,
                            'children': {
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                            'function': adb.select_device

                        },
                        'file_transfer' : {
                            'description' : ['Transfer files from/to mobile devices'],
                            'device_needed': True,
                            'children': {
                                "download_from_mobile" :  { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the path of the file/folder on the mobile device",
                                                    " > the PC folder (where the file will be downloaded)"],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': file_transfer.download_from_user_input
                                },
                                "upload_to_mobile" : { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the path of the file/folder on the PC",
                                                    " > the mobile device folder (where the file will be uploaded)"],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': file_transfer.upload
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                        },
                        "install_uninstall" : {
                            'description': ['Install an app on the mobile device.',],
                            'device_needed': True,
                            'children': {
                                "install_from_apk" : {
                                    'description' : ["Write the path of the apk on your PC to be installed",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': apk_install.install_from_apk
                                },
                                "install_from_playstore" : {
                                    'description' : ["Write the app id of the app to be installed (the command prompt will be open)",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': apk_install.install_from_playstore
                                },                                
                                "uninstall" : {
                                    'description' : ["Write the app id of the app to be uninstalled",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': apk_install.uninstall_app
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                        },
                        "interactive_shell" :{
                            'description': ['Interactive shell for the mobile device',],
                            'device_needed': True,
                            'children': {
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                            'function': shell.interactive_adb_shell
                        },
                        "mirroring" : {
                            'description': ['Launch scrcpy for mobile device mirroring (Press any key to continue)',],
                            'device_needed': True,
                            'children': {
                                "mirroring" : {
                                    'description': ['Launch scrcpy for mobile device mirroring (Press any key to continue)',],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': mirroring.mirroring
                                },
                                "stop_mirroring" : {
                                    'description': ['Stop scrcpy session for mobile device mirroring (Press any key to continue)',],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': mirroring.stop_mirroring
                                },
                                "screenshot_video" : {
                                    'description' : ["Screenshot/Video on the mobile device",],
                                    'device_needed': True,
                                    'children': {
                                        "screenshot" : {
                                            'description' : ["Screenshot.","Press enter to continue...",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': mirroring.screenshot
                                        },
                                        "video_record" : {
                                            'description' : ["Video Recording","Press enter to START recording...",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': mirroring.record_video
                                        },
                                        "stop_video_record" : {
                                            'description' : ["Video recording","Press enter to STOP recording...",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': mirroring.stop_recording
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                        },
                        "mobile_settings" : {
                            'description' : ['Mobile device settings'],
                            'device_needed': True,
                            'children' : {
                                "battery_saver" : {
                                    'description' : ["Battery Saver mode",],
                                    'device_needed': True,
                                    'children': {
                                        "off" : {
                                            'description' : ["Turn off battery saver mode",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': battery.battery_saver_off
                                        },
                                        "on" : {
                                            'description' : ["Turn on battery saver mode",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': battery.battery_saver_on
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "do_not_disturb_mode" : {
                                    'description' : ["Do Not Disturb mode",],
                                    'device_needed': True,
                                    'children': {
                                        "off" : {
                                            'description' : ["Turn off Do Not Disturb mode",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.donotdisturb_disabled
                                        },
                                        "alarms_only" : {
                                            'description' : ["Turn on Do Not Disturb mode with alarms only",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.donotdisturb_alarms_only
                                        },
                                        "priority_only" : {
                                            'description' : ["Turn on Do Not Disturb mode with priority only",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.donotdisturb_priority_only
                                        },
                                        "total_silence" : {
                                            'description' : ["Turn on Do Not Disturb mode with total silence",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.donotdisturb_total_silence
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "connectivity" : {
                                    'description' : ["Connectivity options management (Wifi, airplane mode)",],
                                    'device_needed': True,
                                    'children': {
                                        "wifi_off" : {
                                            'description' : ["Turn off Wifi option",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.disable_wifi
                                        },
                                        "wifi_on" : {
                                            'description' : ["Turn on Wifi option",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.enable_wifi
                                        },
                                        "airplane_off" : {
                                            'description' : ["Turn off Airplane mode",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.disable_airplane_mode
                                        },
                                        "airplane_on" : {
                                            'description' : ["Turn on Airplane mode",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': connectivity.enable_airplane_mode
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                            
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                                          
                        },
                        "processes_list" : {
                            'description' : ["List all the processes","Press enter to continue...",],
                            'device_needed': False,
                            'children': {
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                            'function': modules.tasks_management.list_daemons
                        },
                        "proxy" : {
                            'description': ['Set proxy on the mobile device:',
                                            ' > using the current PC IP',
                                            ' > using another IP'],
                            'device_needed': True,
                            'children': {
                                "dns" : {
                                    'description': ['Set proxy routes using a DNS server'],
                                    'device_needed': True,
                                    'children': {
                                        "get_current_proxy" : {
                                            'description' : ["Press ENTER to see current DNS proxy settings"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.get_current_dns_proxy
                                        },
                                        "set_proxy_with_current_ip" : {
                                            'description' : ["",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_current_pc_dns_proxy
                                        },
                                        "set_proxy_with_other_ip" : {
                                            'description' : ["Write the following values:",
                                                            " > IP address of the proxy",
                                                            " > port number of the proxy"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_generic_dns_proxy
                                        },
                                        "del_proxy" : {
                                            'description' : ["Press ENTER to reset proxy configuration"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.del_dns_proxy
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "invisible_proxy" : {
                                    'description': ['Set global proxy on the mobile device:',
                                                    ' > using the current PC IP',
                                                    ' > using another IP'],
                                    'device_needed': True,
                                    'children': {
                                        "get_current_proxy" : {
                                            'description' : ["Press ENTER to see current proxy settings"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.get_current_invisible_proxy
                                        },
                                        "set_proxy_with_current_ip" : {
                                            'description' : ["Write the port number for the proxy on the current PC",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_current_pc_invisible_proxy
                                        },
                                        "set_proxy_with_other_ip" : {
                                            'description' : ["Write the following values:",
                                                            " > IP address of the proxy",
                                                            " > port number of the proxy"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_generic_invisible_proxy
                                        },
                                        "del_proxy" : {
                                            'description' : ["Press ENTER to reset proxy configuration"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.del_invisible_proxy
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                },
                                "system_proxy" : {
                                    'description': ['Set global proxy on the mobile device:',
                                                    ' > using the current PC IP',
                                                    ' > using another IP'],
                                    'device_needed': True,
                                    'children': {
                                        "get_current_proxy" : {
                                            'description' : ["Press ENTER to see current proxy settings"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.get_current_proxy_settings
                                        },
                                        "set_proxy_with_current_ip" : {
                                            'description' : ["Write the port number for the proxy on the current PC",],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_current_pc_proxy
                                        },
                                        "set_proxy_with_other_ip" : {
                                            'description' : ["Write the following values:",
                                                            " > IP address of the proxy",
                                                            " > port number of the proxy"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.set_generic_proxy
                                        },
                                        "del_proxy" : {
                                            'description' : ["Press ENTER to reset proxy configuration"],
                                            'device_needed': True,
                                            'children': {
                                                "back" : dict(),
                                                "home" : dict()
                                            },
                                            
                                            'function': proxy.del_proxy
                                        },
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                            
                                },
                                "back" : dict(),
                                "home" : dict()
                            },
                            
                                            
                        },
                        "shutdown_reboot" : {
                            'description' : ["Reboot the device with several options",],
                            'device_needed': True,
                            'children': {
                                "shutdown" : {
                                    'description' : ["Shutdown the mobile device.","Press enter to continue...",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.shutdown
                                },
                                "reboot" : {
                                    'description' : ["Reboot the mobile device.","Press enter to continue...",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.reboot
                                },
                                "reboot_recovery" : {
                                    'description' : ["Reboot the mobile device in recovery mode.","Press enter to continue...",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.reboot_recovery
                                },
                                "reboot_bootloader" : {
                                    'description' : ["Reboot the mobile device in bootloader mode.","Press enter to continue...",],
                                    'device_needed': True,
                                    'children': {
                                        "back" : dict(),
                                        "home" : dict()
                                    },
                                    
                                    'function': useful_stuff.reboot_bootloader
                                },
                                "back" : dict(),
                                "home" : dict()
                            }
                        }
                    }
                }
            }