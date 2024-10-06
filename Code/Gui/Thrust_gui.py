import time
import threading
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter import simpledialog
from serial_communicator import Serial_Communications
from serial_sniffer import serial_ports


sp=serial_ports()
print(sp)
running=False
expanded=False
currentDIR=os.getcwd()
armed=False
speed=0
Thrust_value=0


def connect_clicked():
    global running,c,Serial
    refreshSerialPorts()
    if running==True:
        print('stopped')
        connect.itemconfig(toggle_text,text='COM Stopped')
        running=False
        Serial.close()
    else :
        running = True
        print('started')
        connect.itemconfig(toggle_text,text='COM Started')
        try:
            COM=SerialPorts.get()
            Serial=Serial_Communications(COM,9600)
            SerialMonitor()
            pass
        except Exception as e:
            print('Error While Opening Serial Port')

def start_clicked():
    global armed
    global speed
    if armed:
        Send(f"{speed}") #Sent Values
        start.itemconfig(toggle_text,text='Push Motor Speed')
        start.itemconfig(startB,outline=green)
    else:
        start.itemconfig(toggle_text,text='Test Stopped')
        start.itemconfig(startB,outline=red)

def SerialMonitor():
    global expanded
    if expanded:
        expanded=False
        root.geometry("1280x720")
        root.after(0, root.update)
    else:
        expanded=True
        root.geometry("1280x905")
        root.after(0, root.update)
        serialThread=threading.Thread(target=SerialMonitorRefresh).start()

def SerialMonitorRefresh():
    global Serial
    while expanded:
        readings=Serial.read()
        if readings!="":
            Thrust_Change(readings)
            serial_monitor.insert(tk.END, readings+'\n')
            serial_monitor.see(tk.END)
            

        pass
def Send(a): # Send to Serial Port func
    global Serial
    Serial.send(a)
def Send_text(event=None): # Send to Serial Port from user input
    global b,Serial
    Serial.send(serial_sender.get()) #
    serial_sender.delete(0, tk.END)
def refreshSerialPorts(event=None): # checks if a serial port is connected or disconnected while running
    global sp
    sp=serial_ports()
    SerialPorts['values'] = (sp) 
def on_mouse_down(event):
  global lastx, lasty
  lastx = event.widget.winfo_pointerx()
  lasty = event.widget.winfo_pointery()
def on_mouse_move(event):
  global lastx, lasty
  deltax = event.widget.winfo_pointerx() - lastx
  deltay = event.widget.winfo_pointery() - lasty
  root.geometry("+%d+%d" % (root.winfo_x() + deltax, root.winfo_y() + deltay))
  lastx = event.widget.winfo_pointerx()
  lasty = event.widget.winfo_pointery()
def change_color(feature,new_color):
    #feature.itemconfig(f"{feature}B", outline=new_color)
    feature.itemconfig(connectB, outline=new_color)
def arm_clicked():
    global armed
    if not(armed):
        armed=True
        ##Change button color
        arm.itemconfig(toggle_text,text='Armed')
        arm.itemconfig(armB,outline=green)
    else:
        armed=False
        arm.itemconfig(toggle_text,text='Not Armed')
        arm.itemconfig(armB,outline=red)
def set_speed(value):
        global speed
        speed = value
        print(f"Selected Speed: {speed}")
        Label3.config(text=f"Motor Speed = {speed}%")
def open_speed_window():
    speed_window = tk.Toplevel()
    speed_window.title("Select Speed")
    # Create buttons for 25%, 50%, 75%, and 100%
    buttons = [("25%", 25), ("50%", 50), ("75%", 75), ("100%", 100)]
    for (text, value) in buttons:
        button = tk.Button(speed_window, text=text, command=lambda v=value: set_speed(v))
        button.pack(pady=5)
    # Entry for custom speed input
    custom_entry = tk.Entry(speed_window)
    custom_entry.pack(pady=5)
    def close_window():
        speed_window.destroy()  # Close the window

    def add_custom_speed():
        try:
            custom_value = float(custom_entry.get())
            set_speed(custom_value)
        except ValueError:
            print("Please enter a valid number")

    # Button to add custom speed
    add_button = tk.Button(speed_window, text="Add Custom Speed", command=add_custom_speed)
    add_button.pack(pady=5)
def Thrust_Change(t):
    Label2.config(text=f'Thrust= {t} N')


        
# GUI WINDOW
normal_color = "#5b3065" #border
hover_color = "#ba5da3"
press_color = "#fffaaa"
fill_color="#001122"
red="#ff0000"
green="#00ff00"
root=tk.Tk()
root.title("Controller")
root.geometry('1280x720+200+10')
root.resizable(False, False)
root.config(bg='#dddddd')

#root.iconbitmap(f"{currentDIR}/controller_assets/icon.ico")

#Connect button
connect = Canvas(root,width=320*0.75,height=75*0.75, bg="#dddddd",borderwidth=0,highlightthickness=0)
p1 = (10*0.75, 10*0.75)
p2=(10*0.75,35*0.75)
p3=(15*0.75,45*0.75)
p4=(15*0.75,70*0.75)
p5=(310*0.75,70*0.75)
p6=(310*0.75,25*0.75)
p7=(295*0.75,10*0.75)
connectB = connect.create_polygon(
p1,p2,p3,p4,p5,p6,p7,
outline=normal_color, width=3,
fill=fill_color
)
toggle_text=connect.create_text((160*0.75,40*0.75), text="Connect", font="Play 12 bold",fill="white")
connect.place(x=1025,y=620)
connect.bind("<Enter>", lambda event: change_color(connect,hover_color))
connect.bind("<Leave>", lambda event: change_color(connect,normal_color))
connect.bind("<Button-1>", lambda event: change_color(connect,press_color))
connect.bind("<ButtonRelease-1>", lambda event: connect_clicked())

#arm button
arm = Canvas(root,width=320*0.75,height=75*0.75, bg="#dddddd",borderwidth=0,highlightthickness=0)
p1 = (10*0.75, 10*0.75)
p2=(10*0.75,35*0.75)
p3=(15*0.75,45*0.75)
p4=(15*0.75,70*0.75)
p5=(310*0.75,70*0.75)
p6=(310*0.75,25*0.75)
p7=(295*0.75,10*0.75)
armB = arm.create_polygon(
p1,p2,p3,p4,p5,p6,p7,
outline=normal_color, width=3,
fill=fill_color
)
toggle_text=arm.create_text((160*0.75,40*0.75), text="Arm", font="Play 12 bold",fill="white")
arm.place(x=775,y=620)
arm.bind("<Button-1>", lambda event: change_color(arm,press_color))
arm.bind("<ButtonRelease-1>", lambda event: arm_clicked())

# Serial port picker
port_frame=tk.Frame(root,bg='#dddddd')
port_frame.pack()
port_frame.place(y=575,x=1045)
port_frame.bind("<Enter>",refreshSerialPorts)
serial_title=tk.Label(port_frame,font=('Play',14),fg='#001122',bg="#dddddd",text="Serial Port :")
serial_title.pack(side="left")
n = tk.StringVar() 
SerialPorts = ttk.Combobox(port_frame, width = 7, textvariable = n) 
SerialPorts['values'] = (sp) 
SerialPorts.pack(pady=15,padx=20,side=("right"))
SerialPorts.current() 

#Title
Label1=tk.Label(root,text='SSTL Thrust Test Platform',font="play 18 bold",fg="#001122", bg="#dddddd",highlightthickness=0)
Label1.pack()
Label1.place(x=40,y=40)
#Thrust
Label2=tk.Label(root,text=f'Thrust= {Thrust_value} N',font="play 48 bold",fg="#001122", bg="#dddddd",highlightthickness=0)
Label2.pack()
Label2.place(x=450,y=350)
#Motor Speed
Label3=tk.Label(root,text=f'Motor Speed= 0 %',font="play 48 bold",fg="#001122", bg="#dddddd",highlightthickness=0)
Label3.pack()
Label3.place(x=350,y=250)


# Serial monitor
sm_button = Canvas(root,width=320*0.75,height=75*0.75, bg="#dddddd",borderwidth=0,highlightthickness=0) #button
smB = sm_button.create_polygon(
p1,p2,p3,p4,p5,p6,p7,
outline=normal_color, width=2,
fill=fill_color
)
sm_button.create_text((160*0.75,40*0.75), text="Serial Monitor", font="Play 12 bold",fill="white")
sm_button.place(x=30,y=620)
sm_button.bind("<Enter>", lambda event: change_color(sm_button,hover_color))
sm_button.bind("<Leave>", lambda event: change_color(sm_button,normal_color))
sm_button.bind("<Button-1>", lambda event: change_color(sm_button,press_color))
sm_button.bind("<ButtonRelease-1>", lambda event: SerialMonitor())

serial_frame=Frame(width=1280,height=180)
serial_frame.place(y=720)

serial_monitor = scrolledtext.ScrolledText(serial_frame, 
                            width = 114,  
                            height = 7,  
                            font = ("Arial", 
                                    15)) 
serial_monitor.pack(padx=4)
serial_sender=tk.Entry(root,width=1280)
serial_sender.pack(side='bottom')
serial_sender.bind('<Return>',Send_text)


# Speed Controller
speed_controller = Canvas(root,width=320*0.75,height=75*0.75, bg="#dddddd",borderwidth=0,highlightthickness=0) #button
speedB = speed_controller.create_polygon(
p1,p2,p3,p4,p5,p6,p7,
outline=normal_color, width=2,
fill=fill_color
)
speed_controller.create_text((160*0.75,40*0.75), text="Speed Controller", font="Play 12 bold",fill="white")
speed_controller.place(x=530,y=620)
speed_controller.bind("<Enter>", lambda event: change_color(speed_controller,hover_color))
speed_controller.bind("<Leave>", lambda event: change_color(speed_controller,normal_color))
speed_controller.bind("<Button-1>", lambda event: change_color(speed_controller,press_color))
speed_controller.bind("<ButtonRelease-1>", lambda event: open_speed_window())


#start button
start = Canvas(root,width=320*0.75,height=75*0.75, bg="#dddddd",borderwidth=0,highlightthickness=0)
p1 = (10*0.75, 10*0.75)
p2=(10*0.75,35*0.75)
p3=(15*0.75,45*0.75)
p4=(15*0.75,70*0.75)
p5=(310*0.75,70*0.75)
p6=(310*0.75,25*0.75)
p7=(295*0.75,10*0.75)
startB = start.create_polygon(
p1,p2,p3,p4,p5,p6,p7,
outline=normal_color, width=3,
fill=fill_color
)
toggle_text=start.create_text((160*0.75,40*0.75), text="Push Motor Speed", font="Play 12 bold",fill="white")
start.place(x=280,y=620)
start.bind("<Enter>", lambda event: change_color(start,hover_color))
start.bind("<Leave>", lambda event: change_color(start,normal_color))
start.bind("<Button-1>", lambda event: change_color(start,press_color))
start.bind("<ButtonRelease-1>", lambda event: start_clicked())

root.mainloop()