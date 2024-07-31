import nmap
import paramiko
import socket
import ipaddress
import re
import time
import subprocess

# Function to get the current network range
def get_network_range():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_network = ipaddress.ip_network(local_ip + '/24', strict=False)
    return str(ip_network)

# Define the known password and vendor name
known_username = 'kali'
known_password = 'kali'
vendor_name = 'specific_vendor_name'
manufacturer_name = 'Raspberry Pi Foundation'

# Get the current network range
network_range = get_network_range()
print(f"Detected network range: {network_range}")

# Initialize the nmap scanner
nm = nmap.PortScanner()

# Scan the network for devices with open SSH ports
nm.scan(hosts=network_range, arguments='-p 22 --open')



# Function to check for the manufacturer name in the nmap output
def find_manufacturer_name(host):
    if 'vendor' in nm[host]:
        for vendor in nm[host]['vendor'].items():
            print(f"Vendor: {vendor[1]}")
            if re.search(manufacturer_name, vendor[1], re.IGNORECASE):
                return True
    return False

# Iterate over the scanned hosts to find the one with the specific vendor name
target_ip = None
for host in nm.all_hosts():
    if nm[host].has_tcp(22) and nm[host]['tcp'][22]['state'] == 'open':
        print(f"Found device with open SSH port: {host}")
        if find_manufacturer_name(host):
            print(f"Found device with manufacturer name: {manufacturer_name}")
            target_ip = host
            break

# Print all details of the scanned hosts
#for host in nm.all_hosts():
#    print(f"Host: {host}")
#    print(nm[host])

if target_ip:
    print(f"Found target device with IP: {target_ip}")

    # Initialize the SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Attempt to login to the SSH server
        ssh.connect(target_ip, username=known_username, password=known_password)
        print(f"Successfully logged in to {target_ip}")
        

        # Open a new Windows Terminal window and run a command
        command = f'ssh {known_username}@{target_ip} '
        subprocess.run(['wt', '-w', '0', 'nt', 'cmd', '/k', command], shell=True)

        # Execute a command on the SSH server
        #stdin, stdout, stderr = ssh.exec_command('ls')
        #print(stdout.read().decode('utf-8'))


        # Open an interactive shell session
        #shell=ssh.invoke_shell()
        #while True:
        #    if shell.recv_ready():
        #        output = shell.recv(1024).decode('utf-8')
        #        print(output, end=' ')
#
        #    command = input("Enter command to execute (exit/quit to close): ")
        #    if command.lower() in ['exit', 'quit']:
        #        break
        #    shell.send(command + '\n')
        #    time.sleep(1)  # Give the shell time to process the command
    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except Exception as e:
        print(f"Exception in connecting to SSH server: {e}")
    finally:
        ssh.close()
else:
    print("No device with the specified vendor name found.")