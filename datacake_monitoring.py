import paho.mqtt.client as mqtt 
import logging
import time
import minimalmodbus

logging.basicConfig(level=logging.DEBUG)


slaveaddr = 1
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddr, debug=False, mode=minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1.50          # seconds

mqtt_host = "mqtt.datacake.co"
mqtt_port = 8883
mqtt_user = ""
mqtt_pass = ""
mqtt_pub_topic_prefix = "dtck-pub/<slug>/<serial-number>/"

mqtt_connected = False

#Connection success callback
def on_connect(client, userdata, flags, rc):
    logging.info("MQTT - Connected with result code {} ({})".format(str(rc), mqtt.connack_string(rc)))
    global mqtt_connected
    mqtt_connected = True

def on_disconnect(client, userdata, rc):
    logging.info("MQTT - disconnected!")
    global mqtt_connected
    mqtt_connected = False

def on_publish(client, userdata, mid):
    # logging.info("MQTT - published")
    return None

client = mqtt.Client()
# client.enable_logger(logger=logging)

# Specify callback function
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.tls_set()
client.tls_insecure_set(True)

client.username_pw_set(username=mqtt_user,password=mqtt_pass)

logging.info("Connecting...")
client.connect_async(mqtt_host, port=mqtt_port) 

# wait for connection to broker
client.loop_start()
while not mqtt_connected:
    time.sleep(0.1)
client.loop_stop()

# Read registers
try:
    voltage = instrument.read_float(0, functioncode=4)  # Registernumber, number of decimals
    current = instrument.read_float(6, functioncode=4)
    power = instrument.read_float(12, functioncode=4)
    apparentpower = instrument.read_float(18, functioncode=4)
    reactivepower = instrument.read_float(24, functioncode=4)
    kwh = instrument.read_float(384, functioncode=4)
    
    print("Voltage:          {:0.4f} V".format(voltage))
    print("Current:          {:0.4f} A".format(current))
    print("Power:            {:0.4f} W".format(power))
    print("Apparent power:   {:0.4f} VA".format(apparentpower))
    print("Reactive power:   {:0.4f} VAr".format(reactivepower))
    print("kWh:              {:0.4f} kWh".format(kwh))

    # publish data via mqtt
    client.publish(mqtt_pub_topic_prefix + "VOLT", payload=voltage,qos=0)
    client.publish(mqtt_pub_topic_prefix + "CURRENT", payload=current,qos=0)
    client.publish(mqtt_pub_topic_prefix + "POWER", payload=power,qos=0)
    client.publish(mqtt_pub_topic_prefix + "KILOWATTHOURS", payload=kwh,qos=0)
except IOError:
    print("Failed to read from instrument")

# wait to send data
client.loop_start()
time.sleep(5)
client.loop_stop()

client.disconnect()