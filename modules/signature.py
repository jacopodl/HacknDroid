"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from datetime import datetime
from modules.utility import current_date, valid_apk_file
from modules.app_info import app_id_from_apk
import os
from modules.tasks_management import Task
import shutil
import re

def create_keystore(keystore_file, password, alias):
    # Command to create a new keystore file to be used to sign the zip-aligned APK
    # keytool is related to JDK and it is usually at $JAVA_HOME/bin
    command = ['keytool', '-genkeypair', '-v', '-keystore', keystore_file, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-alias', alias, '-storepass', password, '-keypass', password, '-dname', "CN=John Doe, OU=Development, O=MyCompany, L=New York, ST=NY, C=US"]
    print(command)
    output, error = Task().run(command, is_shell=True)

def sign_apk(user_input, signed_file=None):
    """
    Sign an APK file

    Parameters:
    user_input (str): Path of the APK file
    """

    # Path of the APK file
    apk_path = valid_apk_file(user_input)
    
    if not signed_file:
        now = current_date()
        dest_folder = os.path.join("results", app_id_from_apk(apk_path),"signed", now)
        os.makedirs(dest_folder, exist_ok=True)
        signed_file = os.path.join(dest_folder, os.path.basename(apk_path))
        shutil.copy(apk_path, signed_file)

    # Keystore file path
    keystore_file = os.path.join(os.path.dirname(signed_file),'tmp-self-key.keystore')
    # Password
    password = 'Password4dvanc3d!'
    # If the path exists delete the keystore
    if os.path.exists(keystore_file):
        os.remove(keystore_file)

    create_keystore(keystore_file, password, "ks_alias")

    # Command to sign the APK using the password and the keystore created
    command = ['apksigner', 'sign', '--ks', keystore_file, '--ks-pass', f'pass:{password}', '--key-pass', f'pass:{password}', '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true', signed_file]
    print(command)
    output, error = Task().run(command, is_shell=True)

def scheme_verify(apk_filepath):
    command = ['apksigner', 'verify', '--verbose', apk_filepath]
    output, error = Task().run(command, is_shell=True)
    
    schemes = {}
    warnings = []
    utc_timestamp = ''

    for line in output.decode().splitlines():
        if line.startswith("Source Stamp Timestamp:"):
            utc_timestamp = datetime.utcfromtimestamp(int(line.replace("Source Stamp Timestamp:", "").strip()))

        elif line.startswith("WARNING"):
            warnings.append(line.replace("WARNING:", "").strip())

        else:
            matches = re.findall(r"Verified using (.*) \((.*)\): (.*)", line)

            if matches:
                schemes[matches[0][0]] = {
                    "type": matches[0][1], 
                    "check":matches[0][2]
                }

    return schemes, utc_timestamp

def certificate_info(apk_filepath):
    # Command to sign the APK using the password and the keystore created
    command = ['apksigner', 'verify', '--print-certs', apk_filepath]
    print(command)
    output, error = Task().run(command, is_shell=True)
    #print(output.decode())
    certificates = {}

    for line in output.decode().splitlines():
        dn_match = re.match(r"(.*) certificate DN: (.*)", line)
        sha256_match = re.match(r"(.*) certificate SHA-256 digest: (.*)", line)
        sha1_match = re.match(r"(.*) certificate SHA-1 digest: (.*)", line)
        md5_match = re.match(r"(.*) certificate MD5 digest: (.*)", line)

        if dn_match:
            if dn_match[1] not in certificates:
                certificates[dn_match[1]] = {}

            certificates[dn_match[1]]["Distinguished Name"] = dn_match[2]                    

        elif sha256_match:
            if sha256_match[1] not in certificates:
                certificates[sha256_match[1]] = {}

            certificates[sha256_match[1]]["SHA-256 digest"] = sha256_match[2]                    

        elif sha1_match:
            if sha1_match[1] not in certificates:
                certificates[sha1_match[1]] = {}

            certificates[sha1_match[1]]["SHA-1 digest"] = sha1_match[2]                    

        elif md5_match:
            if md5_match[1] not in certificates:
                certificates[md5_match[1]] = {}

            certificates[md5_match[1]]["MD5 digest"] = md5_match[2]                    

    return certificates