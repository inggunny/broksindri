#!/usr/bin/python

# Importamos la libreira de PySerial
import serial
i=0
# Abrimos el puerto del arduino a 9600
PuertoSerie = serial.Serial('/dev/ttyACM0', 9600)
# Creamos un buble sin fin
while (i < 1000):
    i+= 1
    try:
        # leemos hasta que encontarmos el final de linea
        sArduino = PuertoSerie.readline()
        # Mostramos el valor leido y eliminamos el salto de linea del final
        valor=sArduino.decode("utf8").strip('\n')
        print (valor)
    except:
        pass
