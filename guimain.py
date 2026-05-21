import customtkinter as ctk
from PIL import Image
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.configure(fg_color="#0C151E")

app.geometry("747x420")
app.title("SimplyLovelyTimer")

pygame.mixer.init()
engine_sound = pygame.mixer.Sound("engine.wav")

car_image = ctk.CTkImage(
    light_image=Image.open("f1car.png"),
    dark_image=Image.open("f1car.png"),
    size=(707,353)
)

study_time = 25 * 60
break_time = 5 * 60
sec = study_time
paused = False
running = False
session_type = "Study"
timer_id = None
car_x = 20

def timekeeper():
    global sec
    global session_type
    global timer_id

    if running and not paused:
        clockmin = sec // 60
        clocksec = sec % 60

        timer = f"{clockmin:02d}:{clocksec:02d}"
        timer_label.configure(
            text = timer
        )

        if session_type == "Study":
            title_label.configure(text="Focus Time", font=("Exo 2 Bold Italic", 42))
        else:
            title_label.configure(text="Break Time", font=("Exo 2 Bold Italic", 42))

        if sec > 0:
            sec = sec - 1
            timer_id = app.after(1000, timekeeper)
        else:

            if session_type == "Study":
                session_type = "Break"
                sec = break_time
            else:
                session_type = "Study"
                sec = study_time
            timekeeper()

def animate_car():
    global car_x
    global running

    if car_x < 700:
        car_x = car_x + 7
        car_label.place(x=car_x,y=120)
        app.after(16, animate_car)
    else:
        car_label.place_forget()

        timer_label.pack(pady=(0, 20))
        title_label.configure(text="Focus Time", font=("Exo 2 Bold Italic", 32))
        running= True
        timekeeper()

def start_timer():
    global running

    if not running:
        
        start_button.pack_forget()

        pause_button.pack(side="left",padx=10, pady=10)
        stop_button.pack(side="right", padx=10,pady=10)

        engine_sound.play()
        app.after(700, animate_car)

def pause_timer():
    global paused
    global timer_id

    paused = not paused

    if paused:
        pause_button.configure(text="▶")
        if timer_id != None:
            app.after_cancel(timer_id)

    else:
        pause_button.configure(text="⏸")
        timekeeper()

def skip_timer():
    global sec
    global session_type
    global timer_id

    if timer_id != None:
        app.after_cancel(timer_id)
    if session_type == "Study":
        session_type = "Break"
        sec = break_time
    else:
        session_type = "Study"
        sec = study_time
    timekeeper()

header_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header_frame.pack(pady=(45, 0))

title_label = ctk.CTkLabel(
    header_frame,
    text="SimplyLovelyTimer",
    font=("Exo 2 Bold Italic", 36),
    text_color="#ffffff"
)
title_label.pack(pady=(0))
'''
session_label = ctk.CTkLabel(
    app,
    text="Focus Time",

    text_color="#8B5CF6",

    font=("Segoe UI", 15, "bold")
)

session_label.pack()
'''

car_label = ctk.CTkLabel(
    app,
    image=car_image,
    text=""
)
car_label.place(x=car_x,y=120)

timer_label = ctk.CTkLabel(
    header_frame,
    text="25:00",
    text_color="#FFFFFF",
    font=("Exo 2 Black Italic", 116)
)

button_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
    )
button_frame.pack(pady=10)

start_button = ctk.CTkButton(
    button_frame,
    text="Start",
    command=start_timer,

    width=140,
    height=60,
    font=("Orbitron", 32, "bold"),

    fg_color="#891212",
    hover_color="#531B1B",
    corner_radius=15
)
start_button.pack(pady=10)

pause_button = ctk.CTkButton(
    button_frame,
    text="⏸",
    command=pause_timer,

    width=40,
    height=60,
    font=("Iosevka Charon Mono", 30),
    text_color="#FFFFFF",

    fg_color="#891212",
    hover_color="#531B1B",
    corner_radius=15
)

stop_button = ctk.CTkButton(
    button_frame,
    text="⏹",
    command=skip_timer,

    width=40,
    height=60,
    font=("Iosevka Charon Mono", 30),
    text_color="#FFFFFF",

    fg_color="#891212",
    hover_color="#531B1B",
    corner_radius=15
)

app.mainloop()