import subprocess
import os
import signal
import threading
from modules.tasks_management import DAEMONS_MANAGER, Task
from modules.file_transfer import download
from modules.utility import sd_path

MIRRORING_TASK_ID = -1
VIDEO_TASK_ID = -1
MOBILE_VIDEO_PATH = ''

def mirroring(user_input):
    """
    Start screen mirroring on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    global MIRRORING_TASK_ID

    if MIRRORING_TASK_ID == -1:
        MIRRORING_TASK_ID = DAEMONS_MANAGER.add_task('mirroring', ['scrcpy'])
    
def stop_mirroring(user_input):
    """
    Stop screen mirroring on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    global MIRRORING_TASK_ID
    
    if MIRRORING_TASK_ID != -1:
        DAEMONS_MANAGER.stop_task('mirroring', MIRRORING_TASK_ID)
        MIRRORING_TASK_ID = -1

def screenshot(user_input):
    """
    Take a screenshot on the mobile device and download it.

    Args:
        user_input (str): User input (not used in this function).
    """
    mobile_path = os.path.join(sd_path(), 'screenshot.png')
    print(os.sep)
    if os.sep == '\\':
        mobile_path = mobile_path.replace(os.sep, "/")

    print(mobile_path)
    dest_path = './'
    command = ['adb','shell','screencap','-p',mobile_path]
    output, error = Task().run(command)

    download(mobile_path, dest_path)


def record_video(user_input):
    """
    Start recording the screen on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    global VIDEO_TASK_ID, MOBILE_VIDEO_PATH

    MOBILE_VIDEO_PATH = os.path.join(sd_path(), 'screenshot.mp4')
    print(os.sep)
    if os.sep == '\\':
        MOBILE_VIDEO_PATH = MOBILE_VIDEO_PATH.replace(os.sep, "/")

    print(MOBILE_VIDEO_PATH)
    command = ['adb','shell','screenrecord',MOBILE_VIDEO_PATH]
    VIDEO_TASK_ID = DAEMONS_MANAGER.add_task('video', command)

def stop_recording(user_input):
    """
    Stop recording the screen on the mobile device and download the video.

    Args:
        user_input (str): User input (not used in this function).
    """
    global VIDEO_TASK_ID, MOBILE_VIDEO_PATH 
    dest_path = './'
    if MOBILE_VIDEO_PATH != '':
        DAEMONS_MANAGER.stop_task('video', VIDEO_TASK_ID)
        download(MOBILE_VIDEO_PATH, dest_path)