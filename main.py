import os
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
import socket
from urllib import request
from re import findall as find
from threading import Thread as thread

#PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#PROJECT_UI = os.path.join(PROJECT_PATH, "newproject")

class whoami:

    workLock = False

    def __init__(self, master=None):
        # build ui
        self.mainframe = ttk.Frame(master)

        self.hostname_disp = tk.Text(self.mainframe)
        self.hostname_disp.configure(height='1', width='21')
        _text_ = '''Loading...'''
        self.hostname_disp.insert('0.0', _text_)
        self.hostname_disp.place(anchor='nw', relx='0.37', rely='0.06', x='0', y='0')

        self.nameLab = ttk.Label(self.mainframe)
        self.nameLab.configure(text='Device Name:')
        self.nameLab.place(anchor='nw', rely='0.089', x='0', y='0')

        self.myIPLab = ttk.Label(self.mainframe)
        self.myIPLab.configure(text='LAN IP:')
        self.myIPLab.place(anchor='nw', rely='0.29', x='0', y='0')

        self.curIP = tk.Text(self.mainframe)
        self.curIP.configure(height='1', width='21')
        _text_ = '''Loading...'''
        self.curIP.insert('0.0', _text_)
        self.curIP.place(anchor='nw', relx='0.37', rely='0.29', x='0', y='0')

        self.visIPLab = ttk.Label(self.mainframe)
        self.visIPLab.configure(text='Public IP:')
        self.visIPLab.place(anchor='nw', rely='0.49', x='0', y='0')
        self.visIP = tk.Text(self.mainframe)
        self.visIP.configure(height='1', width='21')
        _text_ = '''Loading...'''
        self.visIP.insert('0.0', _text_)
        self.visIP.place(anchor='nw', relx='.37', rely='0.49', x='0', y='0')

        self.refresh_button = ttk.Button(self.mainframe)
        self.refresh_button.configure(text='Refresh')
        self.refresh_button.place(anchor='nw', relx='0.01', rely='0.75', x='0', y='0')
        self.refresh_button.configure(command=self.startRef)

        self.mainframe.configure(borderwidth='2', height='120', padding='2', relief='sunken')
        self.mainframe.configure(width='300')
        self.mainframe.pack(side='top')

        # Main widget
        self.mainwindow = self.mainframe

        # Run startup
        self.startRef()
    

    def startRef(self):
        refresh = thread(target=self.refreshIP)
        refresh.start()

    def refreshIP(self):
            
            # Obtain workLock
            if not self.workLock:
                self.workLock = True
            
            else:
                return

            # Get data
            hostName = socket.gethostname()  # Determine what the device is called
            hostIP = socket.gethostbyname(hostName)  # Determine the device's IP address

            html = request.urlopen('https://check.torproject.org/?lang=en_US').read().decode('utf-8')  # Ask torproject to check ip
            visIP = find('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', string=html)  # Find IP in webpage

            # Display data
            textBoxes = [self.hostname_disp, self.curIP, self.visIP]
            sections = [hostName, hostIP, str(visIP[0])]                      

            pos = 0
            for box in textBoxes:
                box.config(state='normal')
                box.delete('1.0', 'end')
                box.insert('0.0', sections[pos])
                box.config(state='disabled')
                pos += 1
                    

            self.workLock = False  # Open up workLock

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(height=False, width=False)  # Prohibit resizing the height or width of window
    root.wm_title("Who Am I?")  # Sets the title of the window to the string included as an argument
    app = whoami(root)
    app.run()


