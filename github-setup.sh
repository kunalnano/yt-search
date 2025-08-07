#!/bin/bash

# GitHub Setup Script for YT-Search
# Run this after creating a new repository on GitHub

echo "🚀 YT-Search GitHub Setup"
echo "========================="
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'yt-search'"
echo "3. Make it public"
echo "4. Don't initialize with README (we already have one)"
echo ""
read -p "Press Enter when you've created the repository..."

echo ""
echo "Enter your GitHub username:"
read GITHUB_USERNAME

# Add remote origin
git remote add origin "https://github.com/$GITHUB_USERNAME/yt-search.git"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your repository is now at:"
echo "   https://github.com/$GITHUB_USERNAME/yt-search"
echo ""
echo "🎉 Next steps:"
echo "   1. Star your own repo!"
echo "   2. Share with friends: https://github.com/$GITHUB_USERNAME/yt-search"
echo "   3. Install on other machines:"
echo "      curl -sSL https://raw.githubusercontent.com/$GITHUB_USERNAME/yt-search/main/install.sh | bash"
