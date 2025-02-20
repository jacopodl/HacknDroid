from modules.utility import app_id_from_user_input, valid_apk_file
from modules.file_transfer import download
from modules.merge_apks import merge_from_dir
import os
import glob
import shutil
from modules.signature import sign_apk
from modules.tasks_management import Task
from modules.adb import get_session_device_id

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
    # Transfer APKs of the app with info provided in the user input (App ID or words belonging to the App ID)
    num_apks, app_folder = transfer_apks_from_device(user_input)

    apk_name = ''
    if num_apks > 1:
        # Check for app with multiple APKs to be merged
        if check_for_merge:
            # Ask the user to merge or not the APKs 
            print("You have multiple APKs. Do you want to also merge them (y/n)?", end=" ")
            choice = input()

            if choice.lower()=="y":
                # If user input is equal to 'y', merge the APKs
                apk_name = merge_from_dir(app_folder)
        else:
            # Merge the APKs
            apk_name = merge_from_dir(app_folder)
    else:
        # The app is composed by a unique APK 
        apk_files = [os.path.join(app_folder,f) for f in os.listdir(app_folder) if f.endswith('.apk')]
        apk_name = apk_files[0]

    return apk_name


def apk_decompiler_from_device(user_input):
    """
    Get the APKs of an app from the device and decompile it

    Parameters:
    user_input (str): App ID or words belonging to the APP ID 
    """

    # Get the APK from the device
    apk_filepath = get_apk_from_device(user_input)
    print(apk_filepath)

    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_decompiler_from_file(apk_filepath)
    

def apk_decompiler_from_file(user_input):
    """
    Decompile an APK file

    Parameters:
    user_input (str): Path of the APK file on the PC 
    """
    
    # Check if the path is valid for an APK file
    apk_path = valid_apk_file(user_input)
    # Folder name for the decompiled APK is the name of the APK without extension 
    dest_folder = os.path.basename(user_input).replace(".apk", "")

    # Decompile the program
    # apktool d APP.apk -o <dir>
    command = ['apktool','d', user_input, "-o", dest_folder]
    print(command)

    output, error = Task().run(command, is_shell=True)
    print(output)


def jar_from_device(user_input):
    """
    Get the APKs of an app from the device and create a JAR file from them

    Parameters:
    user_input (str): App ID or words belonging to the APP ID 
    """

    # Get the APKs of the App from the device
    apk_filepath = get_apk_from_device(user_input)
    # Create the JAR file from the APKs
    create_jar_from_apk_path(apk_filepath)


def jar_from_file(user_input):
    """
    Create a JAR file from an APK file

    Parameters:
    user_input (str): Path of the APK file on the PC
    """
    # Check if the path is valid for an APK file
    apk_path = valid_apk_file(user_input)
    # Create the JAR file from the APK file
    create_jar_from_apk_path(apk_path)


def create_jar_from_apk_path(apk_filepath):
    """
    Create the JAR file from an APK file

    Parameters:
    apk_filepath (str): Path of the APK file on the PC
    """

    # Create the JAR file with the following command
    # d2j-dex2jar <apk-path> --force <jar-filename>
    # --force to overwrite current JAR file
    command = ['d2j-dex2jar', apk_filepath, "--force", "-o", os.path.basename(apk_filepath).replace(".apk",".jar")]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)


def jadx_from_device(user_input):
    """
    Get the APK from the device and open JADX on the APK file

    Parameters:
    user_input (str): Path of the APK file on the PC
    """

    # Get the APK from the device
    apk_filepath = get_apk_from_device(user_input)    
    # Open JADX on the APK file specified by the user
    jadx_run_on_apk_file(apk_filepath)
    

def jadx_from_file(user_input):
    """
    Open JADX on an APK file specified by the user

    Parameters:
    user_input (str): Path of the APK file on the PC
    """

    # Check if the path is valid for an APK file
    apk_filepath = valid_apk_file(user_input)
    # Open JADX on the APK file specified by the user
    jadx_run_on_apk_file(apk_filepath)


def jadx_run_on_apk_file(apk_filepath):
    """
    Open JADX on an APK file

    Parameters:
    apk_filepath (str): Path of the APK file on the PC
    """

    # Open JADX on the APK file
    # jadx-gui <apk-file>
    command = ['jadx-gui', apk_filepath]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

def apk_compile_from_folder(user_input):
    """
    Compile a source folder to an APK and zip-align it

    Parameters:
    user_input (str): Path of the source folder 

    Returns:
    str: The name of the APK file created (zipaligned_<source-folder>.apk)
    """

    # Check that the user input is a valid folder
    while not os.path.exists(user_input):
        user_input = input("Write the path of the folder with code to be compiled:\n")

    # Compile the program
    # apktool b <folder> -o <folder>.apk
    command = ['apktool','b', user_input, "-o", f"{user_input}.apk"]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    command = ['zipalign', '-v', '4', f"{user_input}.apk", f"zipaligned_{user_input}.apk"]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

    return f"zipaligned_{user_input}.apk"

def apk_compile_and_sign_from_folder(user_input):
    """
    Compile a source folder to an APK and sign the 

    Parameters:
    user_input (str): Path of the APK file on the PC
    """

    # Create a new keystore file for signing the zip aligned APK
    # keytool -genkey -v -keystore <keystore_name> -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
    # Use keystore file for signing the zip aligned APK
    # apksigner sign --ks <keystore_name> --v1-signing-enabled true --v2-signing-enabled true <zip_aligned_apk.apk>

    # Compile and zip-align a source folder
    apk_file = apk_compile_from_folder(user_input)
    # Sign the APK file created
    sign_apk(apk_file)


def transfer_apks_from_device(user_input):
    """
    Get the APKs from the device

    Parameters:
    user_input (str): User input (App ID or words belonging to the App ID) 

    Returns:
    int: Num of the APKs of the App specified
    str: Path of the folder with the downloaded APK files (i.e. '.tmp/<app-id>')
    """

    # Get the App ID from the user input (App ID or words belonging to the App ID)
    app_id = app_id_from_user_input(user_input)

    # Identify the subfolder of /data/app/ for the user-installed app
    # (a subfolder has the format '<app-id>-<uuid>')
    print("GET APKS: "+app_id)
    command = ['adb', '-s', get_session_device_id(), 'shell']
    shell_input = ["su root",f'ls {DATA_APP_FOLDER} | grep "{app_id}"', "exit"]
    
    output, error = Task().run(command, input_to_cmd=shell_input)
    print(output)

    # App folder with the APKs
    app_folder = output.strip()
    print(app_folder)

    # Create a .tmp folder on the current PC
    if not os.path.exists('.tmp'):
        os.mkdir(".tmp")

    # Remove the folder with APKs of the specified App
    if os.path.exists(f".tmp/{app_folder}"):
        shutil.rmtree(f".tmp/{app_folder}")

    # Remove the folder with name <app-id> if already exists in .tmp
    if os.path.exists(f".tmp/{app_id}"):
        shutil.rmtree(f".tmp/{app_id}")

    # Download the App folder to the .tmp
    download(f"{DATA_APP_FOLDER}/{app_folder}", ".tmp")
    # Rename the folder .tmp/<app-id>-<uuid> to .tmp/<app-id>
    os.rename(f".tmp/{app_folder}", f".tmp/{app_id}")

    
    return len(glob.glob(f'.tmp/{app_id}/*.apk', )), f".tmp/{app_id}"