import config
import subprocess
import netifaces

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

def get_proxy():
    '''
        Get the global proxy settings
        settings get global http_proxy
    '''
    command = ['adb', 'shell', 'settings', 'get', 'global', 'http_proxy']
    result = subprocess.run(command, capture_output=True, text=True)

    return result.stdout.strip()

def del_proxy():
    '''
        Reset the global proxy settings
        settings put global http_proxy :0
    '''

    command = ['adb', 'shell', 'settings', 'put', 'global', 'http_proxy', ':0']
    result = subprocess.run(command, capture_output=True, text=True)

    print("Proxy removed on mobile device")

def set_burp_proxy(user_input):
    '''
        Set proxy on the device using the IP machine and the port specified as user input
        adb shell settings put global http_proxy <address>:<port>
    '''
    # If the user input is not a port, ask the user to insert it again
    while not is_port(user_input):
        user_input = input("Insert a valid port number")

    # Retrieve current IP of the PC on the Wi-Fi network  
    ip = pc_wifi_ip()
    # Set the proxy on the mobile device
    set_proxy(ip, user_input)


def set_generic_proxy(user_input):
    pass

def set_proxy(ip, port):
    '''
        Set proxy on the device
        adb shell settings put global http_proxy <address>:<port>
    '''

    command = ['adb', 'shell', 'settings', 'put', 'global', 'http_proxy', f'{ip}:{port}']
    result = subprocess.run(command, capture_output=True, text=True)

    print("Proxy set on mobile device:", end=" ")
    print(get_proxy())

if __name__=="__main__":
    del_proxy()