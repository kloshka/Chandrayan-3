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


start_mission = conn.add_stream(getattr, engines[5], 'active')

#Установка параметров ascent_autopilot
conn.space_center.target_body = conn.space_center.bodies['Moon']
ascent.autostage = False
ascent.desired_orbit_altitude = 176000
ascent.ascent_path_pvg.desired_apoapsis = 36500000
ascent.ascent_path_pvg.pitch_start_velocity = 50
time.sleep(1)
ascent.launch_to_target_plane()
ascent.enabled = True
time.sleep(1)

#Определение времени начала миссии
while start_mission() != True:
    pass
mission_start_time = conn.space_center.ut

current_time = conn.add_stream(getattr, conn.space_center, 'ut')

#Выход на орбиту Земли с отделением ступеней согласно отделению ступеней в реальной миссии
skip(108)

next_stage()
skip(19)

next_stage()
skip(68)

next_stage()
skip(124)

next_stage()

skip(2.5)
next_stage()

#Ускорение физического времени до выхода на первую орбиту
conn.space_center.physics_warp_factor = 3
while ascent.enabled != False:
    pass
conn.space_center.physics_warp_factor = 0

#Отделение l110 и включение c25
next_stage()
next_stage()


#Выполнение манёвров при приближении к Земле

#Включение РСУ
vessel.control.rcs = True

executor = conn.mech_jeb.node_executor

change_apoapsis = maneuver.operation_apoapsis

skip(7000)

#Выполнение первого манёвра
fchange_apoapsis(41762000)

skip(7000)

change_periapsis = maneuver.operation_periapsis

#Выполнение второго манёвра
fchange_periapsis(226000)

#Пропуск времени для нормальной работы солнечных панелей
while vessel.flight().surface_altitude >= 15000000:
    conn.space_center.rails_warp_factor = 4
conn.space_center.rails_warp_factor = 0

#Выполнение третьего манёвра
fchange_apoapsis(51400000)

skip(7000)

while vessel.flight().surface_altitude >= 15000000:
    conn.space_center.rails_warp_factor = 4
conn.space_center.rails_warp_factor = 0

#Выполнение четвёртого манёвра
fchange_apoapsis(71351000)

skip(14000)

while vessel.flight().surface_altitude >= 30000000:
    conn.space_center.rails_warp_factor = 4
conn.space_center.rails_warp_factor = 0

#Выполнение пятого манёвра
fchange_apoapsis(127603000)


#Ожидан момента, когда Луна будет в самом удобном моменте для транслунной инъекции
for_trasfer = 2160000 + mission_start_time - current_time()
skip(for_trasfer, 5)







