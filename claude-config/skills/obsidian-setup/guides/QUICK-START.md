# Obsidian + Zotero Integration - Quick Start

**Estimated Setup Time:** 10 minutes

## Prerequisites Checklist

- [ ] Obsidian installed ([download](https://obsidian.md))
- [ ] Zotero installed ([download](https://www.zotero.org/download/))
- [ ] Zotero API Key obtained ([get key](https://www.zotero.org/settings/keys))
- [ ] Zotero User ID noted (8-digit number from API key page)

## Quick Setup (3 Steps)

### Step 1: Set Environment Variables (2 minutes)

```bash
# Add to ~/.zshrc or ~/.bash_profile
export ZOTERO_API_KEY="your_24_character_api_key"
export ZOTERO_USER_ID="your_8_digit_user_id"

# Reload shell
source ~/.zshrc  # or source ~/.bash_profile
```

**Verify:**
```bash
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID
```

### Step 2: Run Setup Script (3 minutes)

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run automated setup
bash scripts/obsidian-setup/setup-obsidian-vault.sh
```

**What it creates:**
- ✓ `Literature/` - Auto-generated literature notes
- ✓ `Literature/attachments/` - PDFs and files
- ✓ `Synthesis/` - Your research notes
- ✓ `Templates/Zotero-Literature-Note.md` - Note template
- ✓ `README.md` - Setup documentation
- ✓ `.gitignore` - Git configuration

### Step 3: Configure Obsidian (5 minutes)

#### 3a. Open Vault
1. Launch Obsidian
2. **File → Open folder as vault**
3. Select your project directory
4. Click **Open**

#### 3b. Install Plugin
1. **Settings** (⚙️) → **Community plugins**
2. Click **Browse**
3. Search: `Zotero Integration`
4. Click **Install** → **Enable**

#### 3c. Configure Plugin
1. **Settings** → **Zotero Integration**
2. Enter these settings:

| Setting | Value |
|---------|-------|
| **Database Type** | Web Library |
| **User ID** | Your 8-digit Zotero user ID |
| **API Key** | Your 24-character API key |
| **Literature Note Folder** | `Literature/` |
| **Template File** | `Templates/Zotero-Literature-Note.md` |
| **Image Folder** | `Literature/attachments/` |
| **Import Attachments** | ✓ Enabled |
| **Citation Format** | Pandoc (`[@citekey]`) |

3. Click **Save**

## Test the Integration (1 minute)

### Create Your First Literature Note

1. Press `Ctrl/Cmd + P` (Command Palette)
2. Type: `Zotero Integration: Create literature note`
3. Search for a paper in your Zotero library
4. Select it
5. **Done!** Note auto-populates with metadata

### Cite in Your Notes

In any note, type `[@` and autocomplete will show your Zotero items.

**Example:**
```markdown
Recent research shows [@smith2024climate] that...
```

## Verification Commands

```bash
# Test vault structure
bash scripts/obsidian-setup/tests/verify-obsidian-setup.sh

# Test Zotero API connection
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
```

## Common Commands Reference

| Action | Command |
|--------|---------|
| Create literature note | `Ctrl/Cmd + P` → `Zotero Integration: Create literature note` |
| Insert citation | Type `[@` then select from autocomplete |
| Import multiple notes | `Ctrl/Cmd + P` → `Zotero Integration: Import notes` |
| Open in Zotero | `Ctrl/Cmd + P` → `Zotero Integration: Open in Zotero` |
| Update literature note | `Ctrl/Cmd + P` → `Zotero Integration: Update literature note` |

## Troubleshooting (Quick Fixes)

### Plugin won't connect to Zotero
```bash
# Verify credentials
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID

# Test API manually
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
```

### Template not populating
- Check path in settings: `Templates/Zotero-Literature-Note.md`
- Verify file exists: `ls Templates/`

### Citations not working
- Ensure Zotero Integration plugin is enabled
- Type `[@` (not just `@`)
- Check that item has citation key in Zotero

## Next Steps

- [ ] Import 3-5 key papers
- [ ] Create your first synthesis note in `Synthesis/`
- [ ] Practice citing papers using `[@citekey]` format
- [ ] Explore template customization (edit `Templates/Zotero-Literature-Note.md`)

## Full Documentation

- **Complete Setup Guide:** `docs/guides/obsidian-zotero-setup-guide.md`
- **Citation Verification Workflow:** `docs/guides/citation-source-verification-guide.md`
- **Troubleshooting:** `docs/guides/obsidian-zotero-setup-guide.md#troubleshooting`

## Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Zotero Integration Plugin](https://github.com/mgmeyers/obsidian-zotero-integration)
- [Zotero Documentation](https://www.zotero.org/support/)
- [Better BibTeX](https://retorque.re/zotero-better-bibtex/) (optional - for custom citation keys)

---

**Setup Complete!** You're ready to start managing citations and literature notes.
