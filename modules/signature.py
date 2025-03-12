"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from modules.utility import valid_apk_file
import os
from modules.tasks_management import Task
import shutil

def sign_apk(user_input, signed_file=None):
    """
    Sign an APK file

    Parameters:
    user_input (str): Path of the APK file
    """

    # Path of the APK file
    apk_path = valid_apk_file(user_input)
    
    if not signed_file:
        dest_folder = os.path.join("results", os.path.basename(apk_path).replace(".apk", ""),"signed")
        os.makedirs(dest_folder, exist_ok=True)
        signed_file = os.path.join(dest_folder, "signed_"+os.path.basename(apk_path))
        shutil.copy(apk_path, signed_file)

    # Keystore file path
    keystore_file = os.path.join(os.path.dirname(signed_file),'tmp-self-key.keystore')
    # Password
    password = 'Password4dvanc3d!'
    # If the path exists delete the keystore
    if os.path.exists(keystore_file):
        os.remove(keystore_file)

    # Command to create a new keystore file to be used to sign the zip-aligned APK
    # keytool is related to JDK and it is usually at $JAVA_HOME/bin
    command = ['keytool', '-genkeypair', '-v', '-keystore', keystore_file, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-alias', 'my-key-alias', '-storepass', password, '-keypass', password, '-dname', "CN=John Doe, OU=Development, O=MyCompany, L=New York, ST=NY, C=US"]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

    # Command to sign the APK using the password and the keystore created
    command = ['apksigner', 'sign', '--ks', keystore_file, '--ks-pass', f'pass:{password}', '--key-pass', f'pass:{password}', '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true', signed_file]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)