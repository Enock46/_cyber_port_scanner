import socket  # Importing the socket module for network programming

def port_scanner(target_ip, start_port, end_port):
    """
    Scans a range of ports on a target IP address to determine if they are open or closed.
    
    Args:
        target_ip (str): The IP address of the target to scan.
        start_port (int): The starting port number for the scan.
        end_port (int): The ending port number for the scan.
    """
    print(f"Scanning {target_ip} from port {start_port} to {end_port}...")
    
    # Loop through the range of ports
    for port in range(start_port, end_port + 1):
        # Create a socket using context manager to ensure it is closed after use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set a timeout for the connection attempt (0.5 seconds)
            s.settimeout(0.5)
            
            # Try to connect to the specified port on the target IP
            result = s.connect_ex((target_ip, port))
            # connect_ex() returns 0 if the connection is successful, otherwise a non-zero error code
            
            if result == 0:
                # If the connection was successful, the port is open
                print(f"Port {port}: Open")
            else:
                # If the connection failed, the port is closed or unreachable
                print(f"Port {port}: Closed")

# Prompt the user for the target IP address
target = input("Enter the target IP: ")

# Prompt the user for the starting port number and ensure it is converted to an integer
start = int(input("Enter the starting port: "))

# Prompt the user for the ending port number and ensure it is converted to an integer
end = int(input("Enter the ending port: "))

# Call the port_scanner function with the user inputs
port_scanner(target, start, end)
