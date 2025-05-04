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
