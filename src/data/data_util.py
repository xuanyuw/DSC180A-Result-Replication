""" This file contains functions for quality control and potential data cleaning functions"""

#import packages here
import glob
import os
import re
import zipfile
import logging

def run_fastqc(input_path, report_path, test_size=None, start_point=0, end_point=None):
    """
    Run fastqc on fastq.gz files from input_path and save reports in data/tmp/reports folder. 
    If test_size is set to None, then run fastqc on all fastq.gz files in the directory,
    run on the first n files otherwise. 
    If want to run on a certain range of files, use start_point and end_point to specify the range
    """
    logging.basicConfig(filename='fastqc_log.txt', filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG)

    all_files = sorted(glob.glob(input_path + "/*.fastq.gz"))
    os.system('mkdir -p %s' % report_path)
    if test_size == None:
        test_size = len(all_files)
    if end_point == None:
        end_point = test_size
    for i in range(start_point, end_point):
        logging.info('start processing %s'%all_files[i])
        command = '/opt/FastQC/fastqc %s -o %s' % (all_files[i], report_path)
        os.system(command)
        logging.info('finished processing %s' %all_files[i])


