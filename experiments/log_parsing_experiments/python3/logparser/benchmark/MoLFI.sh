echo "Running MoLFI 10 times on 9 datasets...\n"
for d in Apache BGL HDFS HealthApp HPC Mac OpenStack Spark Windows
do
  for s in 2
  do
    for r in 1 2 3 4 5 6 7 8 9 10
    do
        python MoLFI_benchmark.py $d $s $r
        echo "Dataset $d size $s run no $r"
        mv "MoLFI_result/${d}_2k.log_structured.csv" "MoLFI_result/${d}_2k.log_structured_run_${r}.csv"
    done
  done
done
echo "Parsed logs can be found under MoLFI_result/\n"
echo "Computing accuracy results...\n"
