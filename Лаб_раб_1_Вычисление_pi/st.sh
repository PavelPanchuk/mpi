#!/bin/bash
rm out1.txt
printf "инд\tразб\tпотоки\tПи\tОшиб\tвремя\n" >> out1.txt
for ((i = 5000000; i <= 30000000; i=i+4000000)
do
    for ((j = 1; j <= 60; j++))
    do
        for ((k = 1; k <= 10; k++))
        do
            echo "$i, $j, $k, $(mpirun.openmpi -n $j --hostfile ./hostfile.txt ./rad.ip $i)"
        done
    done
done
