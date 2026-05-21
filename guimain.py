import customtkinter as ctk
from PIL import Image
import pygame

# theme and app window ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.configure(fg_color="#0C151E")
app.geometry("747x490")
app.title("SimplyLovelyTimer")
# -------------------------------------

# assets -------------------------------
pygame.mixer.init()
engine_sound = pygame.mixer.Sound("engine.wav")

car_image = ctk.CTkImage(
    light_image=Image.open("f1car.png"),
    dark_image=Image.open("f1car.png"),
    size=(707,353)
)
# ---------------------------------------

# variables -----------------------------
study_time = 25 * 60
break_time = 5 * 60
sec = study_time
paused = False
running = False
session_type = "Study"
timer_id = None
car_x = 20
car_y = 190
button_frame_y = 150
# ---------------------------------------

# clock ---------------------------------
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
            title_label.configure(text="Focus Time")
        else:
            title_label.configure(text="Break Time")

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
# ----------------------------------------

#animation functions ---------------------
def animate_car():
    global car_x
    global running

    if car_x < 700:
        car_x = car_x + 7
        car_label.place(x=car_x,y=car_y)
        app.after(16, animate_car)
    else:
        car_label.place_forget()
        animate_buttons()
        

def animate_buttons():
    global running
    global button_frame_y

    if button_frame_y < 380:
        button_frame_y = button_frame_y + 5
        button_frame.place(relx=0.5,y=button_frame_y)
        app.after(16, animate_buttons)
    else:
        timer_label.place(
            relx=0.5,
            rely=0.2,
            anchor="n"
        )
        title_label.tkraise()
        title_label.configure(text="Focus Time", font=("SansSerifExbFLF", 100), text_color = "#CE2121")
        title_label.pack_configure(pady=(30,20))
        running= True
        timekeeper()
# -----------------------------------------

# button functions ------------------------
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
# -------------------------------------


# header -------------------------------
title_label = ctk.CTkLabel(
    app,
    text="SimplyLovelyTimer",
    font=("SansSerifBldFLF", 73),
    text_color="#FFFFFF"
)
title_label.pack(pady=(40,0))

car_label = ctk.CTkLabel(
    app,
    image=car_image,
    text=""
)
car_label.place(x=car_x,y=car_y)

timer_label = ctk.CTkLabel(
    app,
    text="25:00",
    text_color="#D4900D",
    font=("Exo 2 Black Italic", 206)
)
# ------------------------------------


# BUTTONS ------------------------------
button_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
    )
button_frame.place(
    relx=0.5,
    anchor="n",
    y=button_frame_y
    )

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

    width=100,
    height=60,
    font=("Iosevka Charon Mono", 30),
    text_color="#FFFFFF",

    fg_color="#891212",
    hover_color="#531B1B",
    corner_radius=30
)

stop_button = ctk.CTkButton(
    button_frame,
    text="✖",
    command=skip_timer,

    width=60,
    height=60,
    font=("Iosevka Charon Mono", 30),
    text_color="#FFFFFF",

    fg_color="#891212",
    hover_color="#531B1B",
    corner_radius=30
)
#-------------------------------------------

app.mainloop()