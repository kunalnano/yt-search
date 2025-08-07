# YouTube Terminal Search - Enhanced Version 2.0

## 🚀 Key Improvements Made

### 1. **Clickable URLs** ✅
- URLs now use OSC 8 hyperlink protocol for modern terminals
- Works in iTerm2, macOS Terminal.app (recent versions), and other modern terminals
- Falls back gracefully to colored text for older terminals
- Format: `youtu.be/VIDEO_ID` for cleaner display

### 2. **Smart Search Intent Detection** 🧠
The search now automatically detects what you're looking for:

- **Tutorial Detection**: Adds medium duration filter, prioritizes educational content
- **Music Detection**: Optimizes for music videos and audio content
- **Recency Detection**: Automatically sorts by date for "latest", "2024", "new" queries
- **Quality Detection**: Sorts by views for "best" or "top" queries
- **Duration Detection**: Adjusts length filter based on "quick" or "full" keywords

### 3. **Advanced Filtering System** 🔍

#### **Duration Filters**
```bash
filter duration short   # < 4 minutes
filter duration medium  # 4-20 minutes
filter duration long    # > 20 minutes
```

#### **Date Filters**
```bash
filter date today
filter date week
filter date month
filter date year
```

#### **Sort Options**
```bash
filter sort views      # By popularity (default)
filter sort date       # Most recent first
filter sort relevance  # YouTube's algorithm
```

#### **Quality Filters**
```bash
filter hd             # HD videos only
```

### 4. **Enhanced Search Commands** 📝

- **Exact Phrase**: `exact "machine learning fundamentals"`
- **Channel Search**: `search python channel:CoreySchafer`
- **Refine Search**: `refine advanced topics` (adds to current search)
- **Clear Filters**: `clear filters`
- **Toggle Descriptions**: `desc` (preview video content)

### 5. **Better Result Display** 📊

- **Channel Verification**: Shows ✓ for verified channels
- **Color-Coded Views**:
  - Bold Yellow: Billions of views
  - Yellow: Millions of views
  - Cyan: 100K+ views
  - Dim: Less than 100K
- **Dynamic Column Width**: Adapts to content
- **Description Snippets**: Optional preview of video content

### 6. **Search Session Management** 💾

- Maintains search history
- Remembers current filters
- Progressive refinement capability
- Filter persistence across refinements

## 📋 Quick Command Reference

```bash
# Launch the enhanced YouTube search
yt

# View search tips
yt-tips

# Use classic version
yt-classic

# Basic search (auto-detects intent)
search python pandas tutorial beginner

# Exact phrase search
exact "react hooks useState"

# Channel-specific search
search javascript channel:TraversyMedia

# Refine current search
refine advanced concepts

# Apply filters
filter duration long
filter date month
filter sort views
filter hd

# Clear all filters
clear filters

# Toggle description preview
desc

# Open video
open 1

# Copy URL to clipboard
url 1

# Get help
help

# Exit
quit
```

## 🎯 Search Strategy Tips

### For Better Results:
1. **Be Specific**: More keywords = better targeting
2. **Use Quotes**: For exact phrases that shouldn't be reordered
3. **Add Years**: Especially for technical content (e.g., "2024")
4. **Specify Level**: Add "beginner", "intermediate", or "advanced"
5. **Include Format**: "tutorial", "course", "tips", "explained"

### Example Searches:
```bash
# Beginner Python tutorial from 2024
search python tutorial beginner 2024

# Exact React hooks tutorial
exact "react hooks useEffect cleanup"

# Music from specific artist
search "pink floyd" official video
filter duration long

# Recent tech news
search "apple vision pro" review
filter date week
filter sort date

# Educational content from trusted source
search machine learning channel:3Blue1Brown
filter duration medium
```

## 🔧 Technical Improvements

1. **Better HTML Parsing**: More robust extraction of video metadata
2. **Enhanced View Count Parsing**: Handles K, M, B abbreviations
3. **Channel Verification Detection**: Identifies verified channels
4. **Description Extraction**: Gets video description snippets
5. **Smart Filter Encoding**: Proper YouTube filter parameters
6. **Session State Management**: Maintains context between searches

## 🎨 Visual Enhancements

- Retro cyberpunk aesthetic maintained
- Matrix green for interactive elements
- Color-coded information hierarchy
- Clean table formatting with proper alignment
- Clickable URLs with underline styling
- Verification badges for trusted channels

## 🚫 What This Tool Doesn't Do

- **No Recommendations**: Pure search, no "suggested for you"
- **No Tracking**: No personalization or watch history
- **No Autoplay**: You choose what to watch
- **No Engagement Metrics**: Just views, not "engagement"
- **No Algorithm**: Results sorted by actual popularity

## 🎉 Summary

This enhanced version transforms YouTube search into a powerful, algorithm-free research tool. With smart intent detection, advanced filtering, and clickable URLs, you now have complete control over your content discovery - seeing what's actually popular, not what YouTube wants you to watch.

The tool treats YouTube as a library catalog rather than an engagement platform, giving you the power to find exactly what you're looking for without algorithmic interference.
