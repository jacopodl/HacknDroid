import subprocess
import os
from modules import utility
import shutil

def merge_from_dir(user_input):
    while not os.path.exists(user_input):
        user_input = input("Insert an existing folder path:\n")

    apk_name = "merged_"+utility.rsc_from_path(user_input)+".apk"

    # -f forces the delete of output apk name if it already exists
    command = [f'APKEditor.bat','m',"-f","-i", user_input, "-o", apk_name]
    print(command)
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    process.communicate()

def merge_from_list(user_input):
    check = True
    apks = user_input.split(" ")       

    check = utility.is_apk_on_system(apks)

    while not check:
        user_input = input("Provide a valid list of apks paths on your system:\n")
        apks = user_input.split(" ")
        check = utility.is_apk_on_system(apks)

    if not os.path.exists(".tmp_merge_apks"):
        os.mkdir(".tmp_merge_apks")

    for f in apks:
        shutil.copy(f,".tmp_merge_apks")

    merge_from_dir(".tmp_merge_apks")

    shutil.rmtree(".tmp_merge_apks")