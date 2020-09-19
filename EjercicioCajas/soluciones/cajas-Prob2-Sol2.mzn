%idea de constraint de no solapamiento de Andrés Casillas
int: SX;
int: SY;
int: C;
array [1..C,1..2] of int: caja;
constraint assert (forall (i in 1..C) (caja[i,1] in 1..SX /\ caja[i,2] in 1..SY), "Alguna caja no cabe en la superficie");

array [1..C,1..2] of var 0..max(SX,SY)-1: sol;

%comprueba que se cubre toda la superficie
constraint assert( sum (i in 1..C) (caja[i,1]*caja[i,2]) = SX*SY, "UNSATISFIABLE");

%No se salen de la superficie
constraint forall (i in 1..C) (sol[i,1]+caja[i,1] <= SX);
constraint forall (i in 1..C) (sol[i,2]+caja[i,2] <= SY);

%No hay solapamiento entre cajas
constraint forall(c in 1..C, e in c+1..C)(
   sol[e,1] >= sol[c,1]+caja[c,1] \/ sol[e,1]+caja[e,1] <= sol[c,1] \/ sol[e,2] >= sol[c,2]+caja[c,2] \/ sol[e,2]+caja[e,2] <= sol[c,2]);

output [ "\(sol[i,1]) \(sol[i,2])\n" | i in 1..C ];
