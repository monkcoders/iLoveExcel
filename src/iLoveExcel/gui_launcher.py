"""
iLoveExcel - GUI Launcher.

Provides backend selection for PySimpleGUI or Tkinter GUI.
"""

import logging
import os
import sys

logger = logging.getLogger(__name__)


def launch_gui(backend: str = None):
    """
    Launch the GUI with specified backend.
    
    Args:
        backend: GUI backend to use ('pysimplegui', 'tkinter', or None for auto-select)
                 If None, will check ILOVEEXCEL_GUI environment variable, then default to PySimpleGUI
    
    Raises:
        ImportError: If the specified backend is not available
        ValueError: If an invalid backend is specified
    """
    # Determine backend
    if backend is None:
        backend = os.environ.get('ILOVEEXCEL_GUI', 'pysimplegui').lower()
    
    backend = backend.lower().strip()
    
    if backend not in ['pysimplegui', 'tkinter']:
        raise ValueError(f"Invalid GUI backend: {backend}. Must be 'pysimplegui' or 'tkinter'")
    
    logger.info(f"Launching GUI with backend: {backend}")
    
    if backend == 'pysimplegui':
        try:
            from .gui import main_gui
            logger.info("Using PySimpleGUI backend")
            main_gui()
        except ImportError as e:
            logger.error(f"PySimpleGUI backend not available: {e}")
            print(f"Error: PySimpleGUI backend not available: {e}")
            print("Install with: pip install PySimpleGUI")
            print("Or use Tkinter backend with: --gui-backend tkinter")
            sys.exit(1)
    
    elif backend == 'tkinter':
        try:
            from .gui_tk import main_gui
            logger.info("Using Tkinter backend")
            main_gui()
        except ImportError as e:
            logger.error(f"Tkinter backend not available: {e}")
            print(f"Error: Tkinter backend not available: {e}")
            print("Note: Tkinter should be included with Python by default")
            sys.exit(1)


def get_available_backends():
    """
    Get list of available GUI backends.
    
    Returns:
        List of available backend names
    """
    available = []
    
    try:
        import PySimpleGUI
        available.append('pysimplegui')
    except ImportError:
        pass
    
    try:
        import tkinter
        available.append('tkinter')
    except ImportError:
        pass
    
    return available


def print_backend_info():
    """Print information about available GUI backends."""
    available = get_available_backends()
    
    print("Available GUI Backends:")
    print("-" * 50)
    
    if 'pysimplegui' in available:
        try:
            import PySimpleGUI as sg
            version = getattr(sg, '__version__', 'unknown')
            print(f"✓ PySimpleGUI (version {version})")
        except:
            print("✓ PySimpleGUI")
    else:
        print("✗ PySimpleGUI (not installed)")
    
    if 'tkinter' in available:
        try:
            import tkinter
            version = tkinter.TkVersion
            print(f"✓ Tkinter (version {version})")
        except:
            print("✓ Tkinter")
    else:
        print("✗ Tkinter (not installed)")
    
    print("-" * 50)
    
    if available:
        print(f"\nDefault backend: {os.environ.get('ILOVEEXCEL_GUI', 'pysimplegui')}")
        print("\nTo change default, set ILOVEEXCEL_GUI environment variable:")
        print("  export ILOVEEXCEL_GUI=tkinter    (Linux/macOS)")
        print("  set ILOVEEXCEL_GUI=tkinter        (Windows)")
    else:
        print("\n⚠ No GUI backends available!")
        print("Install PySimpleGUI: pip install PySimpleGUI")
        print("Or ensure Tkinter is installed with your Python distribution")


if __name__ == '__main__':
    # For testing
    print_backend_info()
