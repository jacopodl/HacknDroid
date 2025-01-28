import config.menu as menu
import config.style as tool_style

from termcolor import cprint, colored

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import Application
from prompt_toolkit.shortcuts import clear
from pyfiglet import Figlet

# Function pointer in OPTIONS
from modules import apk_analyzer, apk_install, app_logs, cli_management, file_transfer
from modules.tasks_management import DAEMONS_MANAGER

class CLI():

    def __init__(self):
        """
        Initialize the CLI with options and styles.
        """
        global CURRENT_OPTION
        self._options = menu.OPTIONS
        self._current_path = []
        self._current_path.append(list(self._options.keys())[0])
        CURRENT_OPTION = self._options[self._current_path[0]]

        self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))
        self._style = Style.from_dict(tool_style.STYLE)

        self._title = "HacknDroid" 
        self._title_f = Figlet(font='slant')

    def completer(text, state):
        """
        Tab completion for CLI options.

        Args:
            text (str): The current input text.
            state (int): The state of the completion.

        Returns:
            str: The matching option.
        """
        matches = [option for option in list(CURRENT_OPTION['children'].keys()) if option.startswith(text)]

        if state < len(matches):
            return matches[state]
        else:
            return None        


    def cli_options(self):
        """
        Display and handle CLI options.
        """
        global CURRENT_OPTION

        while True:        
            try:
                clear()
                
                print(self._title_f.renderText(self._title))
                print_formatted_text(HTML("<option>[TAB to see options | Ctrl+C or exit to terminate the program]</option>"), style=self._style)

                print("")
                
                for x in CURRENT_OPTION['description']:
                    print_formatted_text(HTML(f"<descr>{x}</descr>"), style=self._style)
                
                if len(self._current_path)>1:
                    print("")
                    path = f"<section{1}> {self._current_path[2]} </section{1}>"
                    
                    for i in range(4,len(self._current_path),2):
                        path+=f"<section{i/2}> {self._current_path[i]} </section{i/2}>"

                else:
                    path = f"<section> {self._current_path[-1]} </section>"

                choice = prompt(HTML(path+" "), completer=self._prompt_completer, style=self._style, multiline=False)
                
                if choice in CURRENT_OPTION['children']:
                    if choice == 'back' and len(self._current_path)>1:
                        self._current_path = self._current_path[:-2]
                        CURRENT_OPTION = self._options[self._current_path[0]]
                        for i in self._current_path[1:]:
                            CURRENT_OPTION = CURRENT_OPTION[i]
                        self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))
                    elif len(CURRENT_OPTION['children'][choice]['children'].keys())>1:
                        self._current_path.append('children')
                        self._current_path.append(choice)
                        CURRENT_OPTION = CURRENT_OPTION['children'][choice]
                        self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))
                    else:
                        self._current_path.append('children')
                        self._current_path.append(choice)
                        CURRENT_OPTION = CURRENT_OPTION['children'][choice]
                        self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))    
                elif choice == 'exit':
                    break
                elif len(CURRENT_OPTION['children']) == 1:
                    CURRENT_OPTION['function'](choice)
                    print_formatted_text(HTML("<option>Press ENTER to continue</option>"), style=self._style)
                    x=input()
                    
            except (KeyboardInterrupt, EOFError):
                break

        DAEMONS_MANAGER.stop_all_tasks()

