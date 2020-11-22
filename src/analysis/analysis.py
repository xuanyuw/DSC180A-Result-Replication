""" This file contains the essential functions for data analysis. """

#import packages here
import os
import re
import glob
import logging

def run_kallisto(input_path, quant_path, transcripts, bootstrap, test_size=None, start_point=0, end_point=None):
    """
    Run pseudo-alignment and quantification on the fastq data
    If test_size is set to None, then run fastqc on all fastq.gz files in the directory,
    run on the first n files otherwise.
    If want to run on a certain range of files, use start_point and end_point to specify the range
    """
    logging.basicConfig(filename='kallisto_log.txt', filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)
    all_files = sorted(glob.glob(input_path + "/*.fastq.gz"))
    if test_size == None:
        test_size = len(all_files)
    if end_point == None:
        end_point = test_size
    for i in range(start_point, end_point, 2):
        folder = quant_path + '/' + re.findall('srp073813/(.*)\_', all_files[i])[0]
        command = "/opt/kallisto_linux-v0.42.4/kallisto quant -i %s -o %s -b %d %s %s" \
                        % (transcripts, folder, bootstrap, all_files[i], all_files[i + 1])
        logging.info('start analysing %s' %folder )
        os.system("mkdir -p %s" % quant_path)
        os.system(command)
        logging.info('finished analysing %s' %folder )
    