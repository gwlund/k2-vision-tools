# K2 Vision Tools

Development tools and setup automation for K2 Vision team members.

## Quick Start (New MacBook)

```bash
# 1. Install Xcode Command Line Tools (if not already installed)
xcode-select --install

# 2. Clone this repo
git clone https://github.com/gwlund/k2-vision-tools.git ~/Documents/Projects/k2-vision-tools

# 3. Run the setup script
cd ~/Documents/Projects/k2-vision-tools/scripts
bash setup-macbook.sh --starter-kit ~/Downloads/claude-starter-kit.tar.gz
```

The script installs Python, Node.js, VS Code, Claude Code, Zotero, Obsidian, and custom CLI tools. It pauses when manual steps are needed (browser logins, plugin installs).

See `docs/Intern-MacBook-Setup-Guide.md` for the full manual guide.

## What's Included

| Directory | Purpose |
|-----------|---------|
| `scripts/setup-macbook.sh` | Automated MacBook setup (~45 min) |
| `scripts/zotero-cli/` | 25 CLI commands for Zotero library management |
| `scripts/obsidian-setup/` | Obsidian vault setup with Zotero integration |
| `docs/` | Setup guide and documentation |

## Zotero CLI Quick Reference

```bash
zotero-verify-api                    # Test API credentials
zotero-import-doi 10.1234/example    # Import paper by DOI
zotero-search-items "search term"    # Search library
zotero-list-collections              # Show all collections
```

Run `zotero-verify-api --help` for any command's options.
