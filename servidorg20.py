import paho.mqtt.client as mqtt
import logging
import time
import os 
import globales
import threading
import socket
import binascii

# JAPO Configuracion de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

# JAPO Funcion a ejecutar cuando se establece la conexion
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

# JAPO Funcion que se ejecuta cuando llega un mensaje nuevo a un topic al que se esta suscrito.
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))
    
    #Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)

client = mqtt.Client(clean_session=True)         # JAPO Nueva instancia de cliente MQTT
client.on_connect = on_connect                   # JAPO Funcion "Handler" a ejecutar cuando suceda la conexion
client.on_publish = on_publish                   # JAPO Funcion "Handler" a ejecutar al publicar algo
client.on_message = on_message                   # JAPO Funcion "Handler" a ejecutar al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS)     # JAPO Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) # JAPO Conectar al servidor remoto

qos = 2

# Suscripcion de topics
client.subscribe(("comandos/14/#", qos))
client.subscribe(("usuarios/14/#", qos))
client.subscribe(("salas/14/#", qos))



try:
    client.loop_start()
except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")