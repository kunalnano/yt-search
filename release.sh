#!/bin/bash

# YT-Search Release Helper
# Prepares releases for GitHub, Homebrew, npm, and PyPI

VERSION="1.0.0"
REPO="kunalnano/yt-search"

echo "🚀 YT-Search Release Helper v$VERSION"
echo "===================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "\n${BLUE}Step 1: Create GitHub Release${NC}"
echo "--------------------------------"
echo "1. Ensure all changes are committed and pushed"
echo "2. Go to: https://github.com/$REPO/releases/new"
echo "3. Create tag: v$VERSION"
echo "4. Release title: YT-Search v$VERSION"
echo "5. Description: Algorithm-free YouTube terminal browser"
echo "6. Attach the tarball (will be created after tagging)"
echo ""
read -p "Press Enter when ready to create the release tag..."

# Create and push tag
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

echo -e "\n${GREEN}✓ Tag created and pushed${NC}"

# Get the SHA256 for Homebrew
echo -e "\n${BLUE}Step 2: Update Homebrew Formula${NC}"
echo "--------------------------------"
echo "Getting SHA256 for Homebrew formula..."

# Download the tagged release
TARBALL_URL="https://github.com/$REPO/archive/refs/tags/v$VERSION.tar.gz"
curl -sL "$TARBALL_URL" -o "/tmp/yt-search-$VERSION.tar.gz"
SHA256=$(shasum -a 256 "/tmp/yt-search-$VERSION.tar.gz" | cut -d' ' -f1)

echo -e "${GREEN}SHA256: $SHA256${NC}"

# Update Homebrew formula
cat > homebrew-formula.rb << EOF
class YtSearch < Formula
  desc "Algorithm-free YouTube search in your terminal"
  homepage "https://github.com/$REPO"
  url "$TARBALL_URL"
  sha256 "$SHA256"
  license "MIT"

  depends_on "python@3.11"

  def install
    # Install Python package
    ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python3.11/site-packages"
    
    # Copy all Python files
    libexec.install Dir["*"]
    
    # Create wrapper script
    (bin/"yt-search").write <<~EOS
      #!/usr/bin/env bash
      export PYTHONPATH="#{libexec}:$PYTHONPATH"
      cd "#{libexec}" && exec python3 -m yt_search.main "\$@"
    EOS
    
    chmod 0755, bin/"yt-search"
    
    # Create additional shortcuts
    bin.install_symlink bin/"yt-search" => "yts"
    bin.install_symlink bin/"yt-search" => "youtube-search"
  end

  test do
    system "#{bin}/yt-search", "--version"
  end
end
EOF

echo -e "${GREEN}✓ Homebrew formula created: homebrew-formula.rb${NC}"

echo -e "\n${BLUE}Step 3: Homebrew Tap Setup${NC}"
echo "--------------------------------"
echo "1. Create a new repo: https://github.com/new"
echo "   Name: homebrew-yt-search"
echo "2. Copy homebrew-formula.rb to Formula/yt-search.rb in that repo"
echo "3. Push the tap repository"
echo ""
echo "Users can then install with:"
echo -e "${YELLOW}  brew tap $REPO"
echo -e "  brew install yt-search${NC}"

echo -e "\n${BLUE}Step 4: NPM Publishing${NC}"
echo "--------------------------------"
echo "To publish to npm:"
echo -e "${YELLOW}  npm login"
echo -e "  npm publish${NC}"

echo -e "\n${BLUE}Step 5: PyPI Publishing${NC}"
echo "--------------------------------"
echo "To publish to PyPI:"
echo -e "${YELLOW}  pip install build twine"
echo -e "  python -m build"
echo -e "  python -m twine upload dist/*${NC}"

echo -e "\n${GREEN}🎉 Release preparation complete!${NC}"
echo ""
echo "Installation methods will be:"
echo -e "${YELLOW}  # Homebrew"
echo "  brew tap $REPO"
echo "  brew install yt-search"
echo ""
echo "  # npm"
echo "  npm install -g yt-search-terminal"
echo ""
echo "  # pip"
echo "  pip install yt-search-terminal"
echo ""
echo "  # Direct"
echo "  curl -sSL https://raw.githubusercontent.com/$REPO/main/install.sh | bash${NC}"

# Cleanup
rm -f "/tmp/yt-search-$VERSION.tar.gz"
