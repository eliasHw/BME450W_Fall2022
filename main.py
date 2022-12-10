from pathlib import Path
import sys
from threading import *
from time import *
from record import *

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label
import tkinter as tk
import tkinter.filedialog # Keep this

# Multithreading context switching every 1.0 seconds 
sys.setswitchinterval(1.0)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")
print(ASSETS_PATH)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH/Path(path)

# Function to record the baseline
def recBaselineFunc():
    addr = entry_1.get("1.0",'end-1c')
    if not addr:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter IP Address.")
        return
    
    global ip_addr
    ip_addr = "ws://" + addr

    print("Recording Baseline")
    updateConsole("Basline Recorded")
    record_baseline(ip_addr)

# Starts the main program
def startFunc():
    addr = entry_1.get("1.0",'end-1c')
    if not addr:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter IP Address.")
        return
    
    global ip_addr
    ip_addr = "ws://" + addr

    print("Starting program")
    updateConsole("Starting program")
    global record_app
    global stream_data_app
    record_app.start()
    stream_data_app.start()

# Exit the program 
def exitFunc():
    print("Exiting")
    sys.exit()

#########################################################################
# Returns a score based on the acceleration
def score_acc(data):
    baseline_acc_fn = 'baseline_data/baseline_acc.csv'

    x, y, z = [], [], []
    with open(baseline_acc_fn,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))

    const = 0.0
    px = (abs(max(x)-min(x)) * const)
    py = (abs(max(y)-min(y)) * const)
    pz = (abs(max(z)-min(z)) * const)

    xmax, xmin = max(x)+px, min(x)-px
    ymax, ymin = max(y)+py, min(y)-py
    zmax, zmin = max(z)+pz, min(z)-pz

    # Score:
    score = 0
    for tx,ty,tz in data:
        ref = 3
        if (tx>xmax or tx<xmin):
            ref -= 1
        if (ty>ymax or ty<ymin):
            ref -= 1
        if (tz>zmax or tz<zmin):
            ref -= 1

        if (ref < 2): # ABNORMAL
            pass
        else: # NORMAL
            score += 1
            pass
    
    score = (score/len(data)) * 100
    updateScore(score)
    print(score)

# Returns a score based on gyroscope data
# FIXME - not in use
def score_gyr(data):
    baseline_gyr_fn = 'baseline_data/baseline_gyr.csv'

    x, y, z = [], [], []
    with open(baseline_gyr_fn,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))

    const = 0.0
    px = (abs(max(x)-min(x)) * const)
    py = (abs(max(y)-min(y)) * const)
    pz = (abs(max(z)-min(z)) * const)

    xmax, xmin = max(x)+px, min(x)-px
    ymax, ymin = max(y)+py, min(y)-py
    zmax, zmin = max(z)+pz, min(z)-pz

    # Score:
    score = 0
    for tx,ty,tz in data:
        ref = 3
        if (tx>xmax or tx<xmin):
            ref -= 1
        if (ty>ymax or ty<ymin):
            ref -= 1
        if (tz>zmax or tz<zmin):
            ref -= 1

        if (ref < 2): # ABNORMAL
            pass
        else: # NORMAL
            score += 1
            pass
    
    score = (score/len(data)) * 100

# Function to update the score on the ui
def updateScore(chng):
    label_1.config(text = chng)

# Function to update the console
def updateConsole(chng):
    label_2.config(text = chng)
#########################################################################

# Main code for the ui
def ui():
    window = Tk()
    window.geometry("400x550")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 550,
        width = 400,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        34.0,
        114.0,
        355.0,
        349.0,
        fill="#D9D9D9",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        206.0,
        55.0,
        image=image_image_1
    )

    canvas.create_text(
        96.0,
        139.0,
        anchor="nw",
        text="IP Address:",
        fill="#000000",
        font=("Inter Bold", 15 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        242.5,
        149.0,
        image=entry_image_1
    )

    global entry_1
    entry_1 = Text(
        bd=0,
        bg="#F1F1F1",
        fg="#000716",
        highlightthickness=0,
        font=("Helvetica", 7)
    )
    entry_1.place(
        x=191.0,
        y=142.0,
        width=103.0,
        height=12.0
    )

    # Walking Score rectangle
    canvas.create_rectangle(
        95.0,
        402.0,
        306.0,
        525.0,
        fill="#D9D9D9",
        outline="")

    global label_1
    label_1 = Label(
        bd=0,
        bg="#F1F1F1",
        fg="#000716",
        highlightthickness=0,
        text="100"
    )
    label_1.place(
        x=175.0,
        y=450.0,
        width=50.0,
        height=50.0
    )

    global label_2
    label_2 = Label(
        bd=0,
        bg="#F1F1F1",
        fg="#000716",
        highlightthickness=0,
        text=">> Welcome!"
    )
    label_2.place(
        x=100.0,
        y=347.0,
        width=200.0,
        height=30.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=startFunc,
        relief="flat"
    )
    button_1.place(
        x=126.0,
        y=230.0,
        width=136.35812377929688,
        height=40.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=recBaselineFunc,
        relief="flat"
    )
    button_2.place(
        x=95.0,
        y=172.0,
        width=199.0,
        height=40.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=exitFunc,
        relief="flat"
    )
    button_3.place(
        x=152.0,
        y=290.0,
        width=85.0,
        height=34.46666717529297
    )

    canvas.create_text(
        133.0,
        412.0,
        anchor="nw",
        text="Walking Score",
        fill="#000000",
        font=("Inter Bold", 20 * -1)
    )
    window.resizable(False, False)

    window.mainloop()

# Class to start new thread for recording real-time data
class record_APP(Thread):
    def run(self):
        global ip_addr
        record(ip_addr)

# Class to start thread to capture the real-time data
class stream_data_APP(Thread):
    def run(self):
        while True:
            # print(list(LIVE_DATA.queue))
            live_data = list(LIVE_DATA.queue)
            if len(live_data) == REALTIME_SAMPLES:
                score_acc(list(LIVE_DATA.queue))
                # score_gyr(list(LIVE_DATA.queue))
            sleep(0.1)

def main():
    global record_app
    global stream_data_app
    record_app = record_APP(daemon=True)
    stream_data_app = stream_data_APP(daemon=True)

    global ip_addr

    ui()

if __name__ == "__main__":
    main()