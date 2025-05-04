# CLIENT CODE 

import xmlrpc.client

class FactorialClient:
    def __init__(self, address):
        self.proxy = xmlrpc.client.ServerProxy(address)

    def calculate_factorial(self, n):
        """Request the server to calculate factorial of n."""
        try:
            result = self.proxy.factorial(n)
            return result
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    server_address = 'http://localhost:8000'
    client = FactorialClient(server_address)
    
    while True:
        try:
            n = int(input("Enter an integer value (negative to exit): "))
            if n < 0:
                break
            result = client.calculate_factorial(n)
            print(f"Factorial of {n} is {result}")
        except ValueError:
            print("Please enter a valid integer value.")


# SERVER CODE 

import xmlrpc.server
import signal


def factorial(n):
    """Compute factorial of n."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

class FactorialServer(xmlrpc.server.SimpleXMLRPCServer):
    def __init__(self, address):
        super().__init__(address)
        self.register_function(factorial, 'factorial')

    def stop(self):
        """Gracefully stop the server."""
        print("\nShutting down the server...")
        self.shutdown()

def signal_handler(sig, frame):
    """Handle the interrupt signal (Ctrl+C) to stop the server."""
    print("\nReceived shutdown signal...")
    server.stop()

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    server = FactorialServer(server_address)

    # Set up the signal handler to catch Ctrl+C (SIGINT) and stop the server
    signal.signal(signal.SIGINT, signal_handler)

    print(f"Factorial server is running on {server_address[0]}:{server_address[1]}")

    try:
        # Start the server
        server.serve_forever()
    except KeyboardInterrupt:
        # Handle the case where the server is stopped using Ctrl+C
        print("\nServer was manually stopped.")
        server.stop()
