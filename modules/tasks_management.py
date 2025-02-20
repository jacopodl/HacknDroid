import subprocess
import threading
from modules.utility import cmd_to_subprocess_string 
from tabulate import tabulate
import copy
from termcolor import colored

class DaemonTask():
    def __init__(self, command, args=tuple()):
        """
        Initialize a DaemonTask instance.
        """
        self._PROCESS = None
        self._THREAD = None
        self._command = command
        self._args = args

    def run(self):
        """
        Run the daemon task.

        Args:
            command (callable or list): The command to run.
            args (tuple): Arguments for the command.
        """
        if not self._PROCESS:
            if callable(self._command):
                self._THREAD = threading.Thread(target=self._command, args=self._args)
            else:
                self._THREAD = threading.Thread(target=self.thread_function, args=(self._command,))

            self._THREAD.daemon = True
            self._THREAD.start()

    def thread_function(self, command):
        """
        Function to run the command in a separate thread.

        Args:
            command (list): The command to run.
        """
        self._PROCESS = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL ,text=True)
        output, error = self._PROCESS.communicate()
        # Process stoped before by the user
        self._PROCESS = None
    
    def stop(self):
        """
        Stop the daemon task.
        """
        if self._PROCESS:
            self._PROCESS.terminate()
            self._THREAD.join()
        elif self._THREAD:
            self._THREAD = None
        else:
            print("The process was already finished!!!")

class DaemonTaskManager():
    def __init__(self):
        """
        Initialize a DaemonTaskManager instance.
        """
        self._TOOL_TASKS = {}
        self._ID = 0
        self._TASK_HEADERS = ['Functionality', 'Task ID']
        self._ADDITIONAL_HEADERS = []

    def add_task(self, functionality, command, args=None):
        """
        Add a new daemon task.

        Args:
            functionality (str): The functionality of the task.
            command (callable or list): The command to run.
            args (tuple): Arguments for the command.

        Returns:
            int: The ID of the added task.
        """
        task = None 
        task = DaemonTask(command, args)
        if args:
            task = DaemonTask(command, args)
        else:
            task = DaemonTask(command)

        task.run()

        if functionality not in self._TOOL_TASKS:
            self._TOOL_TASKS[functionality] = {}
        
        id = self._ID
        self._TOOL_TASKS[functionality][id] = {'task': task, 'additional info': {}}
        self._ID += 1

        return id
    
    def stop_task(self, functionality, id):
        """
        Stop a specific daemon task.

        Args:
            functionality (str): The functionality of the task.
            id (int): The ID of the task.
        """
        if functionality in self._TOOL_TASKS:
            if id in self._TOOL_TASKS[functionality]:
                self._TOOL_TASKS[functionality][id]['task'].stop()

                for additional_key in list(self._TOOL_TASKS[functionality][id]['additional info'].keys()):
                    self._ADDITIONAL_HEADERS.remove(additional_key)

                del self._TOOL_TASKS[functionality][id]

            if not self._TOOL_TASKS[functionality].keys():
                del self._TOOL_TASKS[functionality]
        else:
            print("No running daemon tasks!!!")

    def stop_all_tasks(self):
        """
        Stop all running daemon tasks.
        """
        tasks_info = []
        for functionality in self._TOOL_TASKS:
            for id in self._TOOL_TASKS[functionality]:
                tasks_info.append((functionality, id))

        for func_id in tasks_info:
            self.stop_task(func_id[0], func_id[1])

    def get_dict(self):
        """
        Get the dictionary of all tasks.

        Returns:
            dict: The dictionary of all tasks.
        """
        return self._TOOL_TASKS
    
    def get_next_id(self):
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID.
        """
        return self._ID
    
    def add_info(self, functionality, id, dict_info):
        """
        Add additional information to a specific task.

        Args:
            functionality (str): The functionality of the task.
            id (int): The ID of the task.
            dict_info (dict): The additional information to add.
        """
        for k in dict_info:
            self._ADDITIONAL_HEADERS.append(k)

        self._TOOL_TASKS[functionality][id]['additional info']=dict_info

    def get_headers(self):
        """
        Get the headers for the task table.

        Returns:
            list: The list of headers.
        """
        headers = copy.deepcopy(self._TASK_HEADERS)

        for k in list(set(self._ADDITIONAL_HEADERS)):
            headers.append(k)

        return headers
        

class Task():
    def __init__(self):
        """
        Initialize a Task instance.
        """
        pass

    def run(self, command : list, is_shell : bool = False, input_to_cmd : list = None):
        """
        Run a command as a task.

        Args:
            command (list): The command to run.
            is_shell (bool): Whether to run the command in a shell.
            input_to_cmd (list): Input to pass to the command.

        Returns:
            tuple: The output and error of the command.
        """
        if is_shell:
            self._PROCESS = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,shell=True)
        else:
            self._PROCESS = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,text=True)
        
        if input_to_cmd:
            output, error = self._PROCESS.communicate(cmd_to_subprocess_string(input_to_cmd))
        else:
            output, error = self._PROCESS.communicate()

        return output, error

def list_daemons(user_input):
    """
    List all running daemon tasks.

    Args:
        user_input (str): User input (not used in this function).

    Returns:
        list: A list of rows representing the running tasks.
    """
    global DAEMONS_MANAGER
    
    headers = DAEMONS_MANAGER.get_headers()

    row_list = []
    TASKS_DICT = DAEMONS_MANAGER.get_dict()

    functionalities = list(TASKS_DICT.keys())
    
    if user_input in functionalities:
        functionalities = [functionality,]
    
    for functionality in functionalities:        
        for id in TASKS_DICT[functionality]:
            row = []

            for k in headers:
                if k=="Functionality":
                    row.append(colored(functionality, 'green'))
                elif k=="Task ID":
                    row.append(colored(id, color='red'))
                elif TASKS_DICT[functionality][id]['additional info'] and k in TASKS_DICT[functionality][id]['additional info']:
                        row.append(TASKS_DICT[functionality][id]['additional info'][k])
                else:
                    row.append("")


            row_list.append(row)

    color_headers = [colored(h, 'blue') for h in headers]
    print("\n")
    print(tabulate(row_list, headers=color_headers, tablefmt='fancy_grid'), end='\n\n')

    return row_list

DAEMONS_MANAGER = DaemonTaskManager()