import config

import subprocess
import re

def app_id(grep_string):
    '''
    Retrieve the full list of the applications on the device:
        adb shell pm list packages
    
    Grep the content based on keywords inserted by the user and separated by whitespaces
    '''

    #Remove a sequence of more than one whitespace
    grep_string = re.sub(r"\s{2,}", " ", grep_string)
    # Take the full list of the values to be searched
    grep_values = grep_string.split(' ')
    
    # List all the application IDs
    command = ['adb', 'shell', 'pm', 'list', 'packages']
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages'], capture_output=True, text=True)

    packages = []
    # If ADB command goes well
    if result.returncode == 0:
        # All the lines returned by the comman (one line per package)
        lines = result.stdout.splitlines()
        
        # Iterate over the lines looking for a match
        for l in lines:
            # If only one value 
            check = grep_values[0] in l

            if len(grep_values)>1:
                for v in grep_values[1:]:
                    check = check and (v in l)

            if check:
                packages.append(l.replace("package:",""))

    print(packages)
    return packages

def sd_path():
    '''
    Identify current SD Card folder
        adb shell
        > echo $EXTERNAL_STORAGE
        > exit
    '''
    
    # Open ADB shell
    command = ['adb', 'shell']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Print the external storage path
    command = ['echo $EXTERNAL_STORAGE','exit']
    output, error = process.communicate(input=cmd_to_subprocess_string(command))
    sdcard_path = output.splitlines()[0]
    
    print(sdcard_path)
    return sdcard_path

def cmd_to_subprocess_string(cmd):
    return '\n'.join(cmd)

if __name__=="__main__":
    app_ids = app_id("ap  mov")
    x=input("Press ENTER to continue")
    sdcard_path = sd_path()
    x=input("Press ENTER to continue")
