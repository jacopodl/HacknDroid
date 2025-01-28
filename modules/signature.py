from modules.utility import valid_apk_file
import os
import subprocess
from modules.tasks_management import Task

def sign_apk(user_input):
    """
    Sign an APK file

    Parameters:
    user_input (str): Path of the APK file
    """

    # Path of the APK file
    apk_path = valid_apk_file(user_input)
    
    # Keystore file path
    keystore_file = 'tmp-self-key.keystore'
    # Password
    password = 'Password123'
    # If the path exists delete the keystore
    if os.path.exists(keystore_file):
        os.remove(keystore_file)
    
    # Command to create a new keystore file to be used to sign the zip-aligned APK
    command = ['keytool', '-genkeypair', '-v', '-keystore', keystore_file, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-alias', 'my-key-alias', '-storepass', password, '-keypass', password, '-dname', "CN=John Doe, OU=Development, O=MyCompany, L=New York, ST=NY, C=US"]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

    # Command to sign the APK using the password and the keystore created
    command = ['apksigner', 'sign', '--ks', keystore_file, '--ks-pass', f'pass:{password}', '--key-pass', f'pass:{password}', '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true', user_input]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)