from tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from threading import Thread
from time import sleep

frame_loop = False

# settings
graph_moves = True
if graph_moves:
    update = 0.01  # update every x seconds

precision = 250  # number of points to plot

# todo autoscale
voltage_step = 0.75  # voltage step per box
v_boxes = 8  # number of voltage step boxes

time_step = 0.1  # time step per box
t_boxes = 10    # number of time step boxes

# each element of list is for one wave, below lists must be same length
hertz = [2, 3, 2, 4, 2.5]  # hertz (frequency) of the signal
voltages = [1, 1, 2, 1, 2]  # voltage (amplitude)
line_colors = ["red", "green", "orange", "pink", "lime"]  # color of the line

# checks
for hz in hertz:
    if not hz >= 1:
        print(hz)
        raise Exception("Hertz must be larger than or equal to 1")
for volt in voltages:
    if not volt >= 1:
        raise Exception("voltages must be larger than or equal to 1")


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

    def get_current(self):
        return self.hz, self.volt

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


# add all waves
wave_added = 0
for i in range(len(wave_plots)):
    wave_added = wave_plots[i-1][0] + wave_plots[i][0]
wave_plots.append([wave_added, "purple"])


# graph setup
time_step_division = time_step*t_boxes / precision
time = [time_step_division*i for i in range(0, precision)]

t_step_boxes = time_step*t_boxes
v_step_boxes = voltage_step*v_boxes


def change_state():
    global frame_loop
    if frame_loop:
        frame_loop = False
    else:
        frame_loop = True


def scope():
    plt = Tk()
    plt.config(background='black')
    plt.geometry("1000x700")
    Label(plt, text="Plot").pack()
    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel("Speed [m/s]")
    ax.set_xlim(0, t_step_boxes)
    ax.set_xticks([time_step*i for i in range(t_boxes+1)])

    ax.set_ylabel("Voltage [V]")
    ax.set_ylim(-v_step_boxes / 2, v_step_boxes / 2)
    ax.set_yticks([voltage_step*(i-v_boxes/2) for i in range(v_boxes+1)])

    ax.grid(True, color="black", linewidth="1.4", alpha=0.2)
    ax.minorticks_on()

    graph = FigureCanvasTkAgg(fig, master=plt)
    graph.get_tk_widget().pack(side="top", fill='both', expand=True)

    lines = []
    for wave_plot, color in wave_plots:
        lines.append(ax.plot(time, wave_plot[:precision], color=color))

    def plotter():
        loop = 0
        while frame_loop:
            if loop != 0:
                for line in lines:
                    line.pop(0).remove()
                lines.clear()
                for wave_plot, color in wave_plots:
                    lines.append(ax.plot(time, wave_plot[loop:loop + precision], color=color))
            graph.draw()
            sleep(update)
            loop += 1
            if loop == (precision*10-precision):
                loop = 0

    def gui_handler():
        change_state()
        Thread(target=plotter).start()

    b = Button(plt, text="Stop/Reset", command=gui_handler, bg="red", fg="white")
    b.pack()
    gui_handler()
    plt.mainloop()


if __name__ == '__main__':
    scope()
