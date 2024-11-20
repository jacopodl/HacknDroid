import config
from modules.utility import app_id_from_user_input, cmd_to_subprocess_string, valid_apk_file
from modules.file_transfer import download
from modules.merge_apks import merge_from_dir
import subprocess
import os
import glob
import shutil
from modules.signature import sign_apk

DATA_APP_FOLDER = "/data/app"


def apk_analysis_from_device(user_input):
    pass


def apk_analysis_from_file(user_input):
    '''
        APK Analysis
        - apk analysis on an apk file on the pc 
        - apk decoding with apktool
        java -jar 
    '''
    pass


def get_apk_from_device(user_input, check_for_merge=False):
    '''
        APK Analysis
        - apk extraction from the mobile device or on the pc
        - apk decoding with apktool
        java -jar 
    '''
    num_apks, app_folder = transfer_apks_from_device(user_input)

    apk_name = ''
    if num_apks > 1:
        if check_for_merge:
            print("You have multiple APKs. Do you want to also merge them (y/n)?", end=" ")
            choice = input()

            if choice.lower()=="y":
                apk_name = merge_from_dir(app_folder)
        else:
            apk_name = merge_from_dir(app_folder)
    else:
        apk_files = [os.path.join(app_folder,f) for f in os.listdir(app_folder) if f.endswith('.apk')]
        apk_name = apk_files[0]

    return apk_name


def apk_decompiler_from_device(user_input, check_for_merge):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_filepath = get_apk_from_device(user_input)

    print(apk_filepath)
    apk_decompiler_from_file(apk_filepath)
    

def apk_decompiler_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_path = valid_apk_file(user_input)

    dest_folder = os.path.basename(user_input).replace(".apk", "")
    command = ['apktool','d', user_input, "-o", dest_folder]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    print(stdout)


def jar_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_filepath = get_apk_from_device(user_input)
    create_jar_from_apk_path(apk_filepath)


def jar_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_path = valid_apk_file(user_input)
    create_jar_from_apk_path(apk_path)


def create_jar_from_apk_path(apk_filepath):
    # --force to overwrite current JAR file
    command = ['d2j-dex2jar', apk_filepath, "--force", "-o", os.path.basename(apk_filepath).replace(".apk",".jar")]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    print(stdout)


def jadx_from_device(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_filepath = get_apk_from_device(user_input)    
    jadx_run_on_apk_file(apk_filepath)
    

def jadx_from_file(user_input):
    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_filepath = valid_apk_file(user_input)
    jadx_run_on_apk_file(apk_filepath)


def jadx_run_on_apk_file(apk_filepath):
    command = ['jadx-gui', apk_filepath]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    print(stdout)    

def apk_compile_from_folder(user_input):
    while not os.path.exists(user_input):
        user_input = input("Write the path of the folder with code to be compiled:\n")

    # Compile the program
    # apktool b <folder> -o <folder>.apk
    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    # Create a new keystore file for signing the zip aligned APK
    # keytool -genkeypair -v -keystore tmp-self-key.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias \
    # -storepass myKeystorePassword123 -keypass myKeyPassword123 -dname "CN=John Doe, OU=Development, O=MyCompany, L=New York, ST=NY, C=US"
    # Use keystore file for signing the zip aligned APK
    # apksigner sign --ks <keystore_name> --v1-signing-enabled true --v2-signing-enabled true <zip_aligned_apk.apk>
    command = ['apktool','b', user_input, "-o", f"{user_input}.apk"]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout)

    command = ['zipalign', '-v', '4', f"{user_input}.apk", f"zipaligned_{user_input}.apk"]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout)

    return f"zipaligned_{user_input}.apk"

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

    apk_file = apk_compile_from_folder(user_input)
    sign_apk(apk_file)


def transfer_apks_from_device(user_input):
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