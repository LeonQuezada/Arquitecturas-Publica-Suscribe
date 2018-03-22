#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: simulador.py
# Capitulo: 3 Patrón Publica-Subscribe
# Autor(es): Perla Velasco & Yonathan Mtz.
# Version: 2.0.1 Mayo 2017
# Descripción:
#
#   Esta clase define el rol de un set-up, es decir, simular el funcionamiento de los wearables del caso de estudio.
#
#   Las características de ésta clase son las siguientes:
#
#                                          simulador.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |  - Iniciar el entorno   |  - Define el id inicial|
#           |        set-up         |    de simulación.       |    a partir del cuál se|
#           |                       |                         |    iniciarán los weara-|
#           |                       |                         |    bles.               |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +-------------------------+--------------------------+-----------------------+
#           |         Nombre          |        Parámetros        |        Función        |
#           +-------------------------+--------------------------+-----------------------+
#           |                         |                          |  - Inicializa los     |
#           |                         |                          |    publicadores       |
#           |     set_up_sensors()    |          Ninguno         |    necesarios para co-|
#           |                         |                          |    menzar la simula-  |
#           |                         |                          |    ción.              |
#           +-------------------------+--------------------------+-----------------------+
#           |                         |                          |  - Ejecuta el método  |
#           |                         |                          |    publish de cada    |
#           |     start_sensors()     |          Ninguno         |    sensor para publi- |
#           |                         |                          |    car los signos vi- |
#           |                         |                          |    tales.             |
#           +-------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import sys
import progressbar
from time import sleep
sys.path.append('publicadores')
from xiaomi_my_band import XiaomiMyBand
from pyfiglet import figlet_format
import time
import pika


class Simulador:
    sensores = []
    id_inicial = 39722608
    medicamentos = []

    def set_up_sensors(self):
        print('cargando')
        self.draw_progress_bar(10)
        print(figlet_format('Bienvenido'))
        print('Tarea 1: arquitecturas Publica - Suscribe')
        print('Cargando simulador')
        self.draw_progress_bar(20)
        print('+---------------------------------------------+')
        print('|        CONFIGURACIÓN DE LA SIMULACIÓN       |')
        print('+---------------------------------------------+')
        adultos_mayores = raw_input('|ingresa el número de adultos mayores: ')
        print('+---------------------------------------------+')
        raw_input('presiona enter para continuar: ')
        print('+---------------------------------------------+')
        print('|            ASIGNACIÓN DE SENSORES           |')
        print('+---------------------------------------------+')
        for x in xrange(0, int(adultos_mayores)):
            
            print('+---------------------------------------------+')
            print('|          ASIGNACIÓN DE MEDICAMENTOS         |')
            print('+---------------------------------------------+')

            adultos_medicamentos = raw_input('|ingresa el número de medicamentos para el adultos: ')
            for x in xrange(0, int(adultos_medicamentos)):
                medicamento_nombre=''
                medicamento_dosis=''
                medicamento_hora=''
                datos_medicamentos = {}
                print('+---------------------------------------------+')
                print('|        NUMERO Y DOSIS DEL MEDICAMENTOS      |')
                print('+---------------------------------------------+')
                medicamento_nombre = raw_input('|ingresa el nombre de medicamentos para el adultos: ')
                medicamento_dosis = raw_input('|ingresa el dosis de medicamentos para el adultos: ')
                salida = True
                while salida:
                    print '|ingresa el Hora del medicamentos para el adultos: '
                    medicamento_hora = raw_input('El formato es de 24 horas : ')
                    try:
                        parte_horas=int(medicamento_hora[0]+medicamento_hora[1])
                        parte_dos_puntos=medicamento_hora[2]
                        parte_minutos=int(medicamento_hora[3]+medicamento_hora[4])
                        if len(medicamento_hora) != 5:
                            print 'El Formato no es correcto HH:MM'
                            continue
                        if parte_horas > 24:
                            print 'la hora esta mal'
                            continue
                        if parte_minutos > 60:
                            print 'los minutos estan mal'
                            continue
                        if parte_dos_puntos != ':':
                            print 'No esta usando 2 puntos'
                            continue
                        salida = False
                    except Exception as e:
                        print 'El Formato no es correcto HH:MM'
                        salida = True
                datos_medicamentos['medicamento_hora']=medicamento_hora
                datos_medicamentos['medicamento_nombre']=medicamento_nombre
                datos_medicamentos['medicamento_dosis']=medicamento_dosis
                self.medicamentos.append(datos_medicamentos)
            s = XiaomiMyBand(self.id_inicial)
            self.sensores.append(s)
            print('| wearable Xiaomi My Band asignado, id: ' + str(self.id_inicial))
            print('+---------------------------------------------+')
            self.id_inicial += 1
        print('+---------------------------------------------+')
        print('|        LISTO PARA INICIAR SIMULACIÓN        |')
        print('+---------------------------------------------+')
        print('')
        print('*Nota: Se enviarán 1000 mensajes como parte de la simulación')
        raw_input('presiona enter para iniciar: ')
        self.mandar_medicamentos()
        self.start_sensors()

    def simulate_medicamentos_reloj(self,id_adulto,medicamentos):
        message = {}
        #self.medicamentos
        for m in medicamentos :
            message['medicamento_nombre'] = m['medicamento_nombre']
            message['medicamento_dosis'] = m['medicamento_dosis']
            message['medicamento_hora'] = m['medicamento_hora']
            message['id'] = str(id_adulto)
            message['datetime'] = self.simulate_datetime()
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            channel.queue_declare(queue='medicamentos', durable=True)
            print('[x] publicando el medicamento '+m['medicamento_nombre']+'...')
            self.draw_progress_bar(2)
            channel.basic_publish(exchange='', routing_key='medicamentos', body=str(message), properties=pika.BasicProperties(
                delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
            connection.close()  # Se cierra la conexión
            print('[x] valor publicado!')
            print('')

    def simulate_datetime(self):
        return time.strftime("%d:%m:%Y:%H:%M:%S")

    def start_sensors(self):
        for x in xrange(0, 1000):
            for s in self.sensores:
                s.publish()

    def mandar_medicamentos(self):
        self.simulate_medicamentos_reloj(self.id_inicial,self.medicamentos)

    def draw_progress_bar(self, value):
        bar = progressbar.ProgressBar(maxval=value, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i in xrange(value):
            bar.update(i+1)
            sleep(0.2)
        bar.finish()

if __name__ == '__main__':
    simulador = Simulador()
    simulador.set_up_sensors()
