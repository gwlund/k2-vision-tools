# Obsidian + Zotero Integration Setup Tools

Complete toolkit for setting up Obsidian vaults with Zotero Integration for academic literature management and citation workflows.

## Quick Start

**Setup time:** ~10 minutes

```bash
# 1. Set environment variables
export ZOTERO_API_KEY="your_24_character_key"
export ZOTERO_USER_ID="your_8_digit_id"

# 2. Navigate to your project
cd /path/to/your/research-project

# 3. Run setup script
bash scripts/obsidian-setup/setup-obsidian-vault.sh

# 4. Verify setup
bash scripts/obsidian-setup/tests/verify-obsidian-setup.sh
```

**Then in Obsidian:**
1. Open folder as vault
2. Install "Zotero Integration" plugin
3. Configure with your credentials
4. Test: `Ctrl/Cmd + P` → "Create literature note"

See [QUICK-START.md](QUICK-START.md) for detailed instructions.

## What's Included

### Scripts

#### `setup-obsidian-vault.sh`
Automated vault setup script that creates:
- Folder structure (Literature, Synthesis, Templates, docs)
- Literature note template with Handlebars variables
- README and documentation
- Git configuration (.gitignore)
- Configuration examples

**Usage:**
```bash
# Interactive mode (prompts for vault path)
./setup-obsidian-vault.sh

# Non-interactive mode (use current directory)
./setup-obsidian-vault.sh --non-interactive --vault-path .

# Specify path
./setup-obsidian-vault.sh --vault-path /path/to/vault
```

### Tests

#### `tests/verify-obsidian-setup.sh`
Comprehensive verification script that checks:
- ✓ Folder structure (Literature, Synthesis, Templates, docs)
- ✓ Required files (template, README, .gitignore)
- ✓ Zotero credentials (format validation)
- ✓ Zotero API connection (live test)
- ✓ Template syntax (YAML, Handlebars)
- ✓ File permissions (write access)

**Usage:**
```bash
# Test current directory
./tests/verify-obsidian-setup.sh

# Test specific vault
./tests/verify-obsidian-setup.sh /path/to/vault
```

**Example output:**
```
======================================================================
  Obsidian Vault Setup Verification
======================================================================

Testing vault at: /Users/username/Research

✓ Found: Literature/
✓ Found: Literature/attachments/
✓ Found: Templates/Zotero-Literature-Note.md
✓ Template contains: {{title}}
✓ ZOTERO_API_KEY is set
✓ Zotero API connection successful
✓ Vault structure is READY
```

### Templates

#### `templates/Zotero-Literature-Note.md`
Production-ready Handlebars template for Zotero Integration plugin.

**Features:**
- YAML frontmatter with metadata fields
- Conditional rendering (`{{#if DOI}}...{{/if}}`)
- Date formatting (`{{date | format("YYYY")}}`)
- Comprehensive sections:
  - Metadata, Abstract, Key Findings
  - Methodology, Relevance, Strengths/Limitations
  - Key Quotes, Personal Notes
  - Related Literature, Tags, Attachments

**Template variables:**
```handlebars
{{title}}           - Paper title
{{authors}}         - Author list
{{date}}            - Publication date (use format filter)
{{itemType}}        - journal-article, book, etc.
{{publicationTitle}} - Journal/book name
{{DOI}}             - Digital Object Identifier
{{url}}             - Item URL
{{abstractNote}}    - Abstract text
{{citekey}}         - Citation key (Better BibTeX)
{{itemKey}}         - Zotero API key
{{desktopURI}}      - zotero://select/items/... link
{{notes}}           - Zotero notes
{{attachments}}     - PDFs and files (use {{#each}})
{{tags}}            - Zotero tags
{{importDate}}      - Import timestamp
{{citation}}        - Formatted citation
```

See [Zotero Integration docs](https://github.com/mgmeyers/obsidian-zotero-integration#template-variables) for full variable list.

### Configuration Examples

#### `config-examples/zotero-integration-settings.json`
Example plugin configuration showing all available settings.

**Key settings:**
- Database connection (Web Library vs Local Zotero)
- Import paths (Literature/, attachments/)
- Template file location
- Citation format (Pandoc, bracket style)
- Date and author formatting

**Usage:** Reference when configuring plugin in Obsidian Settings.

#### `config-examples/env-template.sh`
Template for shell environment variables.

**Usage:**
```bash
# Copy and customize
cp config-examples/env-template.sh ~/.zotero-env.sh
nano ~/.zotero-env.sh  # Add your credentials

# Source in shell config
echo "source ~/.zotero-env.sh" >> ~/.zshrc
source ~/.zshrc
```

See [config-examples/README.md](config-examples/README.md) for detailed configuration guide.

### Documentation

#### [QUICK-START.md](QUICK-START.md)
Fast-track setup guide (10 minutes).
- Prerequisites checklist
- 3-step setup process
- Common commands reference
- Quick troubleshooting

#### [docs/guides/obsidian-zotero-setup-guide.md](../../docs/guides/obsidian-zotero-setup-guide.md)
Complete setup documentation (~500 lines).
- Step-by-step installation
- Plugin configuration
- Template customization
- First citation workflow
- Comprehensive troubleshooting

#### [docs/guides/obsidian-zotero-troubleshooting.md](../../docs/guides/obsidian-zotero-troubleshooting.md)
Dedicated troubleshooting guide.
- Installation issues
- Connection problems
- Template issues
- Citation problems
- Performance optimization
- Advanced debugging

#### [docs/guides/citation-source-verification-guide.md](../../docs/guides/citation-source-verification-guide.md)
Complete citation workflow guide.
- Integration with Zotero CLI
- Citation-source-verification skill
- End-to-end workflow examples
- Test cases

### Examples

#### `examples/README.md`
Example projects and workflows.
- Sample literature notes
- Sample synthesis notes
- Custom templates (books, conference papers)
- Complete workflow demonstrations
- Best practices

## File Structure

```
scripts/obsidian-setup/
├── README.md                          # This file
├── QUICK-START.md                     # Fast setup guide
├── setup-obsidian-vault.sh            # Automated setup script
├── tests/
│   └── verify-obsidian-setup.sh       # Verification script
├── templates/
│   └── Zotero-Literature-Note.md      # Literature note template
├── config-examples/
│   ├── README.md                      # Configuration guide
│   ├── zotero-integration-settings.json  # Plugin settings
│   └── env-template.sh                # Environment variables
└── examples/
    └── README.md                      # Example projects
```

## Prerequisites

### Required

1. **Obsidian** - Download from https://obsidian.md
2. **Zotero** - Download from https://www.zotero.org/download/
3. **Zotero API credentials:**
   - Get from: https://www.zotero.org/settings/keys
   - API Key (24 characters)
   - User ID (8 digits)

### Optional but Recommended

- **Better BibTeX** - Zotero plugin for consistent citation keys
  - Install from: https://retorque.re/zotero-better-bibtex/
- **Pandoc Reference List** - Obsidian plugin for bibliographies
  - Install from Obsidian Community plugins

## Common Workflows

### Workflow 1: New Research Project

```bash
# Create project directory
mkdir ~/Documents/MyResearch
cd ~/Documents/MyResearch

# Run setup
bash /path/to/scripts/obsidian-setup/setup-obsidian-vault.sh

# Open in Obsidian
# File → Open folder as vault

# Install Zotero Integration plugin
# Settings → Community plugins → Browse → "Zotero Integration"

# Configure plugin with credentials

# Import first paper
# Ctrl/Cmd + P → "Create literature note"
```

### Workflow 2: Import Existing Project

```bash
# Navigate to existing project
cd ~/Documents/ExistingProject

# Run setup (adds Obsidian + Zotero structure)
bash /path/to/scripts/obsidian-setup/setup-obsidian-vault.sh

# Verify setup
bash /path/to/scripts/obsidian-setup/tests/verify-obsidian-setup.sh

# Open in Obsidian and configure plugin
```

### Workflow 3: Test Before Real Use

```bash
# Create test vault
mkdir /tmp/test-vault
cd /tmp/test-vault

# Run setup
bash /path/to/scripts/obsidian-setup/setup-obsidian-vault.sh --non-interactive --vault-path .

# Open in Obsidian, test workflow

# Clean up when done
rm -rf /tmp/test-vault
```

## Integration with Citation-Source-Verification Skill

This setup integrates with the `citation-source-verification` skill for complete citation workflow:

1. **Search Zotero** - Using Zotero CLI or MCP server
2. **Add to Library** - Via Zotero CLI (DOI import, manual add)
3. **Verify Source** - Check metadata, attachments
4. **Create Note** - Zotero Integration plugin → literature note
5. **Cite in Writing** - Use `[@citekey]` format in synthesis notes
6. **Generate Bibliography** - Pandoc Reference List plugin

See [docs/guides/citation-source-verification-guide.md](../../docs/guides/citation-source-verification-guide.md) for complete workflow.

## Customization

### Custom Folder Structure

Edit `setup-obsidian-vault.sh` to change folder names:

```bash
FOLDERS=(
    "Literature"           # → "Papers"
    "Literature/attachments"  # → "Papers/PDFs"
    "Synthesis"            # → "Analysis"
    "Templates"
    "docs"
)
```

### Custom Template

1. Edit `templates/Zotero-Literature-Note.md`
2. Add/remove sections as needed
3. Adjust Handlebars variables
4. Rerun setup or copy manually to vault

See `examples/README.md` for custom template examples.

### Custom Configuration

1. Edit `config-examples/zotero-integration-settings.json`
2. Adjust paths, formats, citation styles
3. Use as reference when configuring plugin

## Troubleshooting

### Quick Fixes

**Plugin won't connect:**
```bash
# Verify credentials
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID

# Test API
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
```

**Template not populating:**
- Check path: Settings → Template File: `Templates/Zotero-Literature-Note.md`
- Verify file exists: `ls Templates/Zotero-Literature-Note.md`

**Setup script fails:**
```bash
# Check environment variables
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID

# Make script executable
chmod +x setup-obsidian-vault.sh

# Fix line endings (if needed)
sed -i '' 's/\r$//' setup-obsidian-vault.sh
```

**Verification script fails:**
```bash
# Run with verbose output
bash -x tests/verify-obsidian-setup.sh

# Check specific test
ls -la Literature/
cat Templates/Zotero-Literature-Note.md
```

See [docs/guides/obsidian-zotero-troubleshooting.md](../../docs/guides/obsidian-zotero-troubleshooting.md) for comprehensive troubleshooting.

## Testing

### Test Suite

```bash
# Run setup in test directory
./tests/test-setup.sh

# Verify all components
./tests/verify-obsidian-setup.sh

# Manual testing checklist
# [ ] Setup script completes without errors
# [ ] All folders created correctly
# [ ] Template file exists and is valid
# [ ] README generated correctly
# [ ] Git files created
# [ ] Configuration examples present
# [ ] Verification script passes all tests
```

### Automated Testing

The verification script includes:
- 7 test categories (structure, files, credentials, etc.)
- ~15+ individual checks
- Pass/fail reporting with colored output
- Detailed next steps on failure

**Example test run:**
```bash
$ ./tests/verify-obsidian-setup.sh

Testing vault at: /Users/username/Research

✓ Found: Literature/
✓ Found: Templates/Zotero-Literature-Note.md
✓ Template contains: {{title}}
✓ ZOTERO_API_KEY is set
✓ Zotero API connection successful

Total Tests: 15
Passed: 15
Failed: 0

✓ Vault structure is READY
✓ Zotero credentials are CONFIGURED
```

## Maintenance

### Updating Templates

```bash
# Edit template
nano templates/Zotero-Literature-Note.md

# Update existing vaults
cp templates/Zotero-Literature-Note.md ~/Documents/MyResearch/Templates/

# Or rerun setup (non-destructive)
cd ~/Documents/MyResearch
bash /path/to/scripts/obsidian-setup/setup-obsidian-vault.sh
```

### Updating Scripts

```bash
# Always fix line endings after editing
sed -i '' 's/\r$//' setup-obsidian-vault.sh
sed -i '' 's/\r$//' tests/verify-obsidian-setup.sh

# Make executable
chmod +x setup-obsidian-vault.sh
chmod +x tests/verify-obsidian-setup.sh

# Test changes
./tests/verify-obsidian-setup.sh /tmp/test-vault
```

## Related Tools

### Zotero CLI Scripts

Located in `scripts/zotero-cli/`:
- `zotero-search-items` - Search library
- `zotero-get-item` - Get item metadata
- `zotero-import-doi` - Add paper by DOI
- `zotero-create-collection` - Create collection
- And more...

See [scripts/zotero-cli/README.md](../zotero-cli/README.md)

### Citation Workflow Test

```bash
# Test complete citation workflow
bash scripts/zotero-cli/tests/test-citation-workflow.sh
```

## Resources

### Documentation

- [Obsidian Help](https://help.obsidian.md/)
- [Zotero Integration Plugin](https://github.com/mgmeyers/obsidian-zotero-integration)
- [Zotero Documentation](https://www.zotero.org/support/)
- [Zotero API Reference](https://www.zotero.org/support/dev/web_api/v3/start)
- [Handlebars Syntax](https://handlebarsjs.com/guide/)
- [Pandoc Citations](https://pandoc.org/MANUAL.html#citations)

### Community

- [Obsidian Forum](https://forum.obsidian.md/)
- [Obsidian Discord](https://discord.gg/obsidianmd)
- [Zotero Forums](https://forums.zotero.org/)
- [r/ObsidianMD](https://reddit.com/r/ObsidianMD)

### Plugins

- **Zotero Integration** - Core plugin for this workflow
- **Pandoc Reference List** - Bibliography generation
- **Better BibTeX** - Zotero citation key management
- **Citations** - Alternative plugin (requires manual .bib export)

## Contributing

### Reporting Issues

Found a bug or have a suggestion?

1. Check [troubleshooting guide](../../docs/guides/obsidian-zotero-troubleshooting.md)
2. Review [existing issues](../../issues)
3. Open new issue with:
   - Environment details (OS, Obsidian version, plugin version)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages or screenshots

### Improvements

Contributions welcome:

- Template enhancements
- Additional examples
- Documentation improvements
- Script optimizations
- Test coverage

## Version History

- **v1.0.0** (2025-11-13) - Initial release
  - Automated setup script
  - Verification tests
  - Complete documentation
  - Configuration examples
  - Example projects

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

**Created:** 2025-11-13
**Last Updated:** 2025-11-13
**Maintained by:** Claude Code Templates Repository
