"""
iLoveExcel - Main entry point.

This module allows running the package with `python -m iLoveExcel` to start the GUI.
"""

import sys
import logging

from .gui import main_gui
from .utils import setup_logging


def main():
    """
    Main entry point for the iLoveExcel application.
    
    Starts the GUI interface.
    """
    try:
        setup_logging(level='INFO')
        logger = logging.getLogger(__name__)
        logger.info("Starting iLoveExcel GUI...")
        main_gui()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting iLoveExcel: {e}", file=sys.stderr)
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
