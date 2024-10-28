import config
import utility
import subprocess
import os

def rsc_from_path(path):
    rsc_name = os.path.basename(path)
    if rsc_name == '':
        rsc_name = os.path.basename(path[:-1])

    return rsc_name

def mobile_exists(mobile_path):
    command = ['adb', 'shell']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    shell_input = f"""(test -f "{mobile_path}" || test -d "{mobile_path}") && echo "1" """
    output, error = process.communicate(input=shell_input)
    
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
    result = subprocess.run(command, capture_output=True, text=True)

    command = ['adb', 'shell']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    rsc_name = rsc_from_path(file_folder)
    shell_input = ["su root",f"mv {sdcard}/{rsc_name} {dest_folder}", "exit"]
    output, error = process.communicate(input=utility.cmd_to_subprocess_string(shell_input))

    print("Upload done!!!")

def download(user_input):
    '''
        Download process
        adp pull <mobile_file_folder> <pc_folder>
    '''
    pass


'''
if __name__=="__main__":
    print(mobile_exists("/data/tmp"))
'''