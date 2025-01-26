import customtkinter as ctk
import pyautogui
import json
import CTkMessagebox as ctkmsg
import os
import keyboard


pallete = {
    "1": "#22223B",
    "2": "#4A4E69",
    "3": "#9A8C98",
    "4": "#C9ADA7",
    "5": "#F2E9E4"
}

window = ctk.CTk()
window.geometry("600x600")
window.title("MS Rewards Grinder V2")
window.resizable(True, True)   
window.iconbitmap("v2.ico")

root = ctk.CTkScrollableFrame(window, fg_color=pallete["5"])
root.pack(expand=True, fill="both")

config = {}

with open("config.json", "r") as file: 
    config = json.load(file)

startTextVariable = ctk.StringVar(value=config["Start"])
loadTextVariable = ctk.StringVar(value=config["Load"])
searchesTextVariable = ctk.StringVar(value=config["Searches"])
customStartPointVariable = ctk.StringVar(value="0")

state = "idle" #idle, countingDown, Searching

searchesDone = 0

def on_closing(): 
    
    with open ("config.json", "w") as file:
        config["Start"] = startTextVariable.get()
        config["Load"] = loadTextVariable.get()
        config["Searches"] = searchesTextVariable.get()
        
        json.dump(config, file, indent=4)

    window.destroy()

def validate_input(value):
    # Allow only digits and empty string
    return value.isdigit() or value == ""

validate_cmd = window.register(validate_input)

startButton = ctk.CTkButton(root,
                            text="START",
                            font=("Impact", 64),
                            width=450, bg_color=pallete["5"],
                            fg_color=pallete["2"],
                            corner_radius=20,
                            hover_color=pallete["1"],
                            )


timeToLoadSiteInput = ctk.CTkEntry(root,
                                   font=("Impact", 30),
                                   width=370,
                                   height=100,
                                   bg_color=pallete["5"],
                                   fg_color=pallete["2"],
                                   corner_radius=10,
                                   justify="center",
                                   validate="key",
                                   validatecommand=(validate_cmd, "%P"),
                                   textvariable=loadTextVariable
                                   )

timeToLoadSiteLabel = ctk.CTkLabel(root,
                                   font=("Impact", 30),
                                   text="Time to load site (in seconds):",
                                   text_color=pallete["1"],
                                   )

timeToWaitBeforeStart = ctk.CTkEntry(root,
                                    font=("Impact", 30),
                                    width=370,
                                    height=100,
                                    bg_color=pallete["5"],
                                    fg_color=pallete["2"],
                                    corner_radius=10,
                                    justify="center",
                                    validate="key",
                                    validatecommand=(validate_cmd, "%P"),
                                    textvariable=startTextVariable
                                    )

timeToWaitBeforeStartLabel = ctk.CTkLabel(root,
                                        font=("Impact", 30),
                                        text="Time to wait before starting (in seconds):",
                                        text_color=pallete["1"],
                                        )


searches = ctk.CTkEntry(root,
                        font=("Impact", 30),
                        width=370,
                        height=100,
                        bg_color=pallete["5"],
                        fg_color=pallete["2"],
                        corner_radius=10,
                        justify="center",
                        validate="key",
                        validatecommand=(validate_cmd, "%P"),
                        textvariable=searchesTextVariable
                        )

searchesLabel = ctk.CTkLabel(root,
                            font=("Impact", 30),
                            text="Number of searches before stopping:",
                            text_color=pallete["1"],
                            )


customStartPoint = ctk.CTkEntry(root,
                            font=("Impact", 30),
                            width=370,
                            height=100,
                            bg_color=pallete["5"],
                            fg_color=pallete["2"],
                            corner_radius=10,
                            justify="center",
                            validate="key",
                            validatecommand=(validate_cmd, "%P"),
                            textvariable=customStartPointVariable
                            )

customStartPointLabel = ctk.CTkLabel(root,
                            font=("Impact", 30),
                            text="Custom point to start counting \n (not saved when application closed):",
                            text_color=pallete["1"],
                            )

                            
timeToWaitIndicator = ctk.CTkLabel(root,
                                   font=("Impact", 30),
                                   text_color=pallete["1"],
                                   text=f"Current wait time: {startTextVariable.get() if state == "countingDown" else "Not started yet!"}",
                                   )

searchesLeftIndicator = ctk.CTkLabel(root,
                                     font=("Impact", 30),
                                     text_color=pallete["1"],
                                     text=f"Searches left: {searchesTextVariable.get() - searchesDone if state == "Searching" else "Not started yet!"}",
                                     )


def perform_search(current, total):
    global state
    if current < total:
        searchesLeftIndicator.configure(text=f"Searches left: {total - current}")
        pyautogui.typewrite(str(current + int(customStartPointVariable.get())) + " ")
        pyautogui.press("enter")
        if keyboard.is_pressed('space') and state == "Searching":
            ctkmsg.CTkMessagebox(message="Searches stopped!", icon="warning")
            state = "idle"
            startButton.configure(state="normal")
            searches.configure(state="normal")
            startButton.configure(text="START")
            timeToWaitBeforeStart.configure(state="normal")
            timeToLoadSiteInput.configure(state="normal")
            customStartPoint.configure(state="normal")
            searchesLeftIndicator.configure(text=f"Searches left: {str(int(searchesTextVariable.get()) - int(searchesDone)) if state == "Searching" else "Not started yet!"}")
            timeToWaitIndicator.configure(text=f"Current wait time: {startTextVariable.get() if state == "countingDown" else "Not started yet!"}")
            return
        root.after(int(loadTextVariable.get()) * 1000, close_tab, current, total)
    else:
        state = "idle"
        startButton.configure(state="normal")
        searches.configure(state="normal")
        timeToWaitBeforeStart.configure(state="normal")
        timeToLoadSiteInput.configure(state="normal")
        customStartPoint.configure(state="normal")
        startButton.configure(text="START")
        searchesLeftIndicator.configure(text=f"Searches left: {str(int(searchesTextVariable.get()) - int(searchesDone)) if state == "Searching" else "Not started yet!"}")
        timeToWaitIndicator.configure(text=f"Current wait time: {startTextVariable.get() if state == "countingDown" else "Not started yet!"}")
        ctkmsg.CTkMessagebox(message="Searches finished!", icon="check")


def close_tab(current, total):
    pyautogui.hotkey("ctrl", "t")
    pyautogui.hotkey('ctrl', 'tab')
    pyautogui.hotkey("ctrl", "w")
    root.after(300, perform_search, current + 1, total)


def start():
    global state
    state = "countingDown"
    startButton.configure(state="disabled")
    searches.configure(state="disabled")
    timeToWaitBeforeStart.configure(state="disabled")
    timeToLoadSiteInput.configure(state="disabled")
    customStartPoint.configure(state="disabled")
    wait_time = int(startTextVariable.get())
    countdown(wait_time)

def countdown(remaining_time):
    global state
    if remaining_time > 0:
        timeToWaitIndicator.configure(text=f"Current wait time: {remaining_time}")
        root.after(1000, countdown, remaining_time - 1)
    else:
        timeToWaitIndicator.configure(text="Finished counting down, searching started!")
        state = "Searching"
        startButton.configure(text="HOLD SPACE TO STOP")   
        perform_search(0, int(searchesTextVariable.get()))

startButton.configure(command=start)



startButton.pack(pady=20)
ctk.CTkFrame(root, bg_color=pallete["5"], height=10, width=570, corner_radius=15, fg_color=pallete["1"]).pack(pady=20)
timeToLoadSiteLabel.pack(pady=5)
timeToLoadSiteInput.pack(pady=10)
timeToWaitBeforeStartLabel.pack(pady=5)
timeToWaitBeforeStart.pack(pady=10)
searchesLabel.pack(pady=5)
searches.pack(pady=10)
customStartPointLabel.pack(pady=5)
customStartPoint.pack(pady=10)
ctk.CTkFrame(root, bg_color=pallete["5"], height=10, width=570, corner_radius=15, fg_color=pallete["1"]).pack(pady=10)
timeToWaitIndicator.pack(pady=10)
searchesLeftIndicator.pack(pady=10)
ctk.CTkFrame(root, bg_color=pallete["5"], height=10, width=570, corner_radius=15, fg_color=pallete["1"]).pack(pady=10)



window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()