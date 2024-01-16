import socket
import threading
from queue import Queue

def scan_target(target, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(1)
        # Attempt to connect to the target and port
        s.connect((target, port))
        
        # Receive up to 1024 bytes of data (banner)
        banner = s.recv(1024).decode('utf-8').strip()
        print(f"[+] Port {port} on {target} is open - Service: {banner}")
    except socket.error:
        pass
    finally:
        # Close the socket
        s.close()

def worker():
    while True:
        # Get a port number from the queue
        port = port_queue.get()
        # Perform the scan for the given port
        scan_target(target, port)
        # Mark the task as done
        port_queue.task_done()

# Get the target IP or hostname from the user
target = input("Enter the target IP or hostname: ")

# Create a queue to hold the port numbers
port_queue = Queue()

# Ask the user for the range of ports to scan
start_port = int(input("Enter the starting port: "))
end_port = int(input("Enter the ending port: "))

# Create and start the worker threads
for _ in range(10):  # You can adjust the number of threads based on your preference
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# Enqueue the port numbers to be scanned
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# Wait for all tasks to be completed
port_queue.join()

print("Scanning complete.")
