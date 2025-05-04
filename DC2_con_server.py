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
