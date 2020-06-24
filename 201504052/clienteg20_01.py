import paho.mqtt.client as mqtt
import logging
import time
import os 
import sys
import threading
import socket
import binascii
import wave

sys.path.insert(0, '../')
from globales import *

# JAPO Configuracion de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)s) %(message)s'
    )
# JAPO Funcion a ejecutar al establecer conexion
def on_connect(client, userdata, flags, rc): 
    logging.info("Conectado al broker")
    # JAPO Suscripcion al topic 'usuario'
    archivoUsr = open(ARCHIVO_USUARIOS, 'r')
    usr = []
    for linea in archivoUsr.readlines():
        usr = linea.split("\n")
    topicUsuarios = "usuarios/20/" + usr[0]
    topicAudio = "audio/20/" + usr[0]
    usuario.subscribir((topicUsuarios, 2))
    # JAPO Suscripcion al topic 'audio'
    usuario.subscribir((topicAudio, 2))
    archivoUsr.close()
    # JAPO Suscripcion al topic 'salas'
    archivo = open(ARCHIVO_SALAS, 'r')
    t = []
    s = []
    for linea in archivo.readlines():
        t = linea.split("20")
        for i in range(1, len(t)):
            s = t[i].split("\n")
            topic = 'salas/' + str(NUMERO_GRUPO) + '/' + s[0]
            topicAudSalas = 'audio/' + str(NUMERO_GRUPO) + '/' + s[0]
            usuario.subscribir((topic, qos))
            usuario.subscribir((topicAudSalas, qos))
    archivo.close()

# JAPO Funcion a ejecutar si se publica algo en el broker
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.info(publishText)

# JAPO Funcion a ejecutar si se recibe algo del broker
def on_message(client, userdata, msg):
    # JAPO Se muestra en pantalla informacion que ha llegado
    logging.info("Tiene un mensaje en el topic: " + str(msg.topic))
    temas = []
    temas = str(msg.topic).split('/')
    if temas[0] == 'audio':             # JAPO Si el topic es de audio
        content = []
        content.append(msg.payload)     # JAPO Agrega el contenido binario del audio a un arreglo para su traspaso
        # JAPO Creacion de hilo
        tReproducir = threading.Thread(target= usuario.reproducirAudio,
                                        name='Reproduccion', 
                                        args=(content),
                                    daemon= False
                                    )
        tReproducir.start()      # JAPO Inicia el hilo
    else:
        logging.info("El contenido del mensaje es: " + str(msg.payload.decode()))

# JAPO Iniciar la conexion con el brocker
client = mqtt.Client(clean_session=True)         # JAPO Nueva instancia de cliente MQTT
client.on_connect = on_connect                   # JAPO Funcion "Handler" a ejecutar cuando suceda la conexion
client.on_publish = on_publish                   # JAPO Funcion "Handler" a ejecutar al publicar algo
client.on_message = on_message                   # JAPO Funcion "Handler" a ejecutar al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS)     # JAPO Credenciales requeridas por el broker
client.connect(host= MQTT_HOST, port = MQTT_PORT) # JAPO Conectar al servidor remoto

class cliente(object):
    # JAPO Clase con las funcionalidades de un cliente

    # JAPO Constructor, recibe objeto de tipo mqtt.Client para poder realizar publicaciones, subscripciones, etc...
    def __init__(self, client):
        self.client = client
    
    # JAPO Publicar contenido en un topic
    def publicar(self, topic, valor, qos = 0, retain = False):
        self.client.publish(topic, valor, qos, retain)
    
    # JAPO Subscribirse a los topics necesarios
    def subscribir(self, topics = []):
        self.client.subscribe(topics)
    
    # JAPO Funcion para grabar el audio
    def grabar(self, topic, duracion):
        os.system('arecord -d {} -f U8 -r 8000 201504052_sent.wav'.format(duracion))
        with open('201504052_sent.wav', 'rb') as audio:
                enviar = audio.read()   # JAPO Se lee el archivo de audio en forma binaria
                usuario.publicar(topic, bytearray(enviar))   # JAPO Se publica el archivo de audio en el topic
                audio.close()        # JAPO Se cierra el archivo de audio

    # JAPO Funcion para reproducir el audio
    def reproducirAudio(self, contenido = []):
        print("Reproduciendo")
        with open("201504052_receive.wav", "wb") as rAudio:   # JAPO Se abre el archivo de audio donde se desea guardar audio
            rAudio.write(contenido)                     # JAPO Se escribe el audio recibido sobre el archivo
            rAudio.close
        os.system('aplay 201504052_receive.wav') # JAPO Reproduce el archivo de audio

    # JAPO Terminar la comunicacion con mqtt
    def desconectar(self):
        self.client.disconnect()

qos = 2
usuario = cliente(client)                 # JAPO Instancia de objeto cliente

client.loop_start()
opcion = 0
try:
    while opcion != '3':
        opcion = input("Menu: \n 1 - Enviar texto \n 2 - Enviar mensaje de voz \n 3 - salir \n")
        if opcion == '1':
            op = input(" 1 - Enviar a un usuario individual \n 2 - Enviar a una sala \n")
            if op == '1':
                userDest = input("Ingrese nombre de usuario \n") # JAPO Usuario de destino
                # JAPO Configuracion topic usuarios
                topic = 'usuarios/' + str(NUMERO_GRUPO) + '/' + str(userDest)
            elif op == '2':
                salaDest = input("Ingrese a que sala desea enviarlo \n")   # JAPO Sala de destino
                # JAPO Configuracion topic salas
                topic = 'salas/' + str(NUMERO_GRUPO) + '/' + str(salaDest)
                #usuario.subscribir((topic, qos))
            msj = input("Ingese mensaje \n") # JAPO Mensaje a enviar
            usuario.publicar(topic, msj.encode())   # JAPO El cliente en cuestion va a publicar el mensaje
            
        elif opcion == '2':
            op = input(" 1 - Enviar a un usuario individual \n 2 - Enviar a una sala \n")
            if op == '1':
                userDest = input("Ingrese nombre de usuario \n")  # JAPO Usuario de destino
                # JAPO Configuracion topic usuarios
                topic = 'audio/' + str(NUMERO_GRUPO) + '/' + str(userDest)
            elif op == '2':
                salaDest = input("Ingrese a que sala desea enviarlo \n")
                # JAPO Configuracion topic salas
                topic = 'audio/' + str(NUMERO_GRUPO) + '/' + str(salaDest)
            duracion = input("Ingese duracion del mensaje de voz \n")   # JAPO Duracion del audio a grabar
            # JAPO Instancia del hilo para grabacion de audio
            tGrabar = threading.Thread(target= usuario.grabar,
                                         name='Grabacion', 
                                         args=(topic, duracion),
                                       daemon= False
                                      )
            tGrabar.start()     # JAPO Inicia grabacion de audio en un hilo distinto
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
finally:
    usuario.desconectar()   # JAPO Se desconecta el usuario del broker
    logging.info("Se ha desconectado del broker. Saliendo...")