import socket

# Define host and port for the server
HOST = '169.254.75.25'  # Replace with Raspberry Pi's IP address
PORT = 5000

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    # Get input from the user
    text = input("Enter text to send (or 'q' to quit): ")

    # Send data to the server
    s.sendall(text.encode())

    # If user enters 'q', break out of the loop and close the connection
    if text == 'q':
        break

# Close the connection
s.close()
