#!/usr/bin/env python3
"""
Retro YouTube Terminal Browser
A cyberpunk-style CLI for browsing YouTube without algorithmic interference
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import urllib.parse
import urllib.request
import re

# ANSI color codes for that retro terminal feel
class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    MATRIX = '\033[38;5;46m'  # Matrix green

def print_banner():
    """Print retro ASCII banner"""
    banner = f"""
{Colors.MATRIX}╔══════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗████████╗██████╗  ██████╗    ██╗   ██╗████████╗  ║
║  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗   ╚██╗ ██╔╝╚══██╔══╝  ║
║  ██████╔╝█████╗     ██║   ██████╔╝██║   ██║    ╚████╔╝    ██║     ║
║  ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║     ╚██╔╝     ██║     ║
║  ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝      ██║      ██║     ║
║  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝       ╚═╝      ╚═╝     ║
║                                                                      ║
║  [YOUTUBE TERMINAL BROWSER v1.0]                                    ║
║  > No algorithms. No suggestions. Just search.                      ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

class YouTubeSearcher:
    """Handle YouTube searches without the algorithm"""
    
    def __init__(self):
        self.base_url = "https://www.youtube.com"
        
    def search_videos(self, query: str, sort_by: str = 'views', max_results: int = 20) -> List[Dict]:
        """
        Search YouTube videos using yt-dlp
        sort_by: 'views', 'date', 'rating'
        """
        print(f"\n{Colors.CYAN}[SEARCHING]{Colors.RESET} Query: '{query}'")
        print(f"{Colors.DIM}Sort by: {sort_by} | Max results: {max_results}{Colors.RESET}")
        
        # Build yt-dlp command
        search_url = f"ytsearch{max_results}:{query}"
        
        # Sort options for yt-dlp
        sort_options = {
            'views': '--sort view_count',
            'date': '--sort upload_date',
            'rating': '--sort rating'
        }
        
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--flat-playlist',
            '--no-warnings',
            '--quiet'
        ]
        
        # Add sort option if available
        if sort_by in sort_options:
            cmd.extend(sort_options[sort_by].split())
            
        cmd.append(search_url)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                print(f"{Colors.RED}Error: yt-dlp not found or failed{Colors.RESET}")
                print("Install with: brew install yt-dlp")
                return []
                
            videos = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        video_data = json.loads(line)
                        videos.append(video_data)
                    except json.JSONDecodeError:
                        continue
                        
            return videos
            
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}Search timeout{Colors.RESET}")
            return []
        except FileNotFoundError:
            print(f"{Colors.RED}yt-dlp not installed!{Colors.RESET}")
            print(f"{Colors.YELLOW}Install with: brew install yt-dlp{Colors.RESET}")
            return []

def format_duration(seconds):
    """Convert seconds to human readable duration"""
    if not seconds:
        return "??:??"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def format_views(views):
    """Format view count for display"""
    if not views:
        return "?"
    views = int(views)
    if views >= 1_000_000:
        return f"{views/1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views/1_000:.1f}K"
    return str(views)

def display_results(videos: List[Dict]):
    """Display search results in retro terminal style"""
    if not videos:
        print(f"{Colors.RED}No results found{Colors.RESET}")
        return
        
    print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  # | TITLE{' '*40} | VIEWS   | DURATION{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")
    
    for idx, video in enumerate(videos, 1):
        title = video.get('title', 'Unknown')[:45]
        duration = format_duration(video.get('duration'))
        views = format_views(video.get('view_count'))
        url = video.get('url', video.get('id', ''))
        
        # Color based on view count
        if video.get('view_count') and int(video.get('view_count', 0)) > 1_000_000:
            view_color = Colors.YELLOW
        else:
            view_color = Colors.DIM
            
        print(f"{Colors.GREEN}{idx:3}{Colors.RESET} | "
              f"{title:45} | "
              f"{view_color}{views:7}{Colors.RESET} | "
              f"{Colors.CYAN}{duration:8}{Colors.RESET}")
              
    print(f"{Colors.GREEN}{'='*70}{Colors.RESET}")

def play_video(videos: List[Dict], index: int, audio_only: bool = False):
    """Play selected video using mpv or vlc"""
    if index < 1 or index > len(videos):
        print(f"{Colors.RED}Invalid selection{Colors.RESET}")
        return
        
    video = videos[index - 1]
    url = f"https://youtube.com/watch?v={video.get('id', '')}"
    title = video.get('title', 'Unknown')
    
    print(f"\n{Colors.GREEN}[LOADING]{Colors.RESET} {title}")
    
    # Try mpv first, then vlc
    players = ['mpv', 'vlc']
    player_cmd = None    
    for player in players:
        try:
            subprocess.run(['which', player], capture_output=True, check=True)
            player_cmd = player
            break
        except:
            continue
            
    if not player_cmd:
        print(f"{Colors.RED}No video player found!{Colors.RESET}")
        print(f"{Colors.YELLOW}Install with: brew install mpv{Colors.RESET}")
        print(f"\n{Colors.DIM}URL: {url}{Colors.RESET}")
        return
        
    # Build player command
    if audio_only and player_cmd == 'mpv':
        cmd = [player_cmd, '--no-video', url]
        print(f"{Colors.CYAN}[AUDIO ONLY MODE]{Colors.RESET}")
    else:
        cmd = [player_cmd, url]
        
    print(f"{Colors.GREEN}[PLAYING]{Colors.RESET} with {player_cmd}")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[STOPPED]{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Error playing video: {e}{Colors.RESET}")

def interactive_mode():
    """Interactive search and play mode"""
    print_banner()
    searcher = YouTubeSearcher()
    current_results = []    
    print(f"\n{Colors.GREEN}Commands:{Colors.RESET}")
    print(f"  {Colors.CYAN}search <query>{Colors.RESET} - Search YouTube")
    print(f"  {Colors.CYAN}play <number>{Colors.RESET} - Play video from results")
    print(f"  {Colors.CYAN}audio <number>{Colors.RESET} - Play audio only")
    print(f"  {Colors.CYAN}sort <views|date|rating>{Colors.RESET} - Change sort order")
    print(f"  {Colors.CYAN}quit{Colors.RESET} - Exit")
    
    sort_mode = 'views'
    
    while True:
        try:
            prompt = f"\n{Colors.MATRIX}[RETRO-YT]{Colors.RESET} > "
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
                
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            if command == 'quit' or command == 'exit':
                print(f"{Colors.GREEN}[SYSTEM SHUTDOWN]{Colors.RESET}")
                break
                
            elif command == 'search' and len(parts) > 1:
                query = parts[1]
                current_results = searcher.search_videos(query, sort_by=sort_mode)
                display_results(current_results)
                
            elif command == 'play' and len(parts) > 1:
                try:
                    index = int(parts[1])
                    play_video(current_results, index, audio_only=False)
                except ValueError:
                    print(f"{Colors.RED}Invalid number{Colors.RESET}")                    
            elif command == 'audio' and len(parts) > 1:
                try:
                    index = int(parts[1])
                    play_video(current_results, index, audio_only=True)
                except ValueError:
                    print(f"{Colors.RED}Invalid number{Colors.RESET}")
                    
            elif command == 'sort' and len(parts) > 1:
                new_sort = parts[1].lower()
                if new_sort in ['views', 'date', 'rating']:
                    sort_mode = new_sort
                    print(f"{Colors.GREEN}Sort mode: {sort_mode}{Colors.RESET}")
                else:
                    print(f"{Colors.RED}Invalid sort mode. Use: views, date, rating{Colors.RESET}")
                    
            elif command == 'help':
                print(f"\n{Colors.GREEN}Commands:{Colors.RESET}")
                print(f"  search <query> - Search YouTube")
                print(f"  play <number> - Play video")
                print(f"  audio <number> - Audio only")
                print(f"  sort <mode> - Change sort")
                print(f"  quit - Exit")
                
            else:
                print(f"{Colors.RED}Unknown command. Type 'help' for commands{Colors.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.RESET}")
            continue
        except EOFError:
            print(f"\n{Colors.GREEN}[EOF - SYSTEM SHUTDOWN]{Colors.RESET}")
            break
def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Retro YouTube Terminal Browser - No algorithms, just search'
    )
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('-s', '--sort', choices=['views', 'date', 'rating'], 
                       default='views', help='Sort results by')
    parser.add_argument('-n', '--number', type=int, default=20, 
                       help='Number of results')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive or not args.query:
        interactive_mode()
    else:
        # Quick search mode
        print_banner()
        searcher = YouTubeSearcher()
        results = searcher.search_videos(args.query, sort_by=args.sort, 
                                        max_results=args.number)
        display_results(results)
        
        if results:
            print(f"\n{Colors.CYAN}To play, run in interactive mode (-i) or use:{Colors.RESET}")
            print(f"  mpv 'https://youtube.com/watch?v=VIDEO_ID'")

if __name__ == "__main__":
    main()