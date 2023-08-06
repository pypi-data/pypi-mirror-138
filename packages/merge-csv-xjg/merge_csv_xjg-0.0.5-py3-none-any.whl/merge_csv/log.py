import logging
import sys

def configure_logging(verbose, log):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
    handler.setFormatter(formatter)
    if verbose:
        # logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
        log.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        # logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
        log.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

    log.addHandler(handler)





