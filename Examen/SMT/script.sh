#!/bin/bash

echo "Script de ejecucion de las entradas de la practica smt"

files=$(ls *.txt)
files=($(echo "$files" | tr " " "\n"))
rm -rf out
mkdir out
rm -rf in/
mkdir in/
for i in "${files[@]}"
do
	echo "Ejecucion del problema con la entrada -> $i"

	$(./practica.py < "$i" > "in/$i".smt2)
	var=$(time z3 "in/$i".smt2)
	echo "$var" > out/"$i".out
	echo "Salida en el fichero out/$i.out"
done

