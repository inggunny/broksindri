# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 13:19:03 2023

@author: elbia
"""

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
PuertoSerie = serial.Serial("/dev/ttyACM0", 9600)

path = "/home/victor/tesis/valores.txt" #Path donde escribe los valores al final


# Función llamada periódicamente por la main
def animate(i, xs, ys):

    sArduino = PuertoSerie.readline()
    valor=sArduino.decode("utf8").strip('\r\n') #la lectura del Arduino decodeada para Linux
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(int(valor)) #el valor lo paso a int

    #Cantidad de muestras que entran en la gráfica
    xs = xs[-288:] 
    ys = ys[-288:]

    # Dibuja X e Y
    ax.clear()
    ax.plot(xs, ys)


    ax.axes.get_xaxis().set_visible(False) #oculta los valores de X
    plt.subplots_adjust(bottom=0.30)
    plt.xlim(0,288) #X de 0 a 288
    plt.ylim(0,1050) #Y de 0 a 1050
    if len(xs) == 288:
        with open(path,"w") as f:
            for elem in ys:
                f.write('{}\n'.format(elem))
        ani.event_source.stop() #Detiene el animation



# Setea plot para llama animate de manera periódica
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=0.001)
plt.show()


