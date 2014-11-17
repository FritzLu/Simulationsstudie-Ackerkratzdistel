#####################################################
###                 Simulationsstudie             ###
###                 Fritz Luther                  ###
#####################################################


# Lade Python Module
from Tkinter import *
import random
import time
import math
import tkMessageBox
import numpy as np


# Startwerte werden für einige Variablen definiert
S=1
ROUNDS=0
DATA=[0]*20
INTER_ROUNDS=0
INTER_DATA=20



# Leere Matrizen werden erstellt
cell = [[0 for row in range(-1,61)] for col in range(-1,81)]
live = [[0 for row in range(-1,61)] for col in range(-1,81)]
temp = [[0 for row in range(-1,61)] for col in range(-1,81)]
summ = [[0 for row in range(0,INTER_DATA)] for col in range(0,20)]

# Hauptprozess der Simulation
def frame():
    global ROUNDS
    if S==0 and ROUNDS<=19:
        choose()
        draw()
        share()
        DATA[ROUNDS]=share()
        ROUNDS = ROUNDS +1
        L_ROUNDS=Label(root,text=ROUNDS,bg='azure',padx=35)
        L_ROUNDS.place(x=1040,y=520)
        naccheck()
        root.after(1500-200*nframes.get(), frame)


# Hauptprozess der 50 Durchläufe
def summary():
    startit()
    global ROUNDS
    global INTER_ROUNDS
    if INTER_ROUNDS < INTER_DATA:
        if S==0 and ROUNDS<= 19:
            naccheck()
            choose()
            share()
            summ[ROUNDS][INTER_ROUNDS]=share()
            ROUNDS = ROUNDS + 1
        else:
            INTER_ROUNDS = INTER_ROUNDS + 1
            ROUNDS = 0
            for y in range(-1,61):
                for x in range(-1,81):
                    live[x][y] = 0
                    temp[x][y] = 0
        root.after(0, summary)
    else:
        summdisplay(summ)
    return


# Pause Option
def stopit():
    global S
    S=1

# Hilfsfunktion zwischen der Option "Simulation starten" und dem Hauptprozess der Simulation
def starttrigger():
    startit()
    frame()


# Neustart Option
def startit():
    global S
    S=0


# Hilfsfunktion für die Menüoption "50 Durchläufe" zu den Funktionen "wait()" und "summary"
def summtrigger():
    global S
    reset()
    S=1
    wait()
    summary()
    return

    # Option für das Zurücksetzen auf Anfangsbedingungen
def reset():
    global S
    global ROUNDS
    global DATA
    global INTER_ROUNDS
    global INTER_DATA
    INTER_ROUNDS=0
    INTER_DATA=20
    DATA=[0]*20
    S=1
    ROUNDS=0
    percent=0
    Label(root,text=percent,bg='azure',padx=35).place(x=1040,y=550)
    L_ROUNDS=Label(root,text=ROUNDS,bg='azure',padx=35)
    summ = [[0 for row in range(0,INTER_DATA)] for col in range(0,20)]
    L_ROUNDS.place(x=1040,y=520) 
    for y in range(-1,61):
        for x in range(-1,81):
            live[x][y] = 0
            temp[x][y] = 0
            cell[x][y] = canvas.create_oval((x*10, y*10, x*10+10, y*10+10), outline="gray", fill="black")
    naccheck()

           
# Zählt alle mit Unkraut bedeckten Zellen
def countall(item):
    count=0
    for y in range(0,60):
        for x in range(0,80):
            if item [x][y] == 1 or item [x][y] == 2:
                count = count+1
    return count


# Erstellt eine Liste der Auswahl an hoch- und niedrigwachsenden Getreidesorten 
def grain():
    high=0
    if weizenvar.get() == 1:
        high = high+1
    if maisvar.get() == 1:
        high = high+1
    if gerstevar.get() == 1:
        high = high+1
    if rapsvar.get() == 1:
        high = high+1
    l_high=[1]*high
	
    low=0
    if zuckerruebevar.get() == 1:
        low = low +1
    if kartoffelnvar.get() == 1:
        low = low +1
    if karottenvar.get() == 1:
        low = low +1
    l_low=[2]*low
	
    g_selection =l_high+l_low 
    return(g_selection)


# Macht eine Zufallsauswahl aus der Liste der gewählten Getreidesorten       
def choose():
    if len(grain()) != 0:
        if random.choice(grain())== 1:
            processhigh()
        else: 
            processlow()
    else:
        mnochoose()
        weizenvar.set(1)
        if random.choice(grain())== 1:
            processhigh()
    return


# Lebenszyklus für hohe Getreidesorten
def processhigh():
    dummy=countall(live)
    for y in range(0,60):
        for x in range(0,80):
            glives=green_neighbors(x,y)
            blives=blue_neighbors(x,y)
            if live [x][y] == 0:
                if (glives+blives)==0:
                    if random.random()<math.sqrt(dummy)/(1000*math.sqrt(4800))+0.0001+(dummy!=0)*(R_values.get()*math.sqrt(dummy)/(1000*math.sqrt(4800))):
                        temp[x][y] = 1
                    else:
                        temp[x][y] = 0
                else:
                    if random.random()<((glives+blives)*0.1):
                        temp[x][y] = 1
                    else:
                        temp[x][y] = 0
            if live [x][y] == 1:
                if random.random()<(1-(glives+blives)*0.1):
                    temp[x][y] = 2
                else: 
                    if random.random()<0.2:
                        temp[x][y] = 0
                    else:
                        temp[x][y] = 1
                
            elif live [x][y] == 2:
                if random.random()<(1-(glives+blives)*0.1):
                   temp[x][y] = 1
                else:
                    temp[x][y] = 0
            
    for y in range(0,60):
        for x in range(0,80):
            live[x][y] = temp[x][y]



# Lebenszyklus für niedrige Getreidesorten
def processlow():
    dummy=countall(live)
    for y in range(0,60):
        for x in range(0,80):
            glives=green_neighbors(x,y)
            blives=blue_neighbors(x,y)
            if live [x][y] == 0:
                if (glives+blives)==0:
                    if random.random()<math.sqrt(dummy)/(500*math.sqrt(4800))+0.0001+(dummy!=0)*(R_values.get()*math.sqrt(dummy)/(500*math.sqrt(4800))):
                        temp[x][y] = 1
                    else:
                        temp[x][y] = 0
                else:
                    if random.random()<((glives+blives)*0.15):
                        temp[x][y] = 1
                    else:
                        temp[x][y] = 0
            if live [x][y] == 1:
                if random.random()<(1-(glives+blives)*0.1):
                    temp[x][y] = 2
                else: 
                    if random.random()<0.1:
                        temp[x][y] = 0
                    else:
                        temp[x][y] = 1             
            elif live [x][y] == 2:
                if random.random()<(1-(glives+blives)*0.1):
                   temp[x][y] = 1
                else:
                    temp[x][y] = 0
            
    for y in range(0,60):
        for x in range(0,80):
            live[x][y] = temp[x][y]            


# Anzahl der jungen Nachbarn werden gezählt (1)
def green_neighbors(a,b):
    lives = 0
    for z in range (-1,2):
        for w in range (-1,2):
            if live[a+z][b+w] == 1:
                if z == 0 and w == 0:
                    lives += 0
                else:
                    lives += 1
    return lives


# Anzahl der reifen Nachbarn werden gezählt (2)
def blue_neighbors(a,b):
    lives = 0
    for z in range (-1,2):
        for w in range (-1,2):
            if live[a-z][b-w] == 2:
                if z == 0 and w == 0:
                    lives += 0
                else:
                    lives += 1
    return lives


# Der Zustand der Zelle wird auf dem Acker graphisch wiedergegeben
def draw():
    for y in range(60):
        for x in range(80):
            if live[x][y]==0:
                canvas.itemconfig(cell[x][y], fill="white")
            if live[x][y]==1:
                canvas.itemconfig(cell[x][y], fill="green")
            if live[x][y]==2:
                canvas.itemconfig(cell[x][y], fill="blue")


# Berechnet den prozentualen Anteil befallener Zellen
def share():
    global percent
    percent=0
    for y in range(60):
        for x in range(80):
            if live[x][y] != 0:
                percent += 1
    percent=round(percent/float(80*60),3)
    Label(root,text=percent,bg='azure',padx=35).place(x=1040,y=550)
    return (percent)


# Hilfsfunktion für die Menüoption "Zeitreihe" und der Funktion "barchart()"
def trigger():
    barchart(DATA)
    return


# Zeigt eine Graphik mit der Entwicklung befallener Zellen
def barchart(seq, width=900, height=700):
    chart=Toplevel()
    chart.title("Ausbreitungsentwicklung der Ackerkratzdistel")
    bar = Canvas(chart,width=width, height=height, bg='azure')
    bar.pack()
    if max(seq)*2000 < 600:
        y_stretch = 2000
    else:
        y_stretch = 2000
    y_gap = 30
    x_stretch = 15
    x_width = 25
    x_gap = 30
    for x, y in enumerate(seq):
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = height - (y * y_stretch + y_gap)
        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = height - y_gap
        bar.create_rectangle(x0, y0, x1, y1, fill="red")
        bar.create_text(x0+2, y0, anchor=SW, text=str(y*100))
    return


# Zeigt eine Graphik mit der Entwicklung befallener Zellen für 50 Durchläufe
def summdisplay(matrix, width=900, height=700):
    chart=Toplevel()
    chart.title("50 Durchläufe dieser Simulation")
    bar = Canvas(chart,width=width, height=height, bg='azure')
    bar.pack()
    if max(matrix)*2000<600:
        y_stretch = 2000
    else:
        y_stretch = 1000
    y_gap = 30
    x_stretch = 15
    x_width = 25
    x_gap = 30
    for y in range(20):
        x0 = y * x_stretch + y * x_width + x_gap
        y0 = height - (max(matrix[y]) * y_stretch + y_gap)
        x1 = y * x_stretch + y * x_width + x_width + x_gap
        y1 = height - (min(matrix[y]) * y_stretch + y_gap)
        x3 = y * x_stretch + y * x_width + x_gap
        y3 = height - (np.percentile(matrix[y],75) * y_stretch + y_gap)
        x4 = y * x_stretch + y * x_width + x_width + x_gap
        y4 = height - (np.percentile(matrix[y],25) * y_stretch + y_gap)
        bar.create_rectangle(x0, y0, x1, y1, fill="red")
        bar.create_rectangle(x3, y3, x4, y4, fill="blue")
        bar.create_text(x0, y0, anchor=SW, text=str(max(matrix[y])*100))
        bar.create_text(x0-2, y1+25, anchor=SW, text=str(min(matrix[y])*100))
    return


# Option um das Programm zu beenden
def mQuit():
    mExit = tkMessageBox.askyesno(title="Simulation beenden",message="Sind Sie sicher, dass sie die Simulation beenden möchten")
    if mExit > 0:
        root.destroy()
        return


# Option um das Handbuch der Simulation anzuzeigen
def mInfo():
    mExit = tkMessageBox.showinfo(title="Handbuch",message="Hier stehen in Kürze eine Fülle von Informationen über die Simulation")
    return


# Option für eine Infobox, wenn keine Getreidesorten gewählt wurden
def mnochoose():
    mExit = tkMessageBox.showinfo(title="Handbuch",
        message="Da Sie keine Getreidesorte ausgewählt haben, läuft der Prozessjetzt so als hätten Sie Weizen ausgewählt")
    return


# Option für eine Infobox, wenn 50 Durchläufe gewählt wurden
def wait():
    mExit = tkMessageBox.showinfo(title="Simulation läuft",
        message="""Bitten warten Sie einen kurzen Moment bis die Grafik aufscheint.
                Drücken Sie auf OK um die Simulation fortzufahren""")
    return


# Verhindert, dass die Einstellungen während der Simulation verändert werden können 
def naccheck():
        if ROUNDS!=0:
            R_Extensiv.config(state='disabled')
            R_Intensiv.config(state='disabled')
            C_Weizen.config(state='disabled')
            C_Zuckerrueben.config(state='disabled')
            C_Mais.config(state='disabled')
            C_Gerste.config(state='disabled')
            C_Kartoffeln.config(state='disabled')
            C_Raps.config(state='disabled')
            C_Hanf.config(state='disabled')
            C_Karotten.config(state='disabled')
            
        else:
            R_Extensiv.config(state='normal')
            R_Intensiv.config(state='normal')
            C_Weizen.config(state='normal')
            C_Zuckerrueben.config(state='normal')
            C_Mais.config(state='normal')
            C_Gerste.config(state='normal')
            C_Kartoffeln.config(state='normal')
            C_Raps.config(state='normal')
            C_Hanf.config(state='normal')
            C_Karotten.config(state='normal')


# Erzeugt eine graphische Oberfläche (Canvas Objekt)
root = Tk()
root.title("Simulationsstudie zum Ausbreitungsverhalten von Ackerkratzdisteln")
canvas = Canvas(root, width=1200, height=600, highlightthickness=0, bd=0, bg='azure')
root.resizable(width=FALSE, height=FALSE)
canvas.pack()


# Setzt fest in welchem Format die Werte der Einstellungen abgespeichert werden
R_values=IntVar()
nframes=IntVar()
percent=DoubleVar()
weizenvar=IntVar()
zuckerruebevar=IntVar()
maisvar=IntVar()
gerstevar=IntVar()
kartoffelnvar=IntVar()
rapsvar=IntVar()
hanfvar=IntVar()
karottenvar=IntVar()


# Erstellt eine Auswahl an Checkboxen für die Getreidesorten
C_Weizen=Checkbutton(root,text="Weizen",variable=weizenvar,bg='azure')
C_Zuckerrueben=Checkbutton(root,text="Zuckerrueben",variable=zuckerruebevar,bg='azure')
C_Mais=Checkbutton(root,text="Mais",variable=maisvar,bg='azure')
C_Gerste=Checkbutton(root,text="Gerste",variable=gerstevar,bg='azure')
C_Kartoffeln=Checkbutton(root,text="Kartoffeln",variable=kartoffelnvar,bg='azure')
C_Raps=Checkbutton(root,text="Raps",variable=rapsvar,bg='azure')
C_Hanf=Checkbutton(root,text="Hanf",variable=hanfvar,bg='azure')
C_Karotten=Checkbutton(root,text="Karotten",variable=karottenvar,bg='azure')
weizenvar.set(1)


# Platziert die Checkboxen für die Getreidesorten
C_Weizen.place(x=850,y=40)
C_Zuckerrueben.place(x=850,y=70)
C_Mais.place(x=850,y=100)
C_Gerste.place(x=850,y=130)
C_Kartoffeln.place(x=850,y=160)
C_Raps.place(x=1030,y=40)
C_Hanf.place(x=1030,y=70)
C_Karotten.place(x=1030,y=100)


# Erstellt Radiobuttons für die Auswahl der Bodenbearbeitung
R_Extensiv=Radiobutton(root,text="Intensiv (Pflügen)",variable=R_values,value=0,indicatoron=1,bg='azure')
R_Intensiv=Radiobutton(root,text="Extensiv (Grubbern)",variable=R_values,value=1,bg='azure')
R_Extensiv.place(x=850,y=240)
R_Intensiv.place(x=850,y=270)
R_values.set(0)


# Erstellt einen Regler für die Schnelligkeit der Simulation
S_Geschwindigkeit=Scale(root,orient=HORIZONTAL,from_=1,to=5,length=200,bg='azure',bd=0,variable=nframes,highlightbackground='azure').place(x=870,y=340)
nframes.set(3)


# Erstellt die Hauptsteuerungselemente für die Simulation
mybutton=Button(root,text='Simulation ausführen',command=starttrigger).place(x=850,y=410)
mybutton=Button(root,text='Zurücksetzen',command=reset).place(x=850,y=460)
mybutton=Button(root,text='Pause',command=stopit).place(x=980,y=460)


# Erstellt Beschriftungen, die im Text aufscheinen
Label(text="Wählen Sie beliebige Ackerpflanzen aus",bg='azure').place(x=850,y=10)
Label(text="Wählen Sie die Art der Bodenbearbeitung",bg='azure').place(x=850,y=210)
Label(text="Geschwindigkeit",bg='azure').place(x=900,y=310)
Label(text="Vergangene Perioden",bg='azure').place(x=850,y=520)
Label(text="Prozentualer Befall",bg='azure').place(x=850,y=550)


# Erstellt eine Menüleiste mit Optionen
filemenu=Menu(root)
filemenu.add_command(label="Statistiken",command=trigger)
filemenu.add_command(label="50 Durchläufe",command=summtrigger)
#filemenu.add_command(label="Handbuch",command=mInfo)
filemenu.add_command(label="Schließen",command=mQuit)
root.config(menu=filemenu)


# Führt den ersten Befehl aus
reset()


# Hauptschleife der Simulation
root.mainloop()





