from modules.cli_management import CLI
from modules.apk_analyzer import apk_analysis

def main():
    OPTIONS = dict()
    OPTIONS =   {
                    'main': { 
                        "description":['TEST','TEST2','TEST3'],
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
                                        'function' : apk_analysis
                                    },
                                    "from_mobile_device" : { 
                                        'description': ["Write the following two strings (separated by space):",
                                                        " > the app id or a part of the app name to be extracted and analysed"
                                                        " > the path of the folder where the apk will be decompiled"
                                                        ],
                                        'children': {
                                            "back" : dict(),
                                        }
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
                                }
                            },
                            "download_from_mobile" :  { 
                                'description': ["Write the following two strings (separated by space):",
                                                " > the path of the file/folder on the mobile device",
                                                " > the PC folder (where the file will be downloaded)"],
                                'children': {
                                    "back" : dict(),
                                }
                            },
                            "install" : {
                                'description': 'Install an app on the mobile device.',
                                'children': {
                                    "from_apk_on_pc" : {
                                        'description' : ["Write the path of the apk on your PC to be installed",],
                                        'children': {
                                            "back" : dict(),
                                        }
                                    },
                                    "from_play_store" : {
                                        'description' : ["Write the app id of the app to be installed (the command prompt will be open)",],
                                        'children': {
                                            "back" : dict(),
                                        }
                                    },
                                    "back" : dict()
                                }
                            }
                        }
                    }
                }
    
    cli_mgmt = CLI(OPTIONS)
    cli_mgmt.cli_options()

if __name__=="__main__":
    main()