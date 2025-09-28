"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from modules.cli_management import CLI
from config.dependencies_setup import github_dependencies, android_dependencies, set_config_var, set_os_env_var
from argparse import ArgumentParser

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--install", help="First setup of the script", action="store_true")
    
    cli_args = parser.parse_args()
    
    return cli_args.install


def main():
    dependencies_install = arg_parser()

    if dependencies_install:
        github_dependencies()
        android_dependencies()
        set_config_var()
    else:
        set_os_env_var()
        cli_mgmt = CLI()
        cli_mgmt.cli_options()

if __name__=="__main__":
    main()