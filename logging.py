import time
import krpc

#Подключение к серверу
conn = krpc.connect("log")

#Открытие файла на запись
file = open("D:\KSP.log", "w")

vessel = conn.space_center.active_vessel

file.write("Time Pitch Altitude Speed Mass\n")

engines = vessel.parts.engines

start_mission = conn.add_stream(getattr, engines[5], 'active')
current_time = conn.add_stream(getattr, conn.space_center, 'ut')

#Ожидание начала миссии
while start_mission() != True:
    pass

#Определение времени начала миссии
mission_start_time = conn.space_center.ut
diffent = mission_start_time

#Цикл получения и записи данных
while True:
    if current_time() - diffent >= 1:
        diffent = current_time()
        altitude = vessel.flight().surface_altitude
        pitch = vessel.flight().pitch
        speed = vessel.flight(vessel.orbit.body.reference_frame).speed
        mass = conn.add_stream(getattr, vessel, 'mass')()
        file.write(f"{diffent-mission_start_time}  {pitch} {altitude} {speed} {mass}\n")  
        file.flush()

