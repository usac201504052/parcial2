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
    format = '[%(levelname)s] (%(threadName)s) %(message)s'
    )
# JAPO Funcion a ejecutar al establecer conexion
def on_connect(client, userdata, flags, rc): 
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)
    logging.info(connectionText)

# JAPO Funcion a ejecutar si se publica algo en el broker
def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

# JAPO Funcion a ejecutar si se recibe algo del broker
def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Tiene un mensaje en el topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))

# JAPO Iniciar la conexion con el brocker
client = mqtt.Client(clean_session=True)         # JAPO Nueva instancia de cliente MQTT
client.on_connect = on_connect                   # JAPO Funcion "Handler" a ejecutar cuando suceda la conexion
client.on_publish = on_publish                   # JAPO Funcion "Handler" a ejecutar al publicar algo
client.on_message = on_message                   # JAPO Funcion "Handler" a ejecutar al llegar un mensaje a un topic subscrito
client.username_pw_set(globales.MQTT_USER, globales.MQTT_PASS)     # JAPO Credenciales requeridas por el broker
client.connect(host= globales.MQTT_HOST, port = globales.MQTT_PORT) # JAPO Conectar al servidor remoto



class controlComandosCliente(object):
    # JAPO Clase para el control de los comandos, enviara y recibira comandos al y del servidor
    def __init__(self, client):
        self.client = client

    # JAPO Metodo para enviar comando ALIVE
    def manifestarse(self, topic, trama, delay):
        while True:
            self.client.publish(topic, tramaAlive, qos = 0, retain = False)
            time.sleep(delay)
    

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
        self.client.subscribe()

    # JAPO Terminar la comunicacion con mqtt
    def desconectar(self):
        self.client.disconnect()
    
    
# JAPO Topics disponibles
topicComandos = 'comandos/' +str(globales.NUMERO_GRUPO) + '/' + globales.USER_NAME
#topicUsuarios = 'usuarios/' + str(userDestino)
#topicSalas = 'salas/' + str(globales.NUMERO_GRUPO) + '/' + str(salaDestino)

dest = b'201501234'
fSize = b'1024'

tramaFTR = globales.COMMAND_FTR + dest + fSize
tramaAlive = globales.COMMAND_ALIVE + b'$' + globales.USER_NAME.encode()

#client.publish(topicComandos, tramaAlive, qos = 0, retain = False)
#client.publish(topicUsuarios, mensaje, qos = 0, retain = False)
#client.publish(topicSalas, mensaje, qos = 0, retain = False)

javier = cliente(client)                 # JAPO Instancia de objeto cliente
cmd = controlComandosCliente(client)     # JAPO Instancia de objeto de control de comandos

# JAPO Hilo para envio de comando Alive
talive = threading.Thread(target= cmd.manifestarse,
                         name='Alive', 
                         args=(topicComandos, tramaAlive, globales.ALIVE_PERIOD),
                         daemon= True
                         )

talive.start()    # JAPO Inicia el hilo
opcion = 0
try:
    while opcion != '3':
        opcion = input("Menu: \n 1 - Enviar texto \n 2 - Enviar mensaje de voz \n 3 - salir \n")
        if opcion == '1':
            op = input(" 1 - Enviar a un usuario individual \n 2 - Enviar a una sala \n")
            if op == '1':
                userDest = input("Ingrese nombre de usuario \n")
                # JAPO Configuracion topic usuarios
                topic = 'usuarios/' + str(globales.NUMERO_GRUPO) + '/' + str(userDest)
            elif op == '2':
                salaDest = input("Ingrese a que sala desea enviarlo \n")
                # JAPO Configuracion topic salas
                topic = 'salas/' + str(globales.NUMERO_GRUPO) + '/' + str(salaDest)
            
            msj = input("Ingese mensaje \n") # JAPO Mensaje a enviar
            # JAPO Enviando por parametros el topic al que se desa enviar y el mensaje
            javier.publicar(topic, msj.encode())   # JAPO El cliente en cuestion va a publicar el mensaje
        elif opcion == '2':
            op = input(" 1 - Enviar a un usuario individual \n 2 - Enviar a una sala \n")
            if op == '1':
                userDest = input("Ingrese nombre de usuario \n")
                duracion = input("Ingese duracion del mensaje de voz \n")

except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
    if talive.is_alive():
        talive._stop()
finally:
    javier.desconectar()
    logging.info("Se ha desconectado del broker. Saliendo...")