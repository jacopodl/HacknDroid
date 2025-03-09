from modules.cli_management import CLI
from config.setup import github_dependencies, android_dependencies, set_android_home_env_var
from argparse import ArgumentParser

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument("-g", "--github", help="Update github dependencies", action="store_true")
    parser.add_argument("-a", "--android", help="Update android dependencies", action="store_true")
    parser.add_argument("--install", help="First setup of the script", action="store_true")
    
    cli_args = parser.parse_args()
    
    if cli_args.install:
        return True, True

    return cli_args.github, cli_args.android

def main():
    github_update, android_update = arg_parser()

    if github_update:
        github_dependencies()

    if android_update:
        android_dependencies()

    if github_update or android_update:
        set_android_home_env_var()

    cli_mgmt = CLI()
    cli_mgmt.cli_options()

if __name__=="__main__":
    main()