import pandas as pd
import numpy as np
import logging

def merge_dataframes(left: pd.DataFrame, right: pd.DataFrame, column: str, keep: str, keep_missing: str):
    """
    Merges two Pandas DataFrames
    
    Not using pd.merge due to handling of rows with empty values

    Parameters:
    left (pd.DataFrame): Path to first file
    right (pd.DataFrame): Path to second file
    column (str): Name of column to merge files on 
    keep (str): Table to keep values from when no match is found. One of ['left', 'right', 'both', 'none']. Default is 'none'
    keep_missing (str): Table to keep values from when row contains no value in given oclumn. One of ['left', 'right', 'both', 'none']. Default is 'none'
    
    Returns:
    (pd.DataFrame): Merged DataFrame

    """
    log = logging.getLogger(__name__)
    
    validate_options(left, right, column, keep, keep_missing)

    copied_from_left = set()
    outRows = []
    for index, row in left.iterrows():
        value = row[column]
        if type(value) == float and np.isnan(value):
            log.debug(f"Missing value in: left, index: {index}")
            if keep_missing in ['left', 'both']:
                outRows.append(row)
                log.debug(f"Keeping row, index: {index}")
            continue
        
        match = right[right[column] == value]
        if len(match) > 0:
            log.debug(f"Match found, index: {index}, value: {value}")
            mergedRow = pd.concat([row, match.iloc[0]])
            mergedRow = mergedRow[~mergedRow.index.duplicated()]
            outRows.append(mergedRow)
            copied_from_left.add(match.index.values[0])
        
        else:
            log.debug(f"No match found in left, {index}, value: {value}")
            if keep in ['left', 'both']:
                log.debug(f"Keeping row, index: {index}")
                outRows.append(row)

    for index, row in right.iterrows():
        if index in copied_from_left:
            continue
        value = row[column]
        if type(value) == float and np.isnan(value):
            log.debug(f"Missing value in: right, index: {index}")
            if keep_missing in ['right', 'both']:
                outRows.append(row)
                log.debug(f"Keeping row, index: {index}")
            continue

        log.debug(f"No match found in right, {index}, value: {value}")
        if keep in ['right', 'both']:
            log.debug(f"Keeping row, index: {index}")
            outRows.append(row)

    df = pd.DataFrame(outRows)
    
    return df