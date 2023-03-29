import logging

def get_logger() -> logging.Logger:
    """_summary_

    Returns:
        logging.Logger: _description_
    """
    logger = logging.getLogger('dataflow')
    logger.setLevel(logging.INFO)
    return logger
