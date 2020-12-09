""" This file contains the essential functions for data analysis. """

#import packages here
import os
import re
import glob
import logging
import pandas as pd


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

def get_gene_matrix(quant_path, tmp_path, gene_naming_path):
    """
    collect the estimated counts from kallisto outputs, remove X and Y chromosomes, and save the output to ./data/tmp/
    output: gene matrix with rows representing each gene and columns representing each sample
    """
    all_tsv = glob.glob('%s*/*.tsv' %quant_path)
    df_li = []
    for f in all_tsv:
        df_name = re.findall('quant/(.*)/abundance.tsv', f)[0]
        df = pd.read_csv(f, sep="\t", usecols = ['target_id','est_counts'], index_col = 'target_id')
        df = df.rename(columns={'est_counts': df_name})
        df_li.append(df)
        
    all_cnts = pd.concat(df_li, axis=1)
    gene_naming = pd.read_csv(gene_naming_path)
    non_xy = gene_naming[~gene_naming.chr.isin(['chrX', 'chrY'])].refseq
    cleaned_cnts = all_cnts[all_cnts.index.isin(non_xy)]
    cleaned_cnts.to_csv('%sgene_matrix.csv'%tmp_path)