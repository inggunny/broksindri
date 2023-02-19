#!/usr/bin/python

# Importamos la libreira de PySerial
import serial
import matplotlib.pyplot as plt
plt.ion()  # turn on interactive mode
fig, ax = plt.subplots()
line, = ax.plot([], [])
xdata, ydata = [], []

i=0
# Abrimos el puerto del arduino a 9600
PuertoSerie = serial.Serial('/dev/ttyACM0', 9600)
# Creamos un buble sin fin
while (i < 200):
    i+= 1
    try:
        # leemos hasta que encontarmos el final de linea
        sArduino = PuertoSerie.readline()
        # Mostramos el valor leido y eliminamos el salto de linea del final
        valor=sArduino.decode("utf8").strip('\r\n')
    except:
        print ("error")
        pass
    
    xdata.append(i)
    print (i ," ", valor)
    ydata.append(valor)
    line.set_data(xdata, ydata)
    #ax.relim()
    #ax.autoscale_view()
    plt.draw()
    plt.pause(0.01)  # pause to allow time for the plot to update

