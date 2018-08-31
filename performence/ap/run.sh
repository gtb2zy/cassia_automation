#!/bin/sh
#while :
#o
echo "Current path is " $PWD
for (( i=$1; i<$2; i++ ))
do
        echo "i=$i"
				#start capwap
					$PWD/WTP $1 $i&
					echo "Daemon WTP (PID=`pidof WTP`)started at `date`"
				#	sleep 1

done

	

#done 


