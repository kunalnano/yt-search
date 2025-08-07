#!/bin/bash

# YT-Search Universal Installer
# Detects the best installation method for your system

set -e

REPO_URL="https://github.com/alsharma/yt-search.git"
INSTALL_DIR="$HOME/.yt-search"
BIN_DIR="$HOME/.local/bin"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print colored message
print_msg() {
    echo -e "${2}${1}${NC}"
}

# Main installation
main() {
    print_msg "🚀 YT-Search Installer" "$BLUE"
    print_msg "========================" "$BLUE"
    
    OS=$(detect_os)
    print_msg "Detected OS: $OS" "$GREEN"
    
    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_msg "✓ Python $PYTHON_VERSION found" "$GREEN"
    else
        print_msg "✗ Python 3 not found. Please install Python 3.7+" "$RED"
        exit 1
    fi
    
    # Clone or update repository
    if [ -d "$INSTALL_DIR" ]; then
        print_msg "Updating existing installation..." "$YELLOW"
        cd "$INSTALL_DIR"
        git pull
    else
        print_msg "Cloning repository..." "$YELLOW"
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    # Create bin directory if it doesn't exist
    mkdir -p "$BIN_DIR"
    
    # Create executable wrapper
    cat > "$BIN_DIR/yt-search" << 'EOF'
#!/bin/bash
python3 -m yt_search.main "$@"
EOF
    
    chmod +x "$BIN_DIR/yt-search"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_msg "Adding $BIN_DIR to PATH..." "$YELLOW"
        
        # Detect shell
        if [ -n "$ZSH_VERSION" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            SHELL_RC="$HOME/.bashrc"
        else
            SHELL_RC="$HOME/.profile"
        fi
        
        echo "" >> "$SHELL_RC"
        echo "# YT-Search" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
        echo "export PYTHONPATH=\"\$PYTHONPATH:$INSTALL_DIR\"" >> "$SHELL_RC"
        
        print_msg "✓ Added to $SHELL_RC" "$GREEN"
        print_msg "  Run: source $SHELL_RC" "$YELLOW"
    fi
    
    # Create aliases
    if [ "$OS" == "macos" ] || [ "$OS" == "linux" ]; then
        cat > "$BIN_DIR/yts" << 'EOF'
#!/bin/bash
yt-search "$@"
EOF
        chmod +x "$BIN_DIR/yts"
    fi
    
    print_msg "" ""
    print_msg "✅ Installation complete!" "$GREEN"
    print_msg "" ""
    print_msg "To start using YT-Search:" "$BLUE"
    print_msg "  1. Reload your shell: source ~/.zshrc (or ~/.bashrc)" "$YELLOW"
    print_msg "  2. Run: yt-search" "$YELLOW"
    print_msg "" ""
    print_msg "Commands:" "$BLUE"
    print_msg "  yt-search          - Launch interactive mode" "$NC"
    print_msg "  yt-search <query>  - Direct search" "$NC"
    print_msg "  yts <query>        - Short alias" "$NC"
    print_msg "" ""
    print_msg "Enjoy algorithm-free YouTube browsing! 🎉" "$GREEN"
}

# Run main function
main
