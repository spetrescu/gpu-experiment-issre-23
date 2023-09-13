#!/bin/bash
usage="$(basename "$0") [-h] [-m method] [-d dataset] -- run experiment using method & dataset
where:
    -h  show instructions to run the script
    -m  set the method (default: Drain)
    -d  set the dataset (default: All datasets)
allowed methods:
 MoLFI
allowed datasets:
 Apache
 BGL
 HDFS
 HealthApp
 HPC
 Mac
 OpenStack
 Spark
 Windows
 Combined_Dataset
 Industry_Dataset"

while getopts ":hm:d:" opt; do
  case $opt in
    h) echo "$usage"
    exit
    ;;
    m) method="$OPTARG"
    ;;
    d) dataset="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ -z "$method" ]
then
      echo "\$method argument empty. \nRunning script with Drain as default method."
      method="Drain"
fi

if [ -z "$dataset" ]
then
      echo "\$dataset argument empty. Thus, running script over all datasets."
      echo "Running $method 10 times on 10 datasets...\n"
      dataset="Apache BGL HDFS HealthApp HPC Mac OpenStack Spark Windows Combined_Dataset Industry_Dataset"
fi

printf "Running method %s\n" "$method"
printf "Datasets used for current experiment: $dataset \n \n"

cd logparser/
cd benchmark/

cd ..
rm -rf results/final_results/
rm -rf results/raw_results/
cd benchmark/

for d in $dataset
do
  for s in 2
  do
    for r in 1 2 3 4 5 6 7 8 9 10
    do
        echo "Parsing $d dataset of size "$s"k using "$method" [run no $r]"
        python "$method"_benchmark.py $d $s $r
        cd ..
        cd results/
        mkdir -p "final_results/""$method""_results/"
        mkdir -p "final_results/""$method""_results_templates/"
        cp "raw_results/""$method""_results/${d}_2k.log_structured.csv" "final_results/""$method""_results/${d}_2k.log_structured_run_${r}.csv"
        cp "raw_results/""$method""_results/${d}_2k.log_templates.csv" "final_results/""$method""_results_templates/${d}_2k.log_templates_run_${r}.csv"
        cd ..
        cd benchmark/
    done
  done
done

cd ..
cd results/
python compute_results.py $method

mkdir -p raw/raw_results_each_run
cp -r final_results/ raw_results_each_run/
cp -r raw_results_each_run/ raw/
rm -rf raw_results_each_run/
rm -rf final_results/
rm -rf raw/final_results/
rm -rf raw_results/

echo "\nThe parsed logs yielded by this experiment can be found under logparser/results/\n"