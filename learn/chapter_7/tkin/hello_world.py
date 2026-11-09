import time
import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title('Hello World app')
window.geometry('400x300')

def hello_world():
    time.sleep(5)
    print('Hello World app')

hello_button = ttk.Button(window, text='Say Hello', command=hello_world)
hello_button.pack()

window.mainloop()