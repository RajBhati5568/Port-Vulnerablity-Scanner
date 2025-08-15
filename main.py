# Importing socket library to create network connections
import socket

# Importing colored output from termcolor for better visibility in terminal
from termcolor import colored

# Function to scan ports on a given target (IP address or hostname)
def scan(target, ports):
    print("\n" + "*** Starting scan for " + str(target) + " ***")
    # Loop through all ports from 1 to the user-defined limit
    for port in range(1, ports + 1):  # "+1" to include the final port in the range
        scan_port(target, port)       # Call function to scan each port individually

# Function to receive and return service/banner information from the socket
def get_banner(s):
    return s.recv(1024)  # Receive up to 1024 bytes of data from the socket

# Function to scan a single port on the given IP address
def scan_port(ipaddress, port):
    try:
        # Create a socket object (default TCP socket)
        sock = socket.socket()
        sock.settimeout(0.3)  # Set a timeout of 0.3 seconds to avoid hanging

        # Try to connect to the target IP and port
        sock.connect((ipaddress, port))

        # Try to grab the banner if available (some services send welcome messages)
        try:
            banner = get_banner(sock)  # Get banner
            # Display the port number and banner in green
            print(colored('[+] Open Port ' + str(port) + ' : ' + banner.decode().strip('\n'), 'green'))
        except:
            # If banner grabbing fails, just report the open port
            print(colored("[+] Open Port " + str(port), 'green'))

        # Close the socket after scanning the port
        sock.close()

    except:
        # If the port is closed or unreachable, do nothing (silently skip)
        pass

# ------------------- MAIN PROGRAM STARTS HERE -------------------

# Ask the user to input the target(s) to scan
# If scanning multiple targets, they should be comma-separated
targets = input("[+] Enter target to scan (comma-separated for multiple): ")

# Ask user how many ports they want to scan (usually top N ports like 1000)
ports = int(input("[+] Enter how many ports you want to scan (e.g., 1000): "))

# Check if the user entered multiple targets
if "," in targets:
    print(colored("\n[*] Scanning multiple targets [*]\n", 'cyan'))

    # Split the targets by comma, strip whitespace, and scan each one
    for ip_add in targets.split(','):
        scan(ip_add.strip(), ports)
else:
    # If only one target is entered, strip whitespace and scan it
    scan(targets.strip(), ports)
