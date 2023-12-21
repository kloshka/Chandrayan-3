import krpc
import time

#Функция для ускорения глобального или физического времени на определённый промежуток времени
def skip(t, acceleration=2):
    start = current_time()
    time.sleep(1.5)
    conn.space_center.rails_warp_factor = acceleration
    if conn.space_center.rails_warp_factor == 0:
        conn.space_center.physics_warp_factor = 3
    while current_time() - start <= t:
        pass
    conn.space_center.rails_warp_factor = 0
    conn.space_center.physics_warp_factor = 0


#Функция для активации следующей ступени
def next_stage():
    vessel.control.activate_next_stage()

#Функция для изменения апоцентра с ускорением времени
def fchange_apoapsis(h):
    change_apoapsis.new_apoapsis = h
    change_apoapsis.make_nodes()
    executor.execute_all_nodes()
    conn.space_center.physics_warp_factor = 1
    flag = False
    while executor.enabled != False:
        if flag != True:
            time.sleep(10)
            if conn.space_center.rails_warp_factor == 0:
                conn.space_center.physics_warp_factor = 3
    conn.space_center.physics_warp_factor = 0  

#Функция для изменения перицентра с ускорением времени
def fchange_periapsis(h):
    change_periapsis.new_periapsis = h
    change_periapsis.make_nodes()
    executor.execute_all_nodes()
    conn.space_center.physics_warp_factor = 1
    flag = False
    while executor.enabled != False:
        if flag != True:
            time.sleep(10)
            if conn.space_center.rails_warp_factor == 0:
                conn.space_center.physics_warp_factor = 3
    conn.space_center.physics_warp_factor = 0   

#Подключение к серверу 
conn = krpc.connect(name="Autopilot")

ascent = conn.mech_jeb.ascent_autopilot
vessel = conn.space_center.active_vessel
maneuver = conn.mech_jeb.maneuver_planner
engines = vessel.parts.engines

current_time = conn.add_stream(getattr, conn.space_center, 'ut')

#Включение РСУ
vessel.control.rcs = True

executor = conn.mech_jeb.node_executor
change_apoapsis = maneuver.operation_apoapsis
change_periapsis = maneuver.operation_periapsis

#Выполнение манёвров при приближении к Луне

#Выполнение второго манёвра

flag = False
while flag != True:
    try:
        fchange_apoapsis(4313000)
        flag = True
    except:
        pass

#Выполнение третьего манёвра
    
flag = False
while flag != True:
    try:
        fchange_apoapsis(1437000)
        flag = True
    except:
        pass

skip(100,1)

#Выполнение четвёртого манёвра
flag = False
while flag != True:
    try:
        fchange_apoapsis(200000)
        flag = True
    except:
        pass

skip(100,1)

#Выполнение пятого манёвра
flag = False
while flag != True:
    try:
        fchange_apoapsis(185000)
        flag = True
    except:
        pass

skip(100,1)

#Отделение двигательного модуля и запуск посадочного
next_stage()
next_stage()

skip(100,1)

#Выполнение маневров по выводу посадочного модуля из орбиты
flag = False
while flag != True:
    try:
        fchange_periapsis(113000)
        flag = True
    except:
        pass

skip(100,1)

flag = False
while flag != True:
    try:
        fchange_periapsis(2500)
        flag = True
    except:
        pass

#Посадка на Луну
landing = conn.mech_jeb.landing_autopilot
landing.touchdown_speed = 2.5
landing.land_untargeted()
