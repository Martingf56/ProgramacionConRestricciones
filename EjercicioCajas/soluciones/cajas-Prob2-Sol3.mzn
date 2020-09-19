%idea de uso de matriz para la superficie de Alberto Redondo y Gonzalo Agudo
int: SX;
int: SY;

int: C;
array[1..C, 1..2] of int: caja;
constraint assert (forall (i in 1..C) (caja[i,1] in 1..SX /\ caja[i,2] in 1..SY), "Alguna caja no cabe en la superficie");

%comprueba que se cubre toda la superficie
constraint assert(sum (i in 1..C) (caja[i, 1] * caja[i, 2]) = SX * SY, "UNSATISFIABLE");

array[1..C, 1..2] of var 0..max(SX, SY) - 1: sol;

array[0..SX - 1, 0..SY - 1] of var 1..C: colocar;

%No se salen de la superficie
constraint forall (i in 1..C) (sol[i,1]+caja[i,1] <= SX);
constraint forall (i in 1..C) (sol[i,2]+caja[i,2] <= SY);

%No hay solapamiento entre cajas
constraint forall (i in 1..C, j in 0..SX-1, k in 0..SY-1) (j<sol[i, 1] \/ j>=sol[i,1]+caja[i,1] \/ k<sol[i, 2] \/ k>=sol[i,2]+caja[i,2] \/ colocar[j,k] = i);

solve satisfy;

output [ "\(sol[i,1]) \(sol[i,2])\n" | i in 1..C ];
