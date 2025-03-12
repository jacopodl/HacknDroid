"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import configparser
import json
import shutil
import subprocess
import urllib3
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import platform
import tarfile
from alive_progress import alive_bar
from termcolor import colored

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GITHUB_DEPENDECIES = {
    "jadx" : {
        "release_url" : "https://api.github.com/repos/skylot/jadx/releases/latest",
        "content_type" : ["application/zip",],
        "final_name": "jadx",
        "os_specific_keywords" : {
            "Windows" : "",
            "Linux" : "",
            "Darwin" : ""
        }
    },
    "apktool" : {
        "release_url":"https://api.github.com/repos/iBotPeaches/Apktool/releases/latest",
        "content_type": ["application/java-archive",],
        "final_name": "apktool.jar",
        "os_specific_keywords" : {
            "Windows" : "",
            "Linux" : "",
            "Darwin" : ""
        }
    },
    "abe" : {
        "release_url" : "https://api.github.com/repos/nelenkov/android-backup-extractor/releases/latest",
        "content_type" : ["application/octet-stream",],
        "final_name": "abe.jar",
        "os_specific_keywords" : {
            "Windows" : "",
            "Linux" : "",
            "Darwin" : ""
        }
    },
    "apkeditor" : {
        "release_url" : "https://api.github.com/repos/REAndroid/APKEditor/releases/latest",
        "content_type" : ["application/x-java-archive",],
        "final_name": "apkeditor.jar",
        "os_specific_keywords" : {
            "Windows" : "",
            "Linux" : "",
            "Darwin" : ""
        }
    },
    "scrcpy" : {
        "release_url" : "https://api.github.com/repos/Genymobile/scrcpy/releases/latest",
        "content_type" : ["application/gzip","application/zip"],
        "final_name": "scrcpy",
        "os_specific_keywords" : {
            "Windows" : "win64",
            "Linux" : "linux",
            "Darwin" : "macos"
        }
    },
    "dex-tools" : {
        "release_url" : "https://api.github.com/repos/pxb1988/dex2jar/releases/latest",
        "content_type" : ["application/zip",],
        "final_name": "dex-tools",
        "os_specific_keywords" : {
            "Windows" : "",
            "Linux" : "",
            "Darwin" : ""
        }
    },    
}

SOFTWARE_DEPENDENCIES = {
    "adb" : {
        "Windows":"https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
        "Linux":"https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
        "Mac":"https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
    },
}

REPOSITORY_DICT = {
    "Windows" : "win",
    "Linux" : "linux",
    "Darwin" : "mac",
}

JAR_WRAPPER_EXT = {
    "Windows":".bat",
    "Linux":"",
    "Darwin":"",
}

def download_file(url, destination):
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
    
    # Get the total file size (from headers)
    total_size_in_bytes = int(response.headers.get('Content-Length', 0))
    
    # Set up the progress bar with alive_bar
    with alive_bar(total_size_in_bytes, bar='smooth', spinner='dots', unit=' B') as bar:
        # Open the file in write-binary mode
        with open(destination, 'wb') as file:
            # Iterate over the content in chunks
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar(len(chunk))  # Update progress bar with the chunk size


def github_dependencies():
    for software in GITHUB_DEPENDECIES:
        response = requests.get(GITHUB_DEPENDECIES[software]['release_url'], verify=False)

        json_response = None

        if response.status_code == 200:
            json_response = json.loads(response.text)

            print(f"{colored(software, 'cyan')}: {json_response['tag_name']}")

            assets_list = json_response['assets']

            # Take only the first file from the list of candidates
            file_url = None
            for asset in assets_list:
                if  asset['content_type'] in GITHUB_DEPENDECIES[software]['content_type'] and \
                    platform.system() in GITHUB_DEPENDECIES[software]['os_specific_keywords'] and \
                    GITHUB_DEPENDECIES[software]['os_specific_keywords'][platform.system()] in asset['name'] and \
                    not file_url:
                    file_url = asset['browser_download_url']
                    break

            if file_url.endswith('.zip') or file_url.endswith('.tar.gz') or file_url.endswith('.jar'):
                
                file_name = file_url.split('/')[-1]
                
                script_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
                dependencies_folder = os.path.join(script_folder, "dependencies")

                # Create the directory if it doesn't exist
                os.makedirs(dependencies_folder, exist_ok=True)

                file_path = os.path.join(dependencies_folder,file_name)
                download_file(file_url, file_path)

                if asset['content_type'] == "application/zip":
                    extraction_folder = os.path.join(dependencies_folder,GITHUB_DEPENDECIES[software]['final_name'])

                    # Open the zip file and extract its contents
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(extraction_folder)
                
                    current_dir = extraction_folder
                    parent_dir = current_dir
                    content_list = [os.path.join(current_dir, content) for content in os.listdir(current_dir)]
                    
                    while (len(content_list) == 1) and os.path.isdir(content_list[0]):
                        current_dir = content_list[0]
                        content_list = [os.path.join(current_dir, content) for content in os.listdir(current_dir)]

                    if current_dir != parent_dir:
                        temp_folder = os.path.join(dependencies_folder, f"temp_{GITHUB_DEPENDECIES[software]['final_name']}")
                        
                        shutil.move(current_dir, os.path.join(dependencies_folder, temp_folder))
                        shutil.rmtree(extraction_folder)
                        os.rename(temp_folder, extraction_folder)

                    os.remove(file_path)
                
                elif asset['content_type'] == "application/gzip":
                    extraction_folder = os.path.join(dependencies_folder,GITHUB_DEPENDECIES[software]['final_name'])

                    # Open the zip file and extract its contents
                    with tarfile.open(file_path, 'r:gz') as tar:
                        # Extract all the contents to the current working directory
                        tar.extractall(extraction_folder)

                    current_dir = extraction_folder
                    parent_dir = current_dir
                    content_list = [os.path.join(current_dir, content) for content in os.listdir(current_dir)]
                    
                    while (len(content_list) == 1) and os.path.isdir(content_list[0]):
                        current_dir = content_list[0]
                        content_list = [os.path.join(current_dir, content) for content in os.listdir(current_dir)]

                    if current_dir != parent_dir:
                        temp_folder = os.path.join(dependencies_folder, f"temp_{GITHUB_DEPENDECIES[software]['final_name']}")
                        
                        shutil.move(current_dir, os.path.join(dependencies_folder, temp_folder))
                        shutil.rmtree(extraction_folder)
                        os.rename(temp_folder, extraction_folder)

                    os.remove(file_path)
                
                else:
                    jar_folder = os.path.join(dependencies_folder, 'JAR')
                    
                    os.makedirs(jar_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(jar_folder, GITHUB_DEPENDECIES[software]["final_name"]))
                    wrapper_path = os.path.join(jar_folder, GITHUB_DEPENDECIES[software]['final_name'].replace('.jar', JAR_WRAPPER_EXT[platform.system()]))
                    
                    with open(wrapper_path, "w") as f:
                        lines = None

                        if platform.system() == "Windows":
                            lines = [
                                        "@echo off\n",
                                        "setlocal\n",
                                        "REM Set the path to your JAR file\n",
                                        f"""set JAR_FILE="{os.path.abspath(os.path.join(jar_folder, GITHUB_DEPENDECIES[software]['final_name']))}"\n""",
                                        "REM Run JAR file\n",
                                        "java -jar %JAR_FILE% %*\n",
                                        "endlocal"
                                    ]
                            
                            f.writelines(lines)
                        
                        else:
                            lines = [
                                        f"""$JAR_FILE = "{os.path.abspath(os.path.join(jar_folder, GITHUB_DEPENDECIES[software]['final_name']))}" """,
                                        """java -jar $JAR_FILE "$@" """
                                    ]
                            
                            f.writelines(lines)
                            os.chmod(wrapper_path, 0o755) # 0o755 is the octal value for rwxr-xr-x


def get_latest_platformtools(sdk_path):
    print(f"{colored('platform-tools:', 'cyan')} latest")

    file_path = os.path.join(sdk_path, 'downloaded_file.zip')
    download_file(SOFTWARE_DEPENDENCIES['adb'][platform.system()], file_path)

    # Open the zip file and extract its contents
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(sdk_path)

    os.remove(file_path)


def get_latest_commandlinetools(sdk_path):
    # URL to the page with the download link (replace this with the actual page URL)
    url = "https://developer.android.com/studio#command-tools"

    # Send HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the download link (you may need to adjust the selector depending on the page structure)
        # This assumes the download link contains 'commandlinetools-win' in the URL.
        download_link = soup.find('a', href=lambda x: x and f"commandlinetools-{REPOSITORY_DICT[platform.system()]}" in x)
        
        if download_link:
            # Extract the version number from the link text (e.g., https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip)
            file_url = download_link['href']
            file_info = file_url.split('-')  # Extract version number (e.g., 11076708)

            print(f"{colored('commandline-tools:', 'cyan')} {file_info[2].split('_')[0]}")
            
            # Create the directory if it doesn't exist
            os.makedirs(sdk_path, exist_ok=True)

            file_path = os.path.join(sdk_path, 'downloaded_file.zip')
            download_file(file_url, file_path)

            # Open the zip file and extract its contents
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(sdk_path)

            os.remove(file_path)
        else:
            print("Download link not found.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

def android_dependencies():
    script_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    dependencies_path = os.path.join(script_folder, "dependencies")
    sdk_path = os.path.join(dependencies_path, 'sdk')

    # Create the directory if it doesn't exist
    os.makedirs(sdk_path, exist_ok=True)

    get_latest_commandlinetools(sdk_path)
    get_latest_platformtools(sdk_path)

    os.environ['ANDROID_HOME'] = sdk_path
    shutil.move(os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools'), os.path.join(os.environ['ANDROID_HOME'], 'latest'))
    
    cmdline_tools_path = os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest')
    shutil.move(os.path.join(os.environ['ANDROID_HOME'], 'latest'), cmdline_tools_path)

    sdkmanager_path = ''

    for f in os.listdir(os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin')):
        tool_path = os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin', f)

        if 'sdkmanager' in f and os.path.isfile(tool_path):
            sdkmanager_path = tool_path
            break
    
    process = subprocess.Popen([sdkmanager_path, '--list'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,text=True)
    output, error = process.communicate()

    build_tools_versions = [ line.split("|")[0] for line in output.split('\n') if line.strip().startswith('build-tools') and "-rc" not in line]

    print(f"build-tools: {build_tools_versions[-1].strip()}")

    print("Installing the build-tools...", end=' ')
    process = subprocess.Popen([sdkmanager_path, build_tools_versions[-1].strip()], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.communicate('y')
    print("DONE")

    os.environ['PATH'] =  os.environ['PATH'] + os.pathsep + \
                          os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin') + os.pathsep + \
                          os.path.join(os.environ['ANDROID_HOME'], 'platform-tools') + os.pathsep + \
                          os.path.join(os.environ['ANDROID_HOME'], 'build-tools', build_tools_versions[-1].strip().split(";")[1]) + os.pathsep + \
                          os.path.join(os.environ['JAVA_HOME'], 'bin') + os.pathsep + \
                          os.path.abspath(os.path.join(dependencies_path, 'JAR')) + os.pathsep + \
                          os.path.abspath(os.path.join(dependencies_path, 'scrcpy')) + os.pathsep + \
                          os.path.abspath(os.path.join(dependencies_path, 'dex-tools')) + os.pathsep + \
                          os.path.abspath(os.path.join(dependencies_path, 'jadx', 'bin'))


def set_android_home_env_var():
    config = configparser.ConfigParser()
    script_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    config_file_path = os.path.join(script_folder, "config.ini")

    if not os.path.exists(config_file_path):
        config.read(config_file_path)

    # Add a new section if it doesn't exist
    if not config.has_section('Environment'):
        config.add_section('Environment')

    config.set('Environment', 'PATH', os.environ['PATH'])
    config.set('Environment', 'ANDROID_HOME', os.environ['ANDROID_HOME'])

    # Write the configuration to a file
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)