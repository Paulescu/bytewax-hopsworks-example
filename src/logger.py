import logging
from typing import Optional

def get_console_logger(name: Optional[str] = 'tutorial') -> logging.Logger:
    
    # Create logger if it doesn't exist
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create console handler with formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add console handler to the logger
        logger.addHandler(console_handler)

    return logger

# def get_console_logger(name: Optional[str] = 'tutorial') -> logging.Logger:
#     # Create logger if it doesn't exist
#     logger = logging.getLogger(name)
#     if not logger.handlers:
#         logger.setLevel(logging.DEBUG)

#         # Check if console handler already exists
#         console_handler = next((handler for handler in logger.handlers if isinstance(handler, logging.StreamHandler)), None)

#         if console_handler is None:
#             # Create console handler with formatting
#             console_handler = logging.StreamHandler()
#             console_handler.setLevel(logging.DEBUG)
#             formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#             console_handler.setFormatter(formatter)

#             # Add console handler to the logger
#             logger.addHandler(console_handler)

#     return logger