# Obsidian Setup Skill

Automated Obsidian vault setup with Zotero Integration for academic literature management.

## Installation

Copy this folder to your user skills directory:

```bash
cp -r skills/custom/obsidian-setup ~/.claude/skills/
```

## Contents

```
obsidian-setup/
├── skill.md                    # Main skill documentation
├── README.md                   # This file
├── scripts/
│   ├── setup-obsidian-vault.sh # Automated vault setup
│   └── verify-obsidian-setup.sh # Verification testing
├── templates/
│   └── Zotero-Literature-Note.md # Handlebars template
├── guides/
│   └── QUICK-START.md          # 10-minute setup guide
└── config-examples/
    └── env-template.sh         # Environment variable template
```

## Usage

After installation, run from any project directory:

```bash
# Set up a new Obsidian vault with Zotero integration
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh

# Verify the setup
bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh
```

## Prerequisites

1. Set Zotero environment variables:
   ```bash
   export ZOTERO_API_KEY="your_24_character_api_key"
   export ZOTERO_USER_ID="your_8_digit_user_id"
   ```

2. Get credentials from: https://www.zotero.org/settings/keys

## Documentation

- **skill.md** - Complete skill documentation with methodology
- **guides/QUICK-START.md** - Fast 10-minute setup guide
- **config-examples/env-template.sh** - Environment variable template

## Version

- **Version**: 1.1.0
- **Updated**: 2025-12-18
- **Author**: Gil Lund
