import shutil
from pathlib import Path
import logging
from .log import configure_logging

def output_file(df, default_filename, output, file, inplace, backup, verbose):
    log = logging.getLogger(__name__)
    configure_logging(verbose, log)
    filename = None
    if output:
        filename = output
    elif inplace:
        filename = file
        if backup:
            backup_filename = f"{file}.bak"
            backup_path = Path(backup_filename)
            if backup_path.exists():
                counter = 0
                while True:
                    temp_filename = f"{backup_filename}{counter}"
                    backup_path = Path(temp_filename)
                    if not backup_path.exists():
                        backup_filename = temp_filename
                        break
                    counter += 1
            log.debug(f"Taking backup to {backup_filename}")
            shutil.move(file, backup_filename)
    else:
        filename = default_filename

    log.debug(f"Outputting to: {filename}")
    df.to_csv(filename, index=False)
