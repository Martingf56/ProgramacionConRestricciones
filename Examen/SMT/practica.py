#!/usr/bin/python3


#Cambio :
#   En esta parte indico que constraint he realizado en smt ordenado por numeros para facilitar su busca
#      #1 -> Constraint de cambiar las durezas diferenciando los vegetales y los normales. Ejercicio 5
#      #2 -> Modificando el beneficio a que supere 0. Primer ejercicio  
#      #3 -> Contolar que hay menor igual que p perdidas. Ejercicio 2
#      #4 -> Vetar aceite mes. Ejercicio 3
#      #5 -> Minimo refinado mensual. Ejercicio 4.

numMeses = 6
tipoAceite = 5
# Entrada
preciosMes = []
for i in range(1, numMeses+1):
    datos = input().split()
    aux = []
    for dato in datos:
        aux.append(int(dato))
    preciosMes.append(aux)

valor = int(input())
maxv = int(input())
maxn = int(input())
mcap = int(input())
#preciosAlmacenamiento = int(input())
mindv = int(input())
maxdv = int(input())
mindn = int(input())
maxdn = int(input())
durezas = []
for i in range(0, tipoAceite):
    durezas.append(float(input()))
cantidadIni = int(input())
#minb = int(input())
k = int(input())
t = int(input())
p = int(input())
vetoMes = []
for i in range(0, numMeses):
	vetoMes.append(int(input()))

minRefinadoMes = []
for i in range(0, numMeses):
	minRefinadoMes.append(int(input()))


# Parte de funciones smt
def aceiteComprado(i, j):                       # asig_0_0 y asig_0_1
    return "aceiteComprado_"+str(i)+"_"+str(j)


def aceiteRefinado(i, j):                       # nsat_0_0
    return "aceiteRefinado_"+str(i)+"_"+str(j)


def aceiteAlmacenado(i, j):                      # ntipo_0_0
    return "aceiteAlmacenado_"+str(i)+"_"+str(j)


def setlogic(l):
    return "(set-logic " + l + ")"


def intvar(v):
    return "(declare-fun "+v+" () Int)"


def bool2int(b):
    return "(ite "+b+" 1 0 )"


def addimplies(a1, a2):
    return "(=> "+a1+" "+a2+" )"


def addand(a1, a2):
    return "(and "+a1+" "+a2+" )"


def addor(a1, a2):
    return "(or "+a1+" "+a2+" )"


def addnot(a):
    return "(not "+a+" )"


def addexists(a):
    if len(a) == 0:
        return "false"
    elif len(a) == 1:
        return a[0]
    else:
        x = a.pop()
        return "(or " + x + " " + addexists(a) + " )"


def addeq(a1, a2):
    return "(= "+a1+" "+a2+" )"


def adddistinct(a1, a2):
    return "(distinct "+a1+" "+a2+" )"


def addle(a1, a2):
    return "(<= "+a1+" "+a2+" )"


def addge(a1, a2):
    return "(>= "+a1+" "+a2+" )"


def addlt(a1, a2):
    return "(< "+a1+" "+a2+" )"


def addgt(a1, a2):
    return "(> "+a1+" "+a2+" )"


def addplus(a1, a2):
    return "(+ "+a1+" "+a2+" )"


def addminus(a1, a2):
    return "(- "+a1+" "+a2+" )"


def addmul(a1, a2):
    return "(* "+a1+" "+a2+" )"


def addassert(a):
    return "(assert "+a+" )"


def addassertsoft(a, w):
    return "(assert-soft "+a+" :weight " + w + " )"


def addsum(a):
    if len(a) == 0:
        return "0"
    elif len(a) == 1:
        return a[0]
    else:
        x = a.pop()
        return "(+ " + x + " " + addsum(a) + " )"


def maximize(w):
    print("(maximize " + w + " )")


def checksat():
    print("(check-sat)")


def getobjectives():
    print("(get-objectives)")


def getmodel():
    print("(get-model)")


def getvalue(l):
    print("(get-value ( " + l + " ) )")

################################
# generamos un fichero smtlib2
################################


print("(set-option :produce-models true)")
# print(setlogic("QF_?"))

# Solucion
for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        print(intvar(aceiteComprado(i, j)))

for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        print(intvar(aceiteRefinado(i, j)))

for i in range(0, numMeses+1):
    for j in range(1, tipoAceite+1):
        print(intvar(aceiteAlmacenado(i, j)))

# Constraints

# La capacidad es limitada
for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        print(addassert(addle(str(0), (aceiteComprado(i, j)))))
        print(addassert(addge(str(mcap), (aceiteComprado(i, j)))))
        print(addassert(addle(str(0), (aceiteRefinado(i, j)))))
        print(addassert(addge(str(mcap), (aceiteRefinado(i, j)))))
        print(addassert(addle(str(0), (aceiteAlmacenado(i, j)))))
        print(addassert(addge(str(mcap), (aceiteAlmacenado(i, j)))))

for i in range(0, numMeses+1):
    for j in range(1, tipoAceite+1):
        print(addassert(addle(str(0), (aceiteAlmacenado(i, j)))))
        print(addassert(addge(str(mcap), (aceiteAlmacenado(i, j)))))

# constraint forall(i in 1..numMeses,j in 1..tiposAceite)(aceiteAlm[i,j] = aceitesComprado[i,j] + aceiteAlm[i-1,j] - (if i == 1 then 0 else aceiteRefinado[i-1,j] endif));
for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        cond = str(0)
        if i > 1:
            cond = aceiteRefinado(i-1, j)
        print(addassert(addeq(addplus(aceiteComprado(i, j), addminus(
            aceiteAlmacenado(i-1, j), cond)), (aceiteAlmacenado(i, j)))))

# constraint forall(i in 1..tiposAceite)(aceiteAlm[0,i] = cantidadPrincipio /\ aceiteAlm[numMeses,i] - aceiteRefinado[numMeses,i] = cantidadPrincipio);
for i in range(1, tipoAceite+1):
    print(addassert(addand(addeq(aceiteAlmacenado(0, i), str(cantidadIni)),
                           addeq(addminus(aceiteAlmacenado(numMeses, i), aceiteRefinado(numMeses, i)), str(cantidadIni)))))

# constraint forall(i in 1..numMeses)(aceiteRefinado[i,1] + aceiteRefinado[i,2] <= MAXV
# /\ aceiteRefinado[i,3] + aceiteRefinado[i,4] + aceiteRefinado[i,tiposAceite] <= MAXN);
for i in range(1, numMeses + 1):
    print(addassert(addand(
        addle(addplus(aceiteRefinado(i, 1), aceiteRefinado(i, 2)), str(maxv)),
        addle(addplus(aceiteRefinado(i, 3), addplus(aceiteRefinado(i, 4), aceiteRefinado(i, 5))), str(maxn)))))

#1
#Cambbio: 
#for i in range(1, numMeses + 1):
#    suma = []
#    suma2 = []
#    for j in range(1, tipoAceite + 1):
#        suma.append(addmul(aceiteRefinado(i, j), str(durezas[j-1])))
#        suma2.append(aceiteRefinado(i, j))
#
#    print(addassert(addand(addle(addsum(suma), addmul(str(maxd), addsum(suma2))),
#                          addge(addsum(suma), addmul(str(mind), addsum(suma2))))))
# constraint forall(i in 1..numMeses)(compDureza(sum(j in 1..tiposAceite)(aceiteRefinado[i,j]*durezasAceite[j]),sum(j in 1..tiposAceite)(aceiteRefinado[i,j])));
for i in range(1, numMeses + 1):
    sumav = []
    sumavcant = []
    suman = []
    sumancant = []
    for j in range(1, 3):
        sumav.append(addmul(aceiteRefinado(i, j), str(durezas[j-1])))
        sumavcant.append(aceiteRefinado(i, j))
    for j in range(3, tipoAceite+1):
        suman.append(addmul(aceiteRefinado(i, j), str(durezas[j-1])))
        sumancant.append(aceiteRefinado(i, j))
        
    print(addassert(addand(
        addand(addle(addsum(sumav), addmul(str(maxdv), addsum(sumavcant))),
                           addge(addsum(sumav), addmul(str(mindv), addsum(sumavcant)))),
        addand(addle(addsum(suman), addmul(str(maxdn), addsum(sumancant))),
                           addge(addsum(suman), addmul(str(mindn), addsum(sumancant)))))))

#2
#Cambio: 
#sum1 = []
#for i in range(1, numMeses+1):
#    for j in range(1, tipoAceite):
#        sum1.append(addmul(aceiteRefinado(i, j), str(valor)))

#sum2 = []
#for i in range(1, numMeses + 1):
#    for j in range(1, tipoAceite + 1):
#        sum2.append(addplus(addmul(aceiteAlmacenado(i, j), str(
#            preciosAlmacenamiento)), addmul(aceiteComprado(i, j), str(preciosMes[i-1][j-1]))))

#print(addassert(addge(addminus(addsum(sum1), addsum(sum2)), str(minb))))
# Gastos >= 0
sum1 = []
for i in range(1, numMeses+1):
    for j in range(1, tipoAceite):
        sum1.append(addmul(aceiteRefinado(i, j), str(valor)))

sum2 = []
for i in range(1, numMeses + 1):
    for j in range(1, tipoAceite + 1):
        sum2.append(addmul(aceiteComprado(i, j), str(preciosMes[i-1][j-1])))

print(addassert(addge(addminus(addsum(sum1), addsum(sum2)), str(0))))

# constraint forall(i in 1..numMeses)(sum(j in 1..tiposAceite)(bool2int(aceiteRefinado[i,j] != 0)) <= K);
for i in range(1, numMeses+1):
    suma = []
    for j in range(1, tipoAceite+1):
        suma.append(bool2int(adddistinct(aceiteRefinado(i, j), str(0))))

    print(addassert(addle(addsum(suma), str(k))))

# constraint forall(i in 1..numMeses, j in 1..tiposAceite)(aceiteRefinado[i,j] != 0 -> aceiteRefinado[i,j] >= T );
for i in range(1, numMeses+1):
    print(addassert(addor(addnot(adddistinct(aceiteRefinado(i, j),str(0))), addge(aceiteRefinado(i, j), str(t)))))

# constraint forall(i in 1..numMeses)((aceiteRefinado[i,1] != 0 \/ aceiteRefinado[i,2] != 0) -> aceiteRefinado[i,5] != 0);
for i in range(1, numMeses+1):
    print(addassert(addor(addnot(addor(adddistinct(aceiteRefinado(i, 1), str(0)), adddistinct(
        aceiteRefinado(i, 2), str(0)))), adddistinct(aceiteRefinado(i, 5), str(0)))))

#3
#constraint sum(i in 1..numMeses)(bool2int(sum(j in 1..tiposAceite)(aceiteRefinado[i,j]*VALOR - aceitesComprado[i,j]*precios[i,j]) < 0)) <= P;
sumTot = []
for i in range(1, numMeses+1):
    sum = []
    for j in range(1,tipoAceite+1):
        sum.append(addminus(addmul(aceiteRefinado(i,j), str(valor)), addmul(aceiteComprado(i,j),str(preciosMes[i-1][j-1]))))
    sumTot.append(bool2int(addlt(addsum(sum),str(0))))

print(addassert(addle(addsum(sumTot),str(p))))

#4
#constraint forall(i in 1..numMeses)(vetoMes[i] != 0 -> aceiteRefinado[i,vetoMes[i]] == 0);
for i in range(1, numMeses+1):
    print(addassert(addor(addnot(adddistinct(str(vetoMes[i-1]),str(0))), addeq(aceiteRefinado(i,vetoMes[i-1]),str(0)))))
    
#5
#constraint forall(i in 1..numMeses)(sum(j in 1..tiposAceite)(aceiteRefinado[i,j]) >= minRefinadoMes[i]);
sumaRefinado = []
for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        sumaRefinado.append(aceiteRefinado(i,j))
    print(addassert(addge(addsum(sumaRefinado), str(minRefinadoMes[i-1]))))


maximize("( "+str(addminus(addsum(sum1), addsum(sum2)))+" )")

checksat()

for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        getvalue(aceiteComprado(i, j))

for i in range(1, numMeses+1):
    for j in range(1, tipoAceite+1):
        getvalue(aceiteRefinado(i, j))

for i in range(0, numMeses+1):
    for j in range(1, tipoAceite+1):
        getvalue(aceiteAlmacenado(i, j))
