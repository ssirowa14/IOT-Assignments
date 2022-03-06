import paho.mqtt.client as mqtt
import os
import urllib.parse as urlparse
import threading

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected: " + str(rc))

def on_message(client, obj, msg):
	# print(msg.topic + " @ " + str(msg.qos) + " " + str(msg.payload))
	print("###############################################")
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	message = msg.payload.decode('utf_8')
	print("############################################")
	user = message[:message.find("#")]
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	print("Message From " + user + ": " + message)

def on_publish(client, obj, mid):
    print("Pub: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

print("Enter CLientID")
clientID = input()
client = mqtt.Client(client_id=clientID, clean_session=False)
# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#client.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)
# print("Enter Topic")
# topic = input()

# Connect
client.username_pw_set(url.username, url.password)
client.connect(url.hostname, url.port)

# Start subscribe, with QoS level 0
client.subscribe("test", 2)


# Continue the network loop, exit when an error occurs
def receive():
	while 1:
		client.loop()
recv = threading.Thread(target=receive)
recv.start()
rc = 0
# client.loop_start()
while rc == 0:
	# rc = client.loop()
	print("Enter msg")
	msg = input()
	msg = "0#"+msg
	client.publish("test", msg)
print("rc: " + str(rc))
recv.join()