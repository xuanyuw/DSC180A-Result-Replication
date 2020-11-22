#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')

from data_util import *
from analysis import *
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
            run_fastqc(data_cfg['input_path'], data_cfg['report_path'], start_point=data_cfg['start_point'], end_point=data_cfg['end_point'])

    if 'analysis' in targets:
        with open('config/analysis_params.json') as fh:
            analysis_cfg = json.load(fh)
            run_kallisto(analysis_cfg['input_path'], analysis_cfg['quant_path'], analysis_cfg['transcripts'], analysis_cfg['bootstrap'],
            start_point= analysis_cfg['start_point'], end_point=analysis_cfg['end_point'])
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