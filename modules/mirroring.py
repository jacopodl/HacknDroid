import subprocess
import os
import signal
import threading
from modules.tasks_management import DAEMONS_MANAGER

MIRRORING_TASK_ID = -1

def mirroring(user_input):
    global MIRRORING_TASK_ID

    if MIRRORING_TASK_ID == -1:
        MIRRORING_TASK_ID = DAEMONS_MANAGER.add_task('mirroring', ['scrcpy'])
    
def stop_mirroring(user_input):
    global MIRRORING_TASK_ID
    DAEMONS_MANAGER.stop_task('mirroring', MIRRORING_TASK_ID)
    MIRRORING_TASK_ID = -1