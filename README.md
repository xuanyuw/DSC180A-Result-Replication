# DSC180A-Result-Replication

This repo is for the result replication project of section B04, DSC 180A, UCSD FA20.
Source paper: Ramaker, R.C., Bowling, K.M., Lasseigne, B.N. et al. Post-mortem molecular profiling of three psychiatric disorders. Genome Med 9, 72 (2017). https://doi.org/10.1186/s13073-017-0458-5

The goal of this project is to identify post-mortem transcriptome profiles of Schizophrenia (SZ), bipolar disorder (BPD), and major depressive disorder (MDD) in RNA-Seq samples from anterior cingulate cortex (AnCg), dorsolateral prefrontal cortex (DLPFC), and nucleus accumbens (nAcc) regions.

The report of this replication project is located in folder notebooks/

## Structure of the project

--config (the parameters of analysis, data, and model)
--notebooks (the jupyter notebooks of the reports)
--references (references to the publications and tools used in this project)
--src (the toolbox python and R files of analysis and data)
    --analysis
    --data

## How to run the project

If wish to run the complete pipeline using origional dataset, simply run the run.py file using command: **python3 run.py preprocessing analysis**

If wish to run part of the pipeline, please append only the module of choice after python3 run.py, e.g. **python3 run.py preprocessing** will run the steps from raw data to processed data.

If wish to run the complete pipeline on dummy test data only, please use the command: **python3 run.py test**


## Team
Brandon Tsui
Xuanyu Wu