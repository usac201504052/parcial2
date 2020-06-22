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
    #cmd.respuesta(msg.topic, msg.payload)

    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic.decode()))
    logging.info("El contenido del mensaje es: " + str(msg.payload))

client = mqtt.Client(clean_session=True)         # JAPO Nueva instancia de cliente MQTT
client.on_connect = on_connect                   # JAPO Funcion "Handler" a ejecutar cuando suceda la conexion
client.on_publish = on_publish                   # JAPO Funcion "Handler" a ejecutar al publicar algo
client.on_message = on_message                   # JAPO Funcion "Handler" a ejecutar al llegar un mensaje a un topic subscrito
client.username_pw_set(globales.MQTT_USER, globales.MQTT_PASS)     # JAPO Credenciales requeridas por el broker
client.connect(host=globales.MQTT_HOST, port = globales.MQTT_PORT) # JAPO Conectar al servidor remoto

class controlComandosServidor(object):
    # JAPO Clase para el control de los comandos, enviara y recibira comandos al y del cliente
    def __init__(self, client):
        self.client = client

    # JAPO Respuesta al cliente segun el topic recibido
    def respuesta(self, topic, content):
        temas = topic.split('/')
        if temas[0] == 'comandos':
            trama = content.split('/')



class servidor(object):
    # JAPO Clase con las funcionalidades de un servidor

    # JAPO Constructor, recibe objeto de tipo mqtt.Client para poder realizar publicaciones, subscripciones, etc...
    def __init__(self, client):
        self.client = client

    # JAPO Publicar contenido en un topic
    def publicar(self, topic, valor, qos = 0, retain = False):
        self.client.publish(topic, valor, qos, retain)
    
    # JAPO Subscribirse a los topics necesarios
    def subscribir(self, topics = []):
        self.client.subscribe(topics)

    # JAPO Terminar la comunicacion con mqtt
    def desconectar(self):
        self.client.disconnect()
    
qos = 2

server1 = servidor(client)                 # JAPO Instancia de objeto de tipo servidor
cmd = controlComandosServidor(client)      # JAPO Instancia de tipo control de comandos

# JAPO Suscripcion a topics
server1.subscribir([("comandos/20/#", qos), ("usuarios/20/#", qos), ("salas/20/#", qos)])




client.loop_start()    # JAPO Inicia el ciclo de escucha

try:
    while True:
        logging.info("olakease")
        time.sleep(60)
except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")