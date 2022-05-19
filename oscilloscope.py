import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(13, 13))#, dpi=100)

# settings
graph_moves = False
if graph_moves:
    plt.ion()
    update = 0.01  # update every x seconds

precision = 1000  # number of points to plot

voltage_step = 0.5  # voltage step per box
v_boxes = 10  # number of voltage step boxes

time_step = 0.1  # time step per box
t_boxes = 10    # number of time step boxes

hertz = 1  # hertz (frequency) of the signal
voltage = 1  # voltage (amplitude)


frequency = round(hertz*time_step*t_boxes, 3)
length = np.pi * 2 * frequency
length2 = np.pi * 2 * frequency

if graph_moves:
    v_precision = int(precision*2)
else:
    v_precision = precision

wave = voltage * np.sin(np.arange(0, length, length / v_precision))
wave2 = 2 * np.sin(np.arange(0, length2, length2 / v_precision))

time_step_division = time_step*v_boxes / precision
time = [time_step_division*i for i in range(0, precision)]

t_step_boxes = time_step*t_boxes
v_step_boxes = voltage_step*v_boxes
loop = 0
while True:
    plt.cla()

    plt.xlabel("Speed [m/s]")
    plt.xlim(0, t_step_boxes)
    plt.xticks([time_step*i for i in range(t_boxes+1)])

    plt.ylabel("Voltage [V]")
    plt.ylim(-v_step_boxes/2, v_step_boxes/2)
    plt.yticks([voltage_step*(i-v_boxes/2) for i in range(v_boxes+1)])

    plt.plot(time, wave[loop:loop+precision], color="green", label="Wave1")
    plt.plot(time, wave2[loop:loop+precision], color="red", label="Wave2")
    plt.title(f'Wave ({loop})')
    plt.grid(True, color="black", linewidth="1.4", alpha=0.5)
    plt.minorticks_on()
    plt.draw()
    plt.show()
    plt.pause(update)
    if not graph_moves:
        input()
    loop += 1
    if loop == precision:
        loop = 0
