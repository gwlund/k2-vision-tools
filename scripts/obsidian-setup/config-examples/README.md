# Configuration Examples

This directory contains example configuration files for Obsidian + Zotero Integration setup.

## Files

### `zotero-integration-settings.json`

Example configuration for the Obsidian Zotero Integration plugin. This represents the settings stored in `.obsidian/plugins/obsidian-zotero-integration/data.json`.

**Usage:**
1. Install Zotero Integration plugin in Obsidian
2. Open Settings → Zotero Integration
3. Configure manually using these values as reference
4. Or copy to `.obsidian/plugins/obsidian-zotero-integration/data.json` (after installing plugin)

**Key Settings:**

| Setting | Value | Description |
|---------|-------|-------------|
| `database.type` | `webLibrary` | Use Zotero Web API (recommended) |
| `database.userId` | 8-digit number | Your Zotero user ID |
| `database.apiKey` | 24 characters | Your Zotero API key |
| `import.dataDirectory` | `Literature/` | Where literature notes are created |
| `import.templateFile` | `Templates/Zotero-Literature-Note.md` | Template path |
| `import.attachmentDirectory` | `Literature/attachments/` | PDF storage |
| `citation.format` | `pandoc` | Pandoc-style citations |
| `citation.bracketStyle` | `[@citekey]` | Standard citation format |

### `env-template.sh`

Template for Zotero environment variables. Add these to your shell configuration file.

**Usage:**

```bash
# Copy template to your home directory
cp config-examples/env-template.sh ~/.zotero-env.sh

# Edit with your credentials
nano ~/.zotero-env.sh

# Add to your shell config
echo "source ~/.zotero-env.sh" >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Verify
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID
```

**Security Note:** Never commit files containing your actual API keys to version control.

## Getting Your Zotero Credentials

### Step 1: Get API Key and User ID

1. Go to: https://www.zotero.org/settings/keys
2. Click **"Create new private key"**
3. Name: `Obsidian Integration`
4. Set permissions:
   - ✓ Allow library access: Read/Write
   - ✓ Allow notes access: Read/Write
   - ✓ Allow file access: Read/Write
   - ✓ Allow write access
5. Click **"Save Key"**
6. Copy the displayed API key (24 characters)
7. Note your User ID (8-digit number shown on the page)

### Step 2: Set Environment Variables

**For macOS/Linux (zsh):**
```bash
echo 'export ZOTERO_API_KEY="your_key_here"' >> ~/.zshrc
echo 'export ZOTERO_USER_ID="your_id_here"' >> ~/.zshrc
source ~/.zshrc
```

**For macOS/Linux (bash):**
```bash
echo 'export ZOTERO_API_KEY="your_key_here"' >> ~/.bash_profile
echo 'export ZOTERO_USER_ID="your_id_here"' >> ~/.bash_profile
source ~/.bash_profile
```

**For Windows (PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("ZOTERO_API_KEY", "your_key_here", "User")
[Environment]::SetEnvironmentVariable("ZOTERO_USER_ID", "your_id_here", "User")
```

### Step 3: Verify

Test your connection:
```bash
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
```

Expected response: JSON data with one Zotero item (or empty array if library is empty).

## Plugin Installation

### Zotero Integration Plugin

1. Open Obsidian
2. **Settings** → **Community plugins**
3. Click **"Browse"**
4. Search: `Zotero Integration`
5. Install plugin by **mgmeyers**
6. Click **"Enable"**

### Configure Plugin

1. **Settings** → **Zotero Integration**
2. Use values from `zotero-integration-settings.json`
3. Click **"Save"**

## Testing Configuration

After setup, test with:

```bash
# Run verification script
bash scripts/obsidian-setup/tests/verify-obsidian-setup.sh

# Or test manually in Obsidian
# Ctrl/Cmd + P → "Zotero Integration: Create literature note"
```

## Troubleshooting

### "Invalid API Key" Error

- Verify key is exactly 24 characters
- Check for extra spaces or quotes
- Ensure permissions include Read/Write access
- Try regenerating key

### "User ID not found" Error

- User ID should be numeric (8 digits)
- Found on https://www.zotero.org/settings/keys
- Often displayed near the top of the API keys page

### Plugin won't connect

1. Check environment variables are set:
   ```bash
   echo $ZOTERO_API_KEY
   echo $ZOTERO_USER_ID
   ```

2. Test API manually:
   ```bash
   curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
     "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
   ```

3. Restart Obsidian after changing settings

### Template not working

- Check template path: `Templates/Zotero-Literature-Note.md`
- Verify file exists: `ls Templates/`
- Check YAML frontmatter syntax (three dashes `---`)
- Validate Handlebars variables (`{{variable}}`)

## Additional Resources

- [Zotero API Documentation](https://www.zotero.org/support/dev/web_api/v3/start)
- [Obsidian Zotero Integration Plugin](https://github.com/mgmeyers/obsidian-zotero-integration)
- [Handlebars Template Syntax](https://handlebarsjs.com/guide/)
- [Pandoc Citation Syntax](https://pandoc.org/MANUAL.html#citations)

---

**See also:**
- Full setup guide: `docs/guides/obsidian-zotero-setup-guide.md`
- Quick start: `scripts/obsidian-setup/QUICK-START.md`
- Citation workflow: `docs/guides/citation-source-verification-guide.md`
