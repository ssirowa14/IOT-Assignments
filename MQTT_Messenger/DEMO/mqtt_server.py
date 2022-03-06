import socket
import sys

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR | socket.SO_REUSEPORT, 1)
server.bind(('' , 4120))
server.listen(100)

user_set =set()


while True:
	conn , addr = server.accept()
	msg = conn.recv(2048).decode('utf_8')
	ind = msg.find('#')
	username = msg[1 : ind]
	pswd = msg[ind+1 : ]
	flag = True
	if msg[0] == '0':
		for elem in user_set:
			if elem[0] == username:
				flag = False
				break
		if flag:
			user_set.add((username , pswd))
			conn.sendall('1'.encode('utf-8'))
		else:
			conn.sendall('0'.encode('utf-8'))
		conn.close()

	else:
		for elem in user_set:
			if username == elem[0] and pswd == elem[1]:
				flag = False
				break
		if flag == False:
			conn.sendall('1'.encode('utf-8'))
		else:
			conn.sendall('0'.encode('utf-8'))
		conn.close()