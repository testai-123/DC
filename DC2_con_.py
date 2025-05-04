# CLIENT CODE

!pip install Pyro4

import Pyro4  # Import the Pyro4 library to communicate with the server

def main():
    # Get the URI (Uniform Resource Identifier) of the server object from the user
    uri = input("Enter the URI of the server object: ").strip()
    
    # Connect to the server using the provided URI. Pyro4.Proxy creates a proxy object for the server
    server = Pyro4.Proxy(uri)  # This proxy acts as if it's a local object, but the method calls are actually sent to the server
    
    # Get user input for the two strings to be concatenated
    str1 = input("Enter the first string: ")
    str2 = input("Enter the second string: ")
    
    # Call the 'concatenate' method on the remote server object, passing the two strings as arguments
    concatenated_string = server.concatenate(str1, str2)
    
    # Print the concatenated result received from the server
    print("Concatenated string:", concatenated_string)

if __name__ == "__main__":  # Check if the script is being executed as the main program
    main()  # Run the main function to start the client



# SERVER CODE 

!pip install Pyro4

import Pyro4  # Importing the Pyro4 library to enable remote communication between client and server

@Pyro4.expose  # This decorator exposes the class and its methods to be accessed remotely by the client
class StringConcatenator(object):
    
    # This method concatenates two strings and returns the result
    def concatenate(self, str1, str2):
        return str1 + str2  # Concatenate str1 and str2 and return the result

def main():
    daemon = Pyro4.Daemon()  # Create a Pyro daemon. The daemon is like a server that listens for incoming requests
    uri = daemon.register(StringConcatenator)  # Register our StringConcatenator class with the daemon so it can be accessed remotely
    
    print("Server URI:", uri)  # Print out the URI, which the client will need to connect to this server
    
    daemon.requestLoop()  # Start the daemon's event loop. This keeps the server running and waiting for requests from clients

if __name__ == "__main__":  # Check if the script is being executed as the main program
    main()  # Run the main function to start the server
