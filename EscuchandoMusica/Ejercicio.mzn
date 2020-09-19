% numero de canciones
int: n; 
constraint assert(n >= 1 /\ n <= 50, "El numero de canciones tiene que ser entre uno y cincuenta");
%tiempo que dura el viaje de ida
int: t1;
%tiempo que dura el viaje de vuelta
int: t2;
constraint assert(1 <= t1 /\ 1 <= t2 /\ t1 <= 100 /\ t2 <= 100, "t1 y t2 deben estar entre 1 y 100");
%Array de canciones con tiempo y satisfaccion
array [1..n, 1..2] of int: canciones;

var set of 1..n: cancionesIda;
var set of 1..n: cancionesVuelta;


constraint sum(i in cancionesIda)(canciones[i,1]) = t1;
constraint sum(i in cancionesVuelta)(canciones[i,1]) = t2;

%solve satisfy;
solve maximize sum(i in cancionesIda, j in cancionesVuelta)(canciones[i,2] + canciones[i,2]);

