import sys

sys.path.append("../")
from logparser import evaluator
from sklearn.metrics import accuracy_score
import os
import pandas as pd
import time
from natsort import natsorted
from nltk.metrics.distance import edit_distance
import numpy as np

n = len(sys.argv)
METHOD = str(sys.argv[1])

print("Now computing results for method {0}...".format(METHOD))

GROUND_TRUTH_FILE_PATHS = {
    "Apache": "../../../../../data/refactored_logs/Apache/Apache_2k.log_structured.csv",
    "BGL": "../../../../../data/refactored_logs/BGL/BGL_2k.log_structured.csv",
    "Combined_Dataset": "../../../../../data/refactored_logs/Combined_Dataset/Combined_Dataset_2k.log_structured.csv",
    "HDFS": "../../../../../data/refactored_logs/HDFS/HDFS_2k.log_structured.csv",
    "HealthApp": "../../../../../data/refactored_logs/HealthApp/HealthApp_2k.log_structured.csv",
    "HPC": "../../../../../data/refactored_logs/HPC/HPC_2k.log_structured.csv",
    "Mac": "../../../../../data/refactored_logs/Mac/Mac_2k.log_structured.csv",
    "OpenStack": "../../../../../data/refactored_logs/OpenStack/OpenStack_2k.log_structured.csv",
    "Spark": "../../../../../data/refactored_logs/Spark/Spark_2k.log_structured.csv",
    "Windows": "../../../../../data/refactored_logs/Windows/Windows_2k.log_structured.csv",
    "Industry_Dataset": "../../../../../data/refactored_logs/Industry_Dataset/Industry_Dataset_2k.log_structured.csv",
}


def compute_accuracy(ground_truth, parsed_result):
    ground_truth_df = pd.read_csv(ground_truth)
    parsed_result_df = pd.read_csv(parsed_result)

    ground_truth_df = ground_truth_df[["EventTemplate"]]
    parsed_result_df = parsed_result_df[["EventTemplate"]]

    if METHOD == "MoLFI":
        parsed_result_df['EventTemplate'] = parsed_result_df['EventTemplate'].str.replace('#spec#', '<*>')

    return accuracy_score(ground_truth_df, parsed_result_df)


def compute_edit_distance(ground_truth, parsed_result):
    ground_truth_df = pd.read_csv(ground_truth)
    parsed_result_df = pd.read_csv(parsed_result)

    edit_distance_result = []
    for i, j in zip(np.array(ground_truth_df.EventTemplate.values, dtype='str'),
                    np.array(parsed_result_df.EventTemplate.values, dtype='str')):
        edit_distance_result.append(edit_distance(i, j))

    edit_distance_result_mean = np.mean(edit_distance_result)
    # edit_distance_result_std = np.std(edit_distance_result)

    print("Edit-distance avg:", edit_distance_result_mean)

    return edit_distance_result_mean


files_parsed = []

for file in os.listdir("final_results/{0}_results/".format(METHOD)):
    if file.endswith(".csv"):
        files_parsed.append(
            os.path.join("final_results/{0}_results/".format(METHOD), file)
        )

dsets = []

for file in files_parsed:
    dset = str(file).split("/")[-1].split("_")[0]
    if "Combine" in dset:
        dsets.append("Combined_Dataset")
    elif "Industry" in dset:
        dsets.append("Industry_Dataset")
    else:
        dsets.append(dset)

dsets = list(dict.fromkeys(dsets))

results = []
averaged_results = []

for dset in dsets:
    list_of_parsed_files_for_specific_dataset = [
        parsed_logfile_name
        for parsed_logfile_name in files_parsed
        if dset in parsed_logfile_name
    ]

    for parsed_log_file in natsorted(list_of_parsed_files_for_specific_dataset):
        print("Evaluating {0}".format(parsed_log_file))
        groundtruth = GROUND_TRUTH_FILE_PATHS["{0}".format(dset)]
        parsedresult = parsed_log_file

        # precision, reacall, F1_measure, accuracy = evaluator.evaluate(
        #     groundtruth=groundtruth, parsedresult=parsedresult
        # )
        accuracy = compute_accuracy(ground_truth=groundtruth, parsed_result=parsedresult)
        print("Accuracy is: ", accuracy, "for {0}".format(parsed_log_file))

        edit_distance_score = compute_edit_distance(ground_truth=groundtruth, parsed_result=parsedresult)
        print("Edit-distance is: ", edit_distance_score, "for {0}".format(parsed_log_file))

        # results.append([dset, precision, reacall, F1_measure, accuracy])
        results.append([dset, edit_distance_score, accuracy, accuracy, accuracy])
        print("")

t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)

res_file = str(METHOD) + "_results_" + str(current_time) + ".csv"
res_file_avg = str(METHOD) + "_avg_results_" + str(current_time) + ".csv"


def append_to_a_new_csv_file(results, new_csv_file):
    df_result = pd.DataFrame(
        results, columns=["Dataset", "Precision", "Recall", "F1_measure", "Accuracy"]
    )
    df_result = df_result.round(
        {"Precision": 3, "Recall": 3, "F1_measure": 3, "Accuracy": 3}
    )
    df_result.set_index("Dataset", inplace=True)
    df_result.to_csv(new_csv_file)
    print("Experiment results:")
    print(df_result.to_string())


def compute_overall_accuracy_measurements(results_file):
    results_file_path = results_file
    df = pd.read_csv(results_file_path)
    df_avg_res = pd.DataFrame(
        columns=[
            "Dataset",
            "Avg_Precision",
            "Avg_Recall",
            "Avg_F1_measure",
            "Avg_Accuracy",
        ]
    )

    avg_precision = (
        df.groupby(["Dataset"])["Precision"].mean().to_frame("Precision").reset_index()
    )
    avg_recall = (
        df.groupby(["Dataset"])["Recall"].mean().to_frame("Recall").reset_index()
    )
    avg_fmeasure = (
        df.groupby(["Dataset"])["F1_measure"]
        .mean()
        .to_frame("F1_measure")
        .reset_index()
    )
    avg_accuracy = (
        df.groupby(["Dataset"])["Accuracy"].mean().to_frame("Accuracy").reset_index()
    )

    temp_df1 = pd.merge(
        avg_precision, avg_recall, left_on="Dataset", right_on="Dataset", how="left"
    )
    temp_df2 = pd.merge(
        temp_df1, avg_fmeasure, left_on="Dataset", right_on="Dataset", how="left"
    )

    df_avg_res = pd.merge(
        temp_df2, avg_accuracy, left_on="Dataset", right_on="Dataset", how="left"
    )
    df_avg_res["Method"] = str(METHOD)
    df_avg_res.rename(
        columns={
            "Precision": "Avg_Precision",
            "Recall": "Avg_Recall",
            "F1_measure": "Avg_F1_measure",
            "Accuracy": "Avg_Accuracy",
        },
        inplace=True,
    )
    df_avg_res = df_avg_res[
        [
            "Dataset",
            "Avg_Precision",
            "Avg_Recall",
            "Avg_F1_measure",
            "Avg_Accuracy",
            "Method",
        ]
    ]

    print("\nAveraged results:")
    print(df_avg_res.to_string(index=False))

    return df_avg_res


append_to_a_new_csv_file(results=results, new_csv_file=res_file)

avg_res = compute_overall_accuracy_measurements(results_file=res_file)
avg_res = avg_res.round(
    {"Avg_Precision": 3, "Avg_Recall": 3, "Avg_F1_measure": 3, "Avg_Accuracy": 3}
)
avg_res.set_index("Dataset", inplace=True)
avg_res.to_csv(res_file_avg)

print(str("\nResults for each run can be found in " + str(res_file)))
print(str("Averaged results can be found in " + str(res_file_avg)))
print("")
