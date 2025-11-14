"""
iLoveExcel - GUI Launcher (Tkinter-only).

Provides Tkinter GUI backend. PySimpleGUI support has been removed.
Streamlit is available via streamlit_app.py but not launched from this module.
"""

import logging
import os
import sys

logger = logging.getLogger(__name__)


def launch_gui(backend: str = None):
    """
    Launch the GUI with Tkinter backend.
    
    Args:
        backend: GUI backend to use ('tkinter' or None for default)
                 If None, will default to 'tkinter'
                 
                 Note: PySimpleGUI support has been removed.
                 For Streamlit, use: streamlit run streamlit_app.py
    
    Raises:
        ImportError: If Tkinter is not available
        ValueError: If an invalid backend is specified
    """
    # Determine backend
    if backend is None:
        backend = os.environ.get('ILOVEEXCEL_GUI', 'tkinter').lower()
    
    backend = backend.lower().strip()
    
    # Only tkinter is supported now
    if backend != 'tkinter':
        logger.warning(f"Unsupported GUI backend: {backend}. Using tkinter instead.")
        print(f"Warning: Backend '{backend}' is not supported. Using Tkinter.", file=sys.stderr)
        backend = 'tkinter'
    
    logger.info(f"Launching GUI with backend: {backend}")
    
    # Launch Tkinter GUI
    try:
        from .gui_tk import main_gui
        logger.info("Using Tkinter backend")
        main_gui()
    except ImportError as e:
        logger.error(f"Tkinter backend not available: {e}")
        print(f"Error: Tkinter is not available: {e}", file=sys.stderr)
        print("\nTkinter should be included with Python by default.", file=sys.stderr)
        print("On Linux, install with:", file=sys.stderr)
        print("  Ubuntu/Debian: sudo apt-get install python3-tk", file=sys.stderr)
        print("  Fedora/RHEL:   sudo dnf install python3-tkinter", file=sys.stderr)
        print("  Arch Linux:    sudo pacman -S tk", file=sys.stderr)
        sys.exit(1)


def get_available_backends():
    """
    Get list of available GUI backends.
    
    Returns:
        List of available backend names (currently only 'tkinter')
    """
    available = []
    
    try:
        import tkinter
        available.append('tkinter')
    except ImportError:
        pass
    
    return available


def print_backend_info():
    """Print information about available GUI backends."""
    available = get_available_backends()
    
    print("Available GUI Backend:")
    print("-" * 50)
    
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
        print("\nNote: Tkinter is the only supported GUI backend.")
        print("For web interface, use: streamlit run streamlit_app.py")
    else:
        print("\n⚠ Tkinter not available!")
        print("On Linux, install with:")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  Fedora/RHEL:   sudo dnf install python3-tkinter")
        print("  Arch Linux:    sudo pacman -S tk")


if __name__ == '__main__':
    # For testing
    print_backend_info()
