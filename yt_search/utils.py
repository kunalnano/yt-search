"""
Utility functions and constants
"""

import os

class Colors:
    """ANSI color codes for terminal output"""
    G = '\033[92m'     # Green
    C = '\033[96m'     # Cyan
    Y = '\033[93m'     # Yellow
    R = '\033[91m'     # Red
    B = '\033[1m'      # Bold
    D = '\033[2m'      # Dim
    X = '\033[0m'      # Reset
    M = '\033[38;5;46m' # Matrix green
    U = '\033[4m'      # Underline

def get_terminal_width() -> int:
    """Get terminal width for proper table formatting"""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except:
        return 120  # Default width

def truncate_text(text: str, max_len: int) -> str:
    """Truncate text to fit within max length"""
    if len(text) <= max_len:
        return text
    return text[:max_len-2] + '..'
