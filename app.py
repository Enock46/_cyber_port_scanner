from flask import Flask, render_template, request
import socket
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def scan_port(target_ip, port):
    """
    Scans a single port to check if it's open.
    Args:
        target_ip (str): The IP address of the target machine.
        port (int): The port to scan.
    
    Returns:
        str: Result indicating if the port is 'Open' or 'Closed'.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Set timeout for faster scanning
            result = s.connect_ex((target_ip, port))
            if result == 0:
                return f"Port {port}: Open"
    except Exception:
        pass
    return f"Port {port}: Closed"

def port_scanner(target_ip, start_port, end_port, max_threads=50):
    """
    Manages scanning for a range of ports using multithreading.
    Args:
        target_ip (str): The IP address of the target machine.
        start_port (int): The starting port.
        end_port (int): The ending port.
        max_threads (int): The maximum number of threads to use (default is 50).
    """
    open_ports = []

    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in range(start_port, end_port + 1)]
        for future in futures:
            result = future.result()
            if "Open" in result:
                open_ports.append(result)

    return open_ports

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        target_ip = request.form.get("target_ip")
        port = request.form.get("port")

        if target_ip:
            # If port is not provided, scan a range of ports (e.g., 1-1065535)
            if not port:
                start_port = 1
                end_port = 65535
                results = port_scanner(target_ip, start_port, end_port)
                return render_template("index.html", result=results, target_ip=target_ip, port=None)
            else:
                # If port is provided, scan only the specified port
                port = int(port)
                result = scan_port(target_ip, port)
                return render_template("index.html", result=[result], target_ip=target_ip, port=port)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
