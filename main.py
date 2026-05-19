import time
import msvcrt

print("Welcome to the SimplyLovelyTimer, a pomodoro style timer for studying, with an f1 theme!")

stime = int(input("Set how many minutes you would like to study in each cycle (Default=25):"))
breaktime = int(input("Set how many minutes you would rest in each cycle (Default=5):"))

def timekeeper(mins, type):
    sec = mins * 60
    paused = False

    while sec != 0:
        clockmin = sec // 60
        clocksec = sec % 60

        if msvcrt.kbhit():
            keypress = msvcrt.getch().decode("utf-8").lower()

            if keypress == "p":
                paused = not paused #toggle switch for pause
                if paused:
                    print("\npaused")
                if not paused:
                    print("unpaused")

        if not paused:
            timer = f"{clockmin:02d}:{clocksec:02d}"
            print(f"\r{type} time : {timer}", end="")

            time.sleep(1)
            sec = sec - 1
    
    print(f"\n{type} timer over!")

while True:
    timekeeper(stime, "Study")

    startbreak = input("Would you like to start break? (PRESS ENTER TO START)")

    timekeeper(breaktime, "Break")

    repeat_cycle = input("Want to start another session? (y/n)")

    if repeat_cycle != "y":
        break

print("thanks for locking in with us twin")