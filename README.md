# DSC180A-Result-Replication

This repo is for the result replication project of section B04, DSC 180A, UCSD FA20.
Source paper: Ramaker, R.C., Bowling, K.M., Lasseigne, B.N. et al. Post-mortem molecular profiling of three psychiatric disorders. Genome Med 9, 72 (2017). https://doi.org/10.1186/s13073-017-0458-5

The goal of this project is to identify post-mortem transcriptome profiles of Schizophrenia (SZ), bipolar disorder (BPD), and major depressive disorder (MDD) in RNA-Seq samples from anterior cingulate cortex (AnCg), dorsolateral prefrontal cortex (DLPFC), and nucleus accumbens (nAcc) regions.

## Structure of the project

--config (the parameters of analysis, data, and model)
--notebooks (the jupyter notebook of the report)
--references (references to the publications and tools used in this project)
--src (the toolbox python files of analysis, data, and model)
    --analysis
    --data
    --model

## How to run the project

Simply run the **run.py** file using command: run.py data analysis model

* Update 10/26/2020: only implemented the framework that loops through the existing files from the input directory. Will use this framework to process data later.

## Team
Brandon Tsui
Xuanyu Wu