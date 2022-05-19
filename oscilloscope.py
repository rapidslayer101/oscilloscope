import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10, 10))#, dpi=100)
#plt.figure()#, dpi=100)

# settings
graph_moves = True
if graph_moves:
    plt.ion()
    update = 0.01  # update every x seconds

precision = 500  # number of points to plot

voltage_step = 0.5  # voltage step per box
v_boxes = 10  # number of voltage step boxes

time_step = 0.1  # time step per box
t_boxes = 10    # number of time step boxes

hertz = 1  # hertz (frequency) of the signal
voltage = 1  # voltage (amplitude)


frequency = round(hertz*time_step*t_boxes, 3)
length = np.pi * 2 * frequency
length2 = np.pi * 2 * 2
length3 = np.pi * 2 * 3

# todo - figure out how to find overlap of all sin waves
if graph_moves:
    v_precision = int(precision*10)
    length = int(length*10)
    length2 = int(length2*10)
    length3 = int(length3*10)
else:
    v_precision = precision

wave = voltage * np.sin(np.arange(0, length, length / v_precision))
wave2 = 2 * np.sin(np.arange(0, length2, length2 / v_precision))
wave3 = 0.5 * np.sin(np.arange(0, length3, length3 / v_precision))

time_step_division = time_step*v_boxes / precision
time = [time_step_division*i for i in range(0, precision)]

t_step_boxes = time_step*t_boxes
v_step_boxes = voltage_step*v_boxes

plt.xlabel("Speed [m/s]")
plt.xlim(0, t_step_boxes)
plt.xticks([time_step*i for i in range(t_boxes+1)])

plt.ylabel("Voltage [V]")
plt.ylim(-v_step_boxes/2, v_step_boxes/2)
plt.yticks([voltage_step*(i-v_boxes/2) for i in range(v_boxes+1)])

plt.grid(True, color="black", linewidth="1.4", alpha=0.5)
plt.minorticks_on()
if graph_moves:
    plt.show()

line1 = plt.plot(time, wave[:precision], color="green", label="Wave1")
line2 = plt.plot(time, wave2[:precision], color="red", label="Wave2")
line3 = plt.plot(time, wave3[:precision], color="blue", label="Wave3")

loop = 0
while True:
    try:
        line1.pop(0).remove()
        line2.pop(0).remove()
        line3.pop(0).remove()
    except NameError:
        pass

    plt.title(f'Wave ({loop})')
    line1 = plt.plot(time, wave[loop:loop+precision], color="green", label="Wave1")
    line2 = plt.plot(time, wave2[loop:loop+precision], color="red", label="Wave2")
    line3 = plt.plot(time, wave3[loop:loop+precision], color="blue", label="Wave3")
    plt.draw()
    if not graph_moves:
        plt.show()
        input()
    plt.pause(update)
    loop += 1
    if loop == (precision*5):
        loop = 0
