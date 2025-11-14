"""
iLoveExcel - Main entry point.

This module allows running the package with `python -m iLoveExcel` to start the GUI.
"""

import sys
import logging
import os

from .utils import setup_logging


def check_tkinter_available():
    """
    Check if Tkinter is available.
    
    Returns:
        bool: True if Tkinter is available, False otherwise
    """
    try:
        import tkinter
        return True
    except ImportError:
        return False


def launch_gui_entry_point():
    """
    Entry point for the `iloveexcel` console command.
    
    Launches the GUI with Tkinter as default backend (no extra deps needed).
    Falls back to PySimpleGUI if specified via --gui-backend flag or ILOVEEXCEL_GUI env var.
    """
    try:
        setup_logging(level='INFO')
        logger = logging.getLogger(__name__)
        
        # Check for backend selection
        backend = os.environ.get('ILOVEEXCEL_GUI', 'tkinter').lower()
        
        # Handle command-line arguments
        if '--gui-backend' in sys.argv:
            idx = sys.argv.index('--gui-backend')
            if idx + 1 < len(sys.argv):
                backend = sys.argv[idx + 1].lower()
                # Remove the flag and value from sys.argv so GUI doesn't see them
                sys.argv.pop(idx)
                sys.argv.pop(idx)
        
        # Show help if requested
        if '--help' in sys.argv or '-h' in sys.argv:
            print("""
iLoveExcel - CSV & Excel Operations Tool

Usage:
  iloveexcel [OPTIONS]

Options:
  --gui-backend {tkinter|pysimplegui}  Choose GUI backend (default: tkinter)
  --help, -h                            Show this help message

Environment Variables:
  ILOVEEXCEL_GUI                        Set default GUI backend (tkinter or pysimplegui)

GUI Backends:
  tkinter       - Built-in, no extra dependencies needed (default)
  pysimplegui   - Requires: pip install iLoveExcel[gui_pysimplegui]

Examples:
  iloveexcel                            # Launch with Tkinter GUI
  iloveexcel --gui-backend pysimplegui  # Launch with PySimpleGUI
  export ILOVEEXCEL_GUI=tkinter         # Set default backend
  iloveexcel                            # Will use Tkinter

For CLI operations, use: csvexcel --help

Documentation: https://github.com/monkcoders/iLoveExcel
            """)
            sys.exit(0)
        
        logger.info(f"Starting iLoveExcel GUI with backend: {backend}")
        
        # Launch appropriate GUI
        if backend == 'tkinter':
            if not check_tkinter_available():
                print("Error: Tkinter is not available.", file=sys.stderr)
                print("", file=sys.stderr)
                print("Tkinter is usually included with Python, but may need system packages:", file=sys.stderr)
                print("  Ubuntu/Debian: sudo apt-get install python3-tk", file=sys.stderr)
                print("  Fedora/RHEL:   sudo dnf install python3-tkinter", file=sys.stderr)
                print("  Arch Linux:    sudo pacman -S tk", file=sys.stderr)
                print("  macOS:         Tkinter should be included with Python", file=sys.stderr)
                print("  Windows:       Tkinter should be included with Python", file=sys.stderr)
                print("", file=sys.stderr)
                print("Alternative: Use PySimpleGUI backend:", file=sys.stderr)
                print("  pip install iLoveExcel[gui_pysimplegui]", file=sys.stderr)
                print("  iloveexcel --gui-backend pysimplegui", file=sys.stderr)
                sys.exit(1)
            
            from .gui_tk import main_gui
            main_gui()
        
        elif backend == 'pysimplegui':
            try:
                from .gui_tk import main_gui
                main_gui()
            except ImportError:
                print("Error: PySimpleGUI is not installed.", file=sys.stderr)
                print("", file=sys.stderr)
                print("Install with:", file=sys.stderr)
                print("  pip install iLoveExcel[gui_pysimplegui]", file=sys.stderr)
                print("", file=sys.stderr)
                print("Alternative: Use Tkinter backend (no extra install needed):", file=sys.stderr)
                print("  iloveexcel --gui-backend tkinter", file=sys.stderr)
                sys.exit(1)
        
        else:
            print(f"Error: Unknown GUI backend: {backend}", file=sys.stderr)
            print("Available backends: tkinter, pysimplegui", file=sys.stderr)
            print("Use --help for more information", file=sys.stderr)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting iLoveExcel: {e}", file=sys.stderr)
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


def main():
    """
    Main entry point for the iLoveExcel application.
    
    Starts the GUI interface with PySimpleGUI (legacy entry point, backwards compatible).
    """
    try:
        setup_logging(level='INFO')
        logger = logging.getLogger(__name__)
        logger.info("Starting iLoveExcel GUI (legacy entry point)...")
        
        # Try PySimpleGUI first (backwards compatible)
        try:
            from .gui_tk import main_gui
            main_gui()
            # from .gui import main_gui
            # main_gui()
        except ImportError:
            # Fall back to Tkinter
            logger.info("PySimpleGUI not available, falling back to Tkinter")
            if not check_tkinter_available():
                print("Error: No GUI backend available.", file=sys.stderr)
                print("Install PySimpleGUI: pip install iLoveExcel[gui_pysimplegui]", file=sys.stderr)
                print("Or ensure Tkinter is installed (see --help for details)", file=sys.stderr)
                sys.exit(1)
            
            from .gui_tk import main_gui
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
