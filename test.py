import tkinter as tk


file = open('abcd.txt', 'r')
display_msg = file.read()
root = tk.Tk()
root.attributes('-fullscreen', True)
root.config(background='#ffffff')
w = tk.Message(root, text=display_msg, width=240, background="#ffffff", foreground="#000000",
               font=('Helvetica', 16, 'bold'))
w.place(x=20, y=50)

img_close = tk.PhotoImage(file="close.png")
button_close = tk.Button(root, command=quit)
button_close.config(image=img_close, background='#ffffff', borderwidth=0, highlightthickness=0, bd=0)
button_close.place(x=280, y=2)

root.mainloop()
