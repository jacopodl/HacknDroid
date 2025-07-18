"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import subprocess
from modules.adb import get_session_device_id
import config.style as tool_style
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import prompt, print_formatted_text

from modules.tasks_management import Task

CURRENT_USER = ""
CURRENT_DIR = ""

def interactive_adb_shell(user_input):
    global CURRENT_USER, CURRENT_DIR
    print("")
    # Load the CLI style from the tool_style configuration
    shell_style = Style.from_dict(tool_style.STYLE)

    command = ["adb", '-s', get_session_device_id(), "shell"]
    cmd_input = "whoami\npwd\n"
    output, error = Task().run(command, input_to_cmd=["whoami\npwd\n",])
    CURRENT_USER, CURRENT_DIR = output.splitlines()
    
    while True:
        # Prompt the user for input (tab completion enabled)
        cmd = prompt(HTML(f"<shell_user> {CURRENT_USER} </shell_user><shell_pwd> {CURRENT_DIR} </shell_pwd> "), style=shell_style, multiline=False)

        command = ["adb", '-s', get_session_device_id(), "shell"]
        cmd_input = f"su {CURRENT_USER}\ncd {CURRENT_DIR}\n{cmd}\nwhoami;pwd\n"
        output, error = Task().run(command, input_to_cmd=[cmd_input,])

        output_lines = output.strip().splitlines()
        CURRENT_USER = output_lines[-2]
        CURRENT_DIR = output_lines[-1]
        print("\n".join(output_lines[:-2]))
        print(error)