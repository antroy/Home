from Tkinter import Tk
from Tkinter import Label
import socket

ip = socket.getaddrinfo(socket.gethostname(), None)[0][4][0]

root = Tk()

w = Label(root, text="Your IP Address is: ")
w.pack(padx=50)

w2 = Label(root, text=ip, foreground="red", font=("Times", 12, "bold"))
w2.pack(padx=50)

root.title("IP Address")

root.mainloop()


