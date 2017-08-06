import tkinter as tk
import threading
import time
import datetime


def thread_alarm():
    global total_sec
    print("sleeping for " + str(total_sec))
    time.sleep(total_sec)
    show_window()


def show_window():
    print("Alarm Time")
    print(datetime.datetime.time(datetime.datetime.now()))

i = 0
root = tk.Tk()

time_1 = datetime.datetime.now()
a, time_1 = str(time_1).split(' ')
print(time_1)
a, b, c = time_1.split(':')
time_1 = a + ':' + b
alarm_time = '20:49'
alarm_hr, alarm_min = alarm_time.split(':')
hr, min = time_1.split(':')
diff_time_hr = int(alarm_hr) + (24 - int(hr))
if int(alarm_hr) > int(hr):
    diff_time_hr = int(alarm_hr) - int(hr)
if int(alarm_hr) == int(hr) and int(alarm_min) > int(min):
    diff_time_hr = 0

diff_time_min = int(alarm_min) + (60 - int(min))
if int(alarm_hr) == int(hr) and int(alarm_min) > int(min):
    diff_time_min = int(alarm_min) - int(min)
print(diff_time_hr)
print(diff_time_min)
total_min = diff_time_hr * 60 + diff_time_min
total_sec = total_min * 60
print(total_sec)

t = threading.Thread(target=thread_alarm)
t.start()
