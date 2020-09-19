
int: T; %Numero Trabajadores

int: N; %Numero de Trabajadores hora

int: D; %Numero de dias 

int: MaxDT; %Maximo dias consecutivos

int: MaxDL; %Maximo dias libres consecutivos

int: MinDT; %Minimo dias a trabajar

int: numIn; %Numero de pares de incompatibles

array [1..T] of 0..3: noTurnos;

array[1..numIn, 1..2] of 1..T: rel;% pares de incompatibles

set of 1..T: supervisores; %Los supervisores

array [1..T, 1..D] of var 0..3: sol;%Solucion 


constraint assert(3*N <= T, "El numero de trabajadores debe ser mayor que el numero de trabajadores necesarios en un dia");

constraint assert(MinDT <= D,"El numero de dias minimos trabajando debe ser igual menor igual al numero de dias");

%Restricciones
%1 Cada turno tiene N trabajadores
constraint forall(d in 1..D, t in 1..3)(sum(i in 1..T)(bool2int(sol[i,d] == t)) == N);

%2 Un trabajador solo un turno cada dia
% Segun la solucion escogida solo se puede ser asi

%3 Maximo dias consecutivos trabjando
constraint forall(i in 1..T, j in 1..D-MaxDT)(sum(l in j..j+MaxDT)(bool2int(sol[i,l] == 0)) >= 1);

%4 Maximo dias libres consecutivos
constraint forall(i in 1..T, j in 1..D-MaxDL)(sum(l in j..j+MaxDL)(bool2int(sol[i,l] != 0)) >= 1);

%5 Minimo de dias trabajados
constraint forall(i in 1..T)(sum(j in 1..D)(bool2int(sol[i,j] != 0)) >= MinDT);

%6 No puede acabar y empezar el turno de seguido
constraint forall(i in 1..T, j in 2..D)(sol[i, j-1] == 3 -> sol[i,j] != 1);

%7 Trabajadores incompatibles
constraint forall(i in 1..numIn, j in 1..D)(sol[rel[i,1],j] != sol[rel[i,2],j]);

%8 Supervision en cada turno
constraint forall(d in 1..D,t in 1..3)(sum(i in supervisores)(bool2int(sol[i,d] == t)) >= 1);

solve minimize sum(i in 1..T, d in 1..D where noTurnos[i] != 0)(bool2int(sol[i,d] == noTurnos[i]));

output [ "Trabajador \(i): \([sol[i,j] | j in 1..D ])\n" | i in 1..T];
