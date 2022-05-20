import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(8.5, 7))

# settings
graph_moves = True
if graph_moves:
    plt.ion()
    update = 0.03  # update every x seconds

precision = 250  # number of points to plot

# todo autoscale
voltage_step = 0.75  # voltage step per box
v_boxes = 8  # number of voltage step boxes

time_step = 0.1  # time step per box
t_boxes = 10    # number of time step boxes

# each element of list is for one wave, below lists must be same length
hertz = [1, 0.3, 3, 4, 2]  # hertz (frequency) of the signal
voltages = [1, 2, 0.5, 3, 2]  # voltage (amplitude)
line_colors = ["red", "green", "blue", "black", "orange"]  # color of the line


# todo - figure out how to find overlap of all sin waves
if graph_moves:
    v_precision = int(precision*10)
else:
    v_precision = precision


# todo square wave, triangle wave, sawtooth wave
class SineWave:
    def __init__(self, hz, volt, color, moves):
        self.hz = hz
        self.volt = volt
        self.color = color
        self.moves = moves

    def get_wave(self):
        length = np.pi*2*round(self.hz*time_step*t_boxes, 3)
        if self.moves:
            length = int(length*10)
        return self.volt * np.sin(np.arange(0, length, length/v_precision)), self.color


if len(hertz) != len(voltages) or len(hertz) != len(line_colors):
    print("Error: hertz, voltages and line colors must be the same length")
    exit()

waves = []
for i in range(len(hertz)):
    waves.append(SineWave(hertz[i], voltages[i], line_colors[i], graph_moves))
wave_plots = []
for i in waves:
    wave_plots.append(i.get_wave())


# add wave example
res_list = [wave_plots[0][0][i] + wave_plots[1][0][i] for i in range(len(wave_plots[0][0]))]
wave_plots.append([res_list, "purple"])


# graph setup
time_step_division = time_step*t_boxes / precision
time = [time_step_division*i for i in range(0, precision)]

t_step_boxes = time_step*t_boxes
v_step_boxes = voltage_step*v_boxes

plt.xlabel("Speed [m/s]")
plt.xlim(0, t_step_boxes)
plt.xticks([time_step*i for i in range(t_boxes+1)])

plt.ylabel("Voltage [V]")
plt.ylim(-v_step_boxes/2, v_step_boxes/2)
plt.yticks([voltage_step*(i-v_boxes/2) for i in range(v_boxes+1)])

plt.axhline(y=0, color='k', linestyle='--', alpha=0.2)
plt.axvline(x=(t_boxes*time_step)/2, color='k', linestyle='--', alpha=0.2)
plt.grid(True, color="black", linewidth="1.4", alpha=0.2)
plt.minorticks_on()
if graph_moves:
    plt.show()

lines = []
for wave_plot, color in wave_plots:
    lines.append(plt.plot(time, wave_plot[:precision], color=color))

# graph loop
loop = 0
while True:
    if loop != 0:
        for line in lines:
            line.pop(0).remove()
        lines.clear()
        for wave_plot, color in wave_plots:
            lines.append(plt.plot(time, wave_plot[loop:loop+precision], color=color))

    plt.title(f'Wave ({loop})')
    plt.draw()
    if not graph_moves:
        plt.show()
        input()
    plt.pause(update)
    loop += 1
    if loop == (precision*10-precision):
        loop = 0
