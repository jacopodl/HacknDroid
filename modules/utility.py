import config
import subprocess
import re

def get_app_id(grep_string):
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
    result = subprocess.run(command, capture_output=True, text=True)

    packages = []
    # If ADB command goes well
    if result.returncode == 0:
        # All the lines returned by the command (one line per package in the format "package:{app_id}")
        lines = [l.replace("package:","") for l in result.stdout.splitlines()]
        
        # Iterate over the lines looking for a match
        for l in lines:
            # Check that the first value in grep_string is in the line
            check = grep_values[0] in l

            # Check that also 
            if len(grep_values)>1:
                for v in grep_values[1:]:
                    # If the previous keyword was not found in the app ID,
                    # the app ID could not be a good candidate
                    if not check:
                        break
                    
                    # 
                    check = check and (v in l)

            # If all the keywords were found in the current app ID
            # add the app ID to the list of possible packages to be returned
            if check:
                packages.append(l)

    # List of all the packages that pass the check
    return packages

def is_app_id(user_input):
    '''
        Check if the user input is a valid app ID
    '''
    command = ['adb', 'shell', 'pm', 'list', 'packages']
    result = subprocess.run(command, capture_output=True, text=True)

    packages = []
    # If ADB command goes well
    if result.returncode == 0:
        # All the lines returned by the comman (one line per package)
        packages = [x.replace("package:","") for x in result.stdout.splitlines()]

    return user_input in packages 

def check_user_input(user_input):
    '''
        Check if the user input is a valid app ID or a valid set of keywords
    '''
    # Check if the user input is a valid app ID
    if is_app_id(user_input):
        # Return the app IDs
        return user_input
    else:
        # List of app IDs the matches the user input
        possible_app_ids = get_app_id(user_input)

        # If no possible match was found, ask keywords again to the user 
        while not possible_app_ids:
            user_input=input("Write a valid app ID or a set of keyword to be searched\n")
            possible_app_ids = get_app_id(user_input)

        # If some app IDs related to the specified keywords are found
        # List the app IDs previously found
        for (i,x) in enumerate(possible_app_ids):
            print(f"{i})  {x}")

        # The user continues to choose the ID until a valid number is inserted by him
        choice = -1
        while choice<0 or choice>=len(possible_app_ids): 
            try:
                # Number inserted by the user
                choice = int(input("Select the app you want to test: "))
            except ValueError:
                choice = -1

        # Return the app ID related to the number chosen by the user
        return possible_app_ids[choice]


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
    
    # Return the found path
    return sdcard_path

def cmd_to_subprocess_string(cmd):
    '''
        Return a list of commands as a string of commands separated by \n
        to be passed as stdin to a python subprocess 
    '''
    return '\n'.join(cmd)

if __name__=="__main__":
    '''
    check_user_input("ahehexndjax")
    x=input("Press ENTER to continue")
    '''