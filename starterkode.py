import matplotlib.pyplot as plt
import numpy as np
#import scipy as sp

#opprette to tomme lister som vi skal fylle senere
tid = []
ems1 = []
ems2 = []
ems3 = []
ems4 = []


dtf = open("induksjon_egen_23042024.csv", "r")
lines = dtf.readlines()

#lese inn data fra csv filen
for row in lines[2:]:
    vals = row.strip().split(",")
    tid.append(float(vals[1]))
    ems1.append(float(vals[2]))
    ems2.append(float(vals[5]))
    ems3.append(float(vals[8]))
    ems4.append(float(vals[11]))

#plotte titlene
lables = lines[0].strip().split(",")
lables = list(dict.fromkeys(lables))

#plotte dataene
plt.plot(tid, ems1, "r", label = str(lables[0]))
plt.plot(tid, ems2, "b", label = str(lables[1]))
plt.plot(tid, ems3, "g", label = str(lables[2]))
plt.plot(tid, ems4, "y", label = str(lables[3]))

#pynte på plottet og vise det
plt.grid()
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
plt.xlabel("tid/s")
plt.ylabel("ems/V")
plt.show()


#Deriverivasjon her
ems1_derivert = []
for i in range(1, len(ems1)):
    ems1_derivert.append((ems1[i] - ems1[i-1])/(tid[i] - tid[i-1]))


#plotte den deriverte
plt.plot(tid[1:], ems1_derivert, "ro-", label = str(lables[0]))
plt.grid()
plt.xlabel("tid/s")
plt.ylabel("effekt per coloumb/(W/C)")
plt.show()


#Integral her
tot = 0
for i in range(1, len(ems1)):
    tot += abs(ems1[i]) * 0.001
    #print(tot)

#lukke filen
dtf.close()