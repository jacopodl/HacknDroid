import config.menu as menu
import config.style as tool_style

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit import Application
from prompt_toolkit.shortcuts import clear
from pyfiglet import Figlet
from termcolor import colored

# Function pointer in OPTIONS
from modules.tasks_management import DAEMONS_MANAGER
from modules.adb import select_device
from modules.error import ADBConnectionException, OptionNotAvailable

class CLI():

    def __init__(self):
        """
        Initialize the CLI with options and styles.
        """
        # Initialize the global variable CURRENT_OPTION
        global CURRENT_OPTION
        
        # Load the CLI options from the menu configuration
        self._options = menu.OPTIONS
        
        # Initialize the current path with the root option
        self._current_path = []
        self._current_path.append(list(self._options.keys())[0])
        
        # Set the CURRENT_OPTION to the root option
        CURRENT_OPTION = self._options[self._current_path[0]]
        
        # Load the CLI style from the tool_style configuration
        self._style = Style.from_dict(tool_style.STYLE)

        # Set the title of the CLI
        self._title = "HacknDroid"
        
        # Initialize the Figlet object for rendering the title
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
        # Get the matching options
        matches = [option for option in list(CURRENT_OPTION['children'].keys()) if option.startswith(text)]

        # Return the matching option
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
                # Clear the screen
                clear()
                # Print the title
                print(self._title_f.renderText(self._title))
                # Print the shortcut keys
                print_formatted_text(HTML("<option> > TAB to see options</option>"), style=self._style)
                print_formatted_text(HTML("<option> > Ctrl+C to stop the program</option>"), style=self._style)

                print("")
                print_formatted_text(HTML(f"<descr>Select the device you want to use</descr>"), style=self._style)
                print("")

                select_device("")
                break
            
            except OptionNotAvailable:
                print(colored("Invalid choice. Please select a valid device.", 'red'))
                print_formatted_text(HTML("<option>Press ENTER to continue</option>"), style=self._style)
                
                try:
                    x= input()
                except (KeyboardInterrupt,EOFError) as e:
                    # Clear the screen
                    clear()
                    # Print the title
                    print(self._title_f.renderText(self._title))
                    print_formatted_text(HTML(f"<descr>Thank you for using the program!!!</descr>"), style=self._style, end='\n\n')
                    exit(0)

            except KeyboardInterrupt as e:
                # Clear the screen
                clear()
                # Print the title
                print(self._title_f.renderText(self._title))
                print_formatted_text(HTML(f"<descr>Thank you for using the program!!!</descr>"), style=self._style, end='\n\n')
                exit(0)

            except ADBConnectionException as e:
                print(colored("No device connected to ADB.", 'red'))
                print_formatted_text(HTML("<option>Plug in the device and press ENTER to continue</option>"), style=self._style)

                try:
                    x= input()
                except KeyboardInterrupt as e:
                    # Clear the screen
                    clear()
                    # Print the title
                    print(self._title_f.renderText(self._title))
                    print_formatted_text(HTML(f"<descr>Thank you for using the program!!!</descr>"), style=self._style, end='\n\n')
                    exit(0)

        # Initialize the prompt completer with the children of the current option
        self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))

        while True:        
            try:
                # Clear the screen
                clear()
                # Print the title
                print(self._title_f.renderText(self._title))
                # Print the shortcut keys
                print_formatted_text(HTML("<option> > TAB to see options</option>"), style=self._style)
                print_formatted_text(HTML("<option> > Ctrl+D to stop the program</option>"), style=self._style)
                
                # If arrived at a leaf node, print the CTRL+C shortcut key to cancel the action
                if len(CURRENT_OPTION['children']) == 2:
                    print_formatted_text(HTML("<option> > Ctrl+C to cancel the action</option>"), style=self._style)    

                print("")
                
                # Print the description of the current option
                for x in CURRENT_OPTION['description']:
                    print_formatted_text(HTML(f"<descr>{x}</descr>"), style=self._style)
                
                if len(self._current_path)>1:
                    # Print the current path between functionality
                    print("")
                    path = f"<section{1}> {self._current_path[2]} </section{1}>"
                    
                    for i in range(4,len(self._current_path),2):
                        path+=f"<section{i/2}> {self._current_path[i]} </section{i/2}>"

                else:
                    # Print the home path ('main')
                    path = f"<section> {self._current_path[-1]} </section>"

                # Prompt the user for input (tab completion enabled)
                choice = prompt(HTML(path+" "), completer=self._prompt_completer, style=self._style, multiline=False)
                
                if choice in CURRENT_OPTION['children']:
                    # If the input (choice) is a valid option, navigate to the selected level

                    if choice == 'back' and len(self._current_path)>1:
                        # If the input is 'back' and the program is not in the homepage, navigate back to the parent level
                        self._current_path = self._current_path[:-2]
                        CURRENT_OPTION = self._options[self._current_path[0]]
                        for i in self._current_path[1:]:
                            CURRENT_OPTION = CURRENT_OPTION[i]

                    elif choice == 'home' and len(self._current_path)>1:
                        self._current_path = self._current_path[:1]
                        CURRENT_OPTION = self._options[self._current_path[0]]

                    else:
                        # If the input is not 'back', navigate to the selected level
                        self._current_path.append('children')
                        self._current_path.append(choice)
                        CURRENT_OPTION = CURRENT_OPTION['children'][choice]

                    # Update the completer with the new options for the current level
                    self._prompt_completer = WordCompleter(list(CURRENT_OPTION['children'].keys()))
                
                elif len(CURRENT_OPTION['children']) == 2:
                    # If the input is a leaf node, execute the associated function
                    CURRENT_OPTION['function'](choice)
                    # Wait for the user to press ENTER to continue
                    print_formatted_text(HTML("<option>Press ENTER to continue</option>"), style=self._style)
                    x=input()
                    
            except OptionNotAvailable:
                print(colored("Invalid choice. Please select a valid device.", 'red'))
                print_formatted_text(HTML("<option>Press ENTER to continue</option>"), style=self._style)
                x= input()
                
            except KeyboardInterrupt:
                # Cancel the current operation (input insertion by a user)
                pass
            except EOFError:
                # Clear the screen
                clear()
                # Print the title
                print(self._title_f.renderText(self._title))
                print_formatted_text(HTML(f"<descr>Thank you for using the program!!!</descr>"), style=self._style, end='\n\n')
                break

        # Stop all the tasks
        DAEMONS_MANAGER.stop_all_tasks()

