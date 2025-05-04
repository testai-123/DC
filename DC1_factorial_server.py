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
