#!/usr/bin/env python3
"""
Enhanced YouTube Search Terminal - Improved search with better relevance
"""

import json
import urllib.request
import urllib.parse
import subprocess
import sys
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

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
    U = '\033[4m'      # Underline for URLs
    LINK = '\033]8;;'  # OSC 8 hyperlink (modern terminals)
    LINK_END = '\033]8;;\033\\'

class SearchEnhancer:
    """Enhanced search strategies for better results"""
    
    @staticmethod
    def build_search_query(query: str, filters: Dict) -> str:
        """
        Build an enhanced search query with filters
        
        Filters can include:
        - duration: short (<4min), medium (4-20min), long (>20min)
        - upload_date: today, week, month, year
        - sort: relevance, views, date, rating
        - exact: True/False (use quotes for exact phrase)
        - channel: specific channel name
        - hd: True/False (HD only)
        """
        enhanced_query = query
        
        # Add quotes for exact phrase matching
        if filters.get('exact'):
            enhanced_query = f'"{query}"'
        
        # Add channel filter
        if filters.get('channel'):
            enhanced_query += f' channel:{filters["channel"]}'
        
        # Build YouTube search URL with parameters
        params = {
            'search_query': enhanced_query,
            'sp': ''  # Search parameters encoded
        }
        
        # Encode filters into sp parameter (YouTube's internal filter format)
        sp_filters = []
        
        if filters.get('upload_date'):
            date_filters = {
                'today': 'EgIIAg%3D%3D',
                'week': 'EgIIAw%3D%3D', 
                'month': 'EgIIBA%3D%3D',
                'year': 'EgIIBQ%3D%3D'
            }
            if filters['upload_date'] in date_filters:
                sp_filters.append(date_filters[filters['upload_date']])
        
        if filters.get('duration'):
            duration_filters = {
                'short': 'EgIYAQ%3D%3D',  # <4 minutes
                'medium': 'EgIYAw%3D%3D', # 4-20 minutes
                'long': 'EgIYAg%3D%3D'    # >20 minutes
            }
            if filters['duration'] in duration_filters:
                sp_filters.append(duration_filters[filters['duration']])
        
        if filters.get('hd'):
            sp_filters.append('EgIgAQ%3D%3D')  # HD filter
        
        # Sort order
        sort_filters = {
            'relevance': '',  # Default
            'date': 'CAI%3D',
            'views': 'CAM%3D',
            'rating': 'CAE%3D'
        }
        
        if filters.get('sort') and filters['sort'] in sort_filters:
            if sort_filters[filters['sort']]:
                params['sp'] = sort_filters[filters['sort']]
        
        return urllib.parse.urlencode(params)
    
    @staticmethod
    def parse_search_intent(query: str) -> Tuple[str, Dict]:
        """
        Parse user query to extract intent and modifiers
        
        Examples:
        - "python tutorial beginner" -> focuses on beginner content
        - "how to cook pasta" -> tutorial/guide content
        - "best movies 2024" -> curated/top lists
        - "music video queen" -> specific content type
        """
        filters = {}
        clean_query = query.lower()
        
        # Check for tutorial/learning intent
        tutorial_keywords = ['tutorial', 'how to', 'learn', 'beginner', 'course', 'guide', 'explained']
        if any(keyword in clean_query for keyword in tutorial_keywords):
            filters['type'] = 'educational'
            # Prefer longer videos for tutorials
            filters['duration'] = 'medium'
        
        # Check for music content
        music_keywords = ['music', 'song', 'album', 'lyrics', 'official video', 'audio']
        if any(keyword in clean_query for keyword in music_keywords):
            filters['type'] = 'music'
        
        # Check for recent content needs
        recency_keywords = ['latest', 'new', '2024', '2025', 'recent', 'today']
        if any(keyword in clean_query for keyword in recency_keywords):
            filters['upload_date'] = 'month'
            filters['sort'] = 'date'
        
        # Check for "best of" content
        if 'best' in clean_query or 'top' in clean_query:
            filters['sort'] = 'views'  # Popular content
        
        # Extract year if present
        year_match = re.search(r'\b(202[0-9])\b', query)
        if year_match:
            filters['year'] = year_match.group(1)
        
        # Check for specific duration preferences
        if 'short' in clean_query or 'quick' in clean_query:
            filters['duration'] = 'short'
        elif 'full' in clean_query or 'complete' in clean_query:
            filters['duration'] = 'long'
        
        return query, filters

def search_youtube_advanced(query: str, max_results: int = 25, filters: Optional[Dict] = None) -> List[Dict]:
    """
    Advanced YouTube search with better relevance
    """
    enhancer = SearchEnhancer()
    
    # Parse query for intent
    query, auto_filters = enhancer.parse_search_intent(query)
    
    # Merge with provided filters
    if filters:
        auto_filters.update(filters)
    filters = auto_filters
    
    # Build enhanced search URL
    search_params = enhancer.build_search_query(query, filters)
    search_url = f"https://www.youtube.com/results?{search_params}"
    
    print(f"\n{C.C}[SEARCHING]{C.X} {query}")
    if filters:
        filter_str = ', '.join([f"{k}={v}" for k, v in filters.items()])
        print(f"{C.D}Filters: {filter_str}{C.X}")
    
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
                    
                    # Extract comprehensive video information
                    video_id = video.get('videoId', '')
                    title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    
                    # Parse view count more carefully
                    view_text = video.get('viewCountText', {}).get('simpleText', '')
                    views = parse_view_count_advanced(view_text)
                    
                    # Get channel info
                    channel = video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    channel_verified = video.get('ownerBadges', [{}])[0].get('metadataBadgeRenderer', {}).get('style') == 'BADGE_STYLE_TYPE_VERIFIED'
                    
                    # Duration
                    duration = video.get('lengthText', {}).get('simpleText', '')
                    
                    # Age/upload date
                    age = video.get('publishedTimeText', {}).get('simpleText', '')
                    
                    # Description snippet
                    description = ''
                    if 'detailedMetadataSnippets' in video:
                        snippets = video.get('detailedMetadataSnippets', [])
                        if snippets:
                            description = ''.join([run.get('text', '') for run in snippets[0].get('snippetText', {}).get('runs', [])])
                    
                    video_data = {
                        'id': video_id,
                        'title': title,
                        'duration': duration,
                        'views': views,
                        'views_text': view_text,
                        'channel': channel,
                        'channel_verified': channel_verified,
                        'age': age,
                        'description': description[:100],  # First 100 chars
                        'url': f"https://youtube.com/watch?v={video_id}",
                        'short_url': f"youtu.be/{video_id}"
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

def parse_view_count_advanced(views_str: str) -> int:
    """Convert view string to integer for sorting"""
    if not views_str:
        return 0
    
    # Remove commas and "views" text
    views_str = views_str.replace(',', '').replace(' views', '').replace('watching', '').strip()
    
    # Handle live viewer counts
    if 'watching' in views_str.lower():
        views_str = views_str.replace('watching', '').strip()
    
    # Handle abbreviated numbers
    multipliers = {
        'K': 1_000,
        'M': 1_000_000,
        'B': 1_000_000_000
    }
    
    for suffix, multiplier in multipliers.items():
        if suffix in views_str:
            try:
                number = float(views_str.replace(suffix, '').strip())
                return int(number * multiplier)
            except ValueError:
                return 0
    
    # Try parsing as regular number
    try:
        return int(views_str)
    except ValueError:
        return 0

def make_clickable_url(url: str, display_text: str = None) -> str:
    """
    Make URL clickable in modern terminals that support OSC 8
    Falls back to regular colored text for older terminals
    """
    if not display_text:
        display_text = url
    
    # Try OSC 8 hyperlink (works in iTerm2, modern Terminal.app, etc.)
    # Format: ESC]8;;URL\aDisplay Text ESC]8;;\a
    clickable = f"{C.LINK}{url}{C.LINK_END}{C.M}{C.U}{display_text}{C.X}"
    
    return clickable

def display_results_enhanced(videos: List[Dict], show_descriptions: bool = False):
    """Enhanced display with clickable URLs and better formatting"""
    if not videos:
        print(f"{C.R}No results found{C.X}")
        return
    
    # Sort by views if not already sorted
    videos = sorted(videos, key=lambda x: x.get('views', 0), reverse=True)
    
    # Calculate dynamic column widths
    max_title_len = min(max(len(v['title']) for v in videos[:10]), 50)
    
    # Print header
    print(f"\n{C.G}{'═'*130}{C.X}")
    print(f"{C.B}{C.C}  # │ TITLE{' '*(max_title_len-5)} │ CHANNEL{' '*12} │ VIEWS      │ AGE        │ URL{C.X}")
    print(f"{C.G}{'═'*130}{C.X}")
    
    for idx, video in enumerate(videos, 1):
        # Format fields
        title = video['title'][:max_title_len].ljust(max_title_len)
        channel = video['channel'][:20].ljust(20)
        
        # Add verification badge if verified
        if video.get('channel_verified'):
            channel = channel.rstrip() + ' ✓'
            channel = channel.ljust(20)
        
        views_text = video.get('views_text', 'N/A')[:10].rjust(10)
        age = video['age'][:10].ljust(10) if video['age'] else 'N/A'.ljust(10)
        
        # Create clickable URL
        short_url = video['short_url']
        clickable_url = make_clickable_url(video['url'], short_url)
        
        # Color code by view count
        view_num = video.get('views', 0)
        if view_num >= 1_000_000_000:
            view_color = C.Y + C.B  # Bold yellow for billions
        elif view_num >= 1_000_000:
            view_color = C.Y  # Yellow for millions
        elif view_num >= 100_000:
            view_color = C.C  # Cyan for 100K+
        else:
            view_color = C.D  # Dim for less
        
        # Print row
        print(f"{C.G}{idx:3}{C.X} │ {title} │ {C.D}{channel}{C.X} │ {view_color}{views_text}{C.X} │ {C.D}{age}{C.X} │ {clickable_url}")
        
        # Show description snippet if enabled
        if show_descriptions and video.get('description'):
            print(f"     │ {C.D}{video['description'][:80]}...{C.X}")
    
    print(f"{C.G}{'═'*130}{C.X}")
    print(f"\n{C.D}Showing {len(videos)} results (sorted by views - highest first){C.X}")
    print(f"{C.D}Tip: URLs are clickable in modern terminals (iTerm2, Terminal.app, etc.){C.X}")

class SearchSession:
    """Manage search session with history and refinement"""
    
    def __init__(self):
        self.history = []
        self.current_results = []
        self.current_query = ""
        self.current_filters = {}
        self.result_offset = 0
    
    def search(self, query: str, filters: Optional[Dict] = None):
        """Perform a new search"""
        self.current_query = query
        self.current_filters = filters or {}
        self.result_offset = 0
        
        self.current_results = search_youtube_advanced(query, filters=filters)
        self.history.append({
            'query': query,
            'filters': filters,
            'results': len(self.current_results)
        })
        
        display_results_enhanced(self.current_results)
    
    def refine_search(self, additional_terms: str):
        """Refine current search with additional terms"""
        new_query = f"{self.current_query} {additional_terms}"
        self.search(new_query, self.current_filters)
    
    def filter_results(self, filter_type: str, value: str):
        """Apply filters to current search"""
        self.current_filters[filter_type] = value
        self.search(self.current_query, self.current_filters)
    
    def show_help(self):
        """Display advanced search help"""
        help_text = f"""
{C.G}═══ ADVANCED SEARCH COMMANDS ═══{C.X}

{C.C}Basic Commands:{C.X}
  {C.B}search <query>{C.X} - Search YouTube (auto-detects intent)
  {C.B}open <number>{C.X} - Open video in browser
  {C.B}url <number>{C.X} - Copy video URL to clipboard
  {C.B}desc{C.X} - Toggle description snippets
  {C.B}next{C.X} - Load more results
  {C.B}quit{C.X} - Exit

{C.C}Search Modifiers:{C.X}
  {C.B}exact "<phrase>"{C.X} - Search for exact phrase
  {C.B}channel:<name>{C.X} - Search within specific channel
  {C.B}refine <terms>{C.X} - Add terms to current search
  
{C.C}Filters:{C.X}
  {C.B}filter duration short|medium|long{C.X} - Video length
  {C.B}filter date today|week|month|year{C.X} - Upload date
  {C.B}filter sort views|date|relevance{C.X} - Sort order
  {C.B}filter hd{C.X} - HD videos only
  {C.B}clear filters{C.X} - Remove all filters

{C.C}Search Tips:{C.X}
  • {C.D}Use quotes for exact phrases: "python list comprehension"{C.X}
  • {C.D}Add year for recent content: "react tutorial 2024"{C.X}
  • {C.D}Use "best" or "top" for popular content{C.X}
  • {C.D}Add "beginner" or "advanced" for skill level{C.X}
  • {C.D}Include duration hints: "quick python tips" or "full course"{C.X}

{C.C}Smart Detection:{C.X}
  The search automatically detects:
  • Tutorial/educational content
  • Music videos
  • Recent/trending topics
  • "Best of" compilations
  • Preferred video duration
"""
        print(help_text)

def main():
    """Enhanced main interactive loop"""
    # Print banner
    print(f"""
{C.M}╔══════════════════════════════════════════════════════════════════════════╗
║  ██╗   ██╗████████╗    ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗ ║
║  ╚██╗ ██╔╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║ ║
║   ╚████╔╝    ██║       ███████╗█████╗  ███████║██████╔╝██║     ███████║ ║
║    ╚██╔╝     ██║       ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║ ║
║     ██║      ██║       ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║ ║
║     ╚═╝      ╚═╝       ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ║
║                                                                           ║
║  [ENHANCED SEARCH v2.0 - SMART FILTERS & CLICKABLE URLS]                 ║
╚══════════════════════════════════════════════════════════════════════════╝{C.X}
""")
    
    session = SearchSession()
    show_descriptions = False
    
    print(f"\n{C.G}Type 'help' for advanced search tips or 'search <query>' to begin{C.X}\n")
    
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
            
            elif command == 'help':
                session.show_help()
            
            elif command == 'search' and len(parts) > 1:
                query = parts[1]
                session.search(query)
            
            elif command == 'exact' and len(parts) > 1:
                # Search for exact phrase
                query = parts[1].strip('"')
                session.search(query, {'exact': True})
            
            elif command == 'refine' and len(parts) > 1:
                session.refine_search(parts[1])
            
            elif command == 'filter' and len(parts) > 1:
                filter_parts = parts[1].split(maxsplit=1)
                if len(filter_parts) >= 2:
                    filter_type, filter_value = filter_parts[0], filter_parts[1]
                    session.filter_results(filter_type, filter_value)
                elif filter_parts[0] == 'hd':
                    session.filter_results('hd', True)
            
            elif command == 'clear' and len(parts) > 1 and parts[1] == 'filters':
                session.current_filters = {}
                print(f"{C.G}Filters cleared{C.X}")
            
            elif command == 'desc':
                show_descriptions = not show_descriptions
                display_results_enhanced(session.current_results, show_descriptions)
            
            elif command in ['open', 'play'] and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(session.current_results):
                        url = session.current_results[index]['url']
                        print(f"\n{C.G}[OPENING]{C.X} {url}")
                        subprocess.run(['open', url] if sys.platform == 'darwin' else ['xdg-open', url])
                    else:
                        print(f"{C.R}Invalid video number{C.X}")
                except (ValueError, IndexError):
                    print(f"{C.R}Invalid number{C.X}")
            
            elif command == 'url' and len(parts) > 1:
                try:
                    index = int(parts[1]) - 1
                    if 0 <= index < len(session.current_results):
                        url = session.current_results[index]['url']
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
            
            else:
                # If command not recognized, treat as search query
                if command and not command.startswith('#'):
                    session.search(user_input)
        
        except KeyboardInterrupt:
            print(f"\n{C.Y}[INTERRUPTED]{C.X}")
            continue
        except EOFError:
            print(f"\n{C.G}[GOODBYE]{C.X}")
            break

if __name__ == "__main__":
    main()
