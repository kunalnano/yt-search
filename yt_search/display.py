"""
Display functionality for terminal output
"""

import os
import sys
import subprocess
from typing import List, Dict
from .utils import Colors as C, get_terminal_width, truncate_text

class Display:
    """Handle terminal display and formatting"""
    
    def __init__(self):
        self.term_width = get_terminal_width()
    
    def show_banner(self):
        """Display the application banner"""
        banner = f"""
{C.M}╔══════════════════════════════════════════════════════════════════════════╗
║  ██╗   ██╗████████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗ ║
║  ╚██╗ ██╔╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║ ║
║   ╚████╔╝    ██║       ███████╗█████╗  ███████║██████╔╝██║     ███████║ ║
║    ╚██╔╝     ██║       ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║ ║
║     ██║      ██║       ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║ ║
║     ╚═╝      ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ║
║                                                                           ║
║  [NO ALGORITHMS. JUST PURE SEARCH. SORTED BY VIEWS.]                     ║
╚══════════════════════════════════════════════════════════════════════════╝{C.X}
"""
        print(banner)
    
    def show_results(self, videos: List[Dict]):
        """Display search results in table format"""
        if not videos:
            print(f"{C.R}No results found{C.X}")
            return
        
        # Column widths
        col_num = 4
        col_title = 45
        col_channel = 20
        col_views = 12
        col_age = 12
        col_url = 20
        
        # Adjust for wider terminals
        extra_space = max(0, self.term_width - 131)
        col_title += extra_space // 2
        
        # Header
        print(f"\n{C.G}{'═' * min(self.term_width-2, 160)}{C.X}")
        
        header = (
            f"{C.G}{'#':>{col_num}}{C.X} │ "
            f"{C.B}{C.C}{'TITLE':<{col_title}}{C.X} │ "
            f"{C.B}{C.C}{'CHANNEL':<{col_channel}}{C.X} │ "
            f"{C.B}{C.C}{'VIEWS':>{col_views}}{C.X} │ "
            f"{C.B}{C.C}{'AGE':<{col_age}}{C.X} │ "
            f"{C.B}{C.C}{'URL':<{col_url}}{C.X}"
        )
        print(header)
        print(f"{C.G}{'═' * min(self.term_width-2, 160)}{C.X}")
        
        for idx, video in enumerate(videos, 1):
            # Format data
            title = truncate_text(video['title'], col_title)
            channel = truncate_text(video['channel'], col_channel-2)
            
            if video.get('channel_verified'):
                channel = channel + ' ✓'
            
            # Format views
            view_num = video.get('views', 0)
            if view_num >= 1_000_000_000:
                views_text = f"{view_num/1_000_000_000:.1f}B"
            elif view_num >= 1_000_000:
                views_text = f"{view_num/1_000_000:.1f}M"
            elif view_num >= 1_000:
                views_text = f"{view_num/1_000:.0f}K"
            else:
                views_text = str(view_num)
            
            age = truncate_text(video['age'] if video['age'] else 'N/A', col_age)
            url = video['url']
            
            # Color code views
            if view_num >= 1_000_000:
                view_color = C.Y
            elif view_num >= 100_000:
                view_color = C.C
            else:
                view_color = ''
            
            # Print row
            row = (
                f"{C.G}{idx:>{col_num}}{C.X} │ "
                f"{title:<{col_title}} │ "
                f"{C.D}{channel:<{col_channel}}{C.X} │ "
                f"{view_color}{views_text:>{col_views}}{C.X} │ "
                f"{C.D}{age:<{col_age}}{C.X} │ "
                f"{C.M}{url:<{col_url}}{C.X}"
            )
            print(row)
        
        print(f"{C.G}{'═' * min(self.term_width-2, 160)}{C.X}")
        print(f"\n{C.D}Showing {len(videos)} results (sorted by views - highest first){C.X}")
    
    def open_video(self, video: Dict):
        """Open video in browser"""
        url = video['full_url']
        print(f"\n{C.G}[OPENING]{C.X} {url}")
        
        if sys.platform == 'darwin':
            subprocess.run(['open', url])
        elif sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', url])
        else:
            print(f"{C.Y}Please open in browser: {url}{C.X}")
    
    def copy_url(self, video: Dict):
        """Copy video URL to clipboard"""
        url = video['full_url']
        print(f"{C.G}URL:{C.X} {url}")
        
        try:
            if sys.platform == 'darwin':
                subprocess.run(['pbcopy'], input=url.encode(), check=True)
            elif sys.platform.startswith('linux'):
                subprocess.run(['xclip', '-selection', 'clipboard'], input=url.encode(), check=True)
            print(f"{C.D}(Copied to clipboard){C.X}")
        except:
            print(f"{C.D}(Copy command not available){C.X}")
    
    def show_info(self, video: Dict):
        """Show detailed video information"""
        print(f"\n{C.G}═══ VIDEO INFO ═══{C.X}")
        print(f"{C.C}Title:{C.X} {video['title']}")
        print(f"{C.C}Channel:{C.X} {video['channel']} {'✓' if video.get('channel_verified') else ''}")
        print(f"{C.C}Views:{C.X} {video.get('views_text', 'N/A')}")
        print(f"{C.C}Age:{C.X} {video.get('age', 'N/A')}")
        print(f"{C.C}Duration:{C.X} {video.get('duration', 'N/A')}")
        print(f"{C.C}URL:{C.X} {video['full_url']}")
        print(f"{C.G}═════════════════{C.X}")
    
    def show_help(self):
        """Show help information"""
        print(f"\n{C.G}Commands:{C.X}")
        print(f"  search/s <query> - Search YouTube")
        print(f"  open/o <num> - Open video")
        print(f"  url/u <num> - Copy URL")
        print(f"  info/i <num> - Video details")
        print(f"  quit/q - Exit")
