"""Merge two CSV tables based on values in a given column"""
import click
import logging

from .merge_files import merge_files
from .log import configure_logging
from .output_file import output_file

@click.command()
@click.option("--left-file", "-l", help="One of two CSVs to be merged")
@click.option("--right-file", "-r", help="Two of two CSVs to be merged")
@click.option("--columns", "-c", help="Names of columns to match entries", callback=lambda ctx, param, value: list(map(lambda column: column.strip(), value.split(","))))
@click.option("--output", "-o", help="Output file path")
@click.option("--keep", "-k", help="Table to keep values from if no match is found", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--keep-missing", help="Keep rows where value in named column is null", type=click.Choice(['left', 'right', 'both', 'none']), default="none")
@click.option("--verbose", "-v", is_flag=True, help="Output extra information")
@click.option("--in-place", "-i", is_flag=True, help="Overwrite input file")
@click.option("--backup", "-b", is_flag=True, help="Backup file before overwriting")
def main(left_file, right_file, columns, output, keep, keep_missing, verbose, in_place, backup):
    log = logging.getLogger(__name__)
    configure_logging(verbose, log)
    
    df = merge_files(left_file, right_file, columns, keep, keep_missing)
    log.debug(df)
    
    output_file(df, "merged.csv", output, left_file, in_place, backup, verbose)
    log.info("Complete")
    
exit(main())