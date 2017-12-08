#!/bin/bash


for ((i=64;i<2049;i=i*2))
do
        for ((j=4;j<257;j=j*2))
        do
                for ((k=4;k<257;k=k*2))
                do
                        $GEM5/build/X86/gem5.opt --stats-file=stats_${i}_${j}_${k}.txt  hw3config.py -c daxpy/daxpy --cpu-type="DerivO3CPU" --caches --l2cache --num-phys-float-regs=${i} --num-rob-entries=${j} --num-iq-entries=${k}
                done
        done
done
