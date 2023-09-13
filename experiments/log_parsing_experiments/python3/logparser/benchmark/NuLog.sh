for d in OpenStack
do
  for s in 2
  do
    for r in 1 2 3 4 5 6 7 8 9 10
    do
        python NuLog_benchmark.py $d $s $r
        echo "Dataset $d size $s run no $r"
        mv "NuLog_result/${d}_2k.log_structured.csv" "NuLog_result/${d}_2k.log_structured_run_${r}.csv"
    done
  done
done
