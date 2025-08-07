"""
YouTube search functionality
"""

import json
import urllib.request
import urllib.parse
import re
from typing import List, Dict

class YouTubeSearcher:
    """Handle YouTube searches without the algorithm"""
    
    def __init__(self):
        self.base_url = "https://www.youtube.com"
    
    def search(self, query: str, max_results: int = 20) -> List[Dict]:
        """
        Search YouTube and return video data
        """
        query_encoded = urllib.parse.quote(query)
        search_url = f"{self.base_url}/results?search_query={query_encoded}"
        
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
            
            # Extract initial data
            pattern = r'var ytInitialData = ({.*?});'
            match = re.search(pattern, html)
            
            if not match:
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
                        video_data = self._parse_video(video)
                        videos.append(video_data)
                        
                        if len(videos) >= max_results:
                            return self._sort_by_views(videos)
            
            except KeyError:
                pass
            
            return self._sort_by_views(videos)
            
        except Exception:
            return []
    
    def _parse_video(self, video: Dict) -> Dict:
        """Parse video data from YouTube response"""
        video_id = video.get('videoId', '')
        
        # Extract basic info
        title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
        
        # Views
        view_text = video.get('viewCountText', {}).get('simpleText', '')
        views = self._parse_view_count(view_text)
        
        # Channel
        channel = video.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown')
        
        # Check if verified
        channel_verified = False
        if 'ownerBadges' in video:
            for badge in video.get('ownerBadges', []):
                if 'metadataBadgeRenderer' in badge:
                    if badge['metadataBadgeRenderer'].get('style') == 'BADGE_STYLE_TYPE_VERIFIED':
                        channel_verified = True
                        break
        
        # Other metadata
        duration = video.get('lengthText', {}).get('simpleText', '')
        age = video.get('publishedTimeText', {}).get('simpleText', '')
        
        return {
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
    
    def _parse_view_count(self, views_str: str) -> int:
        """Convert view string to integer"""
        if not views_str:
            return 0
        
        views_str = views_str.replace(',', '').replace(' views', '').strip()
        
        if 'M' in views_str:
            return int(float(views_str.replace('M', '')) * 1_000_000)
        elif 'K' in views_str:
            return int(float(views_str.replace('K', '')) * 1_000)
        
        try:
            return int(views_str)
        except:
            return 0
    
    def _sort_by_views(self, videos: List[Dict]) -> List[Dict]:
        """Sort videos by view count (descending)"""
        return sorted(videos, key=lambda x: x.get('views', 0), reverse=True)
