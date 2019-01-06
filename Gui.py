import sys
import subprocess
import socket
import re

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    from tkinter.messagebox import showerror
    from tkinter.messagebox import showinfo
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk    
    py3 = True

import Gui_support
from Adb_Handler import Adb_Handler as AdbHandler
from Server import Server as server

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    Gui_support.set_Tk_var()
    top = App (root)
    Gui_support.init(root, top)
    root.mainloop()

w = None
def create_App(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    Gui_support.set_Tk_var()
    top = App (w)
    Gui_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_App():
    global w
    w.destroy()
    w = None

class App:
    def __init__(self, top=None):
        self.adbHandler = AdbHandler
        self.serverStarted = False
        self.root = top

        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#ececec' # Closest X11 color: 'gray92' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])

        top.geometry("453x444+721+167")
        top.title("ADB SMS")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.022, rely=0.023, height=24, width=54)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Device''')

        self.devicesSpinBox = tk.Spinbox(top, from_=1.0, to=100.0)
        self.devicesSpinBox.place(relx=0.243, rely=0.023, relheight=0.063, relwidth=0.651)
        self.devicesSpinBox.configure(activebackground="#f9f9f9")
        self.devicesSpinBox.configure(background="white")
        self.devicesSpinBox.configure(buttonbackground="#d9d9d9")
        self.devicesSpinBox.configure(selectbackground="#c4c4c4")
        self.devicesSpinBox.configure(textvariable=Gui_support.spinbox)
        self.value_list = self.adbHandler.getDeviceList(AdbHandler)
        self.devicesSpinBox.configure(values=self.value_list)
        self.devicesSpinBox.configure(width=295)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.022, rely=0.158, height=24, width=66)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Receiver''')

        self.receiverEntry = tk.Entry(top)
        self.receiverEntry.place(relx=0.243, rely=0.158, height=27, relwidth=0.667)
        self.receiverEntry.configure(background="white")
        self.receiverEntry.configure(font="TkFixedFont")
        self.receiverEntry.configure(foreground="#000000")
        self.receiverEntry.configure(insertbackground="black")
        self.receiverEntry.configure(width=302)

        self.msgText = tk.Text(top)
        self.msgText.place(relx=0.243, rely=0.248, relheight=0.252, relwidth=0.658)
        self.msgText.configure(background="white")
        self.msgText.configure(font="TkTextFont")
        self.msgText.configure(highlightcolor="#ffffff")
        self.msgText.configure(selectbackground="#c4c4c4")
        self.msgText.configure(width=298)
        self.msgText.configure(wrap='word')

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.022, rely=0.248, height=24, width=68)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Message''')

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.022, rely=0.608, relwidth=0.949)

        self.sendBtn = tk.Button(top, command = self.sendSms)
        self.sendBtn.place(relx=0.684, rely=0.518, height=22, width=81)
        self.sendBtn.configure(activebackground="#ececec")
        self.sendBtn.configure(activeforeground="#000000")
        self.sendBtn.configure(background="#d9d9d9")
        self.sendBtn.configure(foreground="#000000")
        self.sendBtn.configure(highlightbackground="#d9d9d9")
        self.sendBtn.configure(highlightcolor="black")
        self.sendBtn.configure(text='''Send''')
        self.sendBtn.configure(width=81)

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.044, rely=0.653, height=24, width=113)
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''http://''' + socket.gethostbyname(socket.getfqdn()) + ''':''')

        self.portEntry = tk.Entry(top)
        self.portEntry.place(relx=0.327, rely=0.653,height=27, relwidth=0.159)
        self.portEntry.configure(background="white")
        self.portEntry.configure(font="TkFixedFont")
        self.portEntry.configure(foreground="#000000")
        self.portEntry.configure(insertbackground="black")
        self.portEntry.configure(width=72)

        self.keyEntry = tk.Entry(top)
        self.keyEntry.place(relx=0.132, rely=0.766,height=27, relwidth=0.336)
        self.keyEntry.configure(background="white")
        self.keyEntry.configure(font="TkFixedFont")
        self.keyEntry.configure(foreground="#000000")
        self.keyEntry.configure(insertbackground="black")

        self.startBtn = tk.Button(top, command = self.startServer)
        self.startBtn.place(relx=0.066, rely=0.901, height=22, width=80)
        self.startBtn.configure(activebackground="#ececec")
        self.startBtn.configure(activeforeground="#000000")
        self.startBtn.configure(background="#d9d9d9")
        self.startBtn.configure(foreground="#000000")
        self.startBtn.configure(highlightbackground="#d9d9d9")
        self.startBtn.configure(highlightcolor="black")
        self.startBtn.configure(text='''Start''')
        self.startBtn.configure(width=80)

        self.stopBtn = tk.Button(top, command = self.stopServer)
        self.stopBtn.place(relx=0.287, rely=0.901, height=22, width=78)
        self.stopBtn.configure(activebackground="#ececec")
        self.stopBtn.configure(activeforeground="#000000")
        self.stopBtn.configure(background="#d9d9d9")
        self.stopBtn.configure(foreground="#000000")
        self.stopBtn.configure(highlightbackground="#d9d9d9")
        self.stopBtn.configure(highlightcolor="black")
        self.stopBtn.configure(text='''Stop''')
        self.stopBtn.configure(width=78)

        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.044, rely=0.766, height=24, width=34)
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Key''')

        self.Message1 = tk.Message(top)
        self.Message1.place(relx=0.508, rely=0.653, relheight=0.167, relwidth=0.424)
        self.Message1.configure(background="#d9d9d9")
        self.Message1.configure(foreground="#000000")
        self.Message1.configure(highlightbackground="#d9d9d9")
        self.Message1.configure(highlightcolor="black")
        self.Message1.configure(text='''Send POST Request with:\n    rec="<RECEIVER>"\n    msg="<MESSAGE>"\n    key="<KEY>"''')
        self.Message1.configure(width=192)

        self.TSeparator1_1 = ttk.Separator(top)
        self.TSeparator1_1.place(relx=0.397, rely=-0.068, relwidth=0.927)

        self.TSeparator1_2 = ttk.Separator(top)
        self.TSeparator1_2.place(relx=0.022, rely=0.113, relwidth=0.949)

        if not self.adbHandler.adbExists(AdbHandler):
            showerror('Error', 'Cannot run adb.\nMake sure PATH vars has been set!')
            exit()
        top.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.serverStarted:
            showerror('Error', 'Server still running! Stop it before closing the app.')
        else:
            self.root.destroy()

    def startServer(self):
        deviceId = self.devicesSpinBox.get()
        port = str(self.portEntry.get()) 
        key = str(self.keyEntry.get())

        if deviceId != '' and port != '' and key != '':
            host = socket.gethostbyname(socket.getfqdn())
            server.start(server, host, int(port), key, deviceId, True)
            self.serverStarted = True
            self.portEntry.config(state='disabled')
            self.keyEntry.config(state='disabled')
        else:
            showerror('Error', 'Port and key cannot be empty!\nEnter valid port number and a key.')

    def stopServer(self):
        if self.serverStarted:
            server.stop(server)
            self.serverStarted = False
            self.portEntry.config(state='normal')
            self.keyEntry.config(state='normal')


    def sendSms(self):
        receiver = str(self.receiverEntry.get())
        msg = str(self.msgText.get(1.0, 'end-1c'))
        deviceId = self.devicesSpinBox.get()        

        if receiver != '' and msg != '' and deviceId != '':
            if len(msg) > 160:
                showerror('Error', 'Message is longer than 160 chars!')
            else:
                rule = re.compile(r'(^\+[0-9]{1,3}[0-9]{10,11}$)')

                if rule.search(receiver):
                    self.adbHandler.sendSms(AdbHandler, deviceId, receiver, msg)
                    showinfo('Done', 'Request processed.')
                else:
                    showerror('Error', 'Receiver number is invalid!\nUse a valid number (ex. +12345678900).')
            