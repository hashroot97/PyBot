import tkinter as tk

list_names = ['Red FM', 'Radio City', 'ABC News', 'Radio City (Int.)']
list_url = ['http://sc-bb.1.fm:8017/', 'http://prclive1.listenon.in:9998/',
            'http://www.abc.net.au/res/streaming/audio/mp3/news_radio.pls',
            'http://prc.streamguys1.com/secure-radiocity-international.mp3']
list_image = ['red_fm_radio.png', 'radio_city_radio.png', 'abc_news_radio.png', 'radio_city_inter_radio.png']
i = 0


def play_button():
    pass


def next_button():
    global i, img_image, button_image

    if i == len(list_names) - 1:
        i = 0
    else:
        i = i + 1
    label_name.config(text=list_names[i])
    img_image.config(file=list_image[i])
    button_image.config(image=img_image)


def prev_button():
    global i, img_image, button_image
    if i == 0:
        i = len(list_names) - 1
    else:
        i = i - 1
    label_name.config(text=list_names[i])
    img_image.config(file=list_image[i])
    button_image.config(image=img_image)


root = tk.Tk()
root.config(background='#000000')

label_name = tk.Label(root, foreground='#E57373', font=('Helvetica', 14), background='#000000')
label_name.config(text=list_names[i])
label_name.place(x=110, y=120)
img_close = tk.PhotoImage(file="close.png")
button_close = tk.Button(root, command=root.quit)
button_close.config(image=img_close, background='#000000', borderwidth=0, highlightthickness=0, bd=0)
button_close.place(x=280, y=2)
root.attributes('-fullscreen', True)

img_prev = tk.PhotoImage(file='radio_prev.png')
button_prev = tk.Button(root, image=img_prev, background="#000000", highlightthickness=0, borderwidth=0, bd=0,
                        command=prev_button)
button_prev.place(x=40, y=170)

img_next = tk.PhotoImage(file='radio_next.png')
button_next = tk.Button(root, image=img_next, background="#000000", highlightthickness=0, borderwidth=0, bd=0
                        , command=next_button)
button_next.place(x=220, y=170)

img_stop = tk.PhotoImage(file='radio_play.png')
button_stop = tk.Button(root, image=img_stop, background="#000000", highlightthickness=0, borderwidth=0, bd=0)
button_stop.place(x=135, y=170)

img_image = tk.PhotoImage(file=list_image[i])
button_image = tk.Button(root, image=img_image, background="#000000", highlightthickness=0, borderwidth=0, bd=0)
button_image.place(x=125, y=30)
root.mainloop()
