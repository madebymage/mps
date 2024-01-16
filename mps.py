import asyncio
import socket

async def scan_target(target, port, semaphore):
    async with semaphore:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Set a timeout for the connection attempt
            s.settimeout(1)
            # Attempt to connect to the target and port
            await asyncio.to_thread(s.connect, (target, port))

            # Receive up to 1024 bytes of data (banner)
            banner = s.recv(1024).decode('utf-8').strip()
            print(f"[+] Port {port} on {target} is open - Service: {banner}")
        except socket.error:
            pass
        finally:
            # Close the socket
            s.close()

async def main():
    semaphore = asyncio.Semaphore(100)  # Adjust the number based on your system's limits
    tasks = [scan_target(target, port, semaphore) for port in range(start_port, end_port + 1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Get the target IP or hostname from the user
    target = input("Enter the target IP or hostname: ")

    # Ask the user for the range of ports to scan
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))

    # Run the event loop
    asyncio.run(main())
