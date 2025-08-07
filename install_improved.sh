#!/bin/bash

# Enhanced YouTube Terminal Search Installer with better shell detection and venv awareness

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect current shell
detect_shell() {
    if [ -n "$ZSH_VERSION" ]; then
        echo "zsh"
    elif [ -n "$BASH_VERSION" ]; then
        echo "bash"
    elif [ -n "$FISH_VERSION" ]; then
        echo "fish"
    else
        # Fallback to checking parent process
        parent_shell=$(ps -p $$ -o comm=)
        case "$parent_shell" in
            *zsh*) echo "zsh" ;;
            *bash*) echo "bash" ;;
            *fish*) echo "fish" ;;
            *) echo "unknown" ;;
        esac
    fi
}

# Get appropriate RC file
get_rc_file() {
    local shell_type=$1
    case "$shell_type" in
        zsh) echo "$HOME/.zshrc" ;;
        bash) 
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS uses .bash_profile for login shells
                echo "$HOME/.bash_profile"
            else
                echo "$HOME/.bashrc"
            fi
            ;;
        fish) echo "$HOME/.config/fish/config.fish" ;;
        *) echo "" ;;
    esac
}

# Check if we're in a virtual environment
check_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo -e "${YELLOW}⚠️  Warning: You're currently in a virtual environment at:${NC}"
        echo -e "${YELLOW}   $VIRTUAL_ENV${NC}"
        echo -e "${YELLOW}   The installation will proceed to your system Python.${NC}"
        echo ""
        read -p "Do you want to continue? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}Installation cancelled.${NC}"
            exit 1
        fi
    fi
}

# Main installation
main() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}     YouTube Terminal Search - Enhanced Installer${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    # Check for virtual environment
    check_venv

    # Detect shell
    DETECTED_SHELL=$(detect_shell)
    RC_FILE=$(get_rc_file "$DETECTED_SHELL")
    
    echo -e "${BLUE}🔍 Detected shell:${NC} $DETECTED_SHELL"
    if [ -z "$RC_FILE" ]; then
        echo -e "${YELLOW}⚠️  Could not detect shell configuration file.${NC}"
        echo "Please manually add the following to your shell's RC file:"
        echo '  alias yt-search="python3 ~/retro-youtube-terminal/youtube_search.py"'
        exit 1
    fi
    echo -e "${BLUE}📝 Configuration file:${NC} $RC_FILE"
    echo ""

    # Install options
    echo -e "${GREEN}Installation Options:${NC}"
    echo "1) Install in current directory (development mode)"
    echo "2) Install in ~/.local/bin (user installation)"
    echo "3) Create symlink only (no file copying)"
    echo ""
    read -p "Choose installation method (1-3): " -n 1 -r install_method
    echo ""

    case $install_method in
        1)
            # Development mode - just create alias to current directory
            INSTALL_DIR=$(pwd)
            echo -e "${BLUE}📦 Installing in development mode...${NC}"
            ;;
        2)
            # User installation
            INSTALL_DIR="$HOME/.local/bin/yt-search"
            echo -e "${BLUE}📦 Installing to ~/.local/bin...${NC}"
            
            # Create directory if it doesn't exist
            mkdir -p "$INSTALL_DIR"
            
            # Copy files
            cp youtube_search.py "$INSTALL_DIR/"
            cp -r src "$INSTALL_DIR/" 2>/dev/null || true
            
            # Make executable
            chmod +x "$INSTALL_DIR/youtube_search.py"
            ;;
        3)
            # Symlink only
            INSTALL_DIR=$(pwd)
            echo -e "${BLUE}🔗 Creating symlink only...${NC}"
            
            # Create ~/.local/bin if it doesn't exist
            mkdir -p "$HOME/.local/bin"
            
            # Create symlink
            ln -sf "$INSTALL_DIR/youtube_search.py" "$HOME/.local/bin/yt-search"
            chmod +x "$INSTALL_DIR/youtube_search.py"
            
            # Check if ~/.local/bin is in PATH
            if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
                echo -e "${YELLOW}⚠️  ~/.local/bin is not in your PATH${NC}"
                echo "Adding to $RC_FILE..."
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
            fi
            
            echo -e "${GREEN}✅ Symlink created successfully!${NC}"
            echo "You can now use 'yt-search' command after reloading your shell."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Exiting.${NC}"
            exit 1
            ;;
    esac

    # Create alias based on shell type
    if [ "$DETECTED_SHELL" = "fish" ]; then
        ALIAS_CMD="alias yt-search='python3 $INSTALL_DIR/youtube_search.py'"
    else
        ALIAS_CMD="alias yt-search='python3 $INSTALL_DIR/youtube_search.py'"
    fi

    # Check if alias already exists
    if grep -q "alias yt-search=" "$RC_FILE" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Alias 'yt-search' already exists in $RC_FILE${NC}"
        echo "Current alias:"
        grep "alias yt-search=" "$RC_FILE"
        echo ""
        read -p "Do you want to update it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Remove old alias
            sed -i.bak '/alias yt-search=/d' "$RC_FILE"
            echo "$ALIAS_CMD" >> "$RC_FILE"
            echo -e "${GREEN}✅ Alias updated!${NC}"
        else
            echo -e "${YELLOW}⏭️  Skipping alias update.${NC}"
        fi
    else
        echo "$ALIAS_CMD" >> "$RC_FILE"
        echo -e "${GREEN}✅ Alias added to $RC_FILE${NC}"
    fi

    # Installation complete
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Installation complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}To start using yt-search:${NC}"
    echo ""
    if [ "$DETECTED_SHELL" = "fish" ]; then
        echo "  source $RC_FILE"
    else
        echo "  source $RC_FILE"
    fi
    echo "  yt-search"
    echo ""
    echo -e "${YELLOW}Or start a new terminal session.${NC}"
    echo ""
    echo -e "${BLUE}Uninstall:${NC}"
    echo "  Remove the alias from $RC_FILE"
    if [ $install_method -eq 2 ]; then
        echo "  rm -rf $INSTALL_DIR"
    elif [ $install_method -eq 3 ]; then
        echo "  rm $HOME/.local/bin/yt-search"
    fi
}

# Run main installation
main
