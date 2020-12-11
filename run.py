#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, './test')

from data_util import *
from analysis import *
from create_testdata import *



def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

    if 'preprocessing' in targets:
        with open('config/data_params.json') as fh:
            data_cfg = json.load(fh)
            run_fastqc(data_cfg['input_path'], data_cfg['report_path'], 
                       start_point=data_cfg['start_point'], end_point=data_cfg['end_point'])

    if 'analysis' in targets:
        with open('config/analysis_params.json') as fh:
            analysis_cfg = json.load(fh)
            run_kallisto(analysis_cfg['input_path'], analysis_cfg['quant_path'], 
                         analysis_cfg['transcripts'], analysis_cfg['bootstrap'],
            start_point= analysis_cfg['start_point'], end_point=analysis_cfg['end_point'])
            # generate gene matrix
            get_gene_matrix(analysis_cfg['quant_path'], analysis_cfg['tmp_path'], analysis_cfg['gene_naming_path'])
    
    # run DESeq analysis
    if 'DESeq' in targets:
        with open('config/analysis_params.json') as fh:
            analysis_cfg = json.load(fh)
            command2 = 'Rscript ./src/analysis/DESeq_analysis.R %s %s %s TRUE' % (analysis_cfg['img_dir'],
                                                                                  analysis_cfg['gene_matrix_path'],
                                                                                  analysis_cfg['run_table_path'])
        
        os.system(command2)
            

    if 'test' in targets:

        with open('config/test_params.json') as fh:
            testdata_cfg = json.load(fh)
            if not os.path.exists(testdata_cfg['input_path']):
                os.mkdir(testdata_cfg['input_path'])
            
            create_dummy_data(input=testdata_cfg['input1'], output=testdata_cfg['output1'], num_lines=testdata_cfg['num_lines'], output_path = testdata_cfg["output_path"])
            create_dummy_data(input=testdata_cfg['input2'], output=testdata_cfg['output2'], num_lines=testdata_cfg['num_lines'], output_path = testdata_cfg["output_path"])
            #run fastqc
            run_fastqc(testdata_cfg['input_path'], testdata_cfg['report_path'])
            #run kallisto
            run_kallisto(testdata_cfg['input_path'], testdata_cfg['quant_path'], 
                         testdata_cfg['transcripts'], testdata_cfg['bootstrap'])
            # generate pseudo gene matrix and run table
            command = 'Rscript ./test/get_test_genes.R %s %s %s %s'% (testdata_cfg['gene_matrix_path'],
                                                                      testdata_cfg['run_table_path'],
                                                                      testdata_cfg['gene_matrix_test'],
                                                                      testdata_cfg['run_table_test'])
            os.system(command)
            # run DESeq analysis
            command2 = 'Rscript ./src/analysis/DESeq_analysis.R %s %s %s TRUE' % (testdata_cfg['img_dir'], 
                                                                                  testdata_cfg['gene_matrix_test'],
                                                                                  testdata_cfg['run_table_test'])
            
            os.system(command2)


    return


if __name__ == '__main__':
    # run via:
    # python run.py data model
    targets = sys.argv[1:]
    main(targets)
