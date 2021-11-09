# -*- coding: cp1252 -*-
from drawnow import *
import numpy as np
import serial
import matplotlib.pyplot as plt
import time

tempc = []
pressure = []
ht = []
axisx = []
axisy = []
axisz = []
arduinoData = serial.Serial('com6', 57600)
plt.ion()
cnt = 0

def fig():
    plt.subplot(2, 3, 1)
    plt.style.use('dark_background')
    plt.rcParams['axes.facecolor'] = 'k'
    plt.title('Altura')
    plt.ylim(-2, 2)
    plt.plot(ht, 'c', label='m')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.ticklabel_format(useOffset=False)
    plt.legend(loc="upper right")
    plt.tight_layout()

    plt.subplot(2, 3, 2)
    plt.title('Temperatura')
    plt.ylim(30, 33)
    plt.plot(tempc, 'm', label='C')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.ticklabel_format(useOffset=False)
    plt.legend(loc="upper right")
    plt.tight_layout()

    plt.subplot(2, 3, 3)
    plt.ylim(99500, 99600)
    plt.title('Pressao')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.plot(pressure, 'y', label='hPa')
    plt.legend(loc='upper right')
    plt.ticklabel_format(useOffset=False)
    plt.tight_layout()

    plt.subplot(2, 3, 4)
    plt.ylim(-500, 500)
    plt.title('Eixo X')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.plot(axisx, 'b', label='Pitch')
    plt.legend(loc='upper right')
    plt.ticklabel_format(useOffset=False)
    plt.tight_layout()

    plt.subplot(2, 3, 5)
    plt.ylim(-500, 500)
    plt.title('Eixo Y')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.plot(axisy, 'g', label='Roll')
    plt.legend(loc='upper right')
    plt.ticklabel_format(useOffset=False)
    plt.tight_layout()

    plt.subplot(2, 3, 6)
    plt.ylim(-500, 500)
    plt.title('Eixo Z')
    plt.grid(False)
    plt.ylabel('Variacao')
    plt.plot(axisz, 'r', label='Yaw')
    plt.legend(loc='upper right')
    plt.ticklabel_format(useOffset=False)
    plt.tight_layout()

tempbucket = 0
pbucket = 0
axbucket = 0
aybucket = 0
azbucket = 0

print('Por favor, coloque o circuito do sensor no chao para calibracao')
print('5')
time.sleep(1)
print('4')
time.sleep(1)
print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('Calibrando o sensor. . .')

for i in np.arange(1, 11, 1):
    while (arduinoData.inWaiting() == 0):
        pass
    arduinoString = arduinoData.readline()
    print(arduinoString)
    dataArray = arduinoString.split(',')
    temp = float(dataArray[0])
    press = float(dataArray[1])
    ax = float(dataArray[2])
    ay = float(dataArray[3])
    az = float(dataArray[4])
    print "temp = ", temp, " , press = ", press, " , ax = ", ax, " , ay = ", ay, " , az = ", az
    tempbucket=tempbucket+temp
    pbucket=pbucket+press
    axbucket=axbucket+ax
    aybucket=aybucket+ay
    azbucket=azbucket+az
    
tempk=(tempbucket/10)+273.15
p0=pbucket/10
pax=axbucket/10
pay=aybucket/10
paz=azbucket/10

print "Parametro da temperatura em K e: ", tempk
print "Parametro da pressao em hPa e: ", p0
print "Parametro do eixo x: ", pax
print "Parametro do eixo y: ", pay
print "Parametro do eixo z: ", paz


while True:
    while (arduinoData.inWaiting() == 0):
        pass
    arduinoString = arduinoData.readline()
    print(arduinoString)
    dataArray = arduinoString.split(',')
    temp = float(dataArray[0])
    press = float(dataArray[1])
    ax = float(dataArray[2])
    ay = float(dataArray[3])
    az = float(dataArray[4])
    h=(98.57*tempk*np.log(p0/press))*0.3048
    print(h)

    ht.append(h)
    tempc.append(temp)                    
    pressure.append(press)
    axisx.append(ax)
    axisy.append(ay)
    axisz.append(az)
    drawnow(fig)
    plt.pause(.0001)
    cnt = cnt + 1

    if cnt > 10:
        tempc.pop(0)
        pressure.pop(0)
        ht.pop(0)
        axisx.pop(0)
        axisy.pop(0)
        axisz.pop(0)
