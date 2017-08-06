import requests
import tkinter as tk
from bs4 import BeautifulSoup
list_symbols = ['DISHTV', 'JPINFRATEC', 'BALRAMCHIN', 'DHAMPURSUG', 'NMDC', 'NTPC', 'SITINET', 'DCBBANK', 'HINDPETRO', 'KOTAKBANK']

base_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='
list_url = []
for i in range(len(list_symbols)):
    string = base_url + list_symbols[i]
    list_url.append(string)

raw_div = ''
dayHigh = []
lastPrice = []
dayLow = []
previousClose = []
todayOpen = []
up_down = []
lastUpdateTime = []
updateTime = 0
perChange = []

def calcValues(string):
    global raw_div, updateTime
    index_lastPrice = raw_div.find(string)
    print(string)
    print(index_lastPrice)
    if index_lastPrice == -1:
        return '0.0'
    raw_lastPrice = raw_div[index_lastPrice - 1:]
    j = 0
    while True:
        if raw_lastPrice[j] == ',':
            break
        else:
            j = j + 1

    raw2_lastPrice = raw_lastPrice[0:j]

    if updateTime == 1:
        a, b, c, d = raw2_lastPrice.split(':')
        b = b + ':' + c + ':' + d
    else:

        a, b = raw2_lastPrice.split(':')
    updateTime = 0
    fin = b[1:len(b)-1]
    return fin


def getValues(m):
    global raw_div, dayHigh, lastPrice, dayLow, updateTime
    r = requests.get(list_url[m])
    soup = BeautifulSoup(r.content, 'html.parser')
    for div in soup.find_all('div'):
        if div.get('id') == 'responseDiv':
            raw_div = str(div)
    dayHigh.append(calcValues('dayHigh'))
    lastPrice.append(calcValues('lastPrice'))
    dayLow.append(calcValues('dayLow'))
    previousClose.append(calcValues('previousClose'))
    todayOpen.append(calcValues('open'))
    updateTime = 1
    lastUpdateTime.append(calcValues('lastUpdateTime'))
    if float(lastPrice[m]) > float(previousClose[m]):
        up_down.append('up')
    else:
        up_down.append('down')
    perChange.append(calcValues('pChange'))

for m in range(len(list_url)):
    getValues(m)
print(list_symbols)
print(lastPrice)
print(previousClose)
print(dayHigh)
print(dayLow)
print(todayOpen)
print(up_down)
print(lastUpdateTime)
print(perChange)
main_i = 0


def next_button():
    global main_i
    if main_i == len(list_symbols) - 1:
        main_i = 0
    else:
        main_i = main_i + 1
    show_data()


def prev_button():
    global main_i
    if main_i == 0:
        main_i = len(list_symbols) - 1
    else:
        main_i = main_i - 1
    show_data()


def show_data():
    global main_i, label_name
    print(main_i)
    print(list_symbols[main_i])
    label_name.config(text=list_symbols[main_i])
    label_lastPrice.config(text=lastPrice[main_i])
    if up_down[main_i] == 'up':
        label_lastPrice.config(foreground='#388E3C')
        label_per_change.config(foreground='#388E3C')
        button_up_down.config(image=img_up)
    else:
        label_lastPrice.config(foreground='#E53935')
        label_per_change.config(foreground='#E53935')
        button_up_down.config(image=img_down)
    label_updateTime.config(text=lastUpdateTime[main_i])
    label_per_change.config(text='(' + perChange[main_i] + '%)')
    label_high.config(text=dayHigh[main_i])
    label_low.config(text=dayLow[main_i])
    label_open.config(text=todayOpen[main_i])

root = tk.Tk()
root.config(background='#ffffff')
root.attributes('-fullscreen', True)

img_prev = tk.PhotoImage(file="images/prev.png")
button_prev = tk.Button(root)
button_prev.config(image=img_prev, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0,
                   command=prev_button)
button_prev.place(x=20, y=200)
img_next = tk.PhotoImage(file="images/next.png")
button_next = tk.Button(root)
button_next.config(image=img_next, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0,
                   command=next_button)
button_next.place(x=280, y=200)

f = tk.Frame(root, width=330, height=140, background="#ffffff")
f.grid(row=0, column=0, sticky="NW")
f.grid_propagate(0)
label_name = tk.Label(f, font=('Helvetica', 14, 'bold'), background="#ffffff", foreground="#000000")
label_name.place(x=165, y=60, anchor="center")
label_lastPrice = tk.Label(f, font=("Helvetica", 12, 'bold'), background="#ffffff", foreground="#000000")
label_lastPrice.place(x=165, y=90, anchor="center")

label_per_change = tk.Label(f, text='(1.60%)', font=("Helvetica", 9, 'bold'), background="#ffffff", foreground="#000000")
label_per_change.place(x=165, y=110, anchor="center")

img_close = tk.PhotoImage(file="images/close.png")
button_close = tk.Button(root, command=quit)
button_close.config(image=img_close, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
button_close.place(x=280, y=2)

label_updateTime = tk.Label(root, font=('Helvetica', 9), background='#ffffff', foreground='#000000')
label_updateTime.place(x=10, y=5)

img_up = tk.PhotoImage(file='images/up_share_market.png')
img_down = tk.PhotoImage(file='images/down_share_market.png')
button_up_down = tk.Button(root, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
button_up_down.place(x=60, y=60)

label_head_high = tk.Label(root, text='High', background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_head_high.place(x=50, y=140)

label_head_low = tk.Label(root, text='Low', background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_head_low.place(x=140, y=140)

label_head_open = tk.Label(root, text='Open', background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_head_open.place(x=220, y=140)

label_high = tk.Label(root, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_high.place(x=50, y=160)

label_low = tk.Label(root, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_low.place(x=140, y=160)

label_open = tk.Label(root, background='#ffffff', foreground='#000000', font=('Helvetica', 10, 'bold'))
label_open.place(x=220, y=160)

show_data()
root.mainloop()
