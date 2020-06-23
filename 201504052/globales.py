# JAPO Archivo con constantes a utilizar en el codigo

ALIVE_PERIOD = 2              # JAPO Enviar comando ALIVE cada 2 segundos
ALIVE_INSISTENT = 0.1         # JAPO Enviar comando ALIVE cada 0.1 segundos

# JAPO Comandos
COMMAND_FRR = b'\x02'         # JAPO Recepcion de archivos, servidor -> cliente
COMMAND_FTR = b'\x03'         # JAPO Transferencia de archivos
COMMAND_ALIVE = b'\x04'       # JAPO Indica que el cliente esta conectado
COMMAND_ACK = b'\x05'         # JAPO Respuesta de confirmacion del servidor al cliente (acknowledge), servidor -> cliente
COMMAND_OK = b'\x06'          # JAPO Respuesta de aceptacion del servidor, servidor -> cliente
COMMAND_NO = b'\x07'          # JAPO Respuesta de negacion del servidor, servidor -> cliente

# JAPO Nombres de archivos de texto a crear
ARCHIVO_USUARIOS = 'usuarios' 
ARCHIVO_SALAS = 'salas'

# JAPO Credenciales del broker
MQTT_HOST = "167.71.243.238"
#MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"

# JAPO Datos para conexion TCP
IP_ADDR = "167.71.243.238"    # JAPO IP a la que se debe de conectar el servidor
#IP_ADDR = "127.0.0.1"
IP_PORT = 9820                # JAPO Puerto para conexion TCP
BUFFER_SIZE = 64 * 1024       # JAPO Tamanio de datos a recibir

# JAPO Datos del grupo
USER_NAME = '201504052'
NUMERO_GRUPO = 20