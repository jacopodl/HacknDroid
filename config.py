from modules import apk_analyzer, apk_install,app_logs, cli_management, file_transfer, utility

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
                                    'function' : apk_analyzer.apk_analysis
                                },
                                "from_mobile_device" : { 
                                    'description': ["Write the following two strings (separated by space):",
                                                    " > the app id or a part of the app name to be extracted and analysed"
                                                    " > the path of the folder where the apk will be decompiled"
                                                    ],
                                    'children': {
                                        "back" : dict(),
                                    },
                                    'function': apk_analyzer.apk_analysis
                                },
                                'back' : dict()
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
                        "download_from_mobile" :  { 
                            'description': ["Write the following two strings (separated by space):",
                                            " > the path of the file/folder on the mobile device",
                                            " > the PC folder (where the file will be downloaded)"],
                            'children': {
                                "back" : dict(),
                            },
                            'function': file_transfer.download
                        },
                        "install" : {
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
                        }
                    }
                }
            }

STYLE = {
    'section': 'bg:#ffffff bold black',
    'section1': 'bg:#dd0000 bold white',
    'section2': 'bg:#ff00ff bold white',
    'section3': 'bg:#ff66ff bold white',
    'option': 'ansigreen bold',
    'descr': 'ansiyellow bold',
    'error':'bg:#ff0000 bold white',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
    'space':'white'
}