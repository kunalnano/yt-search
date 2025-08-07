"""
YT-Search: Algorithm-free YouTube terminal browser
"""

__version__ = "1.0.0"
__author__ = "Al Sharma"
__description__ = "YouTube as a library, not an engagement trap"

from .main import main
from .search import YouTubeSearcher
from .display import Display

__all__ = ['main', 'YouTubeSearcher', 'Display']
