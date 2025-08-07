#!/usr/bin/env python3
"""
YouTube Search with Clickable URLs - Using OSC 8 hyperlinks
"""

import json
import urllib.request
import urllib.parse
import subprocess
import sys
import re
import os
from typing import List, Dict

# ANSI colors
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

def make_hyperlink(url: str, text: str = None) -> str:
    """
    Create OSC 8 hyperlink for terminals that support it
    Works in: iTerm2, modern Terminal.app, kitty, etc.
    """
    if not text:
        text = url
    
    # Ensure URL has protocol
    if not url.startswith('http'):
        url = f"https://{url}"
    
    # OSC 8 format: ESC]8;params;URL ESC\ text ESC]8;; ESC\
    # Using ST (String Terminator) = ESC\ or BEL
    return f"\033]8;;{url}\033\\{C.M}{C.U}{text}{C.X}\033]8;;\033\\"

# Copy all the search functions from youtube_search_fixed.py
def get_terminal_width():
    """Get terminal width for proper table formatting"""
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except:
        return 120

def search_youtube_direct(query: str, max_results: int = 25) -> List[Dict]:
    """Search YouTube using their search page"""
    print(f"\n{C.C}[SEARCHING]{C.X} {query}")
    
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
                    
                    title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    view_text = video.get('viewCountText', {}).get('simpleText', '')
                    views = parse_view_count(view_text)
                    channel = video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    
                    channel_verified = False
                    if 'ownerBadges' in video:
                        for badge in video.get('ownerBadges', []):
                            if 'metadataBadgeRenderer' in badge:
                                if badge['metadataBadgeRenderer'].get('style') == 'BADGE_STYLE_TYPE_VERIFIED':
                                    channel_verified = True
                                    break
                    
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
                        'url': f"youtu.be/{video_id}",
                        'full_url': f"https://youtube.com/watch?v={video_id}"
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
    
    views_str = views_str.replace(',', '').replace(' views', '').replace('watching', '').strip()
    
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

def display_results_clickable(videos: List[Dict]):
    """Display results with clickable hyperlinks"""
    if not videos:
        print(f"{C.R}No results found{C.X}")
        return
    
    videos = sorted(videos, key=lambda x: x.get('views', 0), reverse=True)
    
    term_width = get_terminal_width()
    
    # Column widths
    col_num = 4
    col_title = 45
    col_channel = 20
    col_views = 12
    col_age = 12
    col_url = 22
    
    # Adjust for wider terminals
    extra_space = max(0, term_width - 135)
    col_title += extra_space // 2
    
    # Header
    print(f"\n{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    
    header = (
        f"{C.G}{'#':>{col_num}}{C.X} │ "
        f"{C.B}{C.C}{'TITLE':<{col_title}}{C.X} │ "
        f"{C.B}{C.C}{'CHANNEL':<{col_channel}}{C.X} │ "
        f"{C.B}{C.C}{'VIEWS':>{col_views}}{C.X} │ "
        f"{C.B}{C.C}{'AGE':<{col_age}}{C.X} │ "
        f"{C.B}{C.C}{'CLICK TO OPEN':<{col_url}}{C.X}"
    )
    print(header)
    print(f"{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    
    for idx, video in enumerate(videos, 1):
        # Prepare data
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
        
        # Create clickable hyperlink
        clickable_url = make_hyperlink(video['full_url'], video['url'])
        
        # Color code views
        if view_num >= 1_000_000:
            view_color = C.Y
        elif view_num >= 100_000:
            view_color = C.C
        else:
            view_color = ''
        
        # Format row
        row = (
            f"{C.G}{idx:>{col_num}}{C.X} │ "
            f"{title:<{col_title}} │ "
            f"{C.D}{channel:<{col_channel}}{C.X} │ "
            f"{view_color}{views_text:>{col_views}}{C.X} │ "
            f"{C.D}{age:<{col_age}}{C.X} │ "
            f"{clickable_url}"
        )
        print(row)
    
    print(f"{C.G}{'═' * min(term_width-2, 160)}{C.X}")
    print(f"\n{C.D}Showing {len(videos)} results (sorted by views){C.X}")
    print(f"{C.G}✓ URLs are clickable in supported terminals (iTerm2, modern Terminal.app, Kitty, etc.){C.X}")
    print(f"{C.D}Not working? Use 'open <number>' or 'url <number>' commands{C.X}")

def play_video(url: str):
    """Open video in browser"""
    full_url = f"https://{url}" if not url.startswith('http') else url
    print(f"\n{C.G}[OPENING]{C.X} {full_url}")
    
    if sys.platform == 'darwin':
        subprocess.run(['open', full_url])
    elif sys.platform.startswith('linux'):
        subprocess.run(['xdg-open', full_url])
    else:
        print(f"{C.Y}Please open in browser: {full_url}{C.X}")

def main():
    """Main interactive loop"""
    banner = f"""
{C.M}╔══════════════════════════════════════════════════════════════════════════╗
║  ██╗   ██╗████████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗ ║
║  ╚██╗ ██╔╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║ ║
║   ╚████╔╝    ██║       ███████╗█████╗  ███████║██████╔╝██║     ███████║ ║
║    ╚██╔╝     ██║       ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║ ║
║     ██║      ██║       ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║ ║
║     ╚═╝      ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ║
║                                                                           ║
║  [CLICKABLE URLs - NO ALGORITHMS - SORTED BY VIEWS]                      ║
╚══════════════════════════════════════════════════════════════════════════╝{C.X}
"""
    print(banner)
    
    print(f"\n{C.G}Commands:{C.X}")
    print(f"  {C.C}search <query>{C.X} - Search YouTube")
    print(f"  {C.C}open <number>{C.X} - Open video (backup if clicking doesn't work)")
    print(f"  {C.C}url <number>{C.X} - Copy URL to clipboard")
    print(f"  {C.C}quit{C.X} - Exit\n")
    
    current_results = []
    
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
                current_results = search_youtube_direct(query, max_results=20)
                display_results_clickable(current_results)
            
            elif command in ['open', 'o'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        play_video(current_results[index]['full_url'])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command in ['url', 'u'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(current_results):
                        url = current_results[index]['full_url']
                        print(f"{C.G}URL:{C.X} {url}")
                        try:
                            subprocess.run(['pbcopy'], input=url.encode(), check=True)
                            print(f"{C.D}(Copied to clipboard){C.X}")
                        except:
                            pass
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            else:
                # Treat as search
                if command and not command.startswith('#'):
                    current_results = search_youtube_direct(user_input, max_results=20)
                    display_results_clickable(current_results)
        
        except KeyboardInterrupt:
            print(f"\n{C.Y}[INTERRUPTED]{C.X}")
            continue
        except EOFError:
            print(f"\n{C.G}[GOODBYE]{C.X}")
            break

if __name__ == "__main__":
    main()
