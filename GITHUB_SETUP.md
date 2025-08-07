# 🚀 GitHub Setup Checklist for YT-Search

## Step 1: Create GitHub Repository

1. **Go to:** https://github.com/new
2. **Repository name:** `yt-search`
3. **Description:** Algorithm-free YouTube search in your terminal
4. **Public** repository (select this)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

## Step 2: Push Your Code

Once you've created the repository, run these commands:

```bash
cd /Users/alsharma/retro-youtube-terminal

# Push to GitHub
git push -u origin main
```

If you get authentication issues, you might need to:
- Use a GitHub Personal Access Token (PAT) instead of password
- Or set up SSH keys

## Step 3: Verify It Works

After pushing, you can test the curl installer:

```bash
# Test the installer
curl -sSL https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh | bash
```

## 🎉 Share Your Project!

Once it's up, you can share it with:

### Quick Install (One-liner):
```bash
curl -sSL https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh | bash
```

### Clone and Install:
```bash
git clone https://github.com/kunalnano/yt-search.git
cd yt-search
./install.sh
```

### Direct Python:
```bash
git clone https://github.com/kunalnano/yt-search.git
cd yt-search
python3 -m yt_search.main
```

## Your Repository URLs:
- **GitHub:** https://github.com/kunalnano/yt-search
- **Clone URL:** https://github.com/kunalnano/yt-search.git
- **Installer:** https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh

## Features to Highlight:
- 🚫 No algorithms - Pure search by view count
- 🔒 No tracking - Complete privacy
- 💻 Clean terminal UI
- 🌍 Cross-platform support
- 📦 Zero dependencies
- ⚡ Fast and lightweight

Ready? Go create that repo and let's ship it! 🚀
