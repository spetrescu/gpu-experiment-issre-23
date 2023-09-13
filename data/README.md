# Data
This directory contains all data used for experiments.

## `entity_dataset/`
This directory contains a dataset for training and evaluating entity parsing methods. The dataset can be found under `entity_dataset/entity_dataset.csv`

### Description
This dataset was created by mapping six software repositories' software code to their respective runtime logs.

### Overall stats
```html
|   No. labeled entries  |      Entity types       |                  Systems analyzed                    |
-----------------------------------------------------------------------------------------------------------
|          203803        |  GENERIC_TYPE, ID, PATH  |  Hadoop, Spark, Zookeeper, OpenStack, Linux, Apache  |
-----------------------------------------------------------------------------------------------------------
```

### Csv columns in dataset
```html
Column no.  |         Column name            |      Description                                                   |
-------------------------------------------------------------------------------------------------------------------
 1.         |         runtime_log            |   Contains raw log                                                 |
 2.         |         ground_truth           |   Contains the mined underlying logging statement                  |
 3.         |      entity_log_template       |   Contains the generated log template with entites                 |
 4.         |   variable_entity_type_array   |   Contains the generated log template only with generic entities   |
-------------------------------------------------------------
```
### Entity types considered
```html
No. |     TYPES      |                     Example(s)                       |  Ground truth labels |
-----------------------------------------------------------------------------------------------------
 1  |   GENERIC_TYPE  |             specs, range, targetAddr                 |        YES           |
 2  |     PATH        |      basePath, dataPath, filePath, filePath2         |        YES           |
 3  |     ID          |      reduceId, resID1, responseId, threadId          |        YES           |
 4  |     FILE        |      destFiles, editFile, hostsFile, outputFile      |         NO           |
 5  |     PRIORITY    |   avgRespTimePriority, callVolumePriority, priority  |         NO           |
 -----------------------------------------------------------------------------------------------------
```

### Sources for building the dataset
1. Hadoop (Distributed System) [Code](https://github.com/apache/hadoop)
2. Spark (Distributed System) [Code](https://github.com/apache/spark)
3. Zookeeper (Distributed System) [Code](https://github.com/apache/zookeeper)
4. OpenStack (Distributed System) [Code](https://github.com/openstack/)
5. Linux (Operating System) [Code](https://github.com/torvalds/linux)
6. Apache (Server Application) [Code](https://github.com/apache/httpd)


## `logs/` and `refactored_logs/`
For running log parsing experiments, we used nine publicly available datasets:
1. `Apache`
2. `BGL`
3. `HDFS`
4. `HealthApp`
5. `HPC`
6. `Mac`
7. `OpenStack`
8. `Spark`
9. `Windows`

Each of the datasets was accompanied by three files, namely:
1. \<`DATASET`>_2k.log -> containing 2k logs.
2. \<`DATASET`>_2k.log_structured.csv -> Containing 2k logs with their respective labels.
3. \<`DATASET`>_2k.log_templates.csv -> Containing the templates found in the dataset. For example, if a dataset has 30 templates, their list can be found in this file.

For example, the `Apache` dataset has three files associated with it, namely:
1. Apache_2k.log
2. Apache_2k.log_structured.csv
3. Apache_2k.log_templates.csv

To create a workflow that processes all log datasets, we modified the publicly available datasets by reorganizing them and excluding information considered out of scope. More details about this can be found in `refactor_log_data/`. Additionally, we created a dataset that combined all the datasets, the `Combined_Dataset`.
