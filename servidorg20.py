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

# JAPO Funcion a ejecutar si se publica algo en el broker
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.info(publishText)

# JAPO Funcion que se ejecuta cuando llega un mensaje nuevo a un topic al que se esta suscrito.
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))

client = mqtt.Client(clean_session=True)         # JAPO Nueva instancia de cliente MQTT
client.on_connect = on_connect                   # JAPO Funcion "Handler" a ejecutar cuando suceda la conexion
client.on_publish = on_publish                   # JAPO Funcion "Handler" a ejecutar al publicar algo
client.on_message = on_message                   # JAPO Funcion "Handler" a ejecutar al llegar un mensaje a un topic subscrito
client.username_pw_set(globales.MQTT_USER, globales.MQTT_PASS)     # JAPO Credenciales requeridas por el broker
client.connect(host=globales.MQTT_HOST, port = globales.MQTT_PORT) # JAPO Conectar al servidor remoto

qos = 2

# Suscripcion de topics
client.subscribe(("comandos/14/#", qos))
client.subscribe(("usuarios/14/#", qos))
client.subscribe(("salas/14/#", qos))



try:
    while True:
        client.loop_start()
except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")