"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

from modules.tasks_management import Task
import re

def app_info_from_apk(apk_filepath):
    """
    Get information about an application from an APK file.

    Args:
        apk_filepath (str): Path to the APK file.

    Returns:
        dict: App information.
    """

    # Command to extract APK information using 'aapt' tool
    command = ['aapt', 'dump', 'badging', apk_filepath]
    output, error = Task().run(command)

    # Dictionary to store extracted APK information
    info = {}

    # Process each line of the output
    for line in output.splitlines():
        # Extract package information (e.g., name, version, etc.)
        if line.startswith("package: "):
            package_values = line.replace("package:", "").strip()
            
            # Find key-value pairs in the package information
            matches = re.findall(r"(\w+)='([\w\.]*)'", package_values)
            
            # Store the extracted key-value pairs in the info dictionary
            for match in matches:
                info[match[0]] = match[1]

        # Extract minimum SDK version
        elif line.startswith("sdkVersion:"):
            result = re.match(r"sdkVersion: '(.*)'", line)
            if result:
                print(result.group(1))  # Print the SDK version (optional)

        # Extract target SDK version
        elif line.startswith("targetSdkVersion:"):
            result = re.match(r"targetSdkVersion: '(.*)'", line)
            if result:
                print(result.group(1))  # Print the target SDK version (optional)

        # Extract permissions declared in the APK
        else:
            result = re.match(r"uses-permission: name='(\S*)'", line)
            if result:
                if 'Permissions' not in info:
                    info['Permissions'] = []
                info['Permissions'].append(result.group(1))
            else:
                # Extract system-implied permissions
                system_result = re.match(r"uses-implied-permission: name='(\S*)'", line)
                if system_result:
                    if 'System auto permissions (implied)' not in info:
                        info['System auto permissions (implied)'] = []
                    info['System auto permissions (implied)'].append(system_result.group(1))

    # Return the extracted APK information
    return info

def app_id_from_apk(apk_filepath):
    """
    Get application ID from an APK file.

    Args:
        apk_filepath (str): Path to the APK file.

    Returns:
        str: App ID.
    """

    return app_info_from_apk(apk_filepath)["name"]