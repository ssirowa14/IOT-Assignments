import paho.mqtt.client as mqtt
import os
import urllib.parse as urlparse
import threading
import socket
import time

def sendMsg(msg):              
	s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)           
	port = 4120                
	s.connect(('127.0.0.1', port)) 
	s.sendall(msg.encode('utf-8'))
	msg = s.recv(1024).decode('utf_8')
	s.close()
	if msg == "1":
		return True
	else:
		return False

def login():
	while 1:
		print("1) Register\n2) Login\nEnter Your Choice(1/2): ", end="")
		choice = input()
		print("Enter username: ", end="")
		username = input()
		print("Enter password: ", end="")
		password = input()
		if "#" in username:
			print("ERROR!!! USERNAME CAN'T CONTAIN #")
			continue
		if choice == "1":
			msg = "0"+username+"#"+password
			if sendMsg(msg) == True:
				clientID = username
				print("SUCCESS!!! YOU ARE NOW LOGGED IN")
				break
			else:
				print("ERROR!!! TRY AGAIN")
				continue
		elif choice == "2":
			msg = "1"+username+"#"+password
			if sendMsg(msg) == True:
				clientID = username
				print("SUCCESS!!! YOU ARE NOW LOGGED IN")
				break
			else:
				print("ERROR!!! TRY AGAIN")
				continue
		else:
			print("Wrong Input!!!")

	return clientID

def on_message(client, obj, msg):
	message = msg.payload.decode('utf_8')

	if message[0] == '0':
		user = message[1:message.find("#")]
		message = message[message.find("#")+1:]
		print("\n\nMessage From " + user + ": " + message)
	elif message[0] == '1':
		grp = message[1:message.find("#")]
		user = message[message.find("@")+1 : ]
		message = message[message.find("#")+1 : message.find('@')]
		print("\n\nMessage from " + user + " at group " + grp + " : " + message)


def on_connect(client, userdata, flags, rc):
    print("Connected: " + str(rc))

def on_publish(client, obj, mid):
    print("Published: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos) + obj)

clientID = login()
lock = threading.Lock()
client = mqtt.Client(client_id=clientID, clean_session=False)
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)
client.username_pw_set(url.username, url.password)
client.connect(url.hostname, url.port)
client.subscribe(clientID, 2)
# client.subscribe("test", 2)
print("Client ID:", clientID)
grpSet = set()

def send():
	while 1:
		print("1) Join a Group\n2) Leave a Group\n3) Send Message To User\n4) Send Message To Group\n5)Go Offline\nEnter Your Choice(1-5): ", end="")
		choice = input()
		if choice == "1":
			print("Enter Group ID you want to join: ", end="")
			groupID = input()
			# lock.acquire()
			if groupID not in  grpSet:
				grpSet.add(groupID)
				client.subscribe(groupID, 2)
			else:
				print("already a member\n")
			#groupID.add(clientID)
			# lock.release()
		elif choice == "2":
			print("Enter Group ID you want to leave: ", end="")
			groupID = input()
			if groupID not in grpSet:
				print("Permission denied as you are not a member")
			else:
				client.unsubscribe(groupID)
				grpSet.remove(groupID)			
		elif choice == "3":
			print("Enter the userID you want to send:", end=" ")
			sendTO = input()
			print("Enter your message:", end=" ")
			msg = input()
			msg = '0'+clientID+"#"+ msg
			client.publish(sendTO, msg)
		elif choice == '4':
			print("Enter the GroupID you want to send:", end=" ")
			grpId = input()

			if grpId not in grpSet:
				print("Permission denied as you are not a member")
				continue
			else:
				print("Enter your message:" , end=" ")
				msg = input()
				msg = '1' + grpId + "#" + msg + "@" + clientID
				client.publish(grpId, msg)
		elif choice == "5":
			client.loop_stop()
			print("Enter any key to come online: ", end="")
			input()
			client.loop_start()
			

		else:
			print("WRONG INPUT!!")

client.loop_start()
send()