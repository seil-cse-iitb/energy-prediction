from SEIL_Energy import *
import paho.mqtt.client as mqtt
import MySQLdb
from config import CONFIG
# Open database connection
db = MySQLdb.connect(CONFIG["database"]["host"],CONFIG["database"]["user"],CONFIG["database"]["password"],CONFIG["database"]["name"] )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(CONFIG["mqtt"]["topic"])

queue = []
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    actual_value = str(msg.payload).split(',')[2]
    ts = int(float(str(msg.payload).split(',')[1]))
    # print("ts",ts)
    if len(queue)<6:
        queue.append(actual_value)
        return
    predicted_value = energy_pred_LSTM(queue)
    queue.pop(0)
    queue.append(actual_value)
    print(predicted_value, actual_value)
    sql = "insert into predicted_power(ts,predicted_value) values("+str(ts)+", "+str(predicted_value)+")"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(CONFIG["mqtt"]["host"], CONFIG["mqtt"]["port"], 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()