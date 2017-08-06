try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import datetime
import threading
import pygame
import os
import time
import requests
from bs4 import BeautifulSoup
import PIL
from PIL import Image
from PIL import ImageTk
from mutagen.id3 import ID3
import urllib.request as urllib2
from twitter import *
import json
from PIL import Image, ImageTk

LARGE_FONT = ("Verdana", 12)


class MyClass (tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MediaPlayer, MainPage, Alarm_App, Power_App, TwitterApp, WeatherApp, NewsApp, StartPage2,
                  ShareMarketApp):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


def qf():
    print("Hello")


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

        tk.Label.__init__(self, master, image=self.frames[0], highlightthickness=0, borderwidth=0, bd=0)

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


class MainPage(tk.Frame):

    def app_click_func(self, controller):
        controller.show_frame(StartPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.flag = 0
        self.app_btn_clicked = 0
        self.configure(background='#212121')

        self.img5 = tk.PhotoImage(file="apps.png")
        button3 = tk.Button(self)
        button3.config(image=self.img5, borderwidth=0, background='#212121',
                       command=lambda: self.app_click_func(controller), highlightthickness=0, bd=0)
        button3.place(x=240, y=190)

        self.time = datetime.datetime.time(datetime.datetime.now())
        self.time = str(self.time)
        self.hr, self.min, self.sec = self.time.split(":")
        self.am_pm = "AM"
        if int(self.hr) >= 12:
            self.hr = int(self.hr)
            if self.hr == 12:
                self.hr = 12
            else:
                self.hr = self.hr - 12
            self.am_pm = "PM"
        self.disp_time = str(self.hr) + ':' + self.min + ' ' + self.am_pm

        self.disp_date = datetime.datetime.date(datetime.datetime.now())
        self.disp_date = str(self.disp_date)
        self.year, self.month, self.date = self.disp_date.split("-")
        self.month = int(self.month)
        self.day = datetime.datetime.today().weekday()
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "september", "October",
                  "November", "December"]
        self.today = weekdays[self.day] + ", " + months[self.month] + " " + self.date

        self.label2 = tk.Label(self, foreground='#ffffff', background='#212121', font=("Helvetica", 12))
        self.label2.configure(text=self.today)
        self.label2.place(x=10, y=220)

        self.label = tk.Label(self, foreground='#ffffff', background='#212121', font=("Helvetica", 16))
        self.label.configure(text=self.disp_time)
        self.label.place(x=10, y=190)

        self.anim = MyLabel(self, 'mov_back1.gif')
        self.anim.place(x=0, y=0)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='#212121')

        self.img_power = tk.PhotoImage(file="power.png")
        button_power = tk.Button(self, text="Power", command=lambda: controller.show_frame(Power_App))
        button_power.config(image=self.img_power, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_power.grid(row=0, column=2, pady=4)

        self.img = tk.PhotoImage(file="app_home.png")
        button = tk.Button(self, command=self.sample2)
        button.config(image=self.img, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button.grid(row=1, column=0, padx=15, pady=5)
        self.label1 = tk.Label(self, text="Home", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label1.grid(row=2, column=0)

        self.img2 = tk.PhotoImage(file="app_2_twitter.png")
        button1 = tk.Button(self, command=lambda: controller.show_frame(TwitterApp))
        button1.config(image=self.img2, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button1.grid(row=1, column=1, padx=26, pady=5)
        self.label2 = tk.Label(self, text="Twitter", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label2.grid(row=2, column=1)

        self.img3 = tk.PhotoImage(file="app_3_alarm.png")
        button2 = tk.Button(self, command=lambda: controller.show_frame(Alarm_App))
        button2.config(image=self.img3, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button2.grid(row=1, column=2, padx=26, pady=5)
        self.label3 = tk.Label(self, text="Alarm", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label3.grid(row=2, column=2)

        self.img4 = tk.PhotoImage(file="app_4_news.png")
        button3 = tk.Button(self, command=lambda: controller.show_frame(NewsApp))
        button3.config(image=self.img4, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button3.grid(row=3, column=0, padx=26, pady=5)
        self.label4 = tk.Label(self, text="News", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label4.grid(row=4, column=0)

        self.img5 = tk.PhotoImage(file="app_5_weather.png")
        button4 = tk.Button(self, command=lambda: controller.show_frame(WeatherApp))
        button4.config(image=self.img5, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button4.grid(row=3, column=1, padx=26, pady=5)
        self.label5 = tk.Label(self, text="Weather", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label5.grid(row=4, column=1)

        self.img6 = tk.PhotoImage(file="app_1_media_player.png")
        button5 = tk.Button(self, command=lambda: controller.show_frame(MediaPlayer))
        button5.config(image=self.img6, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button5.grid(row=3, column=2, padx=26, pady=5)
        self.label6 = tk.Label(self, text="Media Player", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label6.grid(row=4, column=2)

        self.img_next = tk.PhotoImage(file="next.png")
        button_next = tk.Button(self, text="Next", command=lambda: controller.show_frame(StartPage2))
        button_next.config(image=self.img_next, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_next.grid(row=5, column=2, pady=4)

        self.label6 = tk.Label(self, text="Page 1 of 2", font=("Helvetica", 10), background='#212121',
                               foreground='#ffffff')
        self.label6.grid(row=5, column=1)

        self.img_prev = tk.PhotoImage(file="prev.png")
        button_prev = tk.Button(self, text="Next")
        button_prev.config(image=self.img_prev, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_prev.grid(row=5, column=0, pady=4)

    def sample2(self):
        os.system('python MainPage.py')


class StartPage2(tk.Frame):

    def sample_radio(self):
        os.system('python radio.py')

    def sample(self):
        os.system("python tryin.py")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='#212121')

        self.img_power = tk.PhotoImage(file="power.png")
        button_power = tk.Button(self, text="Power", command=lambda: controller.show_frame(Power_App))
        button_power.config(image=self.img_power, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_power.grid(row=0, column=2, pady=4)

        self.img = tk.PhotoImage(file="app_snake_game.png")
        button = tk.Button(self, command=self.sample)
        button.config(image=self.img, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button.grid(row=1, column=0, padx=15, pady=5)
        self.label1 = tk.Label(self, text="Slither", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label1.grid(row=2, column=0)

        self.img2 = tk.PhotoImage(file="app_tic_tac_toe.png")
        button1 = tk.Button(self)
        button1.config(image=self.img2, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button1.grid(row=1, column=1, padx=26, pady=5)
        self.label2 = tk.Label(self, text="Tic-Tac-Toe", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label2.grid(row=2, column=1)

        self.img3 = tk.PhotoImage(file="app_radio.png")
        button2 = tk.Button(self, command=self.sample_radio)
        button2.config(image=self.img3, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button2.grid(row=1, column=2, padx=26, pady=5)
        self.label3 = tk.Label(self, text="Radio", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label3.grid(row=2, column=2)

        self.img4 = tk.PhotoImage(file="app_memes.png")
        button3 = tk.Button(self)
        button3.config(image=self.img4, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button3.grid(row=3, column=0, padx=26, pady=5)
        self.label4 = tk.Label(self, text="Memes", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label4.grid(row=4, column=0)

        self.img5 = tk.PhotoImage(file="share_market_app.png")
        button4 = tk.Button(self, command=lambda: controller.show_frame(ShareMarketApp))
        button4.config(image=self.img5, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button4.grid(row=3, column=1, padx=26, pady=5)
        self.label5 = tk.Label(self, text="Share Market", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label5.grid(row=4, column=1)

        self.img6 = tk.PhotoImage(file="clock_app.png")
        button5 = tk.Button(self)
        button5.config(image=self.img6, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button5.grid(row=3, column=2, padx=26, pady=5)
        self.label6 = tk.Label(self, text="Clock", font=("Helvetica", 8), background='#212121',
                               foreground='#ffffff')
        self.label6.grid(row=4, column=2)

        self.label6 = tk.Label(self, text="Page 2 of 2", font=("Helvetica", 10), background='#212121',
                               foreground='#ffffff')
        self.label6.grid(row=5, column=1)
        self.img_next = tk.PhotoImage(file="next.png")
        button_next = tk.Button(self)
        button_next.config(image=self.img_next, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_next.grid(row=5, column=2, pady=4)
        self.img_prev = tk.PhotoImage(file="prev.png")
        button_prev = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        button_prev.config(image=self.img_prev, background='#212121', borderwidth=0, highlightthickness=0, bd=0)
        button_prev.grid(row=5, column=0, pady=4)


class Power_App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background="#424242")
        self.img_power_off = tk.PhotoImage(file='button_power-off.png')
        self.btn_power_off = tk.Button(self, image=self.img_power_off, highlightthickness=0, background="#424242",
                                       borderwidth=0, command=self.quit)
        self.btn_power_off.place(x=45, y=10)

        self.img_reboot = tk.PhotoImage(file='button_reboot.png')
        self.btn_reboot = tk.Button(self, image=self.img_reboot, highlightthickness=0, background="#424242",
                                    borderwidth=0, command=self.quit)
        self.btn_reboot.place(x=45, y=60)

        self.img_exit = tk.PhotoImage(file='button_exit.png')
        self.btn_exit = tk.Button(self, image=self.img_exit, highlightthickness=0, background="#424242", borderwidth=0,
                                  command=self.quit)
        self.btn_exit.place(x=45, y=110)

        self.img_switch = tk.PhotoImage(file='button_switch-to-hdmi.png')
        self.btn_switch = tk.Button(self, image=self.img_switch, highlightthickness=0, background="#424242", borderwidth=0,
                                    command=self.quit)
        self.btn_switch.place(x=45, y=160)


class NewsApp(tk.Frame):

    def show_data(self):
        self.w.config(text=self.headlines[self.i])
        self.label_date.config(text=self.date[self.i], background="#000000", foreground='#ffffff')
        self.label_time.config(text = self.time[self.i])
        self.image = ImageTk.PhotoImage(file='H:\\Projects\\Project\\inshorts_images\\new'
                                             + str(self.i) + '.jpg')
        self.button_image.config(image=self.image)

    def prev_button(self):
        if self.i == 0:
            self.i = 24
        else:
            self.i = self.i - 1
        self.show_data()

    def next_button(self):
        if self.i == 24:
            self.i = 0
        else:
            self.i = self.i + 1
        self.show_data()

    def __init__(self, parent, controller):
        self.i = 0
        tk.Frame.__init__(self, parent)

        self.configure(background="#000000")
        r = requests.get('https://www.inshorts.com/en/read')
        self.images = []
        self.date = []
        self.time = []
        soup = BeautifulSoup(r.content, "html.parser")
        spans_headline = []
        self.headlines = []
        divs_date_time = []
        for span in soup.find_all('span'):
            if span.get('itemprop') == 'headline':
                spans_headline.append(span)

        for span in spans_headline:
            self.headlines.append(span.text)

        for div in soup.find_all('div'):
            if div.get('class') == ['news-card-image']:
                a = div.get('style')
                b, c = str(a).split('(')
                d, e = str(c).split('?')
                f, g = str(d).split("'")
                self.images.append(g)

        for div in soup.find_all('div'):
            if div.get('class') == ['news-card-author-time', 'news-card-author-time-in-title']:
                divs_date_time.append(div)

        for i in range(len(divs_date_time)):
            for span in divs_date_time[i].find_all('span'):
                if span.get('class') == ['time']:
                    self.time.append(span.text)
                elif span.get('clas') == 'date':
                    self.date.append(span.text)
        for i in range(len(self.images)):
            file_name = 'H:\\Projects\\Project\\inshorts_images\\new' + str(i) + '.jpg'
            with open(file_name, 'wb') as f:
                f.write(requests.get(self.images[i]).content)
            img = Image.open('H:\\Projects\\Project\\inshorts_images\\new' + str(i) + '.jpg')
            img = img.resize((130, 130), PIL.Image.ANTIALIAS)
            img.save('H:\\Projects\\Project\\inshorts_images\\new' + str(i) + '.jpg')

        self.i = 0
        self.button_image = tk.Button(self, background="#ffffff", highlightthickness=0, borderwidth=0)
        self.w = tk.Message(self, width=180, background="#000000", foreground="#ffffff",
                            font=('Helvetica', 12))
        self.button_image.place(x=2, y=30)
        self.w.place(x=137, y=50)

        self.img_prev = tk.PhotoImage(file="prev.png")
        self.button_prev = tk.Button(self)
        self.button_prev.config(image=self.img_prev, background='#000000', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.prev_button)
        self.button_prev.place(x=20, y=200)
        self.img_next = tk.PhotoImage(file="next.png")
        self.button_next = tk.Button(self)
        self.button_next.config(image=self.img_next, background='#000000', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.next_button)
        self.button_next.place(x=280, y=200)
        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.button_close.config(image=self.img_close, background='#000000', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)

        self.label_date = tk.Label(self)
        self.label_date.place(x=5, y=5)
        self.label_time = tk.Label(self, background="#000000", foreground="#ffffff")
        self.label_time.place(x=135, y=5)
        self.button_read_more = tk.Button(self, text="Read More", background="#212121", foreground="#ffffff",
                                          highlightthickness=0, borderwidth=0, font=("Helvetica", 12))
        self.button_read_more.place(x=150, y=150)
        self.show_data()


class ShareMarketApp(tk.Frame):

    def show_data(self):
        print('Showing Results')
        self.label_name.config(text=self.list_symbols[self.main_i])
        self.label_lastPrice.config(text=self.lastPrice[self.main_i])
        if self.up_down[self.main_i] == 'up':
            self.label_lastPrice.config(foreground='#388E3C')
            self.label_per_change.config(foreground='#388E3C')
            self.button_up_down.config(image=self.img_up)
        else:
            self.label_lastPrice.config(foreground='#E53935')
            self.label_per_change.config(foreground='#E53935')
            self.button_up_down.config(image=self.img_down)
        self.label_updateTime.config(text=self.lastUpdateTime[self.main_i])
        self.label_per_change.config(text='(' + self.perChange[self.main_i] + '%)')
        self.label_high.config(text=self.dayHigh[self.main_i])
        self.label_low.config(text=self.dayLow[self.main_i])
        self.label_open.config(text=self.previousClose[self.main_i])


    def calcValues(self, string):
        index_lastPrice = self.raw_div.find(string)
        raw_lastPrice = self.raw_div[index_lastPrice - 1:]
        j = 0
        while True:
            if raw_lastPrice[j] == ',':
                break
            else:
                j = j + 1

        raw2_lastPrice = raw_lastPrice[0:j]

        if self.updateTime == 1:
            a, b, c, d = raw2_lastPrice.split(':')
            b = b + ':' + c + ':' + d
        else:

            a, b = raw2_lastPrice.split(':')
        self.updateTime = 0
        fin = b[1:len(b) - 1]
        return fin

    def getValues(self, m):
        r = requests.get(self.list_url[m])
        soup = BeautifulSoup(r.content, 'html.parser')
        for div in soup.find_all('div'):
            if div.get('id') == 'responseDiv':
                self.raw_div = str(div)
        self.dayHigh.append(self.calcValues('dayHigh'))
        self.lastPrice.append(self.calcValues('lastPrice'))
        self.dayLow.append(self.calcValues('dayLow'))
        self.previousClose.append(self.calcValues('previousClose'))
        self.todayOpen.append(self.calcValues('open'))
        self.updateTime = 1
        self.lastUpdateTime.append(self.calcValues('lastUpdateTime'))
        if float(self.lastPrice[m]) > float(self.previousClose[m]):
            self.up_down.append('up')
        else:
            self.up_down.append('down')
        self.perChange.append(self.calcValues('pChange'))

    def next_button(self):
        if self.main_i == len(self.list_symbols) - 1:
            self.main_i = 0
        else:
            self.main_i = self.main_i + 1
        self.show_data()

    def prev_button(self):
        if self.main_i == 0:
            self.main_i = len(self.list_symbols) - 1
        else:
            self.main_i = self.main_i - 1
        self.show_data()

    def refresh_button(self):
        r = requests.get(self.list_url[self.main_i])
        soup = BeautifulSoup(r.content, 'html.parser')
        for div in soup.find_all('div'):
            if div.get('id') == 'responseDiv':
                self.raw_div = str(div)
        self.dayHigh[self.main_i] = self.calcValues('dayHigh')
        print(self.dayHigh[self.main_i])
        self.lastPrice[self.main_i] = self.calcValues('lastPrice')
        self.dayLow[self.main_i] = self.calcValues('dayLow')
        self.previousClose[self.main_i] = self.calcValues('previousClose')
        self.todayOpen[self.main_i] = self.calcValues('open')
        self.updateTime = 1
        self.lastUpdateTime[self.main_i] = self.calcValues('lastUpdateTime')
        print(self.lastUpdateTime[self.main_i])
        if float(self.lastPrice[self.main_i]) > float(self.previousClose[self.main_i]):
            self.up_down[self.main_i] = 'up'
        else:
            self.up_down[self.main_i] = 'down'
        self.perChange[self.main_i] = self.calcValues('pChange')
        print('Updated Share Market Values')
        self.show_data()

    def __init__(self, parent, controller):
        self.list_symbols = ['DISHTV', 'JPINFRATEC', 'BALRAMCHIN', 'DHAMPURSUG', 'NMDC', 'NTPC', 'SITINET', 'DCBBANK',
                        'HINDPETRO', 'KOTAKBANK']

        self.base_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='
        self.list_url = []
        for i in range(len(self.list_symbols)):
            self.string = self.base_url + self.list_symbols[i]
            self.list_url.append(self.string)

        self.raw_div = ''
        self.dayHigh = []
        self.lastPrice = []
        self.dayLow = []
        self.previousClose = []
        self.todayOpen = []
        self.up_down = []
        self.lastUpdateTime = []
        self.updateTime = 0
        self.perChange = []
        self.main_i = 0
        tk.Frame.__init__(self, parent)
        self.config(background='#ffffff')
        for m in range(len(self.list_url)):
            self.getValues(m)
        self.img_prev = tk.PhotoImage(file="prev.png")
        self.button_prev = tk.Button(self)
        self.button_prev.config(image=self.img_prev, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.prev_button)
        self.button_prev.place(x=20, y=200)
        self.img_next = tk.PhotoImage(file="next.png")
        self.button_next = tk.Button(self)
        self.button_next.config(image=self.img_next, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.next_button)
        self.button_next.place(x=280, y=200)

        self.f = tk.Frame(self, width=330, height=140, background="#ffffff")
        self.f.grid(row=0, column=0, sticky="NW")
        self.f.grid_propagate(0)
        self.label_name = tk.Label(self.f, font=('Helvetica', 14, 'bold'), background="#ffffff", foreground="#000000")
        self.label_name.place(x=165, y=60, anchor="center")
        self.label_lastPrice = tk.Label(self.f, font=("Helvetica", 12, 'bold'), background="#ffffff", foreground="#000000")
        self.label_lastPrice.place(x=165, y=90, anchor="center")

        self.label_per_change = tk.Label(self.f, text='(1.60%)', font=("Helvetica", 9, 'bold'), background="#ffffff",
                                         foreground="#000000")
        self.label_per_change.place(x=165, y=110, anchor="center")

        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage2))
        self.button_close.config(image=self.img_close, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)

        self.label_updateTime = tk.Label(self, font=('Helvetica', 9), background='#ffffff', foreground='#000000')
        self.label_updateTime.place(x=10, y=5)

        self.img_up = tk.PhotoImage(file='up_share_market.png')
        self.img_down = tk.PhotoImage(file='down_share_market.png')
        self.button_up_down = tk.Button(self, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
        self.button_up_down.place(x=60, y=60)

        self.label_head_high = tk.Label(self, text='High', background='#ffffff', foreground='#000000',
                                        font=('Helvetica', 10, 'bold'))
        self.label_head_high.place(x=50, y=140)

        self.label_head_low = tk.Label(self, text='Low', background='#ffffff', foreground='#000000',
                                       font=('Helvetica', 10, 'bold'))
        self.label_head_low.place(x=140, y=140)

        self.label_head_open = tk.Label(self, text='Pr. Close', background='#ffffff', foreground='#000000',
                                        font=('Helvetica', 10, 'bold'))
        self.label_head_open.place(x=220, y=140)

        self.label_high = tk.Label(self, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
        self.label_high.place(x=50, y=160)

        self.label_low = tk.Label(self, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
        self.label_low.place(x=140, y=160)

        self.label_open = tk.Label(self, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
        self.label_open.place(x=220, y=160)
        self.img_refresh = tk.PhotoImage(file='button_refresh.png')
        self.btn_refresh = tk.Button(self, image=self.img_refresh, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0,
                                     command=self.refresh_button)
        self.btn_refresh.place(x=100, y=185)
        self.show_data()


class TwitterApp(tk.Frame):

    def getdata(self):
        self.w['text'] = self.x[self.i]['text']
        self.retweet = self.x[self.i]['retweet_count']
        self.favourite = self.x[self.i]['favorite_count']
        self.created_at = self.x[self.i]['created_at']
        self.day_created_at, self.month_created_at, self.date_created_at, self.time_created_at, self.blah, self.year = str(self.created_at).split(" ")
        self.final_created_at = self.day_created_at + ",  " + self.month_created_at + " " + self.date_created_at + ", " + self.time_created_at

        self.user_details = self.x[self.i]['user']
        self.username = self.user_details['screen_name']
        self.name = self.user_details['name']
        self.label_name.config(text=self.name)
        self.label_retweet.config(text=self.retweet)
        self.label_favourite.config(text=self.favourite)
        self.label_screenname.config(text="@" + self.username)
        self.label_date.config(text=self.final_created_at)
        self.show_data()

    def show_data(self):
        self.w.place(x=15, y=80)
        self.label_name.place(x=30, y=20)
        self.label_screenname.place(x=30, y=45)
        self.label_retweet.place(x=110, y=200)
        self.label_favourite.place(x=220, y=200)
        self.label_date.place(x=10, y=0)

    def next_button(self):
        if self.i == 15:
            self.i = 0
        else:
            self.i = self.i + 1
        self.getdata()

    def prev_button(self):
        if self.i == 0:
            self.i = 15
        else:
            self.i = self.i - 1
        self.getdata()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.i = 0
        self.configure(background="#0084b4")
        self.img_prev = tk.PhotoImage(file="prev.png")
        self.button_prev = tk.Button(self)
        self.button_prev.config(image=self.img_prev, background='#0084b4', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.prev_button)
        self.button_prev.place(x=20, y=200)
        self.img_next = tk.PhotoImage(file="next.png")
        self.button_next = tk.Button(self)
        self.button_next.config(image=self.img_next, background='#0084b4', borderwidth=0, highlightthickness=0, bd=0,
                                command=self.next_button)
        self.button_next.place(x=280, y=200)
        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.button_close.config(image=self.img_close, background='#0084b4', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)
        self.t = Twitter(auth=OAuth('753977332788891648-KWXF1E0pFllOa6WV4zmYTMy0JFbSjP2',
                               'twbzilntsJAVFdrKDwR9KNs4IRS86ekL9gRRgSoW1Ox6E', '8VSv8pymCo4lnsUFUVdn1jRko',
                               'iEjoDhnXm6JfU0RWcqj8oj87Bxe4c666nqq8ZkR4fXVrUhOFOk'))

        self.x = self.t.statuses.home_timeline(screen_name="akshatag97")
        self.w = tk.Message(self, width=280, background="#0084b4", foreground="#ffffff", font=("Helvetica", 12))
        self.label_name = tk.Label(self, background="#0084b4", foreground="#ffffff", font=("Helvetica", 14))
        self.label_screenname = tk.Label(self, background="#0084b4", foreground="#ffffff", font=("Helvetica", 12))
        self.label_retweet = tk.Label(self, background="#0084b4", foreground="#212121", font=("Helvetica", 10))
        self.label_favourite = tk.Label(self, background="#0084b4", foreground="#212121", font=("Helvetica", 10))

        self.img_retweet = tk.PhotoImage(file="retweet.png")
        self.button_retweet = tk.Button(self, image=self.img_retweet, background='#0084b4', borderwidth=0,
                                        highlightthickness=0)
        self.button_retweet.place(x=70, y=200)

        self.img_favourite = tk.PhotoImage(file="favourite.png")
        self.button_favourite = tk.Button(self, image=self.img_favourite, background="#0084b4", borderwidth=0,
                                          highlightthickness=0)
        self.button_favourite.place(x=180, y=200)
        self.label_date = tk.Label(self, background="#0084b4", foreground="#ffffff", font=("Helvetica", 10))
        self.getdata()


class WeatherApp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background="#ffffff")
        url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=029911faeb6e25f24aac26d011fba691&zip=110092,in'
        icon_base_url = 'http://openweathermap.org/img/w/'
        list_main = []
        list_list = []
        list2 = []
        self.i = 0
        response = urllib2.urlopen(url)
        json_obj = response.read().decode('utf-8')
        data = json.loads(json_obj)
        list_list = data['list']
        list2.append(list_list[0])
        self.list_weather = []
        self.list_temp = []
        self.list_dt = []
        self.list_humid = []
        self.list_dt_main = []
        self.list_icon_url = []
        list_months = ["January", "February", "March", "April", "May", "June", "July", "August", "sSeptember",
                       "October",
                       "November", "December"]
        date = datetime.datetime.date(datetime.datetime.now())
        date = str(date)
        self.list_dt.append(date)
        for item in list_list:
            if date not in item['dt_txt'] and str(item['dt_txt']).endswith('12:00:00'):
                date = item['dt_txt']
                dt, time = str(date).split(" ")
                self.list_dt.append(dt)
                list2.append(item)
        for item in self.list_dt:
            year, month, date = item.split('-')
            month = int(month)
            mon_t = list_months[month]
            self.list_dt_main.append(date + ' ' + mon_t)
        for item in list2:
            main_txt = item['main']
            weather = item['weather']
            weather1 = weather[0]
            url = weather1['icon']
            base_url = url + '.png'
            self.list_icon_url.append(base_url)
            self.list_weather.append(weather1['description'])
            temp = main_txt['temp'] - 273.15
            temp = int(temp)
            self.list_humid.append(main_txt['humidity'])
            self.list_temp.append(temp)
        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.button_close.config(image=self.img_close, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)
        self.label = tk.Label(self, font=('Helvetica', 15), background='#ffffff', foreground='#212121')
        self.label.place(x=2, y=2)
        self.image_file = self.list_icon_url[self.i]
        self.photo = tk.PhotoImage(file=self.image_file)
        self.button_image = tk.Button(self, background="#ffffff", highlightthickness=0, borderwidth=0)
        self.label2 = tk.Label(self, background='#ffffff', foreground='#212121', font=("Helvetica", 14))
        self.label2.place(x=160, y=70)
        self.label3 = tk.Label(self, background='#ffffff', foreground='#212121', font=("Helvetica", 14))
        self.label3.place(x=140, y=95)
        self.img_next = tk.PhotoImage(file="next.png")
        self.button_next = tk.Button(self, command=self.next_button)
        self.button_next.config(image=self.img_next, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
        self.button_next.place(x=280, y=200)
        self.label4 = tk.Label(self, background='#ffffff', foreground='#212121', font=("Helvetica", 14))
        self.label4.place(x=100, y=140)
        self.img_prev = tk.PhotoImage(file="prev.png")
        self.button_prev = tk.Button(self, command=self.prev_button)
        self.button_prev.config(image=self.img_prev, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
        self.button_prev.place(x=20, y=200)
        self.show_data()

    def next_button(self):
        if self.i == 4:
            self.i = 0
        else:
            self.i = self.i + 1

        self.show_data()

    def prev_button(self):
        if self.i == 0:
            self.i = 4
        else:
            self.i = self.i - 1
        self.show_data()

    def show_data(self):
        t = u"\u00b0"
        self.image_file = self.list_icon_url[self.i]
        self.photo.config(file=self.image_file)
        self.button_image.config(image=self.photo)
        self.button_image.place(x=50, y=65)
        self.label.config(text=self.list_dt_main[self.i])
        self.label2['text'] = str(self.list_temp[self.i]) + t + ' C'
        self.label3['text'] = str(self.list_weather[self.i]).title()
        self.label4['text'] = "Humidity : " + str(self.list_humid[self.i])


class MediaPlayer(tk.Frame):

    def next_button(self):
        if self.i == len(self.listofsongs) - 1:
            self.i = 0
        else:
            self.i = self.i + 1
        self.playasong()

    def prev_button(self):
        if self.i == 0:
            self.i = len(self.listofsongs) - 1
        else:
            self.i = self.i - 1
        self.playasong()

    def pause_button(self):
        if self.pause_status == 0:
            pygame.mixer.music.pause()

            self.button1.config(image=self.img_pause)
            self.pause_status = 1
        else:
            pygame.mixer.music.unpause()
            self.button1.config(image=self.img_play)
            self.pause_status = 0

    def playasong(self):
        pygame.mixer.init()
        self.l.config(text=self.name[self.i])
        self.l2.config(text=self.author[self.i])
        self.album_final = "Album : " + self.album[self.i]
        self.l3.config(text=self.album_final)
        pygame.mixer.music.load(self.listofsongs[self.i])
        pygame.mixer.music.play()

    def stop_button(self):
        if self.stop_status == 0:
            self.playasong()
            self.stop_status = 1
            self.button1.config(image=self.img_play)
        else:
            pygame.mixer.music.stop()
            self.i = 0
            self.l.config(text="Song Name")
            self.l2.config(text="Artist Name")
            self.l3.config(text="Album Name")
            self.button1.config(image=self.img_pause)
            self.stop_status = 0

    def __init__(self, parent, controller):
        self.i = 0

 
        self.stop_status = 0
        self.pause_status = 0
        tk.Frame.__init__(self, parent)
        self.listofsongs = []
        self.configure(background='#7B1FA2')
        self.f = tk.Frame(self, width=330, height=140, background="#7B1FA2")
        self.f.grid(row=0, column=0, sticky="NW")
        self.f.grid_propagate(0)
        self.l = tk.Label(self.f, text="Song Name", font=('Helvetica', 14), background="#7B1FA2", foreground="#ffffff")
        self.l.place(x=165, y=50, anchor="center")
        self.l2 = tk.Label(self.f, text="Artist Name", font=("Helvetica", 12), background="#7B1FA2", foreground="#ffffff")
        self.l2.place(x=165, y=90, anchor="center")
        self.l3 = tk.Label(self.f, text="Album Name", font=("Helvetica", 12), background="#7B1FA2", foreground="#ffffff")
        self.l3.place(x=165, y=120, anchor="center")
        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.button_close.config(image=self.img_close, background='#7B1FA2', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)
        self.img = tk.PhotoImage(file="previous-2.png")
        self.button = tk.Button(self, command=self.prev_button)
        self.button.config(image=self.img, background='#7B1FA2', borderwidth=0, highlightthickness=0)
        self.button.place(x=10, y=160)

        self.img_play = tk.PhotoImage(file="pause-2.png")
        self.img_pause = tk.PhotoImage(file="play-2.png")
        self.button1 = tk.Button(self, command=self.pause_button)
        self.button1.config(image=self.img_pause, background='#7B1FA2', borderwidth=0, highlightthickness=0)
        self.button1.place(x=90, y=160)

        self.img3 = tk.PhotoImage(file="stop-2.png")
        self.button2 = tk.Button(self, command=self.stop_button)
        self.button2.config(image=self.img3, background='#7B1FA2', borderwidth=0, highlightthickness=0)
        self.button2.place(x=170, y=160)

        self.img4 = tk.PhotoImage(file="skip-2.png")
        self.button3 = tk.Button(self, command=self.next_button)
        self.button3.config(image=self.img4, background='#7B1FA2', borderwidth=0, highlightthickness=0)
        self.button3.place(x=250, y=160)
        self.author = []
        self.name = []
        self.album = []
        for file in os.listdir():
            if str(file).endswith(".mp3"):
                self.listofsongs.append(file)
                self.realdir = os.path.realpath(file)
                self.audio = ID3(self.realdir)
                self.author.append(self.audio['TPE1'].text[0])
                self.name.append(self.audio['TIT2'].text[0])
                self.album.append(self.audio['TALB'].text[0])


class Alarm_App(tk.Frame):

    def thread_alarm(self):
        print("sleeping for " + str(self.total_seconds))
        time.sleep(self.total_seconds)
        self.show_window()

    def show_window(self):
        os.system('python on_alarm_time.py')
        print("Alarm Time")

    def set_alarm(self):
        self.label_msg.config(text="The Alarm is set for " + self.label_hr.cget('text') + ":" +
                                   self.label_min.cget('text'))
        time_1 = datetime.datetime.now()
        a, time_1 = str(time_1).split(' ')
        a, b, c = time_1.split(':')
        time_1 = a + ':' + b
        alarm_time = self.label_hr.cget('text') + ":" + self.label_min.cget('text')
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
        total_min = diff_time_hr * 60 + diff_time_min
        self.total_seconds = total_min * 60
        t = threading.Thread(target=self.thread_alarm)
        t.setDaemon(True)
        t.start()

    def plus_button(self, hr_min):
        if hr_min == 'hr':
            if int(self.set_hr) == 23:
                self.set_hr = str(int(0))
            else:
                self.set_hr = str(int(self.set_hr) + 1)
            self.label_hr.config(text=self.set_hr)
        elif hr_min == 'min':
            if int(self.set_min) == 59:
                self.set_min = str(int(0))
            else:
                self.set_min = str(int(self.set_min) + 1)
            self.label_min.config(text=self.set_min)

    def minus_button(self, hr_min):
        if hr_min == 'hr':
            if int(self.set_hr) == 0:
                self.set_hr = str(int(23))
            else:
                self.set_hr = str(int(self.set_hr) - 1)
            self.label_hr.config(text=self.set_hr)
        elif hr_min == 'min':
            if int(self.set_min) == 0:
                self.set_min = str(int(59))
            else:
                self.set_min = str(int(self.set_min) - 1)
            self.label_min.config(text=self.set_min)

    def __init__(self, parent, controller):
        self.cnt = controller
        tk.Frame.__init__(self, parent)
        x = datetime.datetime.time(datetime.datetime.now())
        self.set_hr, self.set_min, e = str(x).split(':')
        self.config(background="#424242")
        self.img_close = tk.PhotoImage(file="close.png")
        self.button_close = tk.Button(self, command=lambda: controller.show_frame(StartPage))
        self.button_close.config(image=self.img_close, background='#424242', borderwidth=0, highlightthickness=0, bd=0)
        self.button_close.place(x=280, y=2)
        self.label_hr = tk.Label(self, text=self.set_hr, width=3, background="#424242", foreground="#ffffff",
                                 font=("Helvetica", 16, "bold"))
        self.label_hr.place(x=70, y=70)
        self.button_plus_hr = tk.Button(self, text="+", width=3, background="#ffffff", foreground="#000000",
                                        highlightthickness=0, borderwidth=0, font=("Helvetica", 16, "bold"),
                                        command=lambda: self.plus_button('hr'))
        self.button_plus_hr.place(x=60, y=20)
        self.button_minus_hr = tk.Button(self, height=1, width=3, text="-", background="#ffffff", foreground="#000000",
                                         highlightthickness=0, borderwidth=0, font=("Helvetica", 16, "bold"),
                                         command=lambda: self.minus_button('hr'))
        self.button_minus_hr.place(x=60, y=110)
        self.label_colon = tk.Label(self, text=":", width=2, background="#424242", foreground="#ffffff",
                                    font=("Helvetica", 16, "bold"))
        self.label_colon.place(x=130, y=70)
        self.label_min = tk.Label(self, text=self.set_min, width=3,background='#424242', foreground="#ffffff",
                                  font=("Helvetica", 16, "bold"))
        self.label_min.place(x=180, y=70)
        self.button_plus_min = tk.Button(self, text="+", width=3, background="#ffffff", foreground="#000000",
                                         highlightthickness=0, borderwidth=0, font=("Helvetica", 16, "bold"),
                                         command=lambda: self.plus_button('min'))
        self.button_plus_min.place(x=170, y=20)
        self.button_minus_min = tk.Button(self, height=1, width=3, text="-", background="#ffffff", foreground="#000000",
                                          highlightthickness=0, borderwidth=0, font=("Helvetica", 16, "bold"),
                                          command=lambda: self.minus_button('min'))
        self.button_minus_min.place(x=170, y=110)

        self.img_set_alarm = tk.PhotoImage(file='button_set-alarm.png')
        self.button_set_alarm = tk.Button(self, image=self.img_set_alarm, background="#424242", highlightthickness=0,
                                          borderwidth=0, command=self.set_alarm)
        self.button_set_alarm.place(x=90, y=200)

        self.label_msg = tk.Label(self, font=("Helvetica", 13, "bold"), background="#424242",
                                  foreground="#ffffff")
        self.label_msg.place(x=40, y=160)


app = MyClass()
app.configure(background='#212121')
app.attributes('-fullscreen', True)
#app.config(cursor="none")
app.mainloop()

