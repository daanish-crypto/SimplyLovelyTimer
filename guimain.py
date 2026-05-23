import customtkinter as ctk
from tkinter import Spinbox, filedialog
from PIL import Image
import pygame
import shutil
import os
import timer_config

# theme and app window ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.configure(fg_color="#0C151E")
app.geometry("850x460")
app.title("SimplyLovelyTimer")
# -------------------------------------

# assets -------------------------------
pygame.mixer.init()
engine_sound = pygame.mixer.Sound("assets/engine.wav")

car_image = ctk.CTkImage(
    light_image=Image.open("assets/f1car.png"),
    dark_image=Image.open("assets/f1car.png"),
    size=(707,353)
)
# ---------------------------------------

# variables -----------------------------
study_time = timer_config.study_time * 60
break_time = timer_config.break_time * 60
sec = study_time
paused = False
running = False
session_type = "Study"
timer_id = None
car_x = 20
car_y = 160
button_frame_y = 140
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

    if car_x < 850:
        car_x = car_x + 7
        car_label.place(x=car_x,y=car_y)
        app.after(16, animate_car)
    else:
        car_label.place_forget()
        animate_buttons() 

def animate_buttons():
    global running
    global button_frame_y

    if button_frame_y < 340:
        button_frame_y = button_frame_y + 5
        button_frame.place(relx=0.5,y=button_frame_y)
        app.after(16, animate_buttons)
    else:
        timer_label.place(
            relx=0.5,
            rely=0.13,
            anchor="n"
        )
        title_label.tkraise()
        title_label.configure(text="Focus Time", font=("SansSerifExbFLF", 100), text_color = "#891212")
        title_label.pack_configure(pady=(20,20))
        running= True
        timekeeper()
# -----------------------------------------

# button functions ------------------------
def start_timer():
    global running

    if not running:
        
        start_button.pack_forget()

        pause_button.pack(side="left",padx=10, pady=10)
        stop_button.pack(side="left", padx=10, pady=10)
        music_button.pack(side="left",padx=10, pady=10)
        settings_button.pack(side="left", padx=10,pady=10)

        engine_sound.play()
        app.after(700, animate_car)

def pause_timer():
    global paused
    global timer_id

    paused = not paused

    if paused:
        pause_button.configure(text="Continue")
        if timer_id != None:
            app.after_cancel(timer_id)

    else:
        pause_button.configure(text="Pause")
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

# music --------------------------------
music_folder = "music"
music_list = os.listdir(music_folder)

current_song = 0
music_paused = False
music_started = False

def load_song():
    global song_length
    song_path = f"{music_folder}/{music_list[current_song]}"
    pygame.mixer.music.load(song_path)
    song_name = music_list[current_song].replace(".mp3", "")

    song_length = pygame.mixer.Sound(song_path).get_length()

    music_title.configure(
        text=song_name,
        font=("SansSerifBldFLF", 24)
    )

def toggle_music():
    global music_started
    global music_paused

    song_name = music_list[current_song].replace(".mp3", "")
    
    if not music_started:
        load_song()
        pygame.mixer.music.play()
        music_started = True

        music_play_button.configure(
            text="⏸"
        )
    elif music_paused:
        pygame.mixer.music.unpause()
        music_paused = False

        music_play_button.configure(
            text="⏸"
        )
        music_title.configure(
        text=song_name,
        font=("SansSerifBldFLF", 24)
    )
    else:
        pygame.mixer.music.pause()
        music_paused = True

        music_play_button.configure(
            text="▶"
        )
        music_title.configure(
        text=song_name,
        font=("SansSerifBldFLF", 24)
    )

def next_song():
    global current_song
    global music_paused

    current_song = current_song + 1

    if current_song >= len(music_list):
        current_song = 0

    load_song()

    pygame.mixer.music.play()
    music_paused = False

    music_play_button.configure(
        text="⏸"
    )

def previous_song():
    global current_song
    global music_paused

    current_song = current_song - 1

    if current_song < 0:
        current_song = len(music_list) - 1
    
    load_song()
    pygame.mixer.music.play()
    music_paused = False

    music_play_button.configure(
        text="⏸"
    )
# --------------------------------------
# menus --------------------------------
def open_music_menu():
    global music_title
    global music_list
    global music_play_button
    global music_bar

    music_list = os.listdir(music_folder)

    music_window = ctk.CTkToplevel(app)
    music_window.geometry("400x180")
    music_window.title("Music")
    music_window.configure(
        fg_color = "#0C151E"
    )
    music_window.attributes("-topmost", True)

    music_title = ctk.CTkLabel(
        music_window,
        text="Music",
        font=("SansSerifBldFLF", 40),
        text_color="#891212"
    )
    music_title.pack(pady=10)
    music_bar = ctk.CTkProgressBar(
        music_window,
        orientation="horizontal",
        corner_radius=15,
        width=300,
        height=10,
        progress_color="#891212",
        fg_color="#2A2A2A"
    )
    music_bar.pack(pady=10)

    controls_frame = ctk.CTkFrame(
        music_window,

        fg_color="transparent"
    )

    controls_frame.pack(pady=10)

    music_rewind_button = ctk.CTkButton(
        controls_frame,
        text="⏮",
        width=50,
        height=50,
        font=("Iosevka Charon Mono", 28),
        text_color="#891212",
        fg_color="transparent",
        hover_color="#1A1A1A",
        border_width=1,
        border_color="#891212",
        corner_radius=25,
        command=previous_song

    )
    music_rewind_button.pack(padx=10, side="left")

    music_play_button = ctk.CTkButton(
        controls_frame,
        text="▶",
        width=50,
        height=50,
        font=("Iosevka Charon Mono", 28),
        text_color="#891212",
        fg_color="transparent",
        hover_color="#1A1A1A",
        border_width=1,
        border_color="#891212",
        corner_radius=25,
        command=toggle_music
    )
    music_play_button.pack(padx=10, side="left")

    music_skip_button = ctk.CTkButton(
        controls_frame,
        text="⏭",
        width=50,
        height=50,
        font=("Iosevka Charon Mono", 28),
        text_color="#891212",
        fg_color="transparent",
        hover_color="#1A1A1A",
        border_width=1,
        border_color="#891212",
        corner_radius=25,
        command=next_song
    )
    music_skip_button.pack(padx=10, side="left")

    update_music_bar()

    def close_music_window():
        pygame.mixer.music.pause()
        music_window.destroy()
    
    music_window.protocol(
        "WM_DELETE_WINDOW",
        close_music_window
    )

def update_music_bar():
    if pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000

        progress = current_pos  /song_length
        music_bar.set(progress)

    app.after(500, update_music_bar)

def open_settings_menu():
    global study_spinbox
    global break_spinbox

    settings_window = ctk.CTkToplevel(app)
    settings_window.geometry("400x300")
    settings_window.title("Settings")
    settings_window.configure(
        fg_color = "#0C151E"
    )
    settings_title = ctk.CTkLabel(
        settings_window,
        text="Settings",
        font=("SansSerifBldFLF", 40),
        text_color="#891212"
    )
    settings_title.pack(pady=(20, 10))
    settings_window.attributes("-topmost", True)

    tabs = ctk.CTkTabview(
        settings_window,
        fg_color="#152432",
        text_color="#0C151E",
        segmented_button_fg_color="#152432",
        segmented_button_unselected_color="#A36F10",
        segmented_button_unselected_hover_color="#94650F",
        segmented_button_selected_color="#891212",
        segmented_button_selected_hover_color="#7E1212",
    )
    tabs._segmented_button.configure(
        font=("SansSerifBldFLF", 20)
    )
    tabs.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=(0, 20)
    )
    tabs.add("Timer")
    tabs.add("Music") 
    timer_tab = tabs.tab("Timer")
    music_tab = tabs.tab("Music")

    study_spinbox = Spinbox(
        timer_tab,
        from_=1,
        to=120,
        width=4,
        font=("SansSerifBldFLF", 24),
        bg="#151515",
        fg="#D4900D",
        buttonbackground='#0C151E',
        command=update_config
    )  
    study_spinbox.delete(0, "end")
    study_spinbox.insert(0, study_time//60)
    study_spinbox.place(
        relx = 0.3,
        rely = 0.3,
        anchor="center",
        )

    break_spinbox = Spinbox(
        timer_tab,
        from_=1,
        to=24,
        width=4,
        font=("SansSerifBldFLF", 24),
        bg="#151515",
        fg="#D4900D",
        buttonbackground='#0C151E',
        command=update_config
    )  
    break_spinbox.delete(0, "end")
    break_spinbox.insert(0, break_time//60)
    break_spinbox.place(
        relx = 0.7,
        rely = 0.3,
        anchor="center"
    )

    study_spinbox_label = ctk.CTkLabel(
        timer_tab,
        text="Study Time\nAmount",
        text_color="#891212",
        font=("SansSerifBldFLF", 24)
    )
    study_spinbox_label.place(
        relx = 0.3,
        rely = 0.7,
        anchor="center"
    )
    break_spinbox_label = ctk.CTkLabel(
        timer_tab,
        text="Break Time\nAmount",
        text_color="#891212",
        font=("SansSerifBldFLF", 24)
    )
    break_spinbox_label.place(
        relx = 0.7,
        rely = 0.7,
        anchor="center"
    )

    upload_button = ctk.CTkButton(
        music_tab,
        text="⭱ Upload Song",
        command=upload_song,
        text_color="#891212",
        fg_color="transparent",
        #hover_color="#531B1B",
        font=("SansSerifBldFLF", 28),
        width=250,
        height=50,
        corner_radius=15,
        border_color="#891212",
        border_width=2
    )
    upload_button.pack(pady=(10,10))

    open_music_button = ctk.CTkButton(
        music_tab,
        text="🖿 Open Music",
        command=open_music_folder,
        text_color="#891212",
        fg_color="transparent",
        #hover_color="#531B1B",
        font=("SansSerifBldFLF", 28),
        width=250,
        height=50,
        corner_radius=15,
        border_color="#891212",
        border_width=2
    )
    open_music_button.pack(pady=(10,10))

def open_music_folder():

    os.startfile("music")

def update_config():
    study_value = int(study_spinbox.get())
    break_value = int(break_spinbox.get())

    with open("timer_config.py", "w") as file:
        file.write(
            f"study_time = {study_value}\n"
            f"break_time = {break_value}"
        )

def upload_song():
    global music_list
    file_path = filedialog.askopenfilename(
        title="Select Song",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav *.ogg")
        ]
    )
    if file_path:
        song_name = os.path.basename(file_path)
        destination = os.path.join(
            "music",
            song_name
        )
        shutil.copy(file_path,destination)
    
    music_list = os.listdir(music_folder)
    
# header -------------------------------
title_label = ctk.CTkLabel(
    app,
    text="SimplyLovelyTimer",
    font=("SansSerifBldFLF", 83),
    text_color="#FFFFFF"
)
title_label.pack(pady=(20,0))

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
    text="Pause",
    command=pause_timer,

    font=("SansSerifBldFLF", 24),
    text_color="#891212",

    width=30,
    height= 80,
    
    border_width=2,
    border_color="#891212",
    corner_radius=30,

    fg_color="transparent",
    #fg_color="#891212",
    #hover_color="#531B1B",
)

stop_button = ctk.CTkButton(
    button_frame,
    text="Stop",
    command=skip_timer,

    font=("SansSerifBldFLF", 24),
    text_color="#891212",

    width=30,
    height= 80,

    border_width=2,
    border_color="#891212",

    fg_color="transparent",
    #fg_color="#891212",
    #hover_color="#531B1B",
    corner_radius=30
)

music_button = ctk.CTkButton(
    button_frame,
    text="Music",
    command=open_music_menu,

    font=("SansSerifBldFLF", 24),
    text_color="#891212",

    width=30,
    height= 80,

    border_width=2,
    border_color="#891212",

    fg_color="transparent",
    #fg_color="#891212",
    #hover_color="#531B1B",
    corner_radius=30
)

settings_button = ctk.CTkButton(
    button_frame,
    text="Settings",
    command=open_settings_menu,

    font=("SansSerifBldFLF", 24),
    text_color="#891212",

    width=30,
    height= 80,

    border_width=2,
    border_color="#891212",

    fg_color="transparent",
    #fg_color="#891212",
    #hover_color="#531B1B",
    corner_radius=30
)
#-------------------------------------------

app.mainloop()