import time
import msvcrt

#intro message
print("Welcome to the SimplyLovelyTimer, a pomodoro style timer for studying, with an f1 theme!")

#take input for time settings
stime = int(input("How many minutes you would like to study in each cycle (25):"))
breaktime = int(input("How many minutes you would rest in each cycle (5):"))

# a countdown function
def timekeeper(mins, type):
    #add seconds variable tp show in countdown
    sec = mins * 60

    #set ts to True if you want to manually start study times
    paused = False

    while sec != 0:
        clockmin = sec // 60
        clocksec = sec % 60

        #checks for keypress, if any
        if msvcrt.kbhit():
            keypress = msvcrt.getch().decode("utf-8").lower()

            if keypress == "p":
                paused = not paused #toggle switch for pause
                if paused:
                    print("\nTimer has been paused")
                if not paused:
                    print("Timer has been unpaused")

        #timer display and crystal timekeeping module (jk on the second part (or am i))
        if not paused:
            timer = f"{clockmin:02d}:{clocksec:02d}"
            print(f"\r{type} time : {timer}", end="")

            time.sleep(1)
            sec = sec - 1
    
    #timer end message
    print(f"\n{type} timer over!")

while True:
    # countdown for STUDY
    timekeeper(stime, "Study")

    # manually start break time so that time for wrapping up study or to finish smthn is not counted (common feature in pomodor timers)
    startbreak = input("Would you like to start break? (PRESS ENTER TO START)")

    #countdown for BREAK
    timekeeper(breaktime, "Break")

    #pretty self explanatory, starts another study-break session for more sdtudying/working
    repeat_cycle = input("Want to start another session? (y/n)")
    if repeat_cycle != "y":
        break

# a fun little (motivational?) message for after the last study sesh (idk I js like the word "twin")
print("thanks for locking in with us twin")