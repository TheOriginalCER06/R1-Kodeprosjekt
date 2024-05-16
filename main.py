import matplotlib.pyplot as plt
import numpy as np

tid = []
ems = []
eksponent = 1e5
farger = ["b","orange","g","r", "c", "m", "y", "k", "w"]

def do_plot(x_label: str = "X-verdier", y_label: str ="Y-verider", title: str = "Graf"):
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    legend = plt.legend(loc='upper left', shadow=True)
    plt.show()

dtf = open("induksjon_egen_23042024.csv", "r")
lines = dtf.readlines()
dtf.close()

lables = lines[0].strip().split(",")
sublables = lines[1].strip().split(",")
lables = list(dict.fromkeys(lables))
valsPerRun = int(len(sublables)/len(lables))
voltageIndex = sublables.index("Spenning (V)")

for i in range(len(lables)):
    ems.append([])

for row in lines[2:]:
    row = row.strip().split(",")
    tid.append(float(row[1]))
    for i in range(len(lables)):
        ems[i].append(float(row[i*valsPerRun + voltageIndex])* eksponent)

for i in range(len(ems)):
    plt.plot(tid, ems[i], label=lables[i], color=farger[i])
do_plot("Tid (s)", "Spenning (V)", "Spenning over tid")

voltsekunder = []
voltsekund = []
for i in range(len(ems)):
    voltsekunder.append(0)
    voltsekund.append([])
    for j in range(len(ems[i])):
        voltsekunder[i] += abs(ems[i][j] * (0.001))
        voltsekund[i].append((ems[i][j] * (0.001)))

for i in range(len(voltsekund)):
    plt.plot(tid, voltsekund[i], label=lables[i], color=farger[i])
do_plot("Tid (s)", "Voltsekund (Vs)", "Fluks(Voltsekund) over tid")

deriverte = []
for i in range(len(ems)):
    deriverte.append([])
    for j in range(len(ems[i])-1):
        deriverte[i].append((ems[i][j+1] - ems[i][j])/(tid[j+1]-tid[j]))
     
for i in range(len(deriverte)):
    plt.plot(tid[1:], deriverte[i], label=lables[i], color=farger[i])
do_plot("Tid (s)", "Spenning per sekund (V/s)", "Spenningsendring over tid")

def np_derivasjon(): 
    deriverte = []
    for i in range(len(ems)):
        deriverte.append(np.gradient(ems[i], tid))
    for i in range(len(deriverte)):
        plt.plot(tid, deriverte[i], label=lables[i], color=farger[i])
    do_plot("Tid (s)", "Spenning per sekund (V/s)", "Spenningsendring over tid")

#np_derivasjon() #Kjører numpy varianten, om du fjerner "#" fremst, skal fungere den også.

toleranse = 42 / 1e5 * eksponent

fortegn = []
tid_lok = []

fjernings_indekser = []
beholde_indekser = []

for j in range(len(deriverte)):
    fortegn.append([])
    tid_lok.append(tid[1:])
    fjernings_indekser.append([])
    beholde_indekser.append([])
    for i in range(len(deriverte[j])):
        if deriverte[j][i] > toleranse:
            fortegn[j].append(1 / 1e5 * eksponent)
        elif deriverte[j][i] < -toleranse:
            fortegn[j].append(-1 / 1e5 * eksponent)
        else:
            fortegn[j].append(0)

    for i, val in enumerate(fortegn[j]):
        if val == 0:
            fjernings_indekser[j].append(i)
        else:
            beholde_indekser[j].append(i)
    
    for i in reversed(fjernings_indekser[j]): # Her er den reversed slik at vi fjerner fra slutten av lista, slik at indeksene ikke endrer seg.
        del tid_lok[j][i]
        del fortegn[j][i]


for i in range(len(fortegn)):
    plt.plot(tid_lok[i], fortegn[i], label=lables[i], color=farger[i])
    plt.plot(tid[beholde_indekser[i][0]:beholde_indekser[i][-1]], ems[i][beholde_indekser[i][0]:beholde_indekser[i][-1]], color=farger[i])
do_plot("Tid (s)", "Fortegn", "Fortegnene")

pos_neg = []
start_pos = []

for i in range(len(fortegn)):
    pos_neg.append([])
    for j in range(len(fortegn[i])-1):
        if fortegn[i][j] != fortegn[i][j+1]:
            pos_neg[i].append(round(fortegn[i][j]*1e5/eksponent))
    pos_neg[i].append(round(fortegn[i][-1]*1e5/eksponent))
    for j in range(len(pos_neg[i])):
        if pos_neg[i][j] == 1 and j != len(pos_neg[i])-1:
            start_pos.append(j)

pos_av_neg = []
pos_av_pos = []
for i, val in enumerate(start_pos):
    if val == 0:
        pos_av_neg.append(i)
    else:
        pos_av_pos.append(i)

print("Totale Voltsekunder (integralen): ", voltsekunder)
print(" ")
print("Forsøkene:", ", ".join([lables[index] for index in pos_av_neg]), "starter med det samme fortegnet, '-' ")
print("Forsøkene:", ", ".join([lables[index] for index in pos_av_pos]), "starter med det samme fortegnet, '+' ")