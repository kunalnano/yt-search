#!/usr/bin/env python3
"""
Fixed YouTube Search Terminal - Better table formatting and clickable URLs
"""

import json
import urllib.request
import urllib.parse
import subprocess
import sys
import re
import os
from typing import List, Dict, Optional

# ANSI colors for retro terminal aesthetics
class C:
    G = '\033[92m'     # Green
    C = '\033[96m'     # Cyan
    Y = '\033[93m'     # Yellow
    R = '\033[91m'     # Red
    B = '\033[1m'      # Bold
    D = '\033[2m'      # Dim
    X = '\033[0m'      # Reset
    M = '\033[38;5;46m' # Matrix green
    U = '\033[4m'      # Underline

def get_terminal_width():
    """Get terminal width for proper table formatting"""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except:
        return 120  # Default width

def search_youtube_direct(query: str, max_results: int = 25) -> List[Dict]:
    """
    Search YouTube using their search page
    Returns list of video data dictionaries
    """
    print(f"\n{C.C}[SEARCHING]{C.X} {query}")
    
    # URL encode the query
    query_encoded = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={query_encoded}"
    
    try:
        req = urllib.request.Request(
            search_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Extract video data from HTML
        pattern = r'var ytInitialData = ({.*?});'
        match = re.search(pattern, html)
        
        if not match:
            print(f"{C.R}Could not parse YouTube response{C.X}")
            return []
        
        data = json.loads(match.group(1))
        videos = []
        
        try:
            contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
            
            for content in contents:
                if 'itemSectionRenderer' not in content:
                    continue
                
                for item in content['itemSectionRenderer']['contents']:
                    if 'videoRenderer' not in item:
                        continue
                    
                    video = item['videoRenderer']
                    video_id = video.get('videoId', '')
                    
                    # Extract video information
                    title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    
                    # Parse view count
                    view_text = video.get('viewCountText', {}).get('simpleText', '')
                    views = parse_view_count(view_text)
                    
                    # Channel info
                    channel = video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    channel_verified = False
                    if 'ownerBadges' in video:
                        for badge in video.get('ownerBadges', []):
                            if 'metadataBadgeRenderer' in badge:
                                if badge['metadataBadgeRenderer'].get('style') == 'BADGE_STYLE_TYPE_VERIFIED':
                                    channel_verified = True
                                    break
                    
                    # Duration and age
                    duration = video.get('lengthText', {}).get('simpleText', '')
                    age = video.get('publishedTimeText', {}).get('simpleText', '')
                    
                    video_data = {
                        'id': video_id,
                        'title': title,
                        'duration': duration,
                        'views': views,
                        'views_text': view_text,
                        'channel': channel,
                        'channel_verified': channel_verified,
                        'age': age,
                        'url': f"youtu.be/{video_id}"
                    }
                    
                    videos.append(video_data)
                    
                    if len(videos) >= max_results:
                        return videos
        
        except KeyError as e:
            print(f"{C.R}Error parsing YouTube data: {e}{C.X}")
            return []
        
        return videos
        
    except Exception as e:
        print(f"{C.R}Error searching YouTube: {e}{C.X}")
        return []

def parse_view_count(views_str: str) -> int:
    """Convert view string to integer for sorting"""
    if not views_str:
        return 0
    
    # Clean the string
    views_str = views_str.replace(',', '').replace(' views', '').replace('watching', '').strip()
    
    # Handle abbreviated numbers
    if 'M' in views_str:
        return int(float(views_str.replace('M', '')) * 1_000_000)
    elif 'K' in views_str:
        return int(float(views_str.replace('K', '')) * 1_000)
    
    try:
        return int(views_str)
    except:
        return 0

def truncate_text(text: str, max_len: int) -> str:
    """Truncate text to fit within max length"""
    if len(text) <= max_len:
        return text
    return text[:max_len-2] + '..'

def display_results_fixed(videos: List[Dict]):
    """Display results with fixed table formatting"""
    if not videos:
        print(f"{C.R}No results found{C.X}")
        return
    
    # Sort by views
    videos = sorted(videos, key=lambda x: x.get('views', 0), reverse=True)
    
    # Get terminal width
    term_width = get_terminal_width()
    
    # Fixed column widths for better alignment
    # Allocate space: # (4) + Title (45) + Channel (20) + Views (12) + Age (12) + URL (20) = 113
    # Add separators: 6 * 3 = 18
    # Total minimum: 131 chars
    
    col_num = 4
    col_title = 45
    col_channel = 20
    col_views = 12
    col_age = 12
    col_url = 20
    
    # If terminal is wider, give more space to title
    extra_space = max(0, term_width - 131)
    col_title += extra_space // 2
    col_url += extra_space // 4
    
    # Print header with proper spacing
    print(f"\n{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    
    # Header row
    header = (
        f"{C.G}{'#':>{col_num}}{C.X} │ "
        f"{C.B}{C.C}{'TITLE':<{col_title}}{C.X} │ "
        f"{C.B}{C.C}{'CHANNEL':<{col_channel}}{C.X} │ "
        f"{C.B}{C.C}{'VIEWS':>{col_views}}{C.X} │ "
        f"{C.B}{C.C}{'AGE':<{col_age}}{C.X} │ "
        f"{C.B}{C.C}{'URL':<{col_url}}{C.X}"
    )
    print(header)
    print(f"{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    
    for idx, video in enumerate(videos, 1):
        # Prepare data
        title = truncate_text(video['title'], col_title)
        channel = truncate_text(video['channel'], col_channel-2)  # -2 for potential ✓
        
        # Add verification badge
        if video.get('channel_verified'):
            channel = channel + ' ✓'
        
        views_text = video.get('views_text', 'N/A')
        if len(views_text) > col_views:
            # Shorten large numbers
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
        view_num = video.get('views', 0)
        if view_num >= 1_000_000:
            view_color = C.Y  # Yellow for millions
        elif view_num >= 100_000:
            view_color = C.C  # Cyan for 100K+
        else:
            view_color = ''   # Normal for less
        
        # Format row with proper spacing
        row = (
            f"{C.G}{idx:>{col_num}}{C.X} │ "
            f"{title:<{col_title}} │ "
            f"{C.D}{channel:<{col_channel}}{C.X} │ "
            f"{view_color}{views_text:>{col_views}}{C.X} │ "
            f"{C.D}{age:<{col_age}}{C.X} │ "
            f"{C.M}{url:<{col_url}}{C.X}"
        )
        print(row)
    
    print(f"{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    print(f"\n{C.D}Showing {len(videos)} results (sorted by views - highest first){C.X}")
    print(f"{C.D}Tip: Copy URLs with 'url <number>' command{C.X}")

def play_video(url: str):
    """Open video in browser"""
    full_url = f"https://{url}" if not url.startswith('http') else url
    print(f"\n{C.G}[OPENING]{C.X} {full_url}")
    
    if sys.platform == 'darwin':  # macOS
        subprocess.run(['open', full_url])
    elif sys.platform.startswith('linux'):
        subprocess.run(['xdg-open', full_url])
    else:
        print(f"{C.Y}Please open in browser: {full_url}{C.X}")

def main():
    """Main interactive loop"""
    # Print banner
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
║  [FIXED TABLE FORMATTING v3.0]                                           ║
╚══════════════════════════════════════════════════════════════════════════╝{C.X}
"""
    print(banner)
    
    print(f"\n{C.G}Commands:{C.X}")
    print(f"  {C.C}search <query>{C.X} - Search YouTube (auto-sorted by views)")
    print(f"  {C.C}s <query>{C.X} - Short alias for search")
    print(f"  {C.C}open <number>{C.X} - Open video in browser")
    print(f"  {C.C}url <number>{C.X} - Copy video URL to clipboard")
    print(f"  {C.C}info <number>{C.X} - Show full video details")
    print(f"  {C.C}quit{C.X} - Exit\n")
    
    current_results = []
    current_query = ""
    
    while True:
        try:
            prompt = f"{C.M}[YT-SEARCH]{C.X} > "
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command in ['quit', 'exit', 'q']:
                print(f"{C.G}[GOODBYE]{C.X}")
                break
            
            elif command in ['search', 's'] and len(parts) > 1:
                query = parts[1]
                current_query = query
                current_results = search_youtube_direct(query, max_results=20)
                display_results_fixed(current_results)
            
            elif command in ['open', 'o', 'play', 'p'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        play_video(current_results[index]['url'])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command in ['url', 'u'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        url = f"https://{current_results[index]['url']}"
                        print(f"{C.G}URL:{C.X} {url}")
                        # Copy to clipboard on macOS
                        try:
                            subprocess.run(['pbcopy'], input=url.encode(), check=True)
                            print(f"{C.D}(Copied to clipboard){C.X}")
                        except:
                            pass
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command in ['info', 'i'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        video = current_results[index]
                        print(f"\n{C.G}═══ VIDEO INFO ═══{C.X}")
                        print(f"{C.C}Title:{C.X} {video['title']}")
                        print(f"{C.C}Channel:{C.X} {video['channel']} {'✓' if video.get('channel_verified') else ''}")
                        print(f"{C.C}Views:{C.X} {video.get('views_text', 'N/A')}")
                        print(f"{C.C}Age:{C.X} {video.get('age', 'N/A')}")
                        print(f"{C.C}Duration:{C.X} {video.get('duration', 'N/A')}")
                        print(f"{C.C}URL:{C.X} https://{video['url']}")
                        print(f"{C.G}═════════════════{C.X}")
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command == 'help':
                print(f"\n{C.G}Commands:{C.X}")
                print(f"  search/s <query> - Search YouTube")
                print(f"  open/o <num> - Open video")
                print(f"  url/u <num> - Copy URL")
                print(f"  info/i <num> - Video details")
                print(f"  quit/q - Exit")
            
            else:
                # Treat as search query if not a command
                if command and not command.startswith('#'):
                    current_results = search_youtube_direct(user_input, max_results=20)
                    display_results_fixed(current_results)
        
        except KeyboardInterrupt:
            print(f"\n{C.Y}[INTERRUPTED]{C.X}")
            continue
        except EOFError:
            print(f"\n{C.G}[GOODBYE]{C.X}")
            break

if __name__ == "__main__":
    main()
