int: SX;
int: SY;
int: C;
array [1..C,1..2] of int: caja;
constraint assert (forall (i in 1..C) (caja[i,1] in 1..SX /\ caja[i,2] in 1..SY), "Alguna caja no cabe en la superficie");

%comprueba que se cubre toda la superficie
constraint assert( sum (i in 1..C) (cajax[i]*cajay[i]) = SX*SY, "UNSATISFIABLE");

array [1..C] of 1..SX: cajax = [caja[i,1] | i in 1..C];
array [1..C] of 1..SY: cajay = [caja[i,2] | i in 1..C];

array [1..C,1..2] of var 0..max(SX,SY)-1: sol;

%No se salen de la superficie
constraint forall (i in 1..C) (sol[i,1]+cajax[i] <= SX);
constraint forall (i in 1..C) (sol[i,2]+cajay[i] <= SY);

%No hay solapamiento entre cajas
constraint forall (i in 1..C, j in 1..C where i!=j) (
  not( sol[i,1] <= sol[j,1] /\ sol[j,1] < sol[i,1]+cajax[i] /\
     (  (sol[i,2] <= sol[j,2] /\ sol[j,2] < sol[i,2]+cajay[i] )
     \/ (sol[j,2] <= sol[i,2] /\ sol[i,2] < sol[j,2]+cajay[j] ))));

%Constraint redundante que dice que todos los puntos de la superficie están cubiertos por alguna caja
constraint forall (i in 0..SX-1, j in 0..SY-1) (exists (c in 1..C) (sol[c,1] <= i /\ i < sol[c,1]+cajax[c] /\ sol[c,2] <= j /\ j < sol[c,2]+cajay[c]));

solve satisfy;

output [ "\(sol[i,1]) \(sol[i,2])\n" | i in 1..C ];
