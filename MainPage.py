import tkinter as tk
import datetime
from PIL import Image, ImageTk
import threading
import time


class MyLabel(tk.Label):
    def __init__(self, master, filename):

        im = Image.open(filename)
        seq = []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq))
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        tk.Label.__init__(
            self, master, image=self.frames[0], highlightthickness=0, borderwidth=0, bd=0)

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)


def app_click_func():
    root.quit()


def update_time():
    global disp_time, today, label2, label
    label.config(text=disp_time)
    label2.configure(text=today)


def update_thread():
    global disp_time, hr, min, am_pm, sec, year, month, date, disp_time, disp_date, day, weekdays, months, today, app_btn_clicked

    while app_btn_clicked == 0:
        time.sleep(60)
        time1 = datetime.datetime.time(datetime.datetime.now())
        time1 = str(time1)
        hr, min, sec = time1.split(":")
        am_pm = "AM"
        if int(hr) >= 12:
            hr = int(hr)
            if hr == 12:
                hr = 12
            else:
                hr = hr - 12
            am_pm = "PM"
        disp_time = str(hr) + ':' + min + ' ' + am_pm

        disp_date = datetime.datetime.date(datetime.datetime.now())
        disp_date = str(disp_date)
        year, month, date = disp_date.split("-")
        month = int(month)
        day = datetime.datetime.today().weekday()
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "september", "October",
                  "November", "December"]
        today = weekdays[day] + ", " + months[month] + " " + date
        update_time()
    print("Thread Terminated")


root = tk.Tk()
root.configure(background='#212121')
root.attributes('-fullscreen', True)
img5 = tk.PhotoImage(file="apps.png")
button3 = tk.Button()
button3.config(image=img5, borderwidth=0, background='#212121',
               command=app_click_func, highlightthickness=0, bd=0)
button3.place(x=240, y=190)

time1 = datetime.datetime.time(datetime.datetime.now())
time1 = str(time1)
hr, min, sec = time1.split(":")
am_pm = "AM"
if int(hr) >= 12:
    hr = int(hr)
    if hr == 12:
        hr = 12
    else:
        hr = hr - 12
    am_pm = "PM"
disp_time = str(hr) + ':' + min + ' ' + am_pm

disp_date = datetime.datetime.date(datetime.datetime.now())
disp_date = str(disp_date)
year, month, date = disp_date.split("-")
month = int(month)
day = datetime.datetime.today().weekday()
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "september", "October",
          "November", "December"]
today = weekdays[day] + ", " + months[month] + " " + date
print(today)
flag = 0
app_btn_clicked = 0
label2 = tk.Label(root, foreground='#ffffff', background='#212121', font=("Helvetica", 12))
label2.configure(text=today)
label2.place(x=10, y=220)
label = tk.Label(root, foreground='#ffffff', background='#212121', font=("Helvetica", 16))
label.configure(text=disp_time)
label.place(x=10, y=190)
anim = MyLabel(root, 'mov_back1.gif')
anim.place(x=0, y=0)
t = threading.Thread(target=update_thread)
t.setDaemon(True)
t.start()
# root.config(cursor='none')
root.mainloop()
