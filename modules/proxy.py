import config.menu as menu
import subprocess
import netifaces
import ipaddress
import threading
import time
import socket
from modules import dns_spoofing
import sys
import ipaddress
from modules.tasks_management import Task, DAEMONS_MANAGER

DNS_END = False

'''
TO BE DONE: Install certificate (specific on device)
'''
def pc_wifi_ip():
    netifaces.gateways()
    iface = netifaces.gateways()['default'][netifaces.AF_INET][1]

    ip = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

    return ip

def is_port(user_input):
    try:
        port = int(user_input)
        return (port>=0 and port< 65536)
    except ValueError:
        return False    

def get_current_proxy_settings(user_input):
    '''
        Get the global proxy settings
        settings get global http_proxy
    '''
    print("Proxy set on mobile device:", end=" ")
    proxy = get_proxy()
    
    if proxy==":0":
        proxy = "NO PROXY"

    print(proxy)


def get_proxy():
    '''
        Get the global proxy settings
        settings get global http_proxy
    '''
    command = ['adb', 'shell', 'settings', 'get', 'global', 'http_proxy']
    output, error = Task().run(command)

    return output.strip()

def del_proxy(user_input):
    '''
        Reset the global proxy settings
        settings put global http_proxy :0
    '''

    command = ['adb', 'shell', 'settings', 'put', 'global', 'http_proxy', ':0']
    output, error = Task().run(command)

    print("Proxy removed on mobile device")

def set_current_pc_proxy(user_input):
    '''
        Set proxy on the device using the port specified as user input
        adb shell settings put global http_proxy <this_pc_ip>:<port>
    '''
    # If the user input is not a port, ask the user to insert it again
    while not is_port(user_input):
        user_input = input("Insert a valid port number")

    # Retrieve current IP of the PC on the Wi-Fi network  
    ip = pc_wifi_ip()
    # Set the proxy on the mobile device
    set_proxy(ip, user_input)


def is_ip(ip_string):
    try:
        ip = ipaddress.ip_address(ip_string)
    except ValueError:
        return False
    
    return True


def set_generic_proxy(user_input):
    '''
        Set proxy on the device using the IP machine and the port specified as user input
        adb shell settings put global http_proxy <address>:<port>
    '''

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
    '''
        Set proxy on the device
        adb shell settings put global http_proxy <address>:<port>
    '''
    command = ['adb', 'shell', 'settings', 'put', 'global', 'http_proxy', f'{ip}:{port}']
    output, error = Task().run(command)

    print("Proxy set on mobile device:", end=" ")
    print(get_proxy())

class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    self.__run_backup = self.run
    self.run = self.__run      
    threading.Thread.start(self)

  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True

# Main function
def dns_proxy(target_ip):
    global dns_thread, stop_flag
    # Start DNSChef in a separate thread
    stop_flag = threading.Event()
    dns_thread = thread_with_trace(target=dns_spoofing.dns_proxy, args=(target_ip,stop_flag))
    dns_thread.start()

    # Here you can perform other tasks in the main thread
    print("DNS Server is running...")

def get_current_dns_proxy(user_input):
    pass

def set_current_pc_dns_proxy(user_input):
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

    '''
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
    '''
    
    print("\nSet the DNS1 and DNS2 on mobile device at: "+pc_wifi_ip())
    print("(If on Windows, disable the firewall)")

    command = ['adb', 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)
    x=input("Press ENTER to launch the DNS Server...\n")

    dns_proxy(pc_wifi_ip())

def set_generic_dns_proxy(user_input):
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
    command = ['adb', 'shell', 'am', 'start', '-a', 'android.settings.WIFI_SETTINGS']
    output, error = Task().run(command)

    x=input("Press ENTER to launch the DNS Server (or CTRL+C to stop the operation)...\n")
    dns_proxy(remote_ip)

def del_dns_proxy(user_input):
    global dns_thread, stop_flag
    stop_flag.set()
    dns_thread.join()
    

def get_current_invisible_proxy(user_input):
    pass

def set_current_pc_invisible_proxy(user_input):
    pass

def set_generic_invisible_proxy(user_input):
    pass

def del_invisible_proxy(user_input):
    pass