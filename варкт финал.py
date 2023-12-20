import matplotlib.pyplot as plt
from math import *


p0 = 1.2230948554874 #кг/м^3
H = 5600 # Характерестическая высота
С = 2.32 # коэффициент сопротивления 2.32
A = 19.04 # Лобовое сопроивление
rashodS200 = 1820 # расход s200
rashodL110 = 558 # расход L110
dt = 0.1 # Шаг по времени
s1 = round(207000 / rashodS200, 1) # время необходимое для сжигания всего топлива в s200 207000
s2 = round(116800 / rashodL110, 1) # время необходимое для сжигания всего топлива в l110 116800
tyagaS200 = 4_942_300 * 2 # тяга s200
tyagaL110 = 863_200 * 2 # тяга L110
tL110launch = s1  #время запуска L110
tS200off =  s1 #время отбрасывания S200
tL110OFF = s1 + s2 #время отбрасывания S200
masses = {'mextra': 12700, 'mlander': 598, 'mpropulsion': 668, 'mCEengine': 588, 'mHPVE1': 826, 'mS200': 30_760 * 2 + 2 * 207_060, 'mL110': 116_800 + 9670, 'mCE': 588 + 28570} # массы компонентов ракеты
mSUM = sum(masses.values()) # Начальная масса


m = [mSUM]
t = [round(i/10,1) for i in range(1,int((s1 + s2)*10))] # течение времени
vy = [0] # скорость по Oy
vx = [0] # скорость по Ox
dy = [15] # координатапо Oy
dx = [0] # координатапо Ox 


f = open("Attitude.txt", 'r') # файл с зависимостью высоты от времени
angle = [90] # угол  взлета + все  углы во время полета
hfile = [] # высота из ksp
# запись значений с ksp
for i in f:
    i = i.split()
    angle.append(round(float(i[2]),2))
    hfile.append(float(i[1]))
N = len(angle)

counter1 = 0.1 # счётчик времени для s200 
counter2 = 0.1 # счётчик времени для L110
#Фиксирование изменения массы по матмодели
while counter1 <= tL110OFF:
    if counter1 < tL110launch: # для момента работы s200
        m.append(mSUM - 2 * rashodS200 * counter1) 
        counter1 = round(counter1 + dt,1)
    elif tL110launch <= counter1 < tS200off: # для момента работы s200 + l110
        m.append(mSUM - 2 * rashodS200 * counter1 - rashodL110 * counter2) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    elif tS200off <= counter1 < tL110OFF: # для момента работы l110
        m.append(mSUM - masses["mS200"]  - rashodL110 * counter2) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    elif counter1 == tL110OFF: # для момента окончания работы l110
        m.append(mSUM - masses["mS200"] - masses['mL110']) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    else:
        break


#Фиксирование изменения высоты по матмодели    
counter1 = 0.1
for i in range(1, N):
    if counter1 < tL110launch: # для момента работы s200
        vy.append(vy[i-1]+ dt*(tyagaS200*sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180))/m[i-1])
        dy.append( dy[i-1]+vy[i]*dt)
        counter1 = round(counter1 + dt,1)
    elif tL110launch <= counter1 < tS200off: # для момента работы s200 + l110
        vy.append(vy[i-1]+ dt*((tyagaS200 + tyagaL110)*sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180))/m[i-1])
        dy.append( dy[i-1]+vy[i]*dt)
        print('a')
        counter1 = round(counter1 + dt,1)
    elif tS200off <= counter1 <= tL110OFF: # до момента прекращения работы l110
        vy.append(vy[i-1] + dt*(tyagaL110*sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180) )/m[i-1])
        dy.append( dy[i-1] + vy[i] * dt)
        counter1 = round(counter1+dt,1)

#вывод графиков
plt.title("Высота от времени")
plt.xlabel("время, c")
plt.ylabel("высота, м")
plt.plot(t[:N-1], dy[:N-1], label="reallife")
plt.plot(t[:N-1], hfile[:N-1], label="KSP")
plt.legend()
plt.show()

f = open("speed.txt", 'r') # файл с зависимостью высоты от времени
vy = [0] # скорость по Oy
vx = [0] # скорость по Ox
dy = [15] # координатапо Oy
dx = [0] # координатапо Ox
m = [mSUM]
speedfile = []
tfile = []
angle = [90]
dt = 0.14

for i in f:
    i = i.split()
    tfile.append(round(float(i[0]), 2))
    speedfile.append(round(float(i[2]), 2))
    angle.append(round(float(i[1]), 2))

    
N = len(angle)
counter1 = 0.1
counter2 = 0.1
while counter1 <= tL110OFF:
    if counter1 < tL110launch: # для момента работы s200
        m.append(mSUM - 2 * rashodS200 * counter1) 
        counter1 = round(counter1 + dt,1)
    elif tL110launch <= counter1 < tS200off: # для момента работы s200 + l110
        m.append(mSUM - 2 * rashodS200 * counter1 - rashodL110 * counter2) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    elif tS200off <= counter1 < tL110OFF: # для момента работы l110
        m.append(mSUM - masses["mS200"]  - rashodL110 * counter2) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    elif counter1 == tL110OFF: # для момента окончания работы l110
        m.append(mSUM - masses["mS200"] - masses['mL110']) 
        counter1 = round(counter1 + dt,1)
        counter2 = round(counter2 + dt,1)
    else:
        break

counter1 = 0.1
for i in range(1, N):
    if counter1 < tL110launch:
        vy.append(vy[i-1] + dt * (tyagaS200 * sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180)) / m[i-1])
        vx.append(vx[i-1] + dt * (tyagaS200 * cos(angle[i-1] * pi/180) - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vx[i-1] ** 2 * cos(angle[i-1] * pi/180)) / m[i-1])
        dy.append( dy[i-1] + vy[i] * dt)
        counter1 = round(counter1 + dt, 2)
    elif tL110launch <= counter1 < tS200off:
        vy.append(vy[i-1] + dt * ((tyagaS200 + tyagaL110) * sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180)) / m[i-1])
        vx.append(vx[i-1] + dt * ((tyagaS200 + tyagaL110)* cos(angle[i-1] * pi/180) - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vx[i-1] ** 2 * cos(angle[i-1] * pi/180)) / m[i-1])
        dy.append(dy[i-1] + vy[i] * dt)
        counter1 = round(counter1 + dt, 2)
    elif tS200off <= counter1 <= tL110OFF:
        vy.append(vy[i-1] + dt * (tyagaL110 * sin(angle[i-1] * pi/180) - m[i-1] * 9.81 - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vy[i-1] ** 2 * sin(angle[i-1] * pi/180)) / m[i-1])
        vx.append(vx[i-1] + dt * (tyagaL110 * cos(angle[i-1] * pi/180) - 0.5 * p0 * exp(-dy[i-1]/H) * С * A * vx[i-1] ** 2 * cos(angle[i-1] * pi/180)) / m[i-1])
        dy.append(dy[i-1] + vy[i] * dt)
        counter1 = round(counter1+dt, 2)
vresult = [sqrt(vx[i] ** 2 + vy[i] ** 2) for i in range(N)]

plt.title("Скорость от времени")
plt.xlabel("время, c")
plt.ylabel("скорость, м/c")
plt.plot(tfile[:N-1], speedfile[:N-1], label="KSP")
plt.plot(tfile[:N-1], vresult[:N-1], label="reallife")
plt.legend()
plt.show()