#!/usr/bin/env python

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

import sys
import json
import os

sys.path.insert(0, './src/data')
sys.path.insert(0, './src/analysis')
sys.path.insert(0, './test')

from src.data.data_util import *
from src.analysis.analysis import *
from test.create_testdata import *
#from model import train


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''
    
    if 'preprocessing' in targets:
        with open('config/data_params.json') as fh:
            data_cfg = json.load(fh)
            run_fastqc(data_cfg['input_path'], data_cfg['report_path'], test_size=data_cfg['test_size'])

    if 'analysis' in targets:
        with open('config/analysis_params.json') as fh:
            analysis_cfg = json.load(fh)
            run_kallisto(analysis_cfg['input_path'], analysis_cfg['quant_path'], analysis_cfg['transcripts'], analysis_cfg['bootstrap'], analysis_cfg['test_size'])

    if 'test-data' in targets:
        with open('config/test_params.json') as fh:
            testdata_cfg = json.load(fh)
            create_dummy_data(input=testdata_cfg['input1'], output=testdata_cfg['output2'], num_lines=testdata_cfg['num_lines'])
            create_dummy_data(input=testdata_cfg['input2'], output=testdata_cfg['output2'], num_lines=testdata_cfg['num_lines'])

    if 'test-all' in targets:

        with open('config/test_params.json') as fh:
            testdata_cfg = json.load(fh)
            if not os.path.exists(testdata_cfg['input_path']):
                os.mkdir(testdata_cfg['input_path'])

            create_dummy_data(input=testdata_cfg['input1'], output=testdata_cfg['output1'], num_lines=testdata_cfg['num_lines'])
            create_dummy_data(input=testdata_cfg['input2'], output=testdata_cfg['output2'], num_lines=testdata_cfg['num_lines'])
            #run fastqc
            run_fastqc(testdata_cfg['input_path'], testdata_cfg['report_path'])
            #run kallisto
            run_kallisto(testdata_cfg['input_path'], testdata_cfg['quant_path'], testdata_cfg['transcripts'], testdata_cfg['bootstrap'])

#
    #if 'model' in targets:
    #    with open('config/model_params.json') as fh:
    #        model_cfg = json.load(fh)
#
    #    # make the data target
    #    train(data, **model_cfg)

    return


if __name__ == '__main__':
    # run via:
    # python run.py data model
    targets = sys.argv[1:]
    main(targets)