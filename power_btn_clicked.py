import tkinter as tk

root = tk.Tk()
root.config(background="#424242")
root.attributes('-fullscreen', True)
img_power_off = tk.PhotoImage(file='button_power-off.png')
btn_power_off = tk.Button(image=img_power_off, highlightthickness=0, background="#424242", borderwidth=0,
                          command=root.quit)
btn_power_off.place(x=30, y=10)

img_reboot = tk.PhotoImage(file='button_reboot.png')
btn_reboot = tk.Button(image=img_reboot, highlightthickness=0, background="#424242", borderwidth=0,
                       command=root.quit)
btn_reboot.place(x=30, y=60)

img_exit = tk.PhotoImage(file='button_exit.png')
btn_exit = tk.Button(image=img_exit, highlightthickness=0, background="#424242", borderwidth=0,
                     command=root.quit)
btn_exit.place(x=30, y=110)

img_switch = tk.PhotoImage(file='button_switch-to-hdmi.png')
btn_switch = tk.Button(image=img_switch, highlightthickness=0, background="#424242", borderwidth=0,
                       command=root.quit)
btn_switch.place(x=30, y=160)
root.mainloop()
