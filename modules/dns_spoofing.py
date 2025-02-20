import argparse
import sys
from dnslib import DNSRecord, RR, QTYPE, A
from dnslib.server import DNSServer
import socket

# Burp Suite IP address 
OVERRIDE_IP = '192.168.1.46'
# Domain to be excluded from the interception 
# (The . at the end is mandatory because the DNS records are stored in this way)
DOMAIN_TO_EXCLUDE = "example.com."
# Forward to Google's public DNS server
FORWARD_DNS = "8.8.8.8"  

class OverrideDNSResolver:
    def resolve(self, request, handler):
        """
        Resolve the DNS request by overriding the IP address.

        Args:
            request (DNSRecord): The DNS request.
            handler: The request handler.

        Returns:
            DNSRecord: The DNS response with the overridden IP address.
        """
        #sys.stdout = open(os.devnull, 'w')  # Redirect stdout to null
        # Parse the DNS request
        reply = request.reply()
        qname = str(request.q.qname)
 
        # Check if the requested domain is demo.com
        print(f"OVERRIDE_IP: {qname}")
        # Add a response for demo.com with the overridden IP
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(OVERRIDE_IP), ttl=60))
 
        return reply
 
    def forward_request(self, request):
        """
        Forward the DNS request to the upstream DNS server.

        Args:
            request (DNSRecord): The DNS request.

        Returns:
            DNSRecord: The DNS response from the upstream DNS server.
        """
        #sys.stdout = open(os.devnull, 'w')  # Redirect stdout to null
        # Send the request to the forward DNS server
        try:
            # Convert the request to bytes
            request_data = request.pack()
            # Create a socket to communicate with the upstream DNS server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # Send the request to the upstream DNS server
            sock.sendto(request_data, (FORWARD_DNS, 53))
            # Receive the response from the upstream DNS server
            response_data, _ = sock.recvfrom(4096)
            # Parse the response and return it
            return DNSRecord.parse(response_data)
        except Exception as e:
            print(f"Error forwarding request: {e}")
            return request.reply()  # Return an empty reply on failure


def args_parser():
    """
    Parse the command-line arguments.

    Returns:
        tuple: The parsed command-line arguments.
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(description="DNS Spoofing Tool")
    # Add the fake IP argument
    parser.add_argument("fake_ip", type=str, help="The fake IP address to use for DNS responses")
    # Parse the command-line arguments
    args = parser.parse_args()
    
    return args.fake_ip

def main():
    global OVERRIDE_IP
    '''
    Start a DNS proxy server that overrides DNS responses with a fake IP.

    Args:
        fake_ip (str): The IP address to use for overriding DNS responses.
        stop_flag (threading.Event): A flag to stop the DNS server.
    '''

    OVERRIDE_IP = args_parser()
    original_stdout = sys.stdout  # Save the original stdout

    # Create a resolver instance
    resolver = OverrideDNSResolver()

    # Bind the DNS server to the localhost and port 53
    server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=False)

    # Start the server
    print("Starting DNS server on 0.0.0.0:53...")
    server.start_thread()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()