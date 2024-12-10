from modules.utility import valid_apk_file
import os
import subprocess
from modules.tasks_management import Task

def sign_apk(user_input):
    apk_path = valid_apk_file(user_input)
    
    keystore_file = 'tmp-self-key.keystore'
    password = 'Password123'
    if os.path.exists(keystore_file):
        os.remove(keystore_file)

    command = ['keytool', '-genkeypair', '-v', '-keystore', keystore_file, '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000', '-alias', 'my-key-alias', '-storepass', password, '-keypass', password, '-dname', "CN=John Doe, OU=Development, O=MyCompany, L=New York, ST=NY, C=US"]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)

    command = ['apksigner', 'sign', '--ks', keystore_file, '--ks-pass', f'pass:{password}', '--key-pass', f'pass:{password}', '--v1-signing-enabled', 'true', '--v2-signing-enabled', 'true', user_input]
    print(command)
    output, error = Task().run(command, is_shell=True)
    print(output)