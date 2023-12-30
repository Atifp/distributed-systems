import sys
from ex2utils import Client
import time
import os


class IRCClient(Client):

	def onMessage(self, socket, message):
		print(message)
		return True

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an IRC client.
client = IRCClient()
# Start server
try:
	client.start(ip, port)
except OSError:
	print("The server has not started")
	sys.exit()
#send message to the server

try:
	while True:
		message = input("Please enter a command followed by a message (Register first):\n")
		command = message.strip()
		if command.upper() == 'QUIT':
			break
		client.send(message.encode())
except KeyboardInterrupt:
	print("\nYou have disconnected")
	client.stop()

except OSError:
	print("Server down")
	client.stop()
	
#stops client
client.stop()