import time
import tkinter as tk
from pyfirmata import Arduino, util


board = Arduino('')  


led_pin = board.get_pin('d:13:o')  


it = util.Iterator(board)
it.start()


root = tk.Tk()
root.title("LED Control")


status_label = tk.Label(root, text="LED OFF", font=('Helvetica', 16))
status_label.pack(pady=20)

def turn_on_led():
    led_pin.write(1)  
    status_label.config(text="LED ON")  
    print("LED ON")  

def turn_off_led():
    led_pin.write(0)  
    status_label.config(text="LED OFF")  
    print("LED OFF")  




root.mainloop()