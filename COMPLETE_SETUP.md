# 🚀 Complete Setup Guide for YT-Search

## Prerequisites

You need to:
1. Push the main repo to GitHub
2. Create GitHub release
3. Set up Homebrew tap
4. Publish to npm (optional)

---

## Step 1: Push Main Repository

```bash
cd /Users/alsharma/retro-youtube-terminal

# If not already done:
git remote add origin https://github.com/kunalnano/yt-search.git
git push -u origin main
```

## Step 2: Create GitHub Release

1. Go to: https://github.com/kunalnano/yt-search/releases/new
2. Click "Choose a tag" → Type `v1.0.0` → Create new tag
3. Release title: `YT-Search v1.0.0`
4. Description:
   ```
   🚀 First release of YT-Search!
   
   Algorithm-free YouTube search in your terminal.
   - No tracking
   - No recommendations
   - Just pure search by view count
   ```
5. Click "Publish release"

## Step 3: Set up Homebrew Tap

### Create the tap repository:

1. Go to: https://github.com/new
2. Repository name: `homebrew-yt-search`
3. Make it public
4. Create repository

### Push the Homebrew formula:

```bash
cd /Users/alsharma/homebrew-yt-search

# Set remote
git remote add origin https://github.com/kunalnano/homebrew-yt-search.git

# First, we need to update the formula with the correct SHA256
# After creating the release, get the SHA256:
curl -sL https://github.com/kunalnano/yt-search/archive/refs/tags/v1.0.0.tar.gz | shasum -a 256

# Update the SHA256 in Formula/yt-search.rb, then:
git add -A
git commit -m "Update SHA256 for v1.0.0"
git push -u origin main
```

## Step 4: Test Installations

### Test Homebrew (after tap is pushed):
```bash
brew tap kunalnano/yt-search
brew install yt-search
yt-search --version
```

### Test curl installer:
```bash
curl -sSL https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh | bash
```

### Test npm (after publishing):
```bash
npm install -g yt-search-terminal
yt-search --version
```

---

## 📦 Publishing to npm (Optional)

If you want to publish to npm:

1. Create account at https://www.npmjs.com/
2. Login:
   ```bash
   npm login
   ```
3. Publish:
   ```bash
   cd /Users/alsharma/retro-youtube-terminal
   npm publish
   ```

---

## 🎯 Final Installation Commands

Once everything is set up, users can install with:

### Homebrew (macOS/Linux):
```bash
brew tap kunalnano/yt-search
brew install yt-search
```

### npm (cross-platform):
```bash
npm install -g yt-search-terminal
```

### Direct install (universal):
```bash
curl -sSL https://raw.githubusercontent.com/kunalnano/yt-search/main/install.sh | bash
```

### Python pip (after PyPI publish):
```bash
pip install yt-search-terminal
```

---

## 🐛 Troubleshooting

### Homebrew issues:
```bash
# If formula not found:
brew tap --repair
brew update

# If installation fails:
brew install --debug yt-search
```

### npm issues:
```bash
# Check Python is installed:
python3 --version

# Clear npm cache:
npm cache clean --force
```

### Direct install issues:
```bash
# Manual install:
git clone https://github.com/kunalnano/yt-search.git
cd yt-search
./install.sh
```

---

## ✅ Checklist

- [ ] Main repo pushed to GitHub
- [ ] Release v1.0.0 created
- [ ] Homebrew tap repo created
- [ ] Formula SHA256 updated
- [ ] Homebrew tap pushed
- [ ] npm package published (optional)
- [ ] Tested all installation methods

---

## 🎉 Success!

Your package is now available globally via multiple installation methods!

Share it with: https://github.com/kunalnano/yt-search
