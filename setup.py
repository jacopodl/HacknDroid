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
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def github_dependencies():
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
    }


    for software in GITHUB_DEPENDECIES:
        response = requests.get(GITHUB_DEPENDECIES[software]['release_url'], verify=False)

        json_response = None

        if response.status_code == 200:
            json_response = json.loads(response.text)

            print(f"{software}: {json_response['tag_name']}")

            for asset in json_response['assets']:
                if asset['content_type'] in GITHUB_DEPENDECIES[software]['content_type'] and \
                    platform.system() in GITHUB_DEPENDECIES[software]['os_specific_keywords'] and \
                    GITHUB_DEPENDECIES[software]['os_specific_keywords'][platform.system()] in asset['name']:
                    
                    file_url = asset['browser_download_url']
                    
                    if file_url.endswith('.zip') or file_url.endswith('.tar.gz') or file_url.endswith('.jar'):
                        
                        file_name = file_url.split('/')[-1]
                        
                        extract_to_directory = 'dependencies'

                        # Create the directory if it doesn't exist
                        os.makedirs(extract_to_directory, exist_ok=True)

                        download_response = requests.get(file_url)
                        with open(f'dependencies/{file_name}', 'wb') as f:
                            f.write(download_response.content)

                        if asset['content_type'] == "application/zip":
                            # Open the zip file and extract its contents
                            with zipfile.ZipFile(f'dependencies/{file_name}', 'r') as zip_ref:
                                zip_ref.extractall(os.path.join(extract_to_directory,GITHUB_DEPENDECIES[software]['final_name']))
                        
                            os.remove(f'dependencies/{file_name}')
                        
                        elif asset['content_type'] == "application/gzip":
                            # Open the zip file and extract its contents
                            with tarfile.open(f'dependencies/{file_name}', 'r:gz') as tar:
                                # Extract all the contents to the current working directory
                                tar.extractall(os.path.join(extract_to_directory,GITHUB_DEPENDECIES[software]['final_name']))
                                
                            os.remove(f'dependencies/{file_name}')
                        
                        else:
                            os.rename(f'dependencies/{file_name}', f'dependencies/{GITHUB_DEPENDECIES[software]["final_name"]}')



def get_latest_platformtools():
    SOFTWARE_DEPENDENCIES = {
        "adb" : {
            "Windows":"https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
            "Linux":"https://dl.google.com/android/repository/platform-tools-latest-linux.zip",
            "Mac":"https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
        },
    }

    
    download_response = requests.get(SOFTWARE_DEPENDENCIES['adb'][platform.system()])

    # Check if the request was successful
    if download_response.status_code == 200:
        extract_to_directory = 'dependencies/sdk'

        # Create the directory if it doesn't exist
        os.makedirs(extract_to_directory, exist_ok=True)

        with open('dependencies/sdk/downloaded_file.zip', 'wb') as f:
            f.write(download_response.content)

        # Open the zip file and extract its contents
        with zipfile.ZipFile('dependencies/sdk/downloaded_file.zip', 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)

        os.remove('dependencies/sdk/downloaded_file.zip')


def get_latest_commandlinetools():
    REPOSITORY_DICT = {
        "Windows" : "win",
        "Linux" : "linux",
        "Darwin" : "mac",
    }

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

            print(f"Version number: {file_info[1]}")
            print(f"Version number: {file_info[2].split('_')[0]}")
            
            print(file_url)

            extract_to_directory = 'dependencies/sdk'

            # Create the directory if it doesn't exist
            os.makedirs(extract_to_directory, exist_ok=True)

            download_response = requests.get(file_url)
            with open('dependencies/sdk/downloaded_file.zip', 'wb') as f:
                f.write(download_response.content)

            # Open the zip file and extract its contents
            with zipfile.ZipFile('dependencies/sdk/downloaded_file.zip', 'r') as zip_ref:
                zip_ref.extractall(extract_to_directory)

            os.remove('dependencies/sdk/downloaded_file.zip')
        else:
            print("Download link not found.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

def android_dependencies():
    get_latest_commandlinetools()
    get_latest_platformtools()


def set_android_home_env_var():
    os.environ['ANDROID_HOME'] = os.path.abspath('dependencies/sdk')
    
    """
    sdkmanager_path = os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin', 'sdkmanager.bat')
    shutil.move(os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools'), os.path.join(os.environ['ANDROID_HOME'], 'latest'))
    
    cmdline_tools_path = os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest')
    shutil.move(os.path.join(os.environ['ANDROID_HOME'], 'latest'), cmdline_tools_path)
    sdkmanager_path = os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin', 'sdkmanager.bat')

    process = subprocess.Popen([sdkmanager_path, '--list'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,text=True)
    output, error = process.communicate()

    build_tools_versions = [ line.split("|")[0] for line in output.split('\n') if line.strip().startswith('build-tools') and "-rc" not in line]

    print(build_tools_versions[-1].strip())

    process = subprocess.Popen([sdkmanager_path, build_tools_versions[-1].strip()], stdin=subprocess.PIPE, stdout=sys.stdout, stderr=subprocess.PIPE, text=True)
    process.communicate('y')

    os.environ['PATH'] =  os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin') + os.pathsep + \
                        os.path.join(os.environ['ANDROID_HOME'], 'platform-tools') + os.pathsep + \
                        os.path.join(os.environ['ANDROID_HOME'], 'build-tools', build_tools_versions[-1].strip().split(";")[1]) + os.pathsep + \
                        os.path.join(os.environ['JAVA_HOME'], 'bin')
    """
    os.environ['PATH'] =  os.path.join(os.environ['ANDROID_HOME'], 'cmdline-tools', 'latest', 'bin') + os.pathsep + \
                        os.path.join(os.environ['ANDROID_HOME'], 'platform-tools') + os.pathsep + \
                        os.path.join(os.environ['ANDROID_HOME'], 'build-tools', '35.0.1') + os.pathsep + \
                        os.path.join(os.environ['JAVA_HOME'], 'bin')
    print(os.environ['PATH'])

    process = subprocess.Popen(['adb', ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE ,text=True, env={'PATH': os.environ['PATH'],})
    output, error = process.communicate()
    
    print(output)
    print(error)
