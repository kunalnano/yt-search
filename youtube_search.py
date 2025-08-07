#!/usr/bin/env python3
import json
import sys
import re
import subprocess
from typing import Dict, List, Optional
from urllib.parse import quote
import urllib.request
import urllib.error

# ANSI Color codes for retro terminal feel
class C:
    """Terminal colors"""
    R = '\033[91m'  # Red
    G = '\033[92m'  # Green  
    Y = '\033[93m'  # Yellow
    B = '\033[94m'  # Blue
    M = '\033[38;5;46m'  # Bright Green
    C = '\033[96m'  # Cyan
    D = '\033[2m'    # Dim
    X = '\033[0m'    # Reset

def search_youtube_direct(query: str, max_results: int = 25) -> List[Dict]:
    """
    Search YouTube by making direct HTTP requests to YouTube
    Returns list of video information
    """
    try:
        print(f"\n{C.C}[SEARCHING]{C.X} {query}")
        
        # Build YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
        
        # Make request with browser-like headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        # Extract the initial data from YouTube's response
        # YouTube embeds JSON data in the HTML containing search results
        start_marker = 'var ytInitialData = '
        end_marker = ';</script>'
        
        start_idx = html_content.find(start_marker)
        if start_idx == -1:
            print(f"{C.R}Could not find YouTube data in response{C.X}")
            return []
            
        start_idx += len(start_marker)
        end_idx = html_content.find(end_marker, start_idx)
        
        if end_idx == -1:
            print(f"{C.R}Could not parse YouTube data{C.X}")
            return []
            
        json_str = html_content[start_idx:end_idx]
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"{C.R}Error parsing JSON: {e}{C.X}")
            return []
        
        # Navigate through the JSON structure to find video results
        videos = []
        try:
            contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
            
            for content in contents:
                if 'itemSectionRenderer' not in content:
                    continue
                    
                items = content['itemSectionRenderer']['contents']
                
                for item in items:
                    if 'videoRenderer' not in item:
                        continue
                        
                    video = item['videoRenderer']
                    
                    # Extract video information
                    video_data = {
                        'id': video.get('videoId', ''),
                        'title': video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown'),
                        'duration': video.get('lengthText', {}).get('simpleText', ''),
                        'views': video.get('viewCountText', {}).get('simpleText', '').replace(' views', '').replace(',', ''),
                        'channel': video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown'),
                        'age': video.get('publishedTimeText', {}).get('simpleText', ''),
                        'url': f"https://youtube.com/watch?v={video.get('videoId', '')}"
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
    if not views_str or views_str == 'N/A':
        return 0
    # Remove commas and convert
    views_str = views_str.replace(',', '').replace(' views', '')
    # Handle M (millions) and K (thousands)
    if 'M' in views_str:
        return int(float(views_str.replace('M', '')) * 1_000_000)
    elif 'K' in views_str:
        return int(float(views_str.replace('K', '')) * 1_000)
    try:
        return int(views_str)
    except:
        return 0

def display_results(videos: List[Dict], sort_by: str = 'views'):
    """Display search results in retro terminal table"""
    if not videos:
        print(f"{C.R}No results found{C.X}")
        return []  # Return empty list
    
    # Sort videos by view count (descending) by default
    if sort_by == 'views':
        videos = sorted(videos, key=lambda x: parse_view_count(x.get('views', '0')), reverse=True)
    
    # Print header with URL column
    print(f"\n{C.G}{'═'*120}{C.X}")
    print(f"{C.B}{C.C}  # │ TITLE{' '*45} │ VIEWS      │ AGE        │ URL{C.X}")
    print(f"{C.G}{'═'*120}{C.X}")
    
    for idx, video in enumerate(videos, 1):
        # Clean title of emojis and special characters for better formatting
        title = video['title']
        # Remove emojis and other Unicode characters that can mess up alignment
        # Keep only ASCII and basic Latin characters
        title = re.sub(r'[^\x00-\x7F]+', '', title)
        title = title[:50].ljust(50)  # Increased from 42 to 50 for better spacing
        
        views = video['views'][:10].rjust(10) if video['views'] else 'N/A'.rjust(10)
        age = video['age'][:10].ljust(10) if video['age'] else 'N/A'.ljust(10)
        
        # Create short URL for display
        video_id = video['url'].split('=')[-1] if '=' in video['url'] else ''
        short_url = f"youtu.be/{video_id[:11]}" if video_id else video['url'][:20]
        
        # Color code by view count
        view_num = parse_view_count(video['views'])
        if view_num >= 1_000_000:
            view_color = C.Y  # Yellow for millions
        elif view_num >= 100_000:
            view_color = C.C  # Cyan for 100K+
        else:
            view_color = C.D  # Dim for less
            
        print(f"{C.G}{idx:3}{C.X} │ {title} │ {view_color}{views}{C.X} │ {C.D}{age}{C.X} │ {C.M}{short_url}{C.X}")
        
    print(f"{C.G}{'═'*120}{C.X}")
    print(f"\n{C.D}Showing {len(videos)} results (sorted by views - highest first){C.X}")
    
    return videos  # Return the sorted list

def play_video(url: str, audio_only: bool = False):
    """Open video in browser or player"""
    print(f"\n{C.G}[OPENING]{C.X} {url}")
    
    if sys.platform == 'darwin':  # macOS
        subprocess.run(['open', url])
    elif sys.platform.startswith('linux'):
        subprocess.run(['xdg-open', url])
    else:
        print(f"{C.Y}Please open in browser: {url}{C.X}")

def main():
    """Main interactive loop"""
    # Print simplified banner
    print(f"""
{C.G}{'='*80}
 █   █ █████   ████ █████  ███  ████   ████ █   █
 █   █   █    █     █     █   █ █   █ █     █   █
  ███    █     ███  ████  █████ ████  █     █████
   █     █        █ █     █   █ █   █ █     █   █
   █     █    ████  █████ █   █ █   █  ████ █   █
{'='*80}
  [NO ALGORITHMS. JUST PURE SEARCH. SORTED BY VIEWS.]
  [FIXED TABLE FORMATTING v3.0]
{'='*80}{C.X}
""")
    
    print(f"\n{C.G}Commands:{C.X}")
    print(f"  {C.C}search <query>{C.X} - Search YouTube (auto-sorted by views)")
    print(f"  {C.C}next{C.X} - Show next 25 results")
    print(f"  {C.C}open <number>{C.X} - Open video in browser")
    print(f"  {C.C}url <number>{C.X} - Copy video URL")
    print(f"  {C.C}quit{C.X} - Exit\n")
    
    current_query = ""
    current_results = []  # Raw results
    sorted_results = []    # Sorted for display
    result_offset = 0
    
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
                
            elif command == 'search' and len(parts) > 1:
                query = parts[1]
                current_query = query
                result_offset = 0
                current_results = search_youtube_direct(query, max_results=25)
                sorted_results = display_results(current_results)  # Get sorted list
                
            elif command == 'next':
                if current_results:  # Check for results, not query
                    result_offset += 25
                    print(f"{C.Y}[Loading more results...]{C.X}")
                    # Get next batch of results
                    more_results = search_youtube_direct(current_query, max_results=25)
                    # Extend the current results list
                    current_results.extend(more_results)
                    # Display the new batch and get sorted list
                    sorted_batch = display_results(more_results)
                    sorted_results.extend(sorted_batch)
                    print(f"{C.D}Showing results {result_offset+1}-{result_offset+25}{C.X}")
                else:
                    print(f"{C.R}No search results. Search something first!{C.X}")
                
            elif command in ['open', 'play'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(sorted_results):
                        play_video(sorted_results[index]['url'])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
                    
            elif command == 'url' and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(sorted_results):
                        url = sorted_results[index]['url']
                        print(f"{C.G}URL:{C.X} {url}")
                        # Try to copy to clipboard on macOS
                        try:
                            subprocess.run(['pbcopy'], input=url.encode(), check=True)
                            print(f"{C.D}(Copied to clipboard){C.X}")
                        except:
                            pass
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
                    
            elif command == 'help':
                print(f"\n{C.G}Commands:{C.X}")
                print(f"  search <query> - Search YouTube (auto-sorted by views)")
                print(f"  next - Show next 25 results")
                print(f"  open <number> - Open in browser")
                print(f"  url <number> - Show/copy URL")
                print(f"  quit - Exit")
                print(f"\n{C.Y}Features:{C.X}")
                print(f"  • Results sorted by view count (highest first)")
                print(f"  • Direct video links shown")
                print(f"  • No algorithmic recommendations")
                
            else:
                if command and not command.startswith('#'):
                    # Treat as search query
                    current_query = user_input
                    current_results = search_youtube_direct(user_input)
                    sorted_results = display_results(current_results)
                    
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully without showing INTERRUPTED
            print()  # Just print a newline
            continue
        except EOFError:
            print(f"\n{C.G}[GOODBYE]{C.X}")
            break

if __name__ == "__main__":
    main()
