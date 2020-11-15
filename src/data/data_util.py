""" This file contains functions for quality control and potential data cleaning functions"""

#import packages here
import glob
import os
import re



def run_fastqc(input_path, report_path test_size=None):
    """
    Run fastqc on fastq.gz files from input_path and save reports in data/tmp/reports folder. 
    If test_size is set to None, then run fastqc on all fastq.gz files in the directory,
    run on the first n files otherwise.
    """
    if test_size = None:
        test_size = len(glob.glob(input_path + "/*.fastq.gz"))
    os.system("./src/data/run_fastqc.sh %s %d %s" %(input_path, test_size, report_path) )

def run_cutadapt(report_path):
    """
    Extract adapter info from fastqc reports, and run cutadapt if the adapter content is not PASS.
    (not implemented yet)
    """
    all_zip = sorted(glob.glob(report_path+'/*.zip'))
    for z in all_zip:
        f_name = re.findall('tmp/(.*)\.zip', z)[0]
        with zipfile.ZipFile(z, 'r') as zipObj:
            with zipObj.open(f_name+'/summary.txt') as f:
                adapter = f.readlines()[9]
                if adapter[:4] != b'PASS':
                    #cutadapt operations
                    pass





#def convert_to_fasta(input_path, fasta_path, test_size=None):
#    """
#    convert fastqc.gz files to fasta and save them into src/data/tmp/fasta_files.
#    If test_size is set to None, then run fastqc on all fastq.gz files in the directory,
#    run on the first n files otherwise. 
#    """
#    if not os.path.exists(fasta_path):
#        os.makedirs(fasta_path)
#    all_files = sorted(glob.glob(input_path + "/*.fastq.gz"))
#    if test_size==None:
#        test_size = len(all_files)
#    for i in range(test_size):
#        f = all_files[i]
#        f_name = re.findall('srp073813/(.*)\.fastq', f)[0]
#        fasta_name = fasta_path + '/' + f_name + '.fa'
#        os.system("gunzip -c %s | paste - - - -  | cut -f 1,2 | sed 's/^/>/'  | tr \"\t\" \"\n\"  > %s" %(f,fasta_name))

