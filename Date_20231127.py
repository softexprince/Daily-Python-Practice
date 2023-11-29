from tkinter import *
from tkinter.ttk import *
from time import strftime
import time

def time(timelabel):
    current_time = strftime('%H:%m:%S %p')
    timelabel.config(text=current_time)
    root.after(1000, time)
    
def date(datelabel):
    current_date = strftime('%d/%M/%Y')
    datelabel.config(text=current_date)
    root.after(10000, time)


root = Tk()
root.title('Clock')

# Styling the label widget to make it look like a button
datelabel = Label(root, font=('calibri', 20, 'bold'),
                  background='purple',
                  foreground='white')
datelabel.grid(row=0, column=0, padx=10, pady=10)# Adjust padx and pady as needed
timelabel = Label(root, font=('calibri', 20, 'bold'),
                  background='purple',
                  foreground='white')
timelabel.grid(row=0, column=5, padx=10, pady=10)

time(timelabel)
date(datelabel)
root.mainloop()
