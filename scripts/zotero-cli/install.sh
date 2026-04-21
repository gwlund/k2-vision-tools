#!/bin/bash
# Install Zotero CLI scripts to ~/.local/bin for global access
# Creates a standalone uv virtual environment in ~/.local/lib/zotero-cli-venv/

set -e

echo "=== Zotero CLI Installer ==="
echo

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check we're in the right directory
if [ ! -d "bin" ] || [ ! -d "lib" ]; then
    echo -e "${RED}✗${NC} Must run from scripts/zotero-cli/ directory"
    exit 1
fi

# Check uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗${NC} uv is not installed"
    echo "  Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Directories
INSTALL_DIR="$HOME/.local/lib/zotero-cli"
VENV_DIR="$HOME/.local/lib/.venv"
BIN_DIR="$HOME/.local/bin"

# Create directories
mkdir -p "$INSTALL_DIR" "$BIN_DIR"

echo "Step 1: Copying scripts and libraries..."
# Copy all scripts and libraries
cp -r bin "$INSTALL_DIR/"
cp -r lib "$INSTALL_DIR/"
cp pyproject.toml "$INSTALL_DIR/"
cp .python-version "$INSTALL_DIR/" 2>/dev/null || echo "3.13" > "$INSTALL_DIR/.python-version"
echo -e "${GREEN}✓${NC} Scripts and libraries copied to $INSTALL_DIR"

echo
echo "Step 2: Creating dedicated virtual environment..."
# Create venv with uv in the install directory
cd "$INSTALL_DIR"
uv venv "$VENV_DIR" --python 3.13
echo -e "${GREEN}✓${NC} Virtual environment created at $VENV_DIR"

echo
echo "Step 3: Installing Python dependencies..."
# Install dependencies into the venv
uv pip install --python "$VENV_DIR/bin/python" pyzotero click rich requests crossrefapi habanero
echo -e "${GREEN}✓${NC} Dependencies installed in venv"

echo
echo "Step 4: Creating executable wrapper scripts..."
# Create wrapper scripts in ~/.local/bin
for script in "$INSTALL_DIR"/bin/*; do
    script_name=$(basename "$script")
    wrapper_path="$BIN_DIR/$script_name"

    cat > "$wrapper_path" << EOF
#!/bin/bash
# Wrapper for $script_name - uses dedicated uv venv at $VENV_DIR
export PYTHONPATH="$INSTALL_DIR/lib:\$PYTHONPATH"
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/bin/$script_name" "\$@"
EOF

    chmod +x "$wrapper_path"
    echo -e "${GREEN}✓${NC} Created: $script_name"
done

echo
echo "=== Installation Complete ==="
echo
echo "Installation location:"
echo "  Scripts:  $INSTALL_DIR"
echo "  Venv:     $VENV_DIR"
echo "  Wrappers: $BIN_DIR"
echo
echo "Installed commands:"
echo ""
echo "Read Operations:"
echo "  - zotero-list-collections     # Browse collection hierarchy"
echo "  - zotero-search-items         # Search and list items"
echo "  - zotero-get-item             # View detailed item information"
echo "  - zotero-get-citekey          # Get Better BibTeX citation key"
echo "  - zotero-list-tags            # List and filter tags"
echo "  - zotero-get-collection-items # View collection contents"
echo ""
echo "Write Operations:"
echo "  - zotero-verify-api           # Test API credentials"
echo "  - zotero-create-collection    # Create collections"
echo "  - zotero-add-item             # Add items manually (with duplicate detection)"
echo "  - zotero-import-doi           # Import from DOI (with duplicate detection)"
echo "  - zotero-add-tags             # Add tags to items"
echo "  - zotero-update-item          # Update item metadata (extended fields)"
echo "  - zotero-create-parent        # Create parent for standalone PDFs"
echo ""
echo "Collection Management:"
echo "  - zotero-rename-collection    # Rename collections"
echo "  - zotero-move-collection      # Move collections to different parents"
echo "  - zotero-delete-collection    # Delete collections and subcollections"
echo ""
echo "Duplicate Management:"
echo "  - zotero-find-duplicates      # Find DOI-based duplicates"
echo "  - zotero-merge-duplicates     # Interactively merge duplicates"
echo "  - zotero-delete-item          # Delete items from library"
echo

# Check PATH
if echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo -e "${GREEN}✓${NC} ~/.local/bin is in your PATH"
    echo
    echo "Test installation:"
    echo "  zotero-verify-api"
else
    echo -e "${YELLOW}⚠${NC}  ~/.local/bin is NOT in your PATH"
    echo "  Add this to ~/.zshrc:"
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo "  Then run: source ~/.zshrc"
    echo
    echo "Then test with:"
    echo "  zotero-verify-api"
fi
echo
