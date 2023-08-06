# Merge CSV

Simple package for merging two CSV files with pandas based on values in a given column. 

This module is required over pd.merge due to proper handling of rows with empty values. 

# Install

`pip install merge_csv_xjg`

# Usage

## As CLI Tool

```
Usage: merge_csv [OPTIONS]

Options:
  -l, --left-file TEXT            One of two CSVs to be merged
  -r, --right-file TEXT           Two of two CSVs to be merged
  -c, --column TEXT               Name of column to match entries
  -o, --output TEXT               Output file path
  -k, --keep [left|right|both|none]
                                  Table to keep values from if no match is
                                  found
  --keep-missing [left|right|both|none]
                                  Keep rows where value in named column is
                                  null
  -v, --verbose                   Output extra information
  --help                          Show this message and exit.
```