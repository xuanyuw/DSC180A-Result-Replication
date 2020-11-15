""" This file contains the essential functions for data analysis. """

#import packages here
import os
import re
import glob

def run_kallisto(input_path, quant_path, transcripts, bootstrap, test_size=None)
    """
    Run pseudo-alignment and quantification on the fastq data
    If test_size is set to None, then run fastqc on all fastq.gz files in the directory,
    run on the first n files otherwise.
    """
    all_files = sorted(glob.glob(input_path + "/*.fastq.gz"))
    if test_size == None:
        test_size = len(all_files)
    for i in range(0, test_size, 2):
        folder = quant_path + '/' + re.findall('srp073813/(.*)\_', all_files[i])[0]
        command = "/opt/kallisto_linux-v0.42.4/kallisto quant -i %s -o %s -b %d %s %s" \
                        % (transcripts, folder, bootstrap, all_files[i], all_files[i+1])
        os.system("mkdir -p %s" %quant_path)
        os.system(command)
    