#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_medicamentos.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): EagleSoft
# Version: 1.0.0 Marzo 2018S
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                   procesador_de_medicamentos.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar valores     |    por el wearable     |
#           |     Procesador de     |    extremos de          |    Xiaomi My Band.     |
#           |     medicamentos      |    medicamentos.        |  - Define el valor ex- |
#           |                       |                         |    tremo de la         |
#           |                       |                         |    medicamentos.       |
#           |                       |                         |  - Notifica al monitor |
#           |                       |                         |    cuando un valor ex- |
#           |                       |                         |    tremo es detectado. |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe los signos  |
#           |       consume()        |          Ninguno         |    vitales vitales    |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    valores extremos   |
#           |                        |     Rabbit.              |    de la medicamentos.|
#           |       callback()       |  - properties: propio de |                       |
#           |                        |     Rabbit.              |                       |
#           |                        |  - body: mensaje recibi- |                       |
#           |                        |     do.                  |                       |
#           +------------------------+--------------------------+-----------------------+
#           |    string_to_json()    |  - string: texto a con-  |  - Convierte un string|
#           |                        |     vertir en JSON.      |    en un objeto JSON. |
#           +------------------------+--------------------------+-----------------------+
#           |    simulador_reloj()   |                          |  - Inicia la simulaci-|
#           |                        |        Ninguno           |    on de un reloj     |
#           +------------------------+--------------------------+-----------------------+
#
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#-------------------------------------------------------------------------
import pika
import sys
sys.path.append('../')
from monitor import Monitor
import time
import threading
from pyfiglet import figlet_format


medicamentosBD_Simulacion=[]

def consume():
    try:
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para leer los mensajes enviados por el
        # Publicador
        channel.queue_declare(queue='medicamentos', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue='medicamentos')
        channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
    except (KeyboardInterrupt, SystemExit):
        channel.close()  # Se cierra la conexión
        sys.exit("Conexión finalizada...")
        time.sleep(1)
        sys.exit("Programa terminado...")

def callback(ch, method, properties, body):
    json_message = string_to_json(body)
    medicamentosBD_Simulacion.append(json_message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def simulador_reloj():
    while True:
        for i in xrange(0,24):
            for x in xrange(0,60):
                print i,':',x
                time.sleep(1)
                try:
                    for z in medicamentosBD_Simulacion:
                        if len(medicamentosBD_Simulacion)>0:
                            parte_horas=int(z['medicamento_hora'][0]+z['medicamento_hora'][1])
                            parte_minutos=int(z['medicamento_hora'][3]+z['medicamento_hora'][4])
                            if i == parte_horas and x == parte_minutos:
                                print(figlet_format('Advertencia'))
                                print 'El adulto con id : ',z['id'],'requiere el medicamento: ',z['medicamento_nombre']
                                medicamentosBD_Simulacion.remove(z)
                                time.sleep(3)
                        else:
                            print 'esta bacio'
                except Exception as e:
                    print e



def string_to_json(string):
    message = {}
    string = string.replace('{', '')
    string = string.replace('}', '')
    values = string.split(', ')
    for x in values:
        v = x.split(': ')
        message[v[0].replace('\'', '')] = v[1].replace('\'', '')
    return message


p_med_cola = threading.Thread(target=consume, name='Servicio')
reloj = threading.Thread(target=simulador_reloj, name='Worker')


reloj.start()
p_med_cola.start()

    #p_medicamentos.consume()
    #p_medicamentos.simulador_reloj()
