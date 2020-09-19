
int: n;
constraint assert(1 <= n /\ n <= 30, "n debe estar entre 1 y 30");
int: presupuesto;

array [1..n,1..2] of int: objetos;

var set of 1..n: selected;

constraint sum(i in selected)(objetos[i,1]) <= presupuesto;

solve maximize sum(i in selected)(objetos[i,2]);

output "Superficie: \(sum(i in selected)(objetos[i,2]))";