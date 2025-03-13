"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import re
from modules.utility import app_id_from_user_input, current_date, valid_apk_file
from modules.file_transfer import download
from modules.merge_apks import merge_from_dir
import os
import glob
import shutil
from modules.signature import sign_apk
from modules.tasks_management import Task
from modules.adb import get_session_device_id
from pathlib import Path
from termcolor import colored, cprint
from alive_progress import alive_bar

DATA_APP_FOLDER = "/data/app"
'''
Certificate Pinning
    - SHA256 string: r'^[a-fA-F0-9]{64}$
    - SHA1 string: r'^[a-fA-F0-9]{40}$'
    - SHA256, SHA1, MD5 base64-encoded string: [sha256|sha1|md5][A-Za-z0-9+/=]+
    - android:networkSecurityConfig="@xml/network_security_config" in Manifest.xml: android:networkSecurityConfig=\"([^\"]+)\"
    - OkHTTP: okhttp3, OkHttpClient, CertificatePinner, certificatePinner(, 
                okhttp3.CertificatePinner, okhttp3.OkHttpClient; okhttp3.Request,
                okhttp3.Response;
    - HttpsURLConnection: X509TrustManager, HttpsURLConnection, 
                            javax.net.ssl.HttpsURLConnection, javax.net.ssl.X509TrustManager,
                            java.security.cert.X509Certificate, java.security.PublicKey,
                            java.security.MessageDigest
    - TrustManager: javax.net.ssl, java.security.cert.X509Certificate, X509TrustManager,
                    SSLContext
    - WebView: MessageDigest, PublicKey, X509Certificate, SSLContext, HttpsURLConnection,
                X509TrustManager, onReceivedSslError(, java.security.MessageDigest, java.security.PublicKey,
                java.security.cert.X509Certificate, javax.net.ssl.SSLContext,
                javax.net.ssl.X509TrustManager, javax.net.ssl.HttpsURLConnection

Root Detection
    - Presence of Root Binaries:
      Checks for the presence of root binaries such as su, busybox, etc., in common system directories (/system/bin/su, /system/xbin/su).
    
    - Executable Root Binaries:
      Verifies if the su binary or other root binaries are executable.
    
    - Unsafe System Paths:
      Checks for dangerous system paths and directories commonly associated with rooted devices (/system/xbin, /data/local/tmp, etc.).
    
    - Root Management Apps:
      Detects the presence of root management apps like SuperSU, Magisk, or RootCloak.
    
    - Unsafe Permissions:
      Checks for permissions like READ_LOGS, ACCESS_SUPERUSER, and other risky permissions that may indicate a rooted device.
    
    - Root-Specific Files:
      Looks for files that are commonly found on rooted devices, such as /system/app/Superuser.apk, or files associated with root apps.
    
    - System Properties:
      Verifies system properties like ro.debuggable, ro.secure, ro.build.tags, and test-keys that are modified on rooted devices.
    
    - SELinux Status:
      Checks if SELinux is set to permissive mode, a common feature on rooted devices.
    
    - Custom ROM Detection:
      Detects if the device is running a custom ROM or firmware modification that could be a sign of a rooted device.
    
    - Integrity Checks (CTS, Attestation):
      Verifies device integrity via CTS (Compatibility Test Suite) profile or SafetyNet attestation to detect root or system tampering.
    
    - System Partition Modifications:
      Detects modifications to system partitions that are typical in rooted devices (e.g., boot image modifications, systemless root).
    
    - Presence of Root-Related Files:
      Checks for files or directories related to root apps like com.noshufou.android.su, Superuser.apk, or root management files.
    
    - Root Hiding Mechanism:
      Detects if tools like Magisk Hide are being used to hide root from apps.
    
    - File System Integrity Checks:
      Verifies the integrity of the file system to detect modifications common in rooted devices.
    
    - Test for Abnormal File Modifications:
      Looks for abnormal file changes or unusual files that may indicate tampering or rooting.
'''

APK_ANALYSIS_DICT = {
    "*.smali" : {
        "Certificate Pinning Hints" : {
            "SHA256 string": [r"^[a-fA-F0-9]{64}$",],
            "SHA1 string": [r"^[a-fA-F0-9]{40}$'",],
            "SHA256; SHA1 and MD5 base64-encoded string": [r"(sha256|sha1|md5)[A-Za-z0-9+/=]+",],
            "OkHTTP": [r"okhttp3", r"OkHttpClient", r"CertificatePinner", r"certificatePinner\(", r"okhttp3\.CertificatePinner", 
                        r"okhttp3\.OkHttpClient", r"okhttp3\.Request", r"okhttp3\.Response",],
            "HttpsURLConnection": [r"X509TrustManager", r"HttpsURLConnection", r"javax\.net\.ssl\.HttpsURLConnection", 
                                    r"javax\.net\.ssl\.X509TrustManager", r"java\.security\.cert\.X509Certificate", r"java\.security\.PublicKey", 
                                    r"java\.security\.MessageDigest"],
            "TrustManager": [r"javax\.net\.ssl", r"java\.security\.cert\.X509Certificate", r"X509TrustManager", r"SSLContext"],
            "WebView": [r"MessageDigest", r"PublicKey", r"X509Certificate", r"SSLContext", r"HttpsURLConnection", r"X509TrustManager", 
                        r"onReceivedSslError\(", r"java\.security\.MessageDigest", r"java\.security\.PublicKey", r"java\.security\.cert\.X509Certificate", 
                        r"javax\.net\.ssl\.SSLContext", r"javax\.net\.ssl\.X509TrustManager", r"javax\.net\.ssl\.HttpsURLConnection"]
        },
        "Root Detection Hints": {
            "RootBeer": [r"RootBeer",r"scottyab\.rootbeer"],
            "Magisk": [r"Magisk",r"com\.topjohnwu\.magisk",r"magisk"],
            "SafetyNet (Google Play Services)": [r"SafetyNet",r"com\.google\.android\.gms\.safetynet",r"SafetyNetApi",r"com\.google\.android\.gms\.common\.api\.Api"],
            "Root Sniffer": [r"RootSniffer",r"com\.p1nox\.rootsniffer"],
            "RootCloak (Xposed Framework)": [r"RootCloak",r"de\.robv\.android\.xposed",r"Xposed",r"com\.devadvance\.rootcloak"],
            "Root JUDGE":[r"RootJudge",r"com\.karbap\.rootjudge"],
            "Android-Root-Checker":[r"RootChecker",r"com\.jmpeu\.androidrootchecker"],
            "RootCheck":[r"RootCheck",r"com\.cryptic\.knight\.rootcheck"],
            "Dr Android (Root Detection and Anti-Tampering)":[r"DrAndroid",r"com\.drandroid"],
            "Anti-Root":[r"AntiRoot",r"com\.antiroot"],
            "General checks": [r"\/system\/bin\/su",r"\/system\/xbin\/su",r"\/system\/xbin",r"\/data\/local\/tmp", r"READ_LOGS", r"ACCESS_SUPERUSER", 
                                r"\/system\/app\/Superuser\.apk", r"Superuser\.apk", r"ro\.debuggable",r"ro\.secure",r"ro\.build\.tags",r"key-tags",
                                r"SELinux",r"com\.noshufou\.android\.su", r"root"]
        }
    },
    "AndroidManifest.xml": {
        "Certificate Pinning Hints" : {
            "networkSecurityConfig": [r"android:networkSecurityConfig=\"([^\"]+)\"",],
        }
    }
}

def signature_scheme_verifier():
    """pm list packages -f"""

def apk_analysis_from_device(user_input):
    """
    Analyze an APK from the device.

    Args:
        user_input (str): The App ID or keywords to identify the application.
    """
    # Get the APK from the device
    apk_filepath = get_apk_from_device(user_input)
    # Perform analysis on the APK file
    perform_apk_analysis(apk_filepath)

def apk_analysis_from_file(user_input):
    """
    Analyze an APK file from the local filesystem.

    Args:
        user_input (str): The path to the APK file.
    """
    # Check if the path is valid for an APK file
    apk_filepath = valid_apk_file(user_input)
    # Perform analysis on the APK file
    perform_apk_analysis(apk_filepath)

def perform_apk_analysis(apk_filepath):
    """
    Perform analysis on an APK file.

    Args:
        apk_filepath (str): The path to the APK file.
    """
    global APK_ANALYSIS_DICT
    # Example analysis: Print the APK file path
    print(f"Analyzing APK: {apk_filepath}")
    
    now = current_date()
    folder_path = apk_decompiler_from_file(apk_filepath)
    
    app_id = app_info_from_apk(apk_filepath)["name"]
    results_folder = os.path.join("results", app_id, "apk_analysis", now)
    
    os.makedirs(results_folder, exist_ok = True)

    output_files = {
        "Certificate Pinning Hints": os.path.join(results_folder, "certificate_pinning_hints.csv"), 
        "Root Detection Hints": os.path.join(results_folder, "root_detection_hints.csv")
    }

    results = analyse_apk(folder_path, APK_ANALYSIS_DICT, output_files)

    choice = 'x'
    while choice!='y' and choice!='n':
        choice = input(colored("\nDo you want to see results also on stdout? (y/n)\n", 'green')).lower()
        
    if choice=='y':
        for feature in results:
            cprint(f"\n\n{feature}", 'red')

            for check_type in results[feature]:
                cprint(check_type, 'cyan')

                for evidence in results[feature][check_type]:
                    cprint(f"  - {evidence['file']}:{evidence['line_number']}:", 'yellow', end=" ") 
                    print(evidence['line_content'])

                print("")

            for check_type in results[feature]:
                cprint(check_type, 'cyan')

                for evidence in results[feature][check_type]:
                    cprint(f"  - {evidence['file']}:{evidence['line_number']}:", 'yellow', end=" ") 
                    print(evidence['line_content'])

        
        print("")


def analyse_apk(folder_path, re_apk_analysis_dict, output_files):
    folder = Path(folder_path)

    results = {}
    
    for file_format in re_apk_analysis_dict:
        files = [str(f) for f in list(folder.rglob(file_format)) if not str(f).startswith(folder_path+"/original") and not str(f).startswith(folder_path+"\\original")]
        
        print("")

        with alive_bar(len(files), title=colored(file_format,'red')) as bar:
            for target_file in files:
                bar.text(colored(target_file,'yellow'))
                #print(target_file)
                with open(target_file, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, start=1):
                        for feature in re_apk_analysis_dict[file_format]:
                            for check_type in re_apk_analysis_dict[file_format][feature]:
                                for check in re_apk_analysis_dict[file_format][feature][check_type]:
                                    try:
                                        if re.search(check, line):
                                            # Add the details of the occurrence
                                            if feature not in results:
                                                results[feature] = {}

                                            if check_type not in results[feature]:
                                                results[feature][check_type] = []

                                            results[feature][check_type].append({
                                                'regex': check,
                                                'file': target_file,
                                                'line_number': line_number,
                                                'line_content': line.strip()
                                            })

                                        
                                    except re.error as e:
                                        print(f"ERROR: {check}")

                bar()

            bar.title(colored(file_format, 'green'))

    print("\n\nResults:")
    for feature in output_files:
        with open(output_files[feature], 'w') as results_f:
            for check_type in results[feature]:            
                # Iterate over the lines of the file
                for evidence in results[feature][check_type]:
                    results_f.write(f"{check_type},{evidence['regex']},{evidence['file']},"+
                                    f"{evidence['line_number']},{evidence['line_content'].strip()}\n")
                
            print("\nresults written to ",colored(output_files[feature], 'red'))

    return results
    

def get_apk_from_device(user_input, check_for_merge=False):
    '''
        APK Analysis
        - apk extraction from the mobile device or on the pc
        - apk decoding with apktool
        java -jar 
    '''
    # Transfer APKs of the app with info provided in the user input (App ID or words belonging to the App ID)
    num_apks, app_folder, app_id = transfer_apks_from_device(user_input)

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
    apk_filepath, app_id = get_apk_from_device(user_input)
    print(apk_filepath)

    # Decompile the program
    # apktool d APP.apk -o <dir>
    apk_decompiler_from_file(apk_filepath, app_id)
    

def apk_decompiler_from_file(user_input):
    """
    Decompile an APK file

    Parameters:
    user_input (str): Path of the APK file on the PC 
    """
    
    print("Decompiling the APK...", end=" ")
    # Check if the path is valid for an APK file
    apk_path = valid_apk_file(user_input)

    # Folder name for the decompiled APK is the name of the APK without extension 
    app_id = app_info_from_apk(user_input)["name"]

    dest_folder = os.path.join("results", app_id, "decompiled")

    os.makedirs(dest_folder, exist_ok=True)

    now = current_date()
    decompiled_folder = os.path.join(dest_folder, now)

    # Decompile the program
    # apktool d APP.apk -o <dir>
    command = ['apktool','d', user_input, "-o", decompiled_folder]

    output, error = Task().run(command, is_shell=True)
    print("DONE")

    return decompiled_folder


def jar_from_device(user_input):
    """
    Get the APKs of an app from the device and create a JAR file from them

    Parameters:
    user_input (str): App ID or words belonging to the APP ID 
    """

    # Get the APKs of the App from the device
    apk_filepath, app_id = get_apk_from_device(user_input)
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
    
    now = current_date()

    app_id = app_info_from_apk(apk_filepath)["name"]
    jar_folder = os.path.join("results", app_id, "jar")
    
    os.makedirs(jar_folder, exist_ok=True)

    print(app_id)
    jar_path = os.path.join(jar_folder,f"{now}_{app_id}.jar")

    command = ['d2j-dex2jar', apk_filepath, "--force", "-o", jar_path]
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
    apk_filepath, app_id = get_apk_from_device(user_input)    
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
    while (not os.path.exists(user_input)) or \
          (not os.path.exists(os.path.join(user_input, "AndroidManifest.xml"))) or \
           (not os.path.exists(os.path.join(user_input, "apktool.yml"))):
        user_input = input("Write the path of the folder with code to be compiled:\n")

    app_id = get_app_id_from_manifest(os.path.join(user_input, "AndroidManifest.xml"))

    # Compile the program
    # apktool b <folder> -o <folder>.apk
    now = current_date()
    compiled_folder = os.path.join("results", app_id, "compiled", now)
    os.makedirs(compiled_folder, exist_ok=True)

    print("Compiling the APK file...", end=" ")
    command = ['apktool','b', user_input, "-o", os.path.join(compiled_folder, f"{app_id}.apk")]
    output, error = Task().run(command, is_shell=True)
    print("DONE")

    # Zipalign is a zip archive alignment tool that helps ensure that all uncompressed files in the archive are aligned
    # relative to the start of the file. Zipalign tool can be found in the “Build Tools” folder within the Android SDK path.
    # zipalign -v 4 <recompiled_apk.apk> <zipaligned_apk.apk>
    print("ZIP-aligning the APK file...", end=" ")
    command = ['zipalign', '-v', '4', os.path.join(compiled_folder, f"{app_id}.apk"), os.path.join(compiled_folder, f"zipaligned_{app_id}.apk")]
    output, error = Task().run(command, is_shell=True)
    print("DONE")

    return os.path.join(compiled_folder, f"zipaligned_{app_id}.apk")

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
    
    dir_name, file_name = os.path.split(apk_file)
    signed_file = os.path.join(dir_name, file_name.replace("zipaligned_", "signed_"))
    shutil.copy(apk_file, signed_file)
    
    # Sign the APK file created
    sign_apk(apk_file, signed_file)


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
    # Note: the apk folder can be also downloaded without root permission 
    # pm list packages -f (to print the path of the apks for each package)
    # adb pull <apk_package_path> <pc_path>
    print("GET APKS: "+app_id)
    command = ['adb', '-s', get_session_device_id(), 'shell']
    shell_input = ["su root",f'ls {DATA_APP_FOLDER} | grep "{app_id}"', "exit"]
    
    output, error = Task().run(command, input_to_cmd=shell_input)
    print(output)

    # App folder with the APKs
    app_folder = output.strip()
    print(app_folder)

    results_folder = os.path.join('results', app_id, "data_folder")

    # Create a .tmp folder on the current PC
    os.makedirs(results_folder, exist_ok=True)
    now = current_date()

    # Download the App folder to the .tmp
    download(f"{DATA_APP_FOLDER}/{app_folder}", results_folder)
    # Rename the folder .tmp/<app-id>-<uuid> to .tmp/<app-id>
    os.rename(os.path.join(results_folder, app_folder), os.path.join(results_folder, f"{now}_data_apk_folder"))

    
    return len(glob.glob(os.path.join(results_folder, f"{now}_data_apk_folder")+'/*.apk', )), os.path.join(os.path.join(results_folder, f"{now}_data_apk_folder")), app_id


def get_app_id_from_manifest(manifest_path):
    import xml.etree.ElementTree as ET

    # Parse the XML file
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # Access the package name from the root element's attribute
    package_name = root.attrib.get('package')

    return package_name

def print_app_info_from_device(user_input):

    # Get the APK from the device
    apk_filepath = get_apk_from_device(user_input)
    info = app_info_from_apk(apk_filepath)

    for k in info:
        print(colored(f"{k}:", 'cyan'), end=" ")

        if k == "permissions":
            print("")
            print('\n'.join(info[k]))
        else:
            print(info[k])

    print("")

def print_app_info_from_pc(user_input):

    apk_filepath = valid_apk_file(user_input)
    info = app_info_from_apk(apk_filepath)

    for k in info:
        print(colored(f"{k}:", 'cyan'), end=" ")

        if k == "permissions":
            print("")
            print('\n'.join(info[k]))
        else:
            print(info[k])

    print("")

def app_info_from_apk(apk_filepath):
    command = ['aapt','dump','badging',apk_filepath]
    output, error = Task().run(command)

    info =  {}

    for line in output.splitlines():
        if line.startswith("package: "):
            package_values = line.replace("package:", "").strip()
            
            matches = re.findall(r"(\w+)='([\w\.]*)'", package_values)
            
            for match in matches:
                info[match[0]] = match[1]

        elif line.startswith("sdkVersion:"):
            result = re.match(r"sdkVersion: '(.*)'", line)

            if result:
                print(result.group(1))

        elif line.startswith("targetSdkVersion:"):
            result = re.match(r"targetSdkVersion: '(.*)'", line)

            if result:
                print(result.group(1))

        else:
            result = re.match(r"uses-permission: name='(.*)'", line)

            if result:
                if 'permissions' not in info:
                    info['permissions'] = []

                info['permissions'].append(result.group(1))

    return info