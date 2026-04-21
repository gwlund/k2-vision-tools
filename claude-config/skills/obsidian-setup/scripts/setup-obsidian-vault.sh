#!/bin/bash
# Automated Obsidian + Zotero Integration Setup Script
# Creates folder structure and templates for Obsidian vault
#
# Usage:
#   bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh
#   bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh --non-interactive --vault-path /path/to/vault
#   bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh --vault-name "My Research Project"

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory - supports both skill location and project location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Determine skill root directory (parent of scripts/)
if [[ "$SCRIPT_DIR" == *"/.claude/skills/obsidian-setup/scripts" ]]; then
    SKILL_DIR="$HOME/.claude/skills/obsidian-setup"
elif [[ "$SCRIPT_DIR" == *"/skills/custom/obsidian-setup/scripts" ]]; then
    SKILL_DIR="$(dirname "$SCRIPT_DIR")"
else
    # Fallback to script's parent directory
    SKILL_DIR="$(dirname "$SCRIPT_DIR")"
fi

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to print header
print_header() {
    echo
    echo "======================================================================"
    echo "  $1"
    echo "======================================================================"
    echo
}

# Check if running in non-interactive mode
NON_INTERACTIVE=false
VAULT_PATH=""
VAULT_NAME=""

# Vault Nickname plugin version
VAULT_NICKNAME_VERSION="1.1.11"
VAULT_NICKNAME_BASE_URL="https://github.com/rscopic/obsidian-vault-nickname/releases/download/${VAULT_NICKNAME_VERSION}"

while [[ $# -gt 0 ]]; do
    case $1 in
        --non-interactive)
            NON_INTERACTIVE=true
            shift
            ;;
        --vault-path)
            VAULT_PATH="$2"
            shift 2
            ;;
        --vault-name)
            VAULT_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--non-interactive] [--vault-path PATH] [--vault-name NAME]"
            exit 1
            ;;
    esac
done

print_header "Obsidian + Zotero Integration Setup"

echo "This script will:"
echo "  1. Check prerequisites"
echo "  2. Create folder structure"
echo "  3. Install templates"
echo "  4. Create README and documentation"
echo "  5. Generate configuration examples"
echo "  6. Install Vault Nickname plugin (custom display name)"
echo

# Check prerequisites
print_header "Step 1: Checking Prerequisites"

# Check for Zotero credentials
PREREQ_PASS=true

if [ -z "$ZOTERO_API_KEY" ]; then
    print_error "ZOTERO_API_KEY not set"
    print_info "Get your API key from: https://www.zotero.org/settings/keys"
    print_info "Set with: export ZOTERO_API_KEY='your_key_here'"
    PREREQ_PASS=false
else
    print_success "ZOTERO_API_KEY is set"
fi

if [ -z "$ZOTERO_USER_ID" ]; then
    print_error "ZOTERO_USER_ID not set"
    print_info "Get your User ID from: https://www.zotero.org/settings/keys"
    print_info "Set with: export ZOTERO_USER_ID='your_id_here'"
    PREREQ_PASS=false
else
    print_success "ZOTERO_USER_ID is set"
fi

# Check for Obsidian (optional)
if command -v obsidian &> /dev/null || [ -d "/Applications/Obsidian.app" ]; then
    print_success "Obsidian is installed"
else
    print_warning "Obsidian not detected (optional - install from https://obsidian.md)"
fi

if [ "$PREREQ_PASS" = false ]; then
    echo
    print_error "Prerequisites not met. Please set required environment variables."
    exit 1
fi

echo

# Get vault path
if [ -z "$VAULT_PATH" ]; then
    if [ "$NON_INTERACTIVE" = true ]; then
        VAULT_PATH="."
    else
        echo "Where should the Obsidian vault be created?"
        echo "  1) Current directory ($(pwd))"
        echo "  2) New directory"
        echo "  3) Specify path"
        echo
        read -p "Choose [1-3]: " choice

        case $choice in
            1)
                VAULT_PATH="."
                ;;
            2)
                read -p "Enter new directory name: " dirname
                VAULT_PATH="$dirname"
                mkdir -p "$VAULT_PATH"
                ;;
            3)
                read -p "Enter full path: " custom_path
                VAULT_PATH="$custom_path"
                ;;
            *)
                print_error "Invalid choice"
                exit 1
                ;;
        esac
    fi
fi

# Convert to absolute path
VAULT_PATH="$(cd "$VAULT_PATH" 2>/dev/null && pwd)" || {
    mkdir -p "$VAULT_PATH"
    VAULT_PATH="$(cd "$VAULT_PATH" && pwd)"
}

print_info "Vault location: $VAULT_PATH"
echo

# Get vault name (for Obsidian display via Vault Nickname plugin)
if [ -z "$VAULT_NAME" ]; then
    if [ "$NON_INTERACTIVE" = true ]; then
        # Default to parent directory name
        VAULT_NAME="$(basename "$(dirname "$VAULT_PATH")")"
    else
        # Suggest parent directory name as default
        DEFAULT_NAME="$(basename "$(dirname "$VAULT_PATH")")"
        echo "What should this vault be called in Obsidian?"
        echo "  (Uses the Vault Nickname plugin to display a custom name)"
        echo
        read -p "Vault display name [$DEFAULT_NAME]: " vault_name_input
        VAULT_NAME="${vault_name_input:-$DEFAULT_NAME}"
    fi
fi

print_info "Vault display name: $VAULT_NAME"
echo

# Confirm settings
if [ "$NON_INTERACTIVE" = false ]; then
    print_header "Configuration Summary"
    echo "Vault Path:        $VAULT_PATH"
    echo "Vault Display Name: $VAULT_NAME"
    echo "Zotero User ID:    $ZOTERO_USER_ID"
    echo "API Key:           ${ZOTERO_API_KEY:0:8}... (hidden)"
    echo
    read -p "Continue with setup? [Y/n]: " confirm
    if [[ $confirm =~ ^[Nn]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
fi

# Create folder structure
print_header "Step 2: Creating Folder Structure"

cd "$VAULT_PATH"

FOLDERS=(
    "Literature"
    "Literature/attachments"
    "Synthesis"
    "Templates"
    "docs"
)

for folder in "${FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        print_warning "$folder already exists"
    else
        mkdir -p "$folder"
        print_success "Created $folder/"
    fi
done

# Install templates
print_header "Step 3: Installing Templates"

# Try to copy from skill directory first, then create inline
TEMPLATE_SOURCE="$SKILL_DIR/templates/Zotero-Literature-Note.md"

if [ -f "$TEMPLATE_SOURCE" ]; then
    cp "$TEMPLATE_SOURCE" Templates/
    print_success "Installed Literature Note template from skill"
else
    # Create inline if template file doesn't exist
    cat > Templates/Zotero-Literature-Note.md << 'TEMPLATE'
---
type: literature-note
title: "{{title}}"
authors: {{authors}}
year: {{date | format("YYYY")}}
citekey: {{citekey}}
zotero-key: {{itemKey}}
tags: [literature, {{tags}}]
---

# {{title}}

## Metadata

- **Authors:** {{authors}}
- **Year:** {{date | format("YYYY")}}
- **Type:** {{itemType}}
{{#if publicationTitle}}- **Publication:** {{publicationTitle}}{{/if}}
{{#if DOI}}- **DOI:** [{{DOI}}](https://doi.org/{{DOI}}){{/if}}
{{#if url}}- **URL:** {{url}}{{/if}}
- **Zotero:** [Open in Zotero]({{desktopURI}})

## Abstract

{{abstractNote}}

## Key Findings

1.
2.
3.

## Methodology

{{#if methods}}
{{methods}}
{{else}}
[Describe research methodology]
{{/if}}

## Relevance to Project

[How this relates to your research]

## Strengths

-

## Limitations

-

## Key Quotes

> "Quote here" (p. XX)

## Personal Notes

{{notes}}

## Related Literature

- [[]]

## Tags

{{tags}}

## Attachments

{{#each attachments}}
- [{{title}}]({{path}})
{{/each}}

---

**Created:** {{importDate | format("YYYY-MM-DD")}}
**Zotero Key:** {{itemKey}}
**Citation:** {{citation}}
TEMPLATE
    print_success "Created Literature Note template"
fi

# Create README
print_header "Step 4: Creating Documentation"

cat > README.md << 'EOF'
# Research Project

Obsidian vault integrated with Zotero for literature management and citation.

## Structure

```
.
├── Literature/              # Auto-generated literature notes from Zotero
│   └── attachments/        # PDFs, images, and other attachments
├── Synthesis/              # Research synthesis and analysis notes
├── Templates/              # Note templates
│   └── Zotero-Literature-Note.md
├── docs/                   # Project documentation
└── README.md              # This file
```

## Getting Started

### 1. Open in Obsidian

1. Launch Obsidian
2. Click "Open folder as vault"
3. Select this directory
4. Click "Open"

### 2. Install Zotero Integration Plugin

1. Settings (⚙️) → Community plugins
2. Click "Browse"
3. Search "Zotero Integration"
4. Install and Enable

### 3. Configure Zotero Integration

Settings → Zotero Integration:

- **Database Type:** Web Library
- **User ID:** Your 8-digit Zotero user ID
- **API Key:** Your Zotero API key
- **Literature Note Folder:** `Literature/`
- **Template File:** `Templates/Zotero-Literature-Note.md`
- **Image Folder:** `Literature/attachments/`

### 4. Import Your First Paper

1. Press `Ctrl/Cmd + P` (Command Palette)
2. Type: "Zotero Integration: Create literature note"
3. Search for a paper in your Zotero library
4. Select it - template auto-populates!

### 5. Cite in Your Notes

In any note, type `[@` and the autocomplete will show your Zotero items.

Example:
```markdown
Recent research shows [@smith2024climate] that...
```

## Common Commands

| Action | Command |
|--------|---------|
| Create literature note | `Ctrl/Cmd + P` → "Zotero Integration: Create literature note" |
| Insert citation | Type `[@` then select |
| Import multiple notes | `Ctrl/Cmd + P` → "Zotero Integration: Import notes" |
| Open in Zotero | `Ctrl/Cmd + P` → "Zotero Integration: Open in Zotero" |

## Troubleshooting

### Plugin not connecting to Zotero

1. Verify credentials:
   ```bash
   echo $ZOTERO_API_KEY
   echo $ZOTERO_USER_ID
   ```

2. Test API:
   ```bash
   curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
   ```

### Template not populating

1. Check template path in settings: `Templates/Zotero-Literature-Note.md`
2. Verify template file exists: `ls Templates/`

## Next Steps

- [ ] Install Zotero Integration plugin in Obsidian
- [ ] Configure plugin with your credentials
- [ ] Import your key papers
- [ ] Create first synthesis note
- [ ] Practice citing in your notes

---

**Vault Type:** Obsidian + Zotero Integration
EOF

print_success "Created README.md"

# Create .gitignore
cat > .gitignore << 'EOF'
# Obsidian
.obsidian/workspace*
.obsidian/cache
.trash/

# System
.DS_Store
Thumbs.db

# Optional: Uncomment to not track attachments (PDFs can be large)
# Literature/attachments/

# Optional: Uncomment to keep .obsidian config private
# .obsidian/
EOF

print_success "Created .gitignore"

# Create marker file
touch .obsidian-setup-complete
print_success "Created setup marker file"

# Generate configuration example
print_header "Step 5: Generating Configuration Examples"

mkdir -p .config-examples

cat > .config-examples/plugin-settings.json << EOF
{
  "zoteroIntegration": {
    "database": {
      "type": "webLibrary",
      "userId": "$ZOTERO_USER_ID",
      "apiKey": "$ZOTERO_API_KEY"
    },
    "import": {
      "dataDirectory": "Literature/",
      "templateFile": "Templates/Zotero-Literature-Note.md",
      "attachmentDirectory": "Literature/attachments/",
      "importAttachments": true
    },
    "citation": {
      "format": "pandoc",
      "bracketStyle": "[@citekey]"
    },
    "format": {
      "dateFormat": "YYYY-MM-DD",
      "authorFormat": "Last, First"
    }
  }
}
EOF

print_success "Created configuration example"

# Install Vault Nickname plugin
print_header "Step 6: Installing Vault Nickname Plugin"

print_info "Installing Vault Nickname plugin for custom display name..."

PLUGIN_DIR=".obsidian/plugins/vault-nickname"
mkdir -p "$PLUGIN_DIR"

# Download plugin files from GitHub release
DOWNLOAD_OK=true

if curl -sL -o "$PLUGIN_DIR/main.js" "${VAULT_NICKNAME_BASE_URL}/main.js" 2>/dev/null && [ -s "$PLUGIN_DIR/main.js" ]; then
    print_success "Downloaded vault-nickname main.js"
else
    print_warning "Failed to download main.js — install Vault Nickname plugin manually in Obsidian"
    DOWNLOAD_OK=false
fi

if curl -sL -o "$PLUGIN_DIR/manifest.json" "${VAULT_NICKNAME_BASE_URL}/manifest.json" 2>/dev/null && [ -s "$PLUGIN_DIR/manifest.json" ]; then
    print_success "Downloaded vault-nickname manifest.json"
else
    print_warning "Failed to download manifest.json — install Vault Nickname plugin manually in Obsidian"
    DOWNLOAD_OK=false
fi

if [ "$DOWNLOAD_OK" = true ]; then
    # Write plugin settings
    cat > "$PLUGIN_DIR/data.json" << 'PLUGINDATA'
{
  "overrideAppTitle": "override-app-title:file-first",
  "enableBackwardsCompatibilty": false
}
PLUGINDATA

    # Write the nickname
    cat > "$PLUGIN_DIR/data-shared.json" << NICKNAME
{
  "nickname": "$VAULT_NAME"
}
NICKNAME

    # Enable the plugin in community-plugins.json
    COMMUNITY_PLUGINS=".obsidian/community-plugins.json"
    if [ -f "$COMMUNITY_PLUGINS" ]; then
        # Check if jq is available for safe JSON manipulation
        if command -v jq &> /dev/null; then
            jq '. += ["vault-nickname"] | unique' "$COMMUNITY_PLUGINS" > "$COMMUNITY_PLUGINS.tmp" && mv "$COMMUNITY_PLUGINS.tmp" "$COMMUNITY_PLUGINS"
        else
            # Fallback: read existing, add if not present
            if ! grep -q '"vault-nickname"' "$COMMUNITY_PLUGINS"; then
                sed -i '' 's/\]/"vault-nickname"]/' "$COMMUNITY_PLUGINS"
                # Fix missing comma if array wasn't empty
                sed -i '' 's/""vault-nickname"/","vault-nickname"/' "$COMMUNITY_PLUGINS"
            fi
        fi
    else
        echo '["vault-nickname"]' > "$COMMUNITY_PLUGINS"
    fi

    print_success "Vault Nickname plugin configured: \"$VAULT_NAME\""
else
    print_warning "Vault Nickname plugin not installed — set display name manually after installing plugin"
    print_info "Install in Obsidian: Settings → Community plugins → Browse → 'Vault Nickname'"
fi

# Summary
print_header "Setup Complete!"

echo "Folder structure created:"
for folder in "${FOLDERS[@]}"; do
    echo "  ✓ $folder/"
done
echo

echo "Files created:"
echo "  ✓ Templates/Zotero-Literature-Note.md"
echo "  ✓ README.md"
echo "  ✓ .gitignore"
echo "  ✓ .config-examples/plugin-settings.json"
if [ "$DOWNLOAD_OK" = true ]; then
echo "  ✓ .obsidian/plugins/vault-nickname/ (display name: \"$VAULT_NAME\")"
fi
echo

print_header "Next Steps"

echo "1. Open this folder in Obsidian:"
echo "   ${BLUE}$VAULT_PATH${NC}"
echo

echo "2. Install Zotero Integration plugin:"
echo "   Settings → Community plugins → Browse → 'Zotero Integration'"
echo

echo "3. Configure the plugin:"
echo "   Settings → Zotero Integration"
echo "   - User ID: $ZOTERO_USER_ID"
echo "   - API Key: ${ZOTERO_API_KEY:0:8}..."
echo "   - Literature folder: Literature/"
echo "   - Template: Templates/Zotero-Literature-Note.md"
echo

echo "4. Test the integration:"
echo "   Ctrl/Cmd + P → 'Zotero Integration: Create literature note'"
echo

echo "5. Verify setup:"
echo "   bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh"
echo

print_success "Setup complete! Happy researching!"
