# YT-Search: Algorithm-Free YouTube Terminal Browser 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **YouTube as it should be**: A library, not an engagement trap. Pure search results sorted by actual popularity, no algorithmic manipulation.

![YT-Search Demo](https://via.placeholder.com/800x400.png?text=YT-Search+Terminal+Demo)

## 🎯 Features

- **No Algorithm**: Results sorted by actual view count, not "engagement"
- **No Tracking**: No personalization, no bubble, no manipulation
- **No Autoplay**: You choose what to watch
- **Pure Search**: See what's actually popular, not what YouTube wants you to see
- **Clickable URLs**: Modern terminal hyperlink support
- **Smart Search**: Auto-detects tutorials, music, recent content
- **Clean UI**: Retro terminal aesthetic with color-coded results

## 📦 Installation

### Option 1: Using pip (Recommended)

```bash
pip install yt-search-terminal
```

### Option 2: Using Homebrew (macOS/Linux)

```bash
brew tap kunalnano/yt-search
brew install yt-search
```

### Option 3: Using npm

```bash
npm install -g yt-search-terminal
```

### Option 4: Direct from GitHub

```bash
# Clone the repository
git clone https://github.com/kunalnano/yt-search.git
cd yt-search

# Install
./install.sh
```

### Option 5: Manual Installation

```bash
# Clone and setup
git clone https://github.com/kunalnano/yt-search.git
cd yt-search

# Make executable
chmod +x yt-search.py

# Add to PATH (add to your .zshrc or .bashrc)
echo 'export PATH="$PATH:$HOME/yt-search"' >> ~/.zshrc
source ~/.zshrc
```

## 🚀 Quick Start

```bash
# Launch the search interface
yt-search

# Direct search from command line
yt-search "python tutorial"

# Search with options
yt-search "react hooks" --max 10 --sort views
```

## 📖 Usage

### Interactive Mode Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `search <query>` | `s` | Search YouTube |
| `open <number>` | `o` | Open video in browser |
| `url <number>` | `u` | Copy video URL |
| `info <number>` | `i` | Show video details |
| `filter <type> <value>` | `f` | Apply filters |
| `help` | `h` | Show help |
| `quit` | `q` | Exit |

### Search Examples

```bash
# Basic search
search python tutorial

# Exact phrase
search "machine learning fundamentals"

# Channel-specific
search python channel:CoreySchafer

# With filters
search javascript
filter duration long
filter date month
```

### Smart Search Detection

The tool automatically detects:
- **Tutorials**: Adds medium duration filter
- **Music**: Optimizes for music videos
- **Recent**: Sorts by date for "latest", "2024", "new"
- **Popular**: Sorts by views for "best", "top"

## 🎨 Customization

### Configuration File

Create `~/.config/yt-search/config.json`:

```json
{
  "default_max_results": 20,
  "default_sort": "views",
  "color_scheme": "matrix",
  "terminal_width": "auto",
  "clickable_urls": true
}
```

### Color Schemes

- `matrix` - Green terminal aesthetic (default)
- `cyberpunk` - Neon colors
- `minimal` - Black and white
- `ocean` - Blue theme

## 🛠️ Development

### Requirements

- Python 3.7+
- No external dependencies! Uses only standard library

### Project Structure

```
yt-search/
├── yt_search/
│   ├── __init__.py
│   ├── main.py           # Main entry point
│   ├── search.py         # YouTube search logic
│   ├── display.py        # Terminal display
│   └── utils.py          # Helper functions
├── tests/
│   └── test_search.py
├── setup.py              # Python package setup
├── package.json          # npm package config
├── Formula/              # Homebrew formula
├── install.sh            # Universal installer
└── README.md
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Inspired by the need for algorithmic transparency
- Built for those who miss when YouTube was a video library
- Special thanks to the terminal UI enthusiasts

## 🐛 Known Issues

- URLs may not be clickable in older terminals
- Some special characters in searches need escaping
- Pagination currently limited to sequential loading

## 🚦 Roadmap

- [ ] Download support via yt-dlp integration
- [ ] Playlist search and management
- [ ] Channel subscription tracking (local)
- [ ] Export search results to JSON/CSV
- [ ] Custom RSS feed generation
- [ ] Terminal GUI with mouse support

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/kunalnano/yt-search/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kunalnano/yt-search/discussions)
- **Email**: your-email@example.com

---

**Remember**: This tool treats YouTube as a library catalog, not an engagement platform. You search, you see what's actually popular, you choose. No manipulation, no rabbit holes, just honest search results.

*If you find this useful, please ⭐ star the repository!*
