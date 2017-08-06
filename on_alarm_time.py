import tkinter as tk
import datetime
import time
import pygame
import threading
import os
stop_clicked = 0
snooze_clicked = 0


def stop_click():
    global stop_clicked
    global snooze_clicked
    stop_clicked = 1
    snooze_clicked = 0
    pygame.mixer.music.stop()
    root.quit()


def thread_time_alarm():
    global time_hr
    am_pm = 'AM'
    while stop_clicked != 1:
        time.sleep(60)
        a = datetime.datetime.time(datetime.datetime.now())
        b, c, d = str(a).split(':')
        if int(b) >= 12:
            am_pm = 'PM'
        time_hr.config(text=b + ':' + c + ' ' + am_pm)


def snooze_action():
    pygame.mixer.music.stop()
    snooze_min = 1
    global label_snooze_time
    global snooze_clicked
    while snooze_clicked == 1 and stop_clicked != 1:
        label_snooze_time.config(text='Snoozed for ' + str(snooze_min) + ' minutes')
        time.sleep(60)
        snooze_min = snooze_min - 1
        if snooze_min == 0:
            label_snooze_time.config(text="")
            break
    play_alarm()


def snooze_button():
    global snooze_clicked
    snooze_clicked = 1
    t_2 = threading.Thread(target=snooze_action)
    t_2.setDaemon(True)
    t_2.start()


def play_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load('Heathens.mp3')
    pygame.mixer.music.play()

root = tk.Tk()
root.config(background="#ffffff")
img_alarm = tk.PhotoImage(file='alarm_ringing.png')
button_alarm = tk.Button(root, image=img_alarm, highlightthickness=0, borderwidth=0, bd=0, background='#ffffff')
button_alarm.place(x=30, y=30)

root.attributes('-fullscreen', True)
root.geometry('320x240')

date_now = datetime.datetime.time(datetime.datetime.now())
hr, min, sec = str(date_now).split(':')
am_pm = 'AM'
if int(hr) >= 12:
    am_pm = 'PM'
time_hr = tk.Label(root, text=hr + ':' + min + ' ' + am_pm, background='#ffffff', foreground='#424242',
                   font=("Helvetica", 20, 'bold'))
time_hr.place(x=150, y=55)
img_snooze = tk.PhotoImage(file="button_snooze.png")
button_snooze = tk.Button(root, image=img_snooze, highlightthickness=0, borderwidth=0, background="#ffffff",
                          command=snooze_button)
button_snooze.place(x=40, y=170)

img_stop = tk.PhotoImage(file="button_stop.png")
button_stop = tk.Button(root, image=img_stop, highlightthickness=0, borderwidth=0, background="#ffffff",
                        command=stop_click)
button_stop.place(x=180, y=170)

label_snooze_time = tk.Label(root, font=("Helvetica", 12, "bold"), background="#ffffff", foreground="#424242")
label_snooze_time.place(x=70, y=125)
t_1 = threading.Thread(target=thread_time_alarm)
t_1.setDaemon(True)
t_1.start()
play_alarm()
root.mainloop()
