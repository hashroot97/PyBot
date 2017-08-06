import subprocess
import tkinter as tk
import time


def func():

    string = 'C:\\Users\\Hash\\Desktop\\Project\\Heathens.mp3'
    print(string)
    proc = subprocess.Popen(['mpsyt', '/twenty one pilots', ', 1'],
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(60)
    proc.kill()

root = tk.Tk()
button = tk.Button(root, text='Next', command=func)
button.pack()
root.mainloop()
