"""Merge two CSV tables based on values in a given column"""
import pandas as pd
import click
import logging
import os

from merge_csv import merge_files, validate_options

def configure_logging(verbose):
    if verbose:
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    else:
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

@click.command()
@click.option("--left-file", "-l", help="One of two CSVs to be merged")
@click.option("--right-file", "-r", help="Two of two CSVs to be merged")
@click.option("--column", "-c", help="Name of column to match entries")
@click.option("--output", "-o", help="Output file path")
@click.option("--keep", "-k", help="Table to keep values from if no match is found", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--keep-missing", help="Keep rows where value in named column is null", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--verbose", "-v", is_flag=True, help="Output extra information")
def main(left_file, right_file, column, output, keep, keep_missing, verbose):
    configure_logging(verbose)
    log = logging.getLogger(__name__)
    
    df = merge_files(left_file, right_file, column, keep, keep_missing)
    log.debug(df)
    
    log.info("Complete")
    
    if output:
        log.debug(f"Outputting to {output}")
        df.to_csv(output, index=False)
    
if __name__ == "__main__":
    exit(main())