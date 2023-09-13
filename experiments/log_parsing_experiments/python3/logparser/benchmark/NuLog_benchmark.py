import sys

sys.path.append("../")
from logparser.NuLog import NuLogParser
from logparser import evaluator
import os

n = len(sys.argv)
DATASET = str(sys.argv[1])
SIZE = str(sys.argv[2])

output_dir = "../results/raw_results/NuLog_results/"
input_dir = "../../../../../data/refactored_logs"

benchmark_settings = {
    "Apache": {
        "log_format": "<Content>",
        "filters": "([ ])",
        "k": 12,
        "nr_epochs": 5,
        "num_samples": 0,
    },
    "BGL": {
        "log_format": "<Content>",
        "filters": "([ |:|\(|\)|=|,])|(core.)|(\.{2,})",
        "k": 50,
        "nr_epochs": 3,
        "num_samples": 0,
    },
    "OpenStack": {
        "log_format": "<Content>",
        "filters": '([ |:|\(|\)|"|\{|\}|@|$|\[|\]|\||;])',
        "k": 5,
        "nr_epochs": 6,
        "num_samples": 0,
    },
    "HDFS": {
        "log_format": "<Content>",
        "filters": "(\s+blk_)|(:)|(\s)",
        "k": 15,
        "nr_epochs": 5,
        "num_samples": 0,
    },
    "HPC": {
        "log_format": "<Content>",
        "filters": "([ |=])",
        "num_samples": 0,
        "k": 10,
        "nr_epochs": 3,
    },
    "Windows": {
        "log_format": "<Content>",
        "filters": "([ ])",
        "num_samples": 0,
        "k": 95,
        "nr_epochs": 5,
    },
    "HealthApp": {
        "log_format": "<Content>",
        "filters": "([ ])",
        "num_samples": 0,
        "k": 100,
        "nr_epochs": 5,
    },
    "Mac": {
        "log_format": "<Content>",
        "filters": "([ ])|([\w-]+\.){2,}[\w-]+",
        "num_samples": 0,
        "k": 300,
        "nr_epochs": 10,
    },
    "Spark": {
        "log_format": "<Content>",
        "filters": "([ ])|(\d+\sB)|(\d+\sKB)|(\d+\.){3}\d+|\b[KGTM]?B\b|([\w-]+\.){2,}[\w-]+",
        "num_samples": 0,
        "k": 50,
        "nr_epochs": 3,
    },
    "Combined_Dataset": {
        "log_format": "<Content>",
        "filters": "([ ])",
        "num_samples": 0,
        "k": 300,
        "nr_epochs": 10,
    },
    "Industry_Dataset": {
        "log_format": "<Content>",
        "filters": "([ ])",
        "num_samples": 0,
        "k": 300,
        "nr_epochs": 10,
    },
}


def parsing_logs(setting, indir, output_dir, log_file):
    parser = NuLogParser.LogParser(
        indir=indir,
        outdir=output_dir,
        filters=setting["filters"],
        k=setting["k"],
        log_format=setting["log_format"],
    )
    parser.parse(
        log_file, nr_epochs=setting["nr_epochs"], num_samples=setting["num_samples"]
    )


bechmark_result = []
for dataset, setting in benchmark_settings.items():
    if dataset == DATASET:
        print("=== Evaluation on %s ===" % dataset)
        logfile = str(DATASET + "/" + DATASET + "_" + SIZE + "k.log")
        indir = os.path.join(input_dir, os.path.dirname(logfile))
        log_file = os.path.basename(logfile)
        parsing_logs(setting, indir, output_dir, log_file)
        print("")
