#!/bin/bash
# =============================================================================
# MacBook Development Environment Setup Script
# For new team members — automates the Intern MacBook Setup Guide
#
# Usage:
#   bash setup-macbook.sh                    # Interactive (prompts for all input)
#
# What this automates (~75% of the guide):
#   - All Homebrew, npm, uv installs
#   - VS Code extensions
#   - Environment variable setup
#   - Git configuration
#   - Zotero CLI installation (if repo is accessible)
#   - Obsidian vault setup (if repo is accessible)
#   - Claude Code customization (.claude directory)
#
# GitHub access is OPTIONAL. Clones via HTTPS (no SSH key needed).
# If the repo can't be cloned, the script skips Zotero CLI and
# Obsidian vault setup gracefully. Re-run after access is granted.
#
# What requires manual action (pauses with instructions):
#   - Claude Desktop login (browser)
#   - Claude Code authentication (browser)
#   - Better BibTeX plugin install (Zotero GUI)
#   - Obsidian community plugins (Obsidian GUI)
#   - Zotero Integration plugin config (Obsidian GUI)
#
# Estimated time: ~45 minutes (down from ~90 manual)
# =============================================================================

set -e

# ---------------------------------------------------------------------------
# Colors and formatting
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; }

phase_header() {
    echo ""
    echo -e "${BOLD}=================================================================${NC}"
    echo -e "${BOLD}  Phase $1: $2${NC}"
    echo -e "${BOLD}=================================================================${NC}"
    echo ""
}

phase_complete() {
    echo ""
    echo -e "${GREEN}${BOLD}  Phase $1 Complete.${NC} $2"
    echo ""
}

manual_pause() {
    echo ""
    echo -e "${YELLOW}${BOLD}  MANUAL STEP REQUIRED${NC}"
    echo -e "${YELLOW}  ─────────────────────${NC}"
    echo -e "  $1"
    echo ""
    read -p "  Press Enter when done (or 's' to skip)... " response
    if [[ "$response" == "s" ]]; then
        warn "Skipped: $2"
        return 1
    fi
    return 0
}

check_installed() {
    if command -v "$1" &> /dev/null; then
        return 0
    fi
    return 1
}

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
REPO_URL="https://github.com/gwlund/k2-vision-tools.git"
REPO_DIR="$HOME/Documents/Projects/k2-vision-tools"

while [[ $# -gt 0 ]]; do
    case $1 in
        --repo-url)
            REPO_URL="$2"
            shift 2
            ;;
        --help)
            echo "Usage: bash setup-macbook.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --repo-url URL  Git repo URL (default: gwlund/k2-vision-tools)"
            echo "  --help          Show this help"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Welcome
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}=================================================================${NC}"
echo -e "${BOLD}  MacBook Development Environment Setup${NC}"
echo -e "${BOLD}=================================================================${NC}"
echo ""
echo "  This script will set up your MacBook for development work."
echo "  It automates most steps from the setup guide, pausing when"
echo "  you need to do something manually (like browser logins)."
echo ""
echo "  Estimated time: ~45 minutes"
echo ""

# ---------------------------------------------------------------------------
# Gather input up front
# ---------------------------------------------------------------------------
echo -e "${BOLD}First, I need some information from you:${NC}"
echo ""

read -p "  Your full name (for git commits): " USER_FULL_NAME
read -p "  Your work email: " USER_EMAIL
read -p "  Your Zotero API key (24 characters): " ZOTERO_API_KEY
read -p "  Your Zotero User ID (8 digits): " ZOTERO_USER_ID

echo ""

# Validate inputs
if [[ -z "$USER_FULL_NAME" || -z "$USER_EMAIL" ]]; then
    error "Name and email are required."
    exit 1
fi

if [[ ${#ZOTERO_API_KEY} -ne 24 ]]; then
    warn "Zotero API key doesn't look right (expected 24 characters, got ${#ZOTERO_API_KEY})."
    read -p "  Continue anyway? (y/n): " confirm
    [[ "$confirm" != "y" ]] && exit 1
fi

if ! [[ "$ZOTERO_USER_ID" =~ ^[0-9]+$ ]]; then
    warn "Zotero User ID should be numeric (got: $ZOTERO_USER_ID)."
    read -p "  Continue anyway? (y/n): " confirm
    [[ "$confirm" != "y" ]] && exit 1
fi

echo ""
info "Starting setup for ${USER_FULL_NAME} <${USER_EMAIL}>"
echo ""

# =========================================================================
# Phase 1: Foundation Tools
# =========================================================================
phase_header 1 "Foundation Tools"

# --- 1.1 Xcode Command Line Tools ---
info "1.1 Xcode Command Line Tools"
if xcode-select -p &> /dev/null; then
    success "Already installed at $(xcode-select -p)"
else
    info "Installing Xcode Command Line Tools (this may take 5-10 minutes)..."
    xcode-select --install 2>/dev/null || true
    manual_pause "A dialog should have appeared. Click 'Install' and wait for it\n  to finish, then press Enter." "Xcode CLT install"
fi

# Verify git is available
if check_installed git; then
    success "git $(git --version | cut -d' ' -f3)"
else
    error "git not found after Xcode CLT install. Please install manually."
    exit 1
fi

# --- 1.2 Git Configuration ---
info "1.2 Git Configuration"
git config --global user.name "$USER_FULL_NAME"
git config --global user.email "$USER_EMAIL"
success "Git identity set to: $USER_FULL_NAME <$USER_EMAIL>"

success "Git configured"

# --- 1.3 Homebrew ---
info "1.3 Homebrew"
if check_installed brew; then
    success "Already installed: $(brew --version | head -1)"
else
    info "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add to PATH for Apple Silicon
    if [[ -f /opt/homebrew/bin/brew ]]; then
        echo >> "$HOME/.zshrc"
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zshrc"
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    success "Homebrew installed: $(brew --version | head -1)"
fi

# --- 1.4 Python via uv ---
info "1.4 Python via uv"
if check_installed uv; then
    success "Already installed: $(uv --version)"
else
    info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source the updated PATH
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    success "uv installed: $(uv --version)"
fi

info "Installing Python 3.13..."
uv python install 3.13
success "Python 3.13 installed"

# --- 1.5 Node.js ---
info "1.5 Node.js"
if check_installed node; then
    success "Already installed: node $(node --version)"
else
    info "Installing Node.js..."
    brew install node
    success "Node.js installed: $(node --version)"
fi

# --- 1.6 Environment Variables ---
info "1.6 Environment Variables"

# Check if already configured
ZSHRC="$HOME/.zshrc"
NEEDS_ZSHRC_UPDATE=false

if ! grep -q "ZOTERO_API_KEY" "$ZSHRC" 2>/dev/null; then
    NEEDS_ZSHRC_UPDATE=true
fi

if [[ "$NEEDS_ZSHRC_UPDATE" == true ]]; then
    info "Adding environment variables to ~/.zshrc..."
    cat >> "$ZSHRC" << ENVEOF

# --- Intern setup: Zotero credentials and PATH ---
export ZOTERO_API_KEY="$ZOTERO_API_KEY"
export ZOTERO_USER_ID="$ZOTERO_USER_ID"
export PATH="\$HOME/.local/bin:\$PATH"
ENVEOF
    success "Environment variables added to ~/.zshrc"
else
    success "Environment variables already in ~/.zshrc"
fi

# Export for current session
export ZOTERO_API_KEY="$ZOTERO_API_KEY"
export ZOTERO_USER_ID="$ZOTERO_USER_ID"
export PATH="$HOME/.local/bin:$PATH"

phase_complete 1 "Git, Homebrew, Python 3.13, Node.js, and environment variables configured."

# =========================================================================
# Phase 2: Development Tools
# =========================================================================
phase_header 2 "Development Tools"

# --- 2.1 Visual Studio Code ---
info "2.1 Visual Studio Code"
if check_installed code; then
    success "Already installed: $(code --version | head -1)"
else
    info "Installing VS Code..."
    brew install --cask visual-studio-code
    success "VS Code installed"
fi

info "Installing VS Code extensions..."
code --install-extension ms-python.python --force 2>/dev/null && success "Extension: Python" || warn "Python extension install failed"
code --install-extension ms-toolsai.jupyter --force 2>/dev/null && success "Extension: Jupyter" || warn "Jupyter extension install failed"

# --- 2.2 Claude Desktop ---
info "2.2 Claude Desktop"
if [[ -d "/Applications/Claude.app" ]]; then
    success "Already installed"
else
    info "Installing Claude Desktop..."
    brew install --cask claude
    success "Claude Desktop installed"
fi

manual_pause "Launch Claude Desktop from Applications and sign in\n  with your Anthropic account." "Claude Desktop login"

# --- 2.3 Claude Code CLI ---
info "2.3 Claude Code CLI"
if check_installed claude; then
    success "Already installed: claude $(claude --version 2>/dev/null || echo '(version check failed)')"
else
    info "Installing Claude Code CLI..."
    npm install -g @anthropic-ai/claude-code
    success "Claude Code installed"
fi

manual_pause "Authenticate Claude Code:\n  1. Run: claude\n  2. A browser window will open — sign in with your Claude account\n  3. After authenticating, type /help to confirm, then /exit" "Claude Code auth"

phase_complete 2 "VS Code, Claude Desktop, and Claude Code CLI installed."

# =========================================================================
# Phase 3: Research & Knowledge Tools
# =========================================================================
phase_header 3 "Research & Knowledge Tools"

# --- 3.1 Zotero ---
info "3.1 Zotero Desktop"
if [[ -d "/Applications/Zotero.app" ]]; then
    success "Already installed"
else
    info "Installing Zotero..."
    brew install --cask zotero
    success "Zotero installed"
fi

manual_pause "Install the Better BibTeX plugin in Zotero:\n  1. Download the .xpi from: https://retorque.re/zotero-better-bibtex/installation/\n  2. In Zotero: Tools → Add-ons → gear icon → Install Add-on From File\n  3. Select the .xpi file\n  4. Restart Zotero when prompted\n  5. Verify: Zotero → Settings should show a 'Better BibTeX' tab" "Better BibTeX install"

# --- 3.2 Obsidian ---
info "3.2 Obsidian"
if [[ -d "/Applications/Obsidian.app" ]]; then
    success "Already installed"
else
    info "Installing Obsidian..."
    brew install --cask obsidian
    success "Obsidian installed"
fi

# --- 3.3 Pandoc ---
info "3.3 Pandoc"
if check_installed pandoc; then
    success "Already installed: $(pandoc --version | head -1)"
else
    info "Installing Pandoc..."
    brew install pandoc
    success "Pandoc installed: $(pandoc --version | head -1)"
fi

phase_complete 3 "Zotero, Obsidian, and Pandoc installed."

# =========================================================================
# Phase 4: Clone Repo & Install Custom Tools
# =========================================================================
phase_header 4 "Clone Repo & Install Custom Tools"

# --- 4.1 Clone Repository ---
info "4.1 Clone Repository"
REPO_AVAILABLE=false
if [[ -d "$REPO_DIR" ]]; then
    success "Repository already exists at $REPO_DIR"
    REPO_AVAILABLE=true
else
    info "Cloning repository via HTTPS..."
    mkdir -p "$(dirname "$REPO_DIR")"
    if git clone "$REPO_URL" "$REPO_DIR" 2>/dev/null; then
        success "Repository cloned to $REPO_DIR"
        REPO_AVAILABLE=true
    else
        warn "Could not clone repository. It may be private or GitHub access not configured."
        warn "Skipping: Zotero CLI, gws-wrap, and Obsidian vault setup."
        warn "Re-run this script after access is granted to install them."
    fi
fi

if [[ "$REPO_AVAILABLE" == true ]]; then
    # --- 4.2 Zotero CLI ---
    info "4.2 Zotero CLI (25 custom commands)"
    if check_installed zotero-verify-api; then
        success "Already installed"
    else
        info "Installing Zotero CLI..."
        (cd "$REPO_DIR/scripts/zotero-cli" && bash install.sh)
        # Ensure PATH is current
        export PATH="$HOME/.local/bin:$PATH"
        success "Zotero CLI installed"
    fi

    # Test Zotero API connection
    info "Testing Zotero API connection..."
    if zotero-verify-api 2>/dev/null; then
        success "Zotero API connection working"
    else
        warn "Zotero API test failed. Check your API key and User ID in ~/.zshrc"
    fi

    # --- 4.3 Obsidian Vault Setup ---
    info "4.3 Obsidian Vault Setup"
    echo ""
    echo "  The Obsidian vault setup requires a project directory."
    echo "  Your manager will tell you which project to set up."
    echo ""
    echo "  When ready, run:"
    echo -e "    ${BOLD}cd ~/Documents/Projects/YOUR-PROJECT${NC}"
    echo -e "    ${BOLD}bash $REPO_DIR/scripts/obsidian-setup/setup-obsidian-vault.sh${NC}"
    echo ""

    manual_pause "After running the vault setup script above, install Obsidian plugins:\n  1. Open the vault in Obsidian (File → Open folder as vault)\n  2. Settings → Community plugins → Turn on community plugins\n  3. Browse and install+enable these 7 plugins:\n     - Vault Nickname\n     - Zotero Integration\n     - Pandoc Reference List\n     - Citations\n     - Dataview\n     - Templater\n     - Pandoc Plugin\n  4. Configure Zotero Integration (Settings → Zotero Integration):\n     - Database Type: Web Library\n     - User ID: $ZOTERO_USER_ID\n     - API Key: (your Zotero API key)\n     - Literature Note Folder: Literature/\n     - Template File: Templates/Zotero-Literature-Note.md\n     - Citation Format: Pandoc\n  5. Test: Cmd+P → 'Zotero Integration: Create literature note'" "Obsidian plugins and Zotero Integration config"

    phase_complete 4 "Repository cloned, Zotero CLI installed."
else
    phase_complete 4 "Skipped repo-dependent tools (no GitHub access). Re-run script later."
fi

# =========================================================================
# Phase 5: Claude Code Customization
# =========================================================================
phase_header 5 "Claude Code Customization"

# --- 5.1 Directory structure ---
info "5.1 Setting up ~/.claude directory"
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/plans
success "Directory structure created"

# --- 5.2-5.4 Install Claude config from repo ---
CLAUDE_CONFIG="$REPO_DIR/claude-config"
if [[ -d "$CLAUDE_CONFIG" ]]; then
    info "5.2 Installing CLAUDE.md and ZOTERO-CLI-REFERENCE.md"
    cp "$CLAUDE_CONFIG/CLAUDE.md" ~/.claude/CLAUDE.md
    success "Installed CLAUDE.md"
    cp "$CLAUDE_CONFIG/ZOTERO-CLI-REFERENCE.md" ~/.claude/ZOTERO-CLI-REFERENCE.md
    success "Installed ZOTERO-CLI-REFERENCE.md"

    info "5.3 Installing skills"
    cp -r "$CLAUDE_CONFIG/skills/"* ~/.claude/skills/
    SKILL_COUNT=$(ls -d ~/.claude/skills/*/SKILL.md ~/.claude/skills/*/skill.md 2>/dev/null | wc -l | tr -d ' ')
    success "Installed $SKILL_COUNT skills"
else
    warn "claude-config/ not found in repo. Skipping CLAUDE.md, skills."
    warn "Re-run this script after cloning the repo to install them."
fi

# --- 5.5 Settings ---
info "5.5 Configuring settings.json"
if [[ -f "$HOME/.claude/settings.json" ]]; then
    warn "~/.claude/settings.json already exists. Skipping to avoid overwriting."
else
    cat > "$HOME/.claude/settings.json" << 'SETTINGSEOF'
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  },
  "permissions": {
    "allow": [
      "Bash(*)",
      "Read(~/.claude/skills/learning-loop/**)",
      "Write(~/.claude/skills/learning-loop/**)",
      "Edit(~/.claude/skills/learning-loop/**)"
    ]
  }
}
SETTINGSEOF
    success "settings.json created"
fi

phase_complete 5 "Claude Code configured with team standards."

# =========================================================================
# Final Summary
# =========================================================================
echo ""
echo -e "${BOLD}=================================================================${NC}"
echo -e "${GREEN}${BOLD}  Setup Complete!${NC}"
echo -e "${BOLD}=================================================================${NC}"
echo ""
echo "  Installed:"

# Check each tool and report status
for tool_check in "git:git --version" "brew:brew --version" "uv:uv --version" "node:node --version" "npm:npm --version" "code:code --version" "claude:claude --version" "pandoc:pandoc --version" "zotero-verify-api:zotero-verify-api --help"; do
    tool="${tool_check%%:*}"
    if check_installed "$tool"; then
        echo -e "    ${GREEN}✓${NC} $tool"
    else
        echo -e "    ${RED}✗${NC} $tool"
    fi
done

# Check apps
for app in "Claude" "Zotero" "Obsidian" "Visual Studio Code"; do
    if [[ -d "/Applications/${app}.app" ]]; then
        echo -e "    ${GREEN}✓${NC} $app.app"
    else
        echo -e "    ${RED}✗${NC} $app.app"
    fi
done

# Check .claude files
echo ""
echo "  Claude Code config:"
for f in "CLAUDE.md" "ZOTERO-CLI-REFERENCE.md" "settings.json"; do
    if [[ -f "$HOME/.claude/$f" ]]; then
        echo -e "    ${GREEN}✓${NC} ~/.claude/$f"
    else
        echo -e "    ${RED}✗${NC} ~/.claude/$f"
    fi
done

SKILL_LIST=$(ls -d ~/.claude/skills/*/SKILL.md ~/.claude/skills/*/skill.md 2>/dev/null | sed 's|.*/skills/||;s|/.*||' | sort -u)
if [[ -n "$SKILL_LIST" ]]; then
    echo -e "    ${GREEN}✓${NC} Skills: $(echo "$SKILL_LIST" | tr '\n' ', ' | sed 's/,$//')"
else
    echo -e "    ${RED}✗${NC} No skills installed"
fi

echo ""
echo "  Next steps:"
echo "    1. Open a new terminal (to pick up ~/.zshrc changes)"
echo "    2. Run 'claude' and type '/skills' to verify skills are loaded"
echo "    3. Start each session with /lla, end with /llr"
if [[ "$REPO_AVAILABLE" != true ]]; then
    echo ""
    echo -e "  ${YELLOW}GitHub-dependent tools not installed yet:${NC}"
    echo "    - Zotero CLI (25 commands)"
    echo "    - Obsidian vault setup script"
    echo ""
    echo "  Once your manager grants GitHub access, re-run this script to"
    echo "  complete the installation. The script is idempotent — it will"
    echo "  skip everything already installed and pick up where it left off."
else
    echo "    4. Set up your first Obsidian vault when your manager assigns a project"
fi
echo ""
