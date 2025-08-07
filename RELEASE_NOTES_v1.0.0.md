# 🚀 YT-Search v1.0.0 - First Release!

## YouTube as a Library, Not an Engagement Trap

Finally, a YouTube search tool that shows you what's **actually popular**, not what an algorithm wants you to watch.

## ✨ What is YT-Search?

YT-Search is a terminal-based YouTube browser that bypasses all algorithmic manipulation:
- **No recommendations** - You search, you choose
- **No tracking** - Complete privacy
- **No personalization bubble** - See raw popularity
- **Pure view counts** - Results sorted by actual views, not "engagement"

## 🎯 Key Features

### Algorithm-Free Search
- Results sorted by **actual view count**
- No "recommended for you" manipulation
- No engagement optimization tricks
- Just honest search results

### Clean Terminal Interface
- 🎨 Retro cyberpunk aesthetic
- 📊 Color-coded view counts (millions in yellow!)
- ✅ Verified channel badges
- 🔗 Clickable URLs in modern terminals
- 📋 Clean table formatting

### Privacy First
- Zero tracking
- No watch history
- No data collection
- No cookies or sessions

### Lightweight & Fast
- **Zero dependencies** - Uses only Python standard library
- Works on macOS, Linux, and Windows (WSL)
- Instant searches
- Minimal resource usage

## 📦 Installation

### Option 1: Direct Install (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh | bash
```

### Option 2: Homebrew (macOS/Linux)
```bash
brew tap kunalnano/yt-search
brew install yt-search
```

### Option 3: npm (Cross-platform)
```bash
npm install -g yt-search-terminal
```

### Option 4: Clone & Install
```bash
git clone https://github.com/kunalnano/yt-search.git
cd yt-search
./install.sh
```

## 🎮 Usage

### Interactive Mode
```bash
yt-search
```

### Direct Search
```bash
yt-search "python tutorial"
```

### Commands
- `search <query>` or `s <query>` - Search YouTube
- `open <number>` or `o <number>` - Open video in browser
- `url <number>` or `u <number>` - Copy video URL
- `info <number>` or `i <number>` - Show video details
- `quit` or `q` - Exit

## 🌟 Why YT-Search?

### The Problem
YouTube's algorithm is designed to maximize watch time, not help you find what you're looking for. It:
- Shows you what it wants you to watch
- Creates filter bubbles
- Hides actual popularity metrics
- Optimizes for "engagement" over quality

### The Solution
YT-Search treats YouTube like a library catalog:
- You search for what YOU want
- You see what's ACTUALLY popular
- You choose what to watch
- No manipulation, no rabbit holes

## 📊 What's in This Release

- ✅ Core search functionality
- ✅ Clean terminal UI with color coding
- ✅ Multiple installation methods
- ✅ Cross-platform support
- ✅ Channel verification badges
- ✅ View count sorting
- ✅ Zero dependencies
- ✅ Full documentation

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **Dependencies**: None! (Uses only standard library)
- **Package Size**: < 100KB
- **Platforms**: macOS, Linux, Windows (WSL)
- **License**: MIT

## 📈 Statistics

- **19 files** of clean, modular code
- **3,500+ lines** of algorithm-free searching
- **0 external dependencies**
- **3 installation methods** ready to go

## 🔮 Future Plans

- [ ] Download support via yt-dlp integration
- [ ] Playlist search functionality
- [ ] Channel browsing
- [ ] Export results to JSON/CSV
- [ ] Terminal GUI with mouse support
- [ ] Custom RSS feed generation

## 🙏 Acknowledgments

Built for everyone who:
- Misses when YouTube was just a video library
- Values privacy and transparency
- Wants to escape the recommendation rabbit hole
- Believes search results should be honest

## 🐛 Known Issues

- URLs may not be clickable in older terminals (use `open` command instead)
- Some special characters in searches need escaping
- Windows requires WSL for full functionality

## 💬 Feedback

Found a bug? Have a suggestion? 
- Open an issue: https://github.com/kunalnano/yt-search/issues
- Start a discussion: https://github.com/kunalnano/yt-search/discussions

## 📝 License

MIT License - Use it, modify it, share it!

---

**Remember**: This tool treats YouTube as a library catalog, not an engagement platform. You search, you see what's actually popular, you choose. No manipulation, no algorithms, just honest results.

If you find this useful, please ⭐ star the repository!

---

*Built with ❤️ for algorithmic transparency*