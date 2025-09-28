"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import subprocess
import time
from flask import Flask, render_template
import random
import os
from modules.adb import get_session_device_id
from modules.apk_analyzer import apk_decompiler_from_device, apk_decompiler_from_file
from modules.utility import pc_wifi_ip
import xml.etree.ElementTree as ET
from modules.tasks_management import Task

# Create an instance of the Flask application
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../http-server'))

# This is a list of dictionaries that will be passed to our HTML template.
# In a real-world application, this data could come from a database.
colors = [
    "bg-red-500", "bg-red-600", "bg-red-700",
    "bg-orange-500", "bg-orange-600", "bg-orange-700",
    "bg-amber-500", "bg-amber-600", "bg-amber-700",
    "bg-yellow-500", "bg-yellow-600", "bg-yellow-700",
    "bg-lime-500", "bg-lime-600", "bg-lime-700",
    "bg-green-500", "bg-green-600", "bg-green-700",
    "bg-emerald-500", "bg-emerald-600", "bg-emerald-700",
    "bg-teal-500", "bg-teal-600", "bg-teal-700",
    "bg-cyan-500", "bg-cyan-600", "bg-cyan-700",
    "bg-sky-500", "bg-sky-600", "bg-sky-700",
    "bg-blue-500", "bg-blue-600", "bg-blue-700",
    "bg-indigo-500", "bg-indigo-600", "bg-indigo-700",
    "bg-violet-500", "bg-violet-600", "bg-violet-700",
    "bg-purple-500", "bg-purple-600", "bg-purple-700",
    "bg-fuchsia-500", "bg-fuchsia-600", "bg-fuchsia-700",
    "bg-pink-500", "bg-pink-600", "bg-pink-700",
    "bg-rose-500", "bg-rose-600", "bg-rose-700",
]

def extract_urls(manifest_file):
    tree = ET.parse(manifest_file)
    root = tree.getroot()
    urls = []

    # AndroidManifest.xml usually has "android" namespace
    ns = {'android': 'http://schemas.android.com/apk/res/android'}

    # Find all <intent-filter>
    for intent_filter in root.findall(".//intent-filter"):
        has_view = intent_filter.find("./action[@android:name='android.intent.action.VIEW']", ns) is not None
        has_browsable = intent_filter.find("./category[@android:name='android.intent.category.BROWSABLE']", ns) is not None

        if has_view and has_browsable:
            # Collect <data> tags
            for data in intent_filter.findall("data", ns):
                scheme = data.get(f"{{{ns['android']}}}scheme", "")
                host = data.get(f"{{{ns['android']}}}host", "")
                path = data.get(f"{{{ns['android']}}}path", "")
                path_prefix = data.get(f"{{{ns['android']}}}pathPrefix", "")
                path_pattern = data.get(f"{{{ns['android']}}}pathPattern", "")

                # Build URL pattern
                url = f"{scheme}://{host}{path}{path_prefix}{path_pattern}"
                urls.append({"name": url, "url": url},)

    return urls

# Define a route for the home page ('/')
@app.route('/')
def home():
    """
    This function renders the 'index.html' template and passes the
    list of links to it. The template then uses this data to
    dynamically generate the links on the page.
    """
    # Assign a random color to each link from the expanded list
    dynamic_links = extract_urls(manifest_file_path)

    for link in dynamic_links:
        link["color"] = random.choice(colors)

    return render_template('index.html', links=dynamic_links)

# This block ensures the server only runs when the script is executed directly.
def custom_urls_server_from_manifest(user_input):
    global manifest_file_path

    manifest_file_path = user_input

    while not os.path.isfile(manifest_file_path) or os.path.basename(manifest_file_path) != "AndroidManifest.xml":
        if not os.path.isfile(manifest_file_path):
            print(f"The path {manifest_file_path} does not exist.")
        elif os.path.basename(manifest_file_path) != "AndroidManifest.xml":
            print(os.path.basename(manifest_file_path))
            print(f"The file at {manifest_file_path} is not named 'AndroidManifest.xml'.")
        
        manifest_file_path = input("Please enter a valid path to the AndroidManifest.xml file: ")

    ip_address = pc_wifi_ip()
    command = ['adb', '-s', get_session_device_id(),'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', f"http://{ip_address}:5000/"]

    print("Attempting to send ADB intent...")
    try:
        # Give the server a moment to start up before sending the intent.
        time.sleep(1)
        # Execute the adb command using the subprocess module.
        output, error = Task().run(command)
        print("ADB intent sent successfully.")
    except subprocess.CalledProcessError as e:
        # Return an error message if the adb command fails.
        print(f"Failed to send ADB intent. Error: {e.stderr}")
    except FileNotFoundError:
        print("ADB not found. Make sure it's in your system's PATH.")

    # Run the Flask application in debug mode.
    app.run(debug=False, host=ip_address, port=5000)

def custom_urls_server_from_mobile(user_input):
    decompiled_folder = apk_decompiler_from_device(user_input)
    manifest_path = os.path.join(decompiled_folder, "AndroidManifest.xml")
    
    if not os.path.exists(manifest_path):
        print(f"Error: AndroidManifest.xml not found in {decompiled_folder}")
        return
    
    custom_urls_server_from_manifest(manifest_path)

def custom_urls_server_from_apk(user_input):
    print(user_input)
    decompiled_folder = apk_decompiler_from_file(user_input)
    
    manifest_path = os.path.join(decompiled_folder, "AndroidManifest.xml")
    
    if not os.path.exists(manifest_path):
        print(f"Error: AndroidManifest.xml not found in {decompiled_folder}")
        return

    custom_urls_server_from_manifest(manifest_path)