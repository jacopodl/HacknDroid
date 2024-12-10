import config.menu as menu
from modules import utility
import subprocess
import os
from modules.tasks_management import Task

def mobile_exists(paths):
    check = True
    for mobile_path in paths:
        command = ['adb', 'shell']
        shell_input = ["su root",f"""(test -f "{mobile_path}" || test -d "{mobile_path}") && echo "1" """, "exit"]
        output, error = Task().run(command, input_to_cmd=shell_input)
    
        check = check and (output.strip() == "1")

        if not check:
            print(f"{mobile_path} NOT FOUND")
            return check
    
    return check

def is_mobile_folder(mobile_path):
    command = ['adb', 'shell']
    shell_input = ["su root",f"""(test -d "{mobile_path}") && echo "1" """, "exit"]
    output, error = Task().run(command, input_to_cmd=shell_input)

    return output.strip() == "1"


def is_mobile_file(mobile_path):
    command = ['adb', 'shell']
    shell_input = ["su root",f"""(test -f "{mobile_path}") && echo "1" """, "exit"]
    output, error = Task().run(command, input_to_cmd=shell_input)

    return output.strip() == "1"


def upload(user_input):
    paths = utility.split_user_input(user_input)

    if len(paths)==1:
        if os.path.exists(paths[0]):
            upload_to_dest(file_folder=paths[0])
        else:
            print(f"Path {paths[0]} NON FOUND!!!")
    elif len(paths)==2:
        if not os.path.exists(paths[0]):
            print("Invalid PC Source path")

        elif not mobile_exists(paths[1]):
            print("Invalid Movile Destination path")
  
        else:
            upload_to_dest(paths[0], paths[1])
    else:
        print("Too many arguments specified!!!")


def upload_to_dest(file_folder, dest_folder="/data/tmp"):
    '''
        Upload process 
        adb push <pc_folder_file> <sd_card_folder>
        (where th <sd_card_folder> is the SD Card folder identified using utility function)
        
        adb shell
        > su root
        > mv <sd_card_folder>/<folder_file> <desired_folder>
        > exit
    '''

    sdcard = utility.sd_path()
    command = ['adb', 'push', file_folder, sdcard]
    output, error = Task().run(command)

    command = ['adb', 'shell']
    rsc_name = utility.rsc_from_path(file_folder)
    shell_input = ["su root",f"mv {sdcard}/{rsc_name} {dest_folder}", "exit"]
    output, error = Task().run(command, input_to_cmd=shell_input)

    print("Upload done!!!")

def download_from_user_input(user_input):
    '''
        Download process
        adp pull <mobile_file_folder> <pc_folder>
    '''

    paths = user_input.split(" ")
    
    while len(paths)<2 or not (mobile_exists(paths[:-1]) and os.path.exists(paths[-1]) and os.path.isdir(paths[-1])):
        user_input = input("""Insert at least two paths separated by spaces:\n > list of the paths of mobile files/folders to be downloaded\n > pc folder where the files will be downloaded\n\n""")
        paths = user_input.split(" ")

    print("ciao")
    for mobile_path in paths[:-1]:
        print(mobile_path)
        download(mobile_path, paths[-1])  

def download(mobile_path, dest_path, permissions_check=True):
    '''
        Download process
        adp pull <mobile_path> <dest_path>
    '''

    command = ['adb', 'pull', mobile_path, dest_path]
    output, error = Task().run(command)

    if permissions_check:
        if "permission denied" in output.lower() or "0 files pulled" in output.lower():
            x = input("[PERMISSION DENIED] Do you want to download the file/folder as Super User (y/n)? ")

            if x.lower() == "y":
                su_download(mobile_path, dest_path)


def su_download(mobile_path, dest_path):
    command = ['adb', 'shell']
    sdcard = utility.sd_path()
    rsc_name = utility.rsc_from_path(mobile_path)

    if is_mobile_folder(mobile_path):
        shell_input = ["su root",
                       f'if [ -d "{sdcard}/{rsc_name}" ]; then rm -r "{sdcard}/{rsc_name}"; fi', 
                       f"cp -r {mobile_path} {sdcard}/{rsc_name}", 
                       f"chmod 666 {sdcard}/{rsc_name}",
                       "exit"]
        
        print("\n".join(shell_input))
        output, error = Task().run(command, input_to_cmd=shell_input)
        download(f"{sdcard}/{rsc_name}", dest_path, permissions_check=False)

    elif is_mobile_file(mobile_path):
        shell_input = ["su root",
                       f'if [ -f "{sdcard}/{rsc_name}" ]; then rm "{sdcard}/{rsc_name}"; fi',
                       f"cp {mobile_path} {sdcard}/{rsc_name}", 
                       f"chmod 666 {sdcard}/{rsc_name}", 
                       "exit"]
        
        print("\n".join(shell_input))
        output, error = Task().run(command, input_to_cmd=shell_input)
        download(f"{sdcard}/{rsc_name}", dest_path, permissions_check=False)