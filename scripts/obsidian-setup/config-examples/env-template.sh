#!/bin/bash
# Zotero Environment Variables Template
# Copy this to your ~/.zshrc or ~/.bash_profile

# ==============================================================================
# Zotero API Credentials
# ==============================================================================
# Get these from: https://www.zotero.org/settings/keys
#
# Instructions:
# 1. Go to https://www.zotero.org/settings/keys
# 2. Click "Create new private key"
# 3. Give it a name (e.g., "Obsidian Integration")
# 4. Set permissions:
#    - Library Access: Read/Write
#    - Notes Access: Read/Write
#    - File Access: Read/Write
# 5. Save the key
# 6. Copy the API key (24 characters) and User ID (8 digits)

export ZOTERO_API_KEY="your_24_character_api_key_here"
export ZOTERO_USER_ID="your_8_digit_user_id_here"

# ==============================================================================
# Optional: Zotero Library Type
# ==============================================================================
# Options: "user" (personal library) or "group" (group library)
# Default: "user"
export ZOTERO_LIBRARY_TYPE="user"

# ==============================================================================
# Optional: Obsidian Vault Path
# ==============================================================================
# Set this if you want to use a specific vault path by default
# export OBSIDIAN_VAULT_PATH="$HOME/Documents/Research"

# ==============================================================================
# Verification
# ==============================================================================
# After adding to your shell config, run:
#   source ~/.zshrc  # or source ~/.bash_profile
#   echo $ZOTERO_API_KEY
#   echo $ZOTERO_USER_ID
#
# Test API connection:
#   curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
#     "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
