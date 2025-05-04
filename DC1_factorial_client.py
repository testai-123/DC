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
