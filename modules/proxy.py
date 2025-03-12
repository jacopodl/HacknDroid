"""
This source file is part of the HacknDroid project.

Licensed under the Apache License v2.0
"""

import sys
import netifaces
import ipaddress
from modules.tasks_management import Task, DAEMONS_MANAGER
import platform
import re
from tabulate import tabulate
from modules.utility import loading_animation
from modules.adb import get_session_device_id

DNS_TASK_ID = -1

def pc_wifi_ip():
    """
    Get the IP address of the current PC on the Wi-Fi network.

    Returns:
        str: The IP address of the PC.
    """
    netifaces.gateways()
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]

    ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

    return ip

def is_port(user_input):
    """
    Check if the user input is a valid port number.

    Args:
        user_input (str): The input string from the user.

    Returns:
        bool: True if the input is a valid port number, False otherwise.
    """
    try:
        port = int(user_input)
        return (port>=0 and port< 65536)
    except ValueError:
        return False    

def get_current_proxy_settings(user_input):
    """
    Get and display the current global proxy settings on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    print("Proxy set on mobile device:", end=" ")
    proxy = get_proxy()
    
    if (proxy==":0"):
        proxy = "NO PROXY"

    print(proxy)


def get_proxy():
    """
    Get the current global proxy settings on the mobile device.

    Returns:
        str: The current proxy settings.
    """
    command = ['adb', '-s', get_session_device_id(), 'shell', 'settings', 'get', 'global', 'http_proxy']
    output, error = Task().run(command)

    return output.strip()

def del_proxy(user_input):
    """
    Reset the global proxy settings on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    command = ['adb', '-s', get_session_device_id(), 'shell', 'settings', 'put', 'global', 'http_proxy', ':0']
    output, error = Task().run(command)

    print("Proxy removed on mobile device")

def set_current_pc_proxy(user_input):
    """
    Set the proxy on the mobile device using the current PC's IP and the specified port.

    Args:
        user_input (str): The port number to use for the proxy.
    """
    # If the user input is not a port, ask the user to insert it again
    while not is_port(user_input):
        user_input = input("Insert a valid port number")

    # Retrieve current IP of the PC on the Wi-Fi network  
    ip = pc_wifi_ip()
    # Set the proxy on the mobile device
    set_proxy(ip, user_input)


def is_ip(ip_string):
    """
    Check if the provided string is a valid IP address.

    Args:
        ip_string (str): The string to check.

    Returns:
        bool: True if the string is a valid IP address, False otherwise.
    """
    try:
        ip = ipaddress.ip_address(ip_string)
    except ValueError:
        return False
    
    return True


def set_generic_proxy(user_input):
    """
    Set the proxy on the mobile device using the specified IP address and port.

    Args:
        user_input (str): The IP address and port in the format <address>:<port>.
    """
    address = []
    check = True
    ip = ''
    port = ''

    if ":" in address:
        address = user_input.split(":")        
        check = (not is_ip(address[0])) or (not is_port(address[1]))

    while check:
        user_input = input("Insert a valid port number")

        if ":" in address:
            address = user_input.split(":")
            check = (not is_ip(address[0])) or (not is_port(address[1]))

    set_proxy(ip, port)
    

def set_proxy(ip, port):
    """
    Set the proxy on the mobile device.

    Args:
        ip (str): The IP address to use for the proxy.
        port (str): The port number to use for the proxy.
    """
    command = ['adb', '-s', get_session_device_id(), 'shell', 'settings', 'put', 'global', 'http_proxy', f'{ip}:{port}']
    output, error = Task().run(command)

    print("Proxy set on mobile device:", end=" ")
    print(get_proxy())


# Main function
def dns_proxy(target_ip):
    """
    Start the DNS proxy server.

    Args:
        target_ip (str): The target IP address for DNS spoofing.
    """
    global DNS_TASK_ID, DAEMONS_MANAGER

    if DNS_TASK_ID == -1:
        # Get the next available ID from the DAEMONS_MANAGER
        DNS_TASK_ID = DAEMONS_MANAGER.get_next_id()
        # Add a new DNS task to the DAEMONS_MANAGER
        DAEMONS_MANAGER.add_task('dns', [sys.executable, 'modules/dns_spoofing.py', target_ip])

        additional_info = {'Fake DNS IP':target_ip,}
        DAEMONS_MANAGER.add_info('dns', DNS_TASK_ID, additional_info)


def get_current_dns_proxy(user_input):
    """
    Get the current DNS proxy settings on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    pass

def set_current_pc_dns_proxy(user_input):
    """
    Set the DNS proxy on the mobile device using the current PC's IP address.

    Args:
        user_input (str): User input (not used in this function).
    """
    """
    Method 1 (NOT WORKING)
    adb shell settings put global wifi_static_ip 1  # Enable Static IP
    adb shell settings put global wifi_static_ip_address "192.168.1.100"  # Set static IP address
    adb shell settings put global wifi_static_gateway "192.168.1.1"  # Set gateway
    adb shell settings put global wifi_static_dns1 "8.8.8.8"  # Set DNS 1
    adb shell settings put global wifi_static_dns2 "8.8.4.4"  # Set DNS 2
    """

    """
    Method 2 (NOT WORKING)
    Define static IP in Wifi configuration page of the Wifi SSID
    adb shell su -c setprop net.dns1 192.168.1.52
    adb shell su -c setprop net.dns2 192.168.1.52
    """

    """
    Method 3 (NOT WORKING)
    adb shell
    su
    then, edit the file /data/misc/wifi/WifiConfigStore.xml
    am broadcast -a android.intent.action.WIFI_STATE_CHANGED
    am broadcast -a android.intent.action.WIFI_SCAN
    am broadcast -a android.intent.action.CONNECTIVITY_CHANGE

    Status:
    0: Disabled (Network is saved but not enabled; it will not be connected).
    1: Enabled (Network is available and can be connected; it might be used by the system to connect automatically).
    2: Connected (Network is currently connected and active).
    3: Disconnected (Network is saved but not connected, and it has been explicitly disconnected).
    """
    
    print("\nSet the DNS1 and DNS2 on mobile device at: "+pc_wifi_ip())
    current_os = platform.system()

    if current_os == "Windows":
        print("(Disable the Microsoft Windows firewall)")

    command = ['adb', '-s', get_session_device_id(), 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)

    # Get the current Wi-Fi SSID
    pc_ssid = get_current_pc_wifi_ssid()
    mobile_ssid = get_mobile_wifi_ssid()

    print("\nWi-Fi SSIDs")
    row_list = []
    
    if pc_ssid:
        row_list.append(["Current PC",pc_ssid])
    else:
        row_list.append(["Current PC","Undetectable"])

    if pc_ssid:
        row_list.append(["Mobile Device",mobile_ssid])
    else:
        row_list.append(["Mobile Device","Undetectable"])

    print(tabulate(row_list, headers=['Device', 'Wi-Fi SSID'], tablefmt='fancy_grid'))

    if pc_ssid!=mobile_ssid:
        print("\nPlease connect the mobile device and the current PC to the same network!!!")

    command = ['adb', '-s', get_session_device_id(), 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)
    x=input("Press ENTER to launch the DNS Server...\n")

    dns_proxy(pc_wifi_ip())

def set_generic_dns_proxy(user_input):
    """
    Set the DNS proxy on the mobile device using the specified IP address.

    Args:
        user_input (str): The IP address to use for the DNS proxy.
    """
    remote_ip = ''

    try:
        remote_ip = ipaddress.ip_address(user_input)
    except ValueError:
        remote_ip = ''
        print('Address is invalid')
    
    while remote_ip == '':
        try:
            user_input = input("Enter adress: ")
            remote_ip = ipaddress.ip_address(user_input)
        except ValueError:
            remote_ip = ''
            print('Address is invalid')

        
    print("\nSet the DNS1 and DNS2 on mobile device at: "+remote_ip)
    print("(If on Windows, disable the firewall)")
    command = ['adb', '-s', get_session_device_id(), 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)

    x=input("Press ENTER to launch the DNS Server (or CTRL+C to stop the operation)...\n")
    dns_proxy(remote_ip)


def del_dns_proxy(user_input):
    """
    Delete the DNS proxy settings on the mobile device.

    Args:
        user_input (str): User input (not used in this function).
    """
    global DNS_TASK_ID, DAEMONS_MANAGER

    if DNS_TASK_ID != -1:
        DAEMONS_MANAGER.stop_task('dns', DNS_TASK_ID)
        DNS_TASK_ID = -1
        loading_animation("Stopping DNS Server", 3, 30)
        print("DNS Server STOPPED!!!\n")


def get_current_invisible_proxy(user_input):
    command = ['adb', '-s', get_session_device_id(), 'shell']
    shell_input = [ "su root",
                   """iptables -t nat -L OUTPUT -v -n | grep 'DNAT' | awk '{print $NF}' | cut -d: -f2"""]
    
    output, error = Task().run(command, input_to_cmd=shell_input)
    print(output)


def set_current_pc_invisible_proxy(user_input):
    # Get the current Wi-Fi SSID
    pc_ssid = get_current_pc_wifi_ssid()
    mobile_ssid = get_mobile_wifi_ssid()

    print("\nWi-Fi SSIDs")
    row_list = []
    
    if pc_ssid:
        row_list.append(["Current PC",pc_ssid])
    else:
        row_list.append(["Current PC","Undetectable"])

    if pc_ssid:
        row_list.append(["Mobile Device",mobile_ssid])
    else:
        row_list.append(["Mobile Device","Undetectable"])

    print(tabulate(row_list, headers=['Device', 'Wi-Fi SSID'], tablefmt='fancy_grid'))

    if pc_ssid!=mobile_ssid:
        print("\nPlease connect the mobile device and the current PC to the same network!!!")

    command = ['adb', '-s', get_session_device_id(), 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)
    x=input("Press ENTER to launch the DNS Server...\n")

    set_invisible_proxy(pc_wifi_ip())

def set_generic_invisible_proxy(user_input):
    remote_ip = ''

    try:
        remote_ip = ipaddress.ip_address(user_input)
    except ValueError:
        remote_ip = ''
        print('Address is invalid')
    
    while remote_ip == '':
        try:
            user_input = input("Enter adress: ")
            remote_ip = ipaddress.ip_address(user_input)
        except ValueError:
            remote_ip = ''
            print('Address is invalid')

    set_invisible_proxy(remote_ip)


def set_invisible_proxy(target_ip):
    command = ['adb', '-s', get_session_device_id(), 'shell']
    shell_input = [ "su root",
                   f"iptables -t nat -A OUTPUT -p tcp --dport 443 -j DNAT --to-destination {target_ip}:443",
                   f"iptables -t nat -A OUTPUT -p tcp --dport 80 -j DNAT --to-destination {target_ip}:80",
                   "iptables -t nat -A POSTROUTING -p tcp --dport 443 -j MASQUERADE",
                   "iptables -t nat -A POSTROUTING -p tcp --dport 80 -j MASQUERADE"
                ]
    
    output, error = Task().run(command, input_to_cmd=shell_input)
    print(output)


def del_invisible_proxy(user_input):
    # flush previous configuration
    #iptables -t nat -F
    command = ['adb', '-s', get_session_device_id(), 'shell']
    shell_input = [ "su root",
                   "iptables -t nat -F"
                ]
    
    output, error = Task().run(command, input_to_cmd=shell_input)
    print(output)


def get_current_pc_wifi_ssid():
    """
    Get the current Wi-Fi SSID of the PC.

    Returns:
        str: The current Wi-Fi SSID.
    """
    current_os = platform.system()

    if current_os == "Windows":
        # Windows command to get Wi-Fi SSID
        command = ['netsh', 'wlan', 'show', 'interfaces']
        output, error = Task().run(command)

        for line in output.splitlines():
            if "SSID" in line:
                return line.split(":")[1].strip()
                
    elif current_os == "Linux":
        # Linux command to get Wi-Fi SSID
        command = ['iwgetid', '-r']
        output, error = Task().run(command)
        return output.strip()

    elif current_os == "Darwin":  # macOS
        # macOS command to get Wi-Fi SSID
        command = ['networksetup', '-getairportnetwork', 'en0']
        output, error = Task().run(command)

        for line in output.splitlines():
            if "Current Wi-Fi Network" in line:
                return line.split(":")[1].strip()

    return None

def get_mobile_wifi_ssid():
    """
    Get the current Wi-Fi SSID of the mobile device.

    Returns:
        str: The current Wi-Fi SSID.
    """
    command = ['adb', '-s', get_session_device_id(), 'shell', 'dumpsys', 'netstats', '|', 'grep', '-E', 'iface=wlan.*networkId']
    output, error = Task().run(command)

    x = None 
    
    if output:
        REGEX_SSID = r'networkId=\"(.*)\"'
        x = re.search(REGEX_SSID, output.splitlines()[0])
    else:
        return None

    if x:
        return x.group(1)
    else:
        return None