import sys
from ex2utils import Server
from datetime import datetime

class EchoServer(Server):

	def onStart(self):
		print("Server has started")
		Server.count = 0
		Server.user = []
		Server.commands = ['MESSAGEALL','MESSAGE','REGISTER','QUIT','HELP','USER','BUSY','FREE','RECEIVED','RECEIVEDALL']
		Server.dict = {}
	
	#called when the user types help
	def helpCommand(self,socket):
		socket.send(str("\nBelow are a list of the commands "+"\n").encode())
		for i in Server.commands:
			if i == 'MESSAGEALL':
				socket.send(str(i + ": This is used to send a message to all active users, Format: <MESSAGEALL><USERNAME><message to send>").encode())
			if i == 'MESSAGE ':
				socket.send(str(i + ": This is used to send a message to a active user, Format: <MESSAGE><USERNAME><message to send>").encode())
			if i == 'REGISTER':
				socket.send(str(i + ": This is used to register a user, Format: <REGISTER><USERNAME>").encode())
			if i == 'QUIT':
				socket.send(str(i + ": This is used to help disconnect the user, Format: <QUIT>").encode())
			if i == 'USER':
				socket.send(str(i + ": This is used to display all active users, Format: <USER>").encode())
			if i == 'RECEIVED':
				socket.send(str(i + ": This is used to display the chat history for private conversations, Format: <RECEIVED>").encode())
			if i == 'RECEIVEDALL':
				socket.send(str(i + ": This is used to display the chat history for conversations sent to all users, Format: <RECEIVEDALL>").encode())
			if i == 'FREE':
				socket.send(str(i + ": This changes your status to AVAILABLE <FREE>").encode())
			if i == 'BUSY':
				socket.send(str(i + ": This changes your status to NOT AVAILABLE, not allowing users to private message, Format: <BUSY>").encode())
		socket.send(str("Enter one of the above commands").encode())
		print('\nCommand is: HELP')
		print ('Message is: <EMPTY>')

	#called when you want to quit
	def quitCommand(self,socket):
		print('\nCommand is: QUIT')
		print ('Message is: <EMPTY>')
		self.onDisconnect(socket)

	def onMessage(self, socket, message):
		#split message up to see what is the message and command
		(command, sep, parameter) = message.strip().partition(" ")
		command1 = message.split()
		#if user already registered
		if command.upper() == 'REGISTER' and socket.register == True:
			socket.send(str("Client is registered, please enter a command followed by the message").encode())
			print('\nCommand is: ',command.upper())
			print ('Username is: ',parameter)
			return True
		#check for a valid command
		if (command.upper() not in Server.commands):
			socket.send(str("Invalid command used, try again").encode())
			print('\nCommand is: ',command.upper())
			print ('Message is: ',parameter)

			return True
		else:
			# if user is not registered they can ask for help or register
			if socket.register == False:
				if command.upper() == "HELP":
					if len(command1) >1:
						socket.send(str("To use HELP command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					self.helpCommand(socket)
					return True
				
				#user chooses to register
				if command.upper() == 'REGISTER':
					#check they specify a username
					if parameter == "":
						socket.send(str("No username inputted, try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Username is: <EMPTY>')
						return True
					#check if the username is taken
					if parameter.upper() in Server.user:
						username = "Username already in use"
						socket.send(username.encode())
						print('\nCommand is: ',command.upper())
						print ('Username is: ',parameter)
						return True
					#check if the username is one word
					if len(parameter.split()) > 1:
						socket.send(str("Invalid Username (Only one word allowed), try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Username is: ',parameter)
						return True

					if not(parameter.isalnum()) or len(parameter) >13:
						socket.send(str("Invalid Username, try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Username is: ',parameter)
						return True
					#add the user to the dictionary
					Server.dict[parameter.upper()] = socket
					#add the username
					Server.user.append(parameter.upper())
					#print command and message to server
					print('\nCommand is: REGISTER')
					print ('Username is: ',parameter.upper())
					#store the name
					socket.name = parameter.upper()
					socket.send(str("You are now registered, enter a new command").encode())
					socket.register = True
					return True

				if command.upper() == 'QUIT':
					if len(command1) >1:
						socket.send(str("To use QUIT command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					self.quitCommand(socket)
					return True
				else:
					socket.send(str("Please register first").encode())
					return True
			#If the user has already registered
			else:
				if command.upper() == "MESSAGE":
					#check they have specified who they want to message
					if len(command1) <2:
						socket.send(str("No user specified, try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					#check they have provided  message
					if len(command1[2:]) == 0:
						socket.send(str("No message inputted, try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					#check the message is not to themselves
					if socket.name == command1[1].upper():
						socket.send(str("You cannot send a message to yourself,Try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					#check if there are actually any users to send to
					if len(Server.user) == 1:
						socket.send(str("No users are active, try again later").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					for i in Server.dict:
						#get the sender and the message
						(sender,messageSend) = parameter.split(" ",1)
						#check to see if they are in the dict
						if i == sender.upper():
							recieves = Server.dict[i]
							if recieves.busy == True:
								socket.send(str(i+" Status: NOT AVAILABLE").encode())
								return True
							socket.send(str("Sending message to "+sender.upper()+" ...").encode())
							now = datetime.now()
							current_time = now.strftime("%H:%M:%S")
							recieves.send((".\n"+"Sender: "+socket.name+"\nMESSAGE: "+messageSend+" (Private)\n"+ "Message sent at: "+ str(current_time)).encode())
							recieves.privMsg.append("\n"+socket.name+" -Sender"+" MESSAGE: "+messageSend+"(Private)\n"+ "Message sent at: "+ str(current_time))
							socket.send(str("Enter a new command and message").encode())
							print('\nCommand is: MESSAGE')
							print ('Message is: ',messageSend)
							print('User Recieving: ',sender.upper())
							return True

					socket.send(str("The user is not registered, try again").encode())
					print('\nCommand is: ',command.upper())
					print ('Message is: ',parameter)
					return True

				if command.upper() =="MESSAGEALL":
					if len(command1[1:]) == 0:
						socket.send(str("No message inputted, try again").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					for i in Server.dict:
						if i == socket.name:
							pass
						else:
							recieves = Server.dict[i]
							(sender,messageSend) = message.split(" ",1)
							now = datetime.now()
							current_time = now.strftime("%H:%M:%S")
							recieves.send((".\n"+"MESSAGE: "+messageSend+"\nSender: "+socket.name+" (To everyone)\n"+ "Message sent at: "+ str(current_time)).encode())
							recieves.allMsg.append("\n"+socket.name+" -Sender"+" MESSAGE: "+messageSend+"(To everyone)\n"+ "Message sent at: "+ str(current_time))

					socket.send(str("Message sent to all users, please enter a new command").encode())
					(sender,messageSend) = message.split(" ",1)
					print('\nCommand is: MESSAGEALL')
					print ('Message is: ',messageSend)
					print('User Recieving: All users')
					return True

				if command.upper() == 'RECEIVED':
					if len(command1) >1:
						socket.send(str("To use RECEIVED command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					if len(socket.privMsg) ==0:
						socket.send(str("You have received no messages").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					for i in socket.privMsg:
						socket.send(str(i).encode())
					socket.send(str("Enter a command followed by a message").encode())
					print('\nCommand is: RECEIVED')
					print ('Message is: <EMPTY>')
					return True

				if command.upper() == 'RECEIVEDALL':
					if len(command1) >1:
						socket.send(str("To use RECEIVEDALL command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					if len(socket.allMsg) ==0:
						socket.send(str("You have received no messages").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					for i in socket.allMsg:
						socket.send(str(i).encode())
					socket.send(str("Enter a command followed by a message").encode())
					print('\nCommand is: RECEIVEDALL')
					print ('Message is: <EMPTY>')
					return True

				if command.upper() == 'BUSY':
					if len(command1) >1:
						socket.send(str("To use BUSY command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					if socket.busy ==True:
						socket.send(str("Status unchanged : "+socket.name+" is NOT AVAILABLE").encode())
						print('\nCommand is: BUSY')
						print ('Message is: <EMPTY>')
						return True
					socket.busy = True
					socket.send(str("Status update : "+socket.name+" is NOT AVAILABLE").encode())
					print('\nCommand is: BUSY')
					print ('Message is: <EMPTY>')
					return True

				if command.upper() == 'FREE':
					if len(command1) >1:
						socket.send(str("To use FREE command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					if socket.busy ==False:
						socket.send(str("Status unchanged : "+socket.name+" is AVAILABLE").encode())
						print('\nCommand is: FREE')
						print ('Message is: <EMPTY>')
						return True
					socket.busy = False
					socket.send(str("Status update : "+socket.name+" is AVAILABLE").encode())
					print('\nCommand is: FREE')
					print ('Message is: <EMPTY>')
					return True


				if command.upper() == 'USER':
					if len(command1) >1:
						socket.send(str("To use USER command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					if len(Server.user) ==1:
						socket.send(str("There are no active users").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					socket.send(str("Below are a list of the active users: ").encode())
					for i in Server.dict:
						if i == socket.name:
							continue
						user = Server.dict[i]
						if user.busy == False:
							socket.send(str(i + "- AVAILABLE").encode())
						else:
							socket.send(str(i + "- NOT AVAILABLE").encode())
					socket.send(str("Enter a command followed by a message").encode())
					print('\nCommand is: USER')
					print ('Message is: <EMPTY>')
					return True

				if command.upper() == "HELP":
					if len(command1) >1:
						socket.send(str("To use HELP command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					self.helpCommand(socket)
					return True

				if command.upper() == 'QUIT':
					if len(command1) >1:
						socket.send(str("To use QUIT command, only enter the command").encode())
						print('\nCommand is: ',command.upper())
						print ('Message is: ',parameter)
						return True
					self.quitCommand(socket)
					return True
		return True
		# Signify all is well

	def onStop(self):
		print("\nServer has been stopped")
		Server.count = 0
		Server.user = []
		Server.dict = {}
	  # This is called just before the server stops, allowing you to clean up any server-
	  # wide variables you may still have set.
	  
	def onConnect(self, socket):
		connect = "\nYou have connected\n"
		socket.send(connect.encode())
		Server.count += 1
		print("Number of clients: ",Server.count)
		socket.register = False
		socket.busy = False
		socket.privMsg = []
		socket.allMsg = []
		socket.name = ""

	def onDisconnect(self, socket):
		disconnect = "\nYou have disconnected"
		socket.send(disconnect.encode())
		Server.count -=1
		if socket.name != "":
			Server.dict.pop(socket.name)
			Server.user.remove(socket.name)
			print(str(socket.name) + " has disconnected")
			print("Number of clients: ",Server.count)
			for i in Server.dict:
				if i == socket.name:
					pass
				user = Server.dict[i]
				if len(user.privMsg) !=0:
					for messages in user.privMsg:
						messageCheck = messages.split()
						if messageCheck[0] == socket.name:
							user.privMsg.remove(messages)

				if len(user.allMsg) !=0:
					for messages in user.allMsg:
						messageCheck = messages.split()
						if messageCheck[0] == socket.name:
							user.allMsg.remove(messages)
		else:
			print("\nClient has disconnected")
			print("Number of clients: ",Server.count)

# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = EchoServer()
# Start server
server.start(ip, port)