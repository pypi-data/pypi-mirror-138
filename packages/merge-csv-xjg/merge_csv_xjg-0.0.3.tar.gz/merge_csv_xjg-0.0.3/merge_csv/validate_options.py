import pandas as pd

def validate_options(left: pd.DataFrame, right: pd.DataFrame, column: str, keep: str, keep_missing: str) -> bool:
    log = logging.getLogger(__name__)
    # Check if column in each file 
    if column not in left.columns:
        raise ValueError(f"Column: {column}, not found in left file")

    if column not in left.columns:
        raise ValueError(f"Column: {column}, not found in right file")
    
    valid_keep_values = ['left', 'right', 'both', 'none']
    if keep not in valid_keep_values:
        raise ValueError(f"Given value for keep: {keep}, not in {valid_keep_values}")
    
    if keep_missing not in valid_keep_values:
        raise ValueError(f"Given value for keep_missing: {keep_missing}, not in {valid_keep_values}")
    
    return True
