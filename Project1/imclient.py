import im
import time
import sys
import atexit

#Function will run before the end of each program
def quit_action():
	if len(server.keys())==1:
		print("\nThe Program has ended")
	else:
		if server['Timeout'] == b'True\n' and b'User1' in server.keys():
			print("Program Timed out")
			print("User 1 input exceeded time limit")

		elif server['Timeout'] == b'True\n' and b'User2' in server.keys():
			print("Program Timed out")
			print("User 2 input exceeded time limit")
		elif server['Quit'] == b'True\n':
			print("User has Quit")

		if name1 == "1" and len(server.keys()) >1:
			server['Quit'] = "True"
			del server['User1']

		if name1 == "2" and len(server.keys()) >1:
			server['Quit'] = "True"
			del server['User2']

		if b'User1' not in server.keys() and b'User2' not in server.keys():
			server.__delitem__('counter')
			server.__delitem__('Quit')
			server.__delitem__('Timeout')
		print("\nThe Program has ended")
		
#connect to server
server= im.IMServerProxy('https://web.cs.manchester.ac.uk/c44054ap/COMP28112_ex1/IMserver.php')

atexit.register(quit_action)
#get userid
name1 = input('Please Enter your userid (1 or 2): ')
#make sure user id is 1 or 2
while not (name1 in ['1','2']):
	print("Incorrect input,try again")
	name1 = input('Please Enter your userid (1 or 2): ')

#makes sure that 2 users are not already using the program
while b'User2' in server.keys() and b'User1' in server.keys():
	print("2 users already active on the program")
	sys.exit()

#makes sure that there are not more than 1 user 1
while name1 =="1" and b'User1' in server.keys():
	print("User 1 is already active")
	print("Please choose the valid id, try again")
	name1 = input('Please Enter your userid (2): ')
	while not (name1 in ['2']):
		print("Incorrect input,try again")
		name1 = input('Please Enter your userid (2): ')

#makes sure that there are not more than 1 user 2
while name1 =="2" and b'User2' in server.keys():
	print("User 2 is already active")
	print("Please choose the valid id, try again")
	name1 = input('Please Enter your userid (1): ')
	while not (name1 in ['1']):
		print("Incorrect input,try again")
		name1 = input('Please Enter your userid (1): ')

#Enter your name
name2 = input('Please Enter your Name: ')
#Inform user of rules
print("\nHi User: "+name1 +": "+name2)
print("If you would like to exit the program, enter Q")
print("If a user has to wait more the 60 seconds for a message")
print("The program will Timeout")
#check for specific keys
if b'counter' not in server.keys():
	server['counter'] = "0"

if b'Quit' not in server.keys():
	server['Quit'] = "False"

if b'Timeout' not in server.keys():
	server['Timeout'] = "False"
#add user keys for specific users
if name1 == "1":
	server['User1'] =""
if name1 == "2":
	server['User2'] =""
#initialise input messages
myMessage = ""
myMessage2 = ""
#make sure there are only 2 users
while (server['Quit'] == b'False\n' and server['Timeout'] == b'False\n'):
	# if u are user 1
	if name1 == "1":
		# get the initial input
		myMessage = input('Type your message: ')
		while myMessage == "":
			print("Nothing was inputted, try again")
			myMessage = input('Type your message: ')
		#if timeout, clear server and exit
		if server['Timeout'] == b'True\n':
			break
		#if timeout, clear server and exit and inform the other user
		if myMessage == "Q":
			print("Sending Quit to User 2")
			server['User1'] = myMessage
			server['counter'] = "1"
			break
		#add the message to the server
		#change value of counter
		server['counter'] = "0"
		server['User1'] = myMessage
		#counter used as a switch
		server['counter'] = "1"
		#wait for user 2 to add to the server
		print('Waiting for User 2')
		counter = 0
		#check the time taken
		while (int(server['counter'].decode()) != 2):
			if server['Quit'] == b'True\n':
				break
			if counter == 60:
				server['Timeout'] = "True"
				break
			time.sleep(1)
			counter +=1
		#if there is a timeout and quit
		if server['Quit'] == b'True\n' or server['Timeout'] == b'True\n':
			break
		#get the message from user2 and print it
		recieve2 = server['User2']
		if recieve2 == b'Q\n':
			print("User 2 has Quit")
			break
		server['User2'] = myMessage2
		print("User 2 message: "+recieve2.decode())

	# if u are user 2
	if name1 == "2":
		#keys should equal 2 if user 1 is connected
		print("Waiting for User 1")
		counter =0
		while (int(server['counter'].decode()) != 1):
			if server['Quit'] == b'True\n':
				break
			if counter == 60:
				server['Timeout'] = "True"
				break
			time.sleep(1)
			counter +=1
		if server['Quit'] == b'True\n' or server['Timeout'] == b'True\n':
			break
		#get the message from user1
		recieve1 = server['User1']
		if recieve1 == b'Q\n':
			print("User 1 has Quit")
			break
		server['User1'] = myMessage
		print("User 1 message: "+recieve1.decode())
		#get the message from user 2
		myMessage2 = input('Type your message: ')
		while myMessage2 == "":
			print("Nothing was inputted, try again")
			myMessage2 = input('Type your message: ')
		if server['Timeout'] == b'True\n':
			break
		if myMessage2 == "Q":
			print("Sending Quit to User 1")
			server['counter'] = "2"
			server['User2'] = myMessage2
			break
		#add to the server, keys should now equal 3
		server['User2'] = myMessage2
		server['counter'] = "2"