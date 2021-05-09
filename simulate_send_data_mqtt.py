# pip3 install paho-mqtt

from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "ecomposteira/composter/measurements"

mac_address = ''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()

    print("Entre uma opção:\n")
    print("1 - Definir mac address")
    print("2 - Enviar mensagem OK")
    print("3 - Enviar alerta")
    print("0 - Sair")

    _input = input()
    while(_input != '0'):
        if _input == '1':
            print("Entre com o mac address:")
            mac_address = input()
        elif _input == '2':
            msg = '{{"ph": 7, "pressure": 0.1362032, "humidity": 0.2, "co2": 0.4712036, "temperature": 50, "cn": 30, "oxigen": 0.4, "weight": 100, "macAddress": "{mac_address}"}}'.format(mac_address=mac_address)
            publish(client, msg)
        elif _input == '3':
            msg = '{{"ph": 0.09952164, "pressure": 0.1362032, "humidity": 0.3774571, "co2": 0.4712036, "temperature": 0.6403599, "cn": 0.9677949, "oxigen": 0.2593356, "weight": 0.7614026, "macAddress": "{mac_address}"}}'.format(mac_address=mac_address)
            publish(client, msg)

        _input = input()