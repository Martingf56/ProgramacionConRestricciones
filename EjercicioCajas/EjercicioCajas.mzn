

int: X;
int: Y;
int: numCajas;
array [1..numCajas,1..2] of 0..max(X,Y): cajas;

array [1..numCajas,1..2] of var 0..max(X,Y): solucion;


constraint forall(i in 1..numCajas)(solucion[i,1] + cajas[i,1] <= X );

constraint forall(i in 1..numCajas)(solucion[i,2] + cajas[i,2] <= Y);

constraint forall(i,j in 1..numCajas where i != j)( solucion[i,1] >= solucion[j,1] ->
                                                    (solucion[i,1] >= solucion[j,1] + cajas[j,1] 
                                                    \/ solucion[i,2] >= solucion[j,2] + cajas[j,2]));

solve satisfy;

