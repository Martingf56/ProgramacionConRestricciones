import sys

import SMT2


m = int(input())
n = int(input())
minSat = int(input())

juguetes = []
for i in range(0,m):
    j = int(input())
    juguetes.append(j)

tipos_juguete = []  
for i in range(0,m):
    tipos_juguete.append(input())

print("sat")
satisfaction = []  
for i in range(0,n):
    sat = []
    for k in range(0,m):
        sat.append(input())
    satisfaction.append(sat)

print(satisfaction)
