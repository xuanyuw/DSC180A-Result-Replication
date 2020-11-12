""" This file contains functions for data mining"""

#import packages here
import glob

#def get_data(input_path, out_path=None):
#    """
#    Get data from the website and return data. If out_path is not None, then save data to out_path.
#    """
#    all_files = glob.glob(input_path + "/*.fastq.gz")
#    for i in all_files:
#        print('loading file: %s' %i)
#        # place holder: convert data format using fastq_dump here
#        print('converting to fastq...')
#        # place holder: pre-processing using catadapt
#        print('catadapt WIP...')
#    
#    data = None # save converted data here
#
#    if out_path is not None:
#        pass  #write data
#
#    return data

def run_fastqc(input_path, tmp_path, test_size=None):
    all_files = sorted(glob.glob(input_path + "/*.fastq.gz"))
    if test_size==None:
        test_size = len(all_files)
    for i in range(test_size):
        os.system("/opt/FastQC/fastqc %s -o %s" %all_files[i] %tmp_path)

#def run_cutadapt(tmp_path)