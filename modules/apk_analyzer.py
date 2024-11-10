import config
from modules.utility import app_id_from_user_input, cmd_to_subprocess_string
from modules.file_transfer import download
from modules.merge_apks import merge_from_dir
import subprocess
import os
import glob
import shutil

DATA_APP_FOLDER = "/data/app"

def apk_analysis_from_device(user_input):
    '''
        APK Analysis
        - apk extraction from the mobile device or on the pc
        - apk decoding with apktool
        java -jar 
    '''
    num_apks, app_folder = get_apks_on_device(user_input)

    if num_apks > 1:
        print("You have multiple APKs. Do you want to also merge them (y/n)?", end=" ")
        choice = input()

        if choice.lower()=="y":
            merge_from_dir(app_folder)


def apk_analysis_from_file(user_input):
    '''
        APK Analysis
        - apk analysis on an apk file on the pc 
        - apk decoding with apktool
        java -jar 
    '''
    pass

def apk_decompiler_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def apk_decompiler_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jar_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jar_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass


def jadx_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def jadx_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    pass

def apk_compile_from_folder(user_input):
    # Decompile the program
    # apktool b <folder>
    # The final modded app will be in the "dist" folder located inside the original app folder created by apktool.
    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    # Create a new keystore file for signing the zip aligned APK
    # keytool -genkey -v -keystore <keystore_name> -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
    # Use keystore file for signing the zip aligned APK
    # apksigner sign --ks <keystore_name> --v1-signing-enabled true --v2-signing-enabled true <zip_aligned_apk.apk>

    pass

def apk_compile_and_sign_from_folder(user_input):
    # Decompile the program
    # apktool b <folder>
    # The final modded app will be in the "dist" folder located inside the original app folder created by apktool.
    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    # Create a new keystore file for signing the zip aligned APK
    # keytool -genkey -v -keystore <keystore_name> -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
    # Use keystore file for signing the zip aligned APK
    # apksigner sign --ks <keystore_name> --v1-signing-enabled true --v2-signing-enabled true <zip_aligned_apk.apk>

    pass

def get_apks_on_device(user_input):
    app_id = app_id_from_user_input(user_input)

    print("GET APKS: "+app_id)

    command = ['adb', 'shell']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    shell_input = ["su root",f'ls {DATA_APP_FOLDER} | grep "{app_id}"', "exit"]
    output, error = process.communicate(input=cmd_to_subprocess_string(shell_input))

    if not os.path.exists('.tmp'):
        os.mkdir(".tmp")

    app_folder = output.strip()
    print(app_folder)

    if os.path.exists(f".tmp/{app_folder}"):
        shutil.rmtree(f".tmp/{app_folder}")

    download(f"{DATA_APP_FOLDER}/{app_folder}", ".tmp")

    if os.path.exists(f".tmp/{app_id}"):
        shutil.rmtree(f".tmp/{app_id}")

    os.rename(f".tmp/{app_folder}", f".tmp/{app_id}")

    return len(glob.glob(f'.tmp/{app_id}/*.apk', )), f".tmp/{app_id}"