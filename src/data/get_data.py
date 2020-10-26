""" This file contains functions for data mining"""

#import packages here
import glob

def get_data(input_path, out_path=None):
    """
    Get data from the website and return data. If out_path is not None, then save data to out_path.
    """
    all_files = glob.glob(input_path + "/*.1")
    for i in all_files:
        # convert data format using fastq_dump here
        
        print(i) #only to test the functionality, will be deleted later

    data = None # save converted data here

    if out_path is not None:
        pass  #write data

    return data
