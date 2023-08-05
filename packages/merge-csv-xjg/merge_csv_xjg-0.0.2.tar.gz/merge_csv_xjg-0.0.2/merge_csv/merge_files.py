import pandas as pd
import logging

from . import merge_dataframes

def merge_files(left_file: str, right_file: str, column: str, keep: str = 'none', keep_missing: str = 'none') -> pd.DataFrame:
    """
    Merges two csv files 
    Parameters:
    left_file (str): Path to first file
    right_file (str): Path to second file
    column (str): Name of column to merge files on 
    keep (str): Table to keep values from when no match is found. One of ['left', 'right', 'both', 'none']. Default is 'none'
    keep_missing (str): Table to keep values from when row contains no value in given oclumn. One of ['left', 'right', 'both', 'none']. Default is 'none'
    
    Returns:
    (pd.DataFrame): Merged DataFrame

    """
    log = logging.getLogger(__name__)

    dfLeft = pd.read_csv(left_file)
    dfRight = pd.read_csv(right_file)

    validate_options(dfLeft, dfRight, column, keep, keep_missing)
    
    log.info("Starting Merge")
    return merge_data_frames(dfLeft, dfRight, column, keep, keep_missing)