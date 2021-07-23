import paho.mqtt.client as mqtt

clientID = 'api_iota2'
usernameMQTT = 'client_iota'
passwordMQTT = 'Amauta2021!'
ipBroker = 'mqtt.zignar.io'
portMQTT = 1883
#topicSub = 'v1/devices/iota/#'
#topicPub = 'v1/devices/iota/rover'
myPayload = "hola"

#Connection success callback
def on_connect(client: mqtt.Client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    #client.subscribe(topicSub)

# Message receiving callback
def on_message(client: mqtt.Client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def mqtt_iota():

    # Define clientID
    client = mqtt.Client(clientID)

    # Set a username and optionally a password for broker authentication
    client.username_pw_set(usernameMQTT, passwordMQTT)

    # Specify callback function
    client.on_connect = on_connect
    client.on_message = on_message

    # Establish a connection
    client.connect(ipBroker, portMQTT, 60)

    # Runs a thread in the background 
    client.loop_start()

    #client.publish(topicPub,myPayload,qos=0)

    return client

    #client.loop_stop()

def publish(topicPub: str, request: str, qos: int):
    mqtt = mqtt_iota()
    mqtt.publish(topicPub, request, qos=qos)
    mqtt.loop_stop()