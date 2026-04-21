# MacBook Development Environment Setup Guide

**For:** New team members setting up a development MacBook from scratch
**End state:** A fully configured machine with Python, Node.js, VS Code, Claude Code, Zotero, Obsidian, and all custom CLI tools ready for project work
**Estimated time:** ~90 minutes manual, ~45 minutes with the automation script
**Automation:** `scripts/intern-setup/setup-macbook.sh` automates ~75% of this guide
**Last tested:** 2026-04-15

---

## Table of Contents

- [MacBook Development Environment Setup Guide](#macbook-development-environment-setup-guide)
  - [Table of Contents](#table-of-contents)
  - [What You'll Have When Done](#what-youll-have-when-done)
  - [Prerequisites](#prerequisites)
  - [Phase 1: Foundation Tools](#phase-1-foundation-tools)
    - [1.1 Xcode Command Line Tools](#11-xcode-command-line-tools)
    - [1.2 Git Configuration](#12-git-configuration)
    - [1.3 Homebrew](#13-homebrew)
    - [1.4 Python via uv](#14-python-via-uv)
    - [1.5 Node.js](#15-nodejs)
    - [1.6 Environment Variables](#16-environment-variables)
  - [Phase 2: Development Tools](#phase-2-development-tools)
    - [2.1 Visual Studio Code](#21-visual-studio-code)
    - [2.2 Claude Desktop](#22-claude-desktop)
    - [2.3 Claude Code CLI](#23-claude-code-cli)
  - [Phase 3: Research \& Knowledge Tools](#phase-3-research--knowledge-tools)
    - [3.1 Zotero Desktop](#31-zotero-desktop)
    - [3.2 Obsidian](#32-obsidian)
    - [3.3 Pandoc](#33-pandoc)
  - [Phase 4: Clone Repo \& Install Custom Tools](#phase-4-clone-repo--install-custom-tools)
    - [4.1 Clone the Repository](#41-clone-the-repository)
    - [4.2 Install Zotero CLI](#42-install-zotero-cli)

    - [4.4 Set Up Obsidian Vault with Zotero Integration](#44-set-up-obsidian-vault-with-zotero-integration)
  - [Phase 5: Claude Code Customization](#phase-5-claude-code-customization)
    - [5.1 Set Up ~/.claude Directory](#51-set-up-claude-directory)
    - [5.2 Install CLAUDE.md](#52-install-claudemd)
    - [5.3 Install ZOTERO-CLI-REFERENCE.md](#53-install-zotero-cli-referencemd)
    - [5.4 Install Skills](#54-install-skills)
    - [5.5 Configure settings.json](#55-configure-settingsjson)
    - [5.6 Understanding Key Concepts](#56-understanding-key-concepts)
  - [Verification Checklist](#verification-checklist)
    - [Phase 1: Foundation](#phase-1-foundation)
    - [Phase 2: Development Tools](#phase-2-development-tools-1)
    - [Phase 3: Research Tools](#phase-3-research-tools)
    - [Phase 4: Custom Tools](#phase-4-custom-tools)
    - [Phase 5: Claude Code Customization](#phase-5-claude-code-customization-1)
  - [Troubleshooting](#troubleshooting)
    - [General Issues](#general-issues)
    - [Phase 1 Issues](#phase-1-issues)
    - [Phase 2 Issues](#phase-2-issues)
    - [Phase 3 Issues](#phase-3-issues)
    - [Phase 4 Issues](#phase-4-issues)
    - [Phase 5 Issues](#phase-5-issues)
  - [Quick Reference Card](#quick-reference-card)
  - [Appendix: .claude Customization Package (For Managers)](#appendix-claude-customization-package-for-managers)
    - [Files to Package](#files-to-package)
    - [Packaging Script](#packaging-script)
    - [Installation Instructions for the Intern](#installation-instructions-for-the-intern)

---

## What You'll Have When Done

After completing this guide, your MacBook will have:

- **Python 3.13** managed by the `uv` package manager (fast, modern Python tooling)
- **uv** for Python dependency management and virtual environments
- **Node.js** (v20+ or v22+) and npm for JavaScript tooling
- **Visual Studio Code** with Python and Jupyter extensions
- **Claude Desktop** for conversational AI access
- **Claude Code CLI** for AI-assisted development in the terminal
- **Zotero** with the Better BibTeX plugin for reference management
- **Obsidian** with 7 community plugins for knowledge management and citation workflows
- **Zotero CLI** (25 custom commands) for managing your Zotero library from the terminal

- **Claude Code customizations** including global instructions, skills, and settings

---

## Prerequisites

Before you start, make sure you have:

- **Claude Code subscription** -- You need a [Claude Pro plan](https://support.claude.com/en/articles/11049762-choosing-a-claude-plan). Claude Code authenticates via `claude login` using your browser. You do **NOT** need an Anthropic API key.
- **Zotero account + API key** -- Create a free account at [zotero.org](https://www.zotero.org/). Then go to [https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys) and create a new key with "Allow library access" and "Allow write access" enabled. Copy the 24-character API key. Your 8-digit User ID is shown on the same page.
- **GitHub account** -- If you don't have one, create it at [github.com](https://github.com/). Gil will add you to the organization permissions if you send him your user id.
- **Internet connection** -- Required throughout the entire setup.

> **Note:** An Anthropic API key is NOT required when you have a Claude subscription. The subscription handles authentication automatically.

---

## Phase 1: Foundation Tools

This phase installs the core tools that everything else depends on.

### 1.1 Xcode Command Line Tools

Apple's developer tools include git, compilers, and other essentials that Homebrew and many packages need.

```bash
xcode-select --install
```

A dialog box will appear -- click **Install** and wait for it to finish (5-10 minutes).

**Verify:**

```bash
git --version
```
Expected: `git version 2.x.x`

```bash
xcode-select -p
```
Expected: `/Library/Developer/CommandLineTools`

### 1.2 Git Configuration

Now that git is installed, set up your identity for commits and configure SSH access to GitHub.

```bash
git config --global user.name "Jack LastName"
git config --global user.email "jack@example.com"
```

Replace the name and email with your actual name and your work email address.

Generate an SSH key for GitHub authentication:

```bash
ssh-keygen -t ed25519 -C "jack@example.com"
```

Press Enter three times to accept defaults (default file location, no passphrase). Then display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`). Then:

1. Go to [github.com](https://github.com/) and sign in
2. Click your profile picture (top right) --> **Settings**
3. In the left sidebar, click **SSH and GPG keys**
4. Click **New SSH key**
5. Give it a title like "Work MacBook", paste the key, and click **Add SSH key**

**Verify:**

```bash
ssh -T git@github.com
```
Expected: `Hi username! You've successfully authenticated, but GitHub does not provide shell access.`

### 1.3 Homebrew

Homebrew is the standard macOS package manager. Almost everything else installs through it.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**IMPORTANT:** After the install finishes, Homebrew will print two lines that you need to run. They look like this (for Apple Silicon Macs):

```bash
echo >> ~/.zshrc
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Run those exact lines that Homebrew gives you. This adds Homebrew to your shell PATH so you can use the `brew` command.

**Verify:**

```bash
brew --version
```
Expected: `Homebrew 4.x.x`

### 1.4 Python via uv

`uv` is a fast, modern Python package manager that replaces pip, virtualenv, and pyenv. We use it for all Python projects.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reload your shell configuration:

```bash
source ~/.zshrc
```

Install Python 3.13:

```bash
uv python install 3.13
```

**Verify:**

```bash
uv --version
```
Expected: `uv 0.x.x`

```bash
uv run python --version
```
Expected: `Python 3.13.x`

### 1.5 Node.js

Node.js is needed for Claude Code CLI and other JavaScript tools.

```bash
brew install node
```

**Verify:**

```bash
node --version
```
Expected: `v20.x.x` or `v22.x.x`

```bash
npm --version
```
Expected: `10.x.x`

### 1.6 Environment Variables

Add your Zotero credentials and local bin path to your shell configuration. Open `~/.zshrc` in a text editor:

```bash
open -e ~/.zshrc
```

Add these lines at the bottom of the file:

```bash
# Zotero API credentials
export ZOTERO_API_KEY="your_24_character_api_key"
export ZOTERO_USER_ID="your_8_digit_user_id"

# Ensure local bin is in PATH (for custom CLI tools)
export PATH="$HOME/.local/bin:$PATH"
```

Replace `your_24_character_api_key` with your actual Zotero API key and `your_8_digit_user_id` with your actual Zotero User ID. Save and close the file.

Load the changes:

```bash
source ~/.zshrc
```

**Verify:**

```bash
echo $ZOTERO_API_KEY
```
Expected: your 24-character API key

```bash
echo $ZOTERO_USER_ID
```
Expected: your 8-digit user ID

```bash
echo $PATH | tr ':' '\n' | grep local
```
Expected: a line containing `/Users/yourname/.local/bin`

> **Phase 1 Complete.** You now have git, Homebrew, Python 3.13, Node.js, and your environment variables configured. Everything else builds on these foundations.

---

## Phase 2: Development Tools

This phase installs the applications you'll use for writing code and working with Claude.

### 2.1 Visual Studio Code

VS Code is the primary code editor. Install it with Homebrew:

```bash
brew install --cask visual-studio-code
```

Install the Python and Jupyter extensions:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

**Verify:**

```bash
code --version
```
Expected: version number, commit hash, and architecture on three lines

### 2.2 Claude Desktop

Claude Desktop gives you a native app for conversational AI. Install it with Homebrew:

```bash
brew install --cask claude
```

Alternatively, download it from [https://claude.ai/download](https://claude.ai/download).

After installing:

1. Launch Claude from your Applications folder
2. Sign in with your Anthropic account (the same one tied to your subscription)
3. Send a test message to confirm it works

**Verify:** The app launches and you can send and receive messages.

### 2.3 Claude Code CLI

Claude Code is a command-line AI assistant that can read your codebase, run commands, and edit files. Install it globally via npm:

```bash
npm install -g @anthropic-ai/claude-code
```

**Verify:**

```bash
claude --version
```
Expected: a version number like `1.x.x`

Authenticate with your subscription:

```bash
claude
```

A browser window will open -- follow the prompts to sign in with your Claude account. Once authenticated, you'll see the Claude Code prompt. Type `/help` to confirm it's working, then type `/exit` to quit.

> **Phase 2 Complete.** You now have VS Code, Claude Desktop, and Claude Code CLI installed and authenticated. These are your primary development tools.

---

## Phase 3: Research & Knowledge Tools

This phase installs Zotero for reference management and Obsidian for knowledge management.

### 3.1 Zotero Desktop

Zotero manages your research library -- papers, books, web pages, and their citations.

```bash
brew install --cask zotero
```

After installing:

1. Launch Zotero from your Applications folder
2. Sign in with your Zotero account (Edit --> Settings --> Sync)

**Install the Better BibTeX plugin:**

Better BibTeX adds citation key support, which our tools depend on for linking Zotero to Obsidian.

1. Download the latest `.xpi` file from [https://retorque.re/zotero-better-bibtex/installation/](https://retorque.re/zotero-better-bibtex/installation/)
2. In Zotero: **Tools** --> **Add-ons** --> click the gear icon --> **Install Add-on From File**
3. Select the `.xpi` file you downloaded
4. Restart Zotero when prompted

**Verify:** Open Zotero Preferences (Zotero --> Settings). A **Better BibTeX** tab should appear in the preferences window.

### 3.2 Obsidian

Obsidian is a markdown-based knowledge management tool. We use it for project notes, literature reviews, and research documentation.

```bash
brew install --cask obsidian
```

**Verify:** Launch Obsidian from your Applications folder. It should open successfully. Don't create a vault yet -- that happens in Phase 4.

### 3.3 Pandoc

Pandoc converts documents between formats and handles citation rendering in Obsidian.

```bash
brew install pandoc
```

**Verify:**

```bash
pandoc --version
```
Expected: `pandoc 3.x.x`

> **Phase 3 Complete.** You now have Zotero with Better BibTeX, Obsidian, and Pandoc installed. These form your research and knowledge management stack.

---

## Phase 4: Clone Repo & Install Custom Tools

This phase gets our custom tools installed from the team repository.

### 4.1 Clone the Repository

Create the Projects directory and clone the templates repository:

```bash
mkdir -p ~/Documents/Projects
git clone https://github.com/gwlund/k2-vision-tools.git ~/Documents/Projects/k2-vision-tools
cd ~/Documents/Projects/k2-vision-tools
```

**Verify:**

```bash
ls ~/Documents/Projects/k2-vision-tools/scripts/
```
Expected: directories including `zotero-cli/` and `obsidian-setup/`

### 4.2 Install Zotero CLI

The Zotero CLI provides 25 custom Python commands for managing your Zotero library from the terminal. This lets Claude Code search, import, and organize your references programmatically.

```bash
cd ~/Documents/Projects/k2-vision-tools/scripts/zotero-cli
bash install.sh
```

**Verify:**

```bash
zotero-verify-api
```
Expected: output showing your library stats (number of items, collections, etc.)

**Complete Command Reference:**

| Command | Description |
|---------|-------------|
| `zotero-verify-api` | Test API credentials and show library stats |
| `zotero-import-doi` | Add paper from DOI (recommended method) |
| `zotero-search-items` | Search by title/author/keywords |
| `zotero-get-item` | View item details |
| `zotero-get-citekey` | Get Better BibTeX citation key |
| `zotero-find-by-doi` | Find paper by DOI |
| `zotero-list-collections` | Show all collections |
| `zotero-get-collection-items` | View collection contents |
| `zotero-list-tags` | Browse all tags |
| `zotero-export-annotations` | Export paper annotations |
| `zotero-search-annotations` | Search PDF highlights |
| `zotero-add-item` | Manual item entry |
| `zotero-add-tags` | Tag items |
| `zotero-add-pdf` | Attach PDF to item |
| `zotero-update-item` | Update metadata |
| `zotero-create-parent` | Create parent for standalone PDFs |
| `zotero-create-collection` | Create collection |
| `zotero-rename-collection` | Rename collection |
| `zotero-move-collection` | Move/nest collection |
| `zotero-delete-collection` | Delete collection |
| `zotero-delete-item` | Delete item |
| `zotero-find-duplicates` | Find DOI-based duplicates |
| `zotero-merge-duplicates` | Interactive merge |
| `zotero-analyze-pdf` | Extract text from PDF |
| `zotero-create-note-from-annotations` | Generate note from highlights |

### 4.3 Set Up Obsidian Vault with Zotero Integration

This creates a structured Obsidian vault with templates and folder organization for research projects.

**Step 1: Run the automated setup script**

For your first project vault:

```bash
cd ~/Documents/Projects/your-project-name
bash ~/Documents/Projects/k2-vision-tools/scripts/obsidian-setup/setup-obsidian-vault.sh
```

Replace `your-project-name` with the actual project directory your manager gives you.

**Step 2: Open the vault in Obsidian**

1. Launch Obsidian
2. Click **Open folder as vault** (or File --> Open folder as vault)
3. Navigate to your project directory and select it
4. When prompted "Trust author and enable plugins?", click **Trust**

**Step 3: Enable community plugins**

This is a security step that cannot be automated -- Obsidian requires manual approval.

1. Click the gear icon (bottom left) to open **Settings**
2. Go to **Community plugins** in the left sidebar
3. Click **Turn on community plugins**

**Step 4: Install these 7 plugins**

Go to Settings --> Community plugins --> **Browse** and install each of these:

| Plugin | Search Term | Version | Purpose |
|--------|------------|---------|---------|
| Vault Nickname | vault nickname | v1.1.11 | Custom vault display name |
| Zotero Integration | zotero | v3.2.1 | Import Zotero items as notes |
| Pandoc Reference List | pandoc reference | v2.0.25 | Live citation rendering |
| Citations | citations | v0.4.5 | BibTeX citekey insertion |
| Dataview | dataview | v0.5.x | Dynamic YAML queries |
| Templater | templater | v2.16.2 | Advanced templates |
| Pandoc Plugin | pandoc | v0.4.1 | Export to DOCX/PDF |

Versions are current as of April 2026 -- accept updates if prompted.

For each plugin: search for it, click **Install**, then click **Enable**.

**Step 5: Configure Zotero Integration**

Go to Settings --> **Zotero Integration** and set these values:

| Setting | Value |
|---------|-------|
| Database Type | Web Library |
| User ID | Your 8-digit Zotero user ID |
| API Key | Your 24-character API key |
| Literature Note Folder | `Literature/` |
| Template File | `Templates/Zotero-Literature-Note.md` |
| Image Folder | `Literature/attachments/` |
| Import Attachments | Enabled |
| Citation Format | Pandoc (`[@citekey]`) |

**Step 6: Test the integration**

1. Press `Cmd + P` to open the Command Palette
2. Type: `Zotero Integration: Create literature note`
3. Search for a paper in your Zotero library
4. Select it -- a new note should appear, auto-populated with metadata from Zotero

> **Phase 4 Complete.** You now have the team repository cloned with Zotero CLI installed and an Obsidian vault with full Zotero integration.

---

## Phase 5: Claude Code Customization

This phase configures Claude Code with team-standard instructions, skills, and settings.

### 5.1 Set Up ~/.claude Directory

Create the directory structure Claude Code uses for configuration:

```bash
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/plans
```

### 5.2 Install CLAUDE.md

Your manager will provide you with a customized `CLAUDE.md` file. This contains global instructions that Claude Code follows in every session -- coding standards, file naming conventions, git commit style, and tool references.

Place it at:

```bash
cp /path/to/provided/CLAUDE.md ~/.claude/CLAUDE.md
```

Replace `/path/to/provided/CLAUDE.md` with the actual path to the file your manager gives you. (See the [Appendix](#appendix-claude-customization-package-for-managers) for how the package is created.)

### 5.3 Install ZOTERO-CLI-REFERENCE.md

This quick reference for all 25 Zotero CLI commands is available to Claude in every session.

```bash
cp /path/to/provided/ZOTERO-CLI-REFERENCE.md ~/.claude/ZOTERO-CLI-REFERENCE.md
```

### 5.4 Install Skills

Skills are specialized instruction sets that give Claude Code domain-specific capabilities. Your manager will provide a skills package.

```bash
cp -r /path/to/provided/skills/* ~/.claude/skills/
```

Skills included:

| Skill | Purpose |
|-------|---------|
| `learning-loop` | Save and recall learnings across sessions |
| `lla` | Shortcut: query prior learnings before starting work |
| `llr` | Shortcut: save learnings after completing work |
| `jupyter-notebook-safety` | Prevent Jupyter notebook corruption during edits |
| `obsidian-setup` | Automated Obsidian vault provisioning |
| `obsidian-vault-keeper` | Maintain LLM-managed knowledge vaults |
| `citation-source-verification` | Citation management and source verification |

**Verify:** Start Claude Code and type `/skills` -- you should see all installed skills listed.

### 5.5 Configure settings.json

Create the global settings file with recommended starter permissions:

```bash
cat > ~/.claude/settings.json << 'EOF'
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
EOF
```

This allows Claude Code to:
- Run shell commands without prompting for each one
- Read and write learning-loop files automatically

Other operations will ask for your permission -- approve or deny as you see fit.

### 5.6 Understanding Key Concepts

Before you start using Claude Code daily, here are the key concepts:

**CLAUDE.md** -- This is your global instructions file, stored at `~/.claude/CLAUDE.md`. Claude Code reads it at the start of every session. It contains coding standards, naming conventions, and tool references that apply across all projects. Projects can also have their own `CLAUDE.md` that overrides or extends the global one.

**Skills** -- Skills are specialized workflows you invoke with `/skill-name` in Claude Code. For example, `/lla` surfaces prior learnings before you start work, and `/llr` captures what you learned when you're done. Skills give Claude domain expertise for specific tasks like citation management or notebook editing.

**Learning Loop** -- Start each session with `/lla` (advise) to see what worked and failed in previous sessions. End each session with `/llr` (retrospective) to save what you learned. Over time, this builds a searchable knowledge base that makes Claude more effective on your projects.

**settings.json vs settings.local.json** -- `settings.json` contains your intentional global configuration (permissions, environment variables). `settings.local.json` is auto-generated as you approve or deny permission prompts during sessions. Both live in `~/.claude/`. You edit `settings.json`; leave `settings.local.json` alone.

**mcp.json** -- This configures MCP (Model Context Protocol) server connections, which give Claude Code access to external services. This is an advanced feature -- your manager will help you set this up later as specific projects require it.

> **Phase 5 Complete.** Claude Code is now configured with team standards, skills, and permissions. You're ready to start working on projects.

---

## Verification Checklist

Run through this checklist to confirm everything is working. Check off each item as you verify it.

### Phase 1: Foundation

- [ ] `git --version` returns a version
- [ ] `git config user.name` returns your name
- [ ] `ssh -T git@github.com` shows "successfully authenticated"
- [ ] `brew --version` returns a version
- [ ] `uv --version` returns a version
- [ ] `uv run python --version` returns 3.13.x
- [ ] `node --version` returns v20+ or v22+
- [ ] `npm --version` returns a version
- [ ] `echo $ZOTERO_API_KEY` returns your key
- [ ] `echo $ZOTERO_USER_ID` returns your ID

### Phase 2: Development Tools

- [ ] `code --version` returns a version
- [ ] Claude Desktop launches and responds to messages
- [ ] `claude --version` returns a version
- [ ] `claude` authenticates successfully (browser flow works)

### Phase 3: Research Tools

- [ ] Zotero launches
- [ ] Better BibTeX tab visible in Zotero Preferences
- [ ] Obsidian launches
- [ ] `pandoc --version` returns a version

### Phase 4: Custom Tools

- [ ] `ls ~/Documents/Projects/k2-vision-tools/` shows repo contents
- [ ] `zotero-verify-api` shows library stats

- [ ] Obsidian vault opens with correct folder structure
- [ ] Community plugins enabled in Obsidian
- [ ] All 7 plugins installed and enabled
- [ ] Can create a literature note from Zotero in Obsidian

### Phase 5: Claude Code Customization

- [ ] `ls ~/.claude/CLAUDE.md` shows the file exists
- [ ] `ls ~/.claude/ZOTERO-CLI-REFERENCE.md` shows the file exists
- [ ] `claude` then `/skills` shows installed skills
- [ ] `ls ~/.claude/settings.json` shows the file exists

---

## Troubleshooting

### General Issues

**"command not found" after installing something**
You likely forgot to reload your shell configuration. Run:
```bash
source ~/.zshrc
```
Or close and reopen your Terminal app entirely.

**Apple Silicon path issues**
On Apple Silicon Macs (M1/M2/M3/M4), Homebrew installs to `/opt/homebrew/` not `/usr/local/`. If a tool isn't found, check that `/opt/homebrew/bin` is in your PATH:
```bash
echo $PATH | tr ':' '\n' | grep homebrew
```

### Phase 1 Issues

**Xcode CLT install hangs or fails**
Open System Settings --> General --> Software Update and check for pending updates. Install any available updates, then retry `xcode-select --install`.

**Homebrew post-install steps missed**
If `brew` isn't found after installing Homebrew, run:
```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
```

### Phase 2 Issues

**`code` command not found after installing VS Code**
Open VS Code, press `Cmd+Shift+P`, type "Shell Command", and select **Shell Command: Install 'code' command in PATH**.

**Claude Code authentication fails**
Make sure you have an active Claude subscription (Max plan or team seat). If auth gets stuck, try:
```bash
claude logout
claude login
```

### Phase 3 Issues

**Better BibTeX .xpi won't install**
Make sure you downloaded the actual `.xpi` file, not the GitHub release page HTML. The file should be named something like `zotero-better-bibtex-6.x.x.xpi`.

**Zotero won't connect or sync**
Check that your API key has the right permissions. Go to [https://www.zotero.org/settings/keys](https://www.zotero.org/settings/keys) and verify your key has "Allow library access" and "Allow write access" checked.

### Phase 4 Issues

**`git clone` fails with "Permission denied (publickey)"**
Your SSH key isn't set up correctly with GitHub. Double-check that you added the key (from Phase 1.2) to your GitHub account. Alternatively, use the HTTPS URL:
```bash
git clone https://github.com/gwlund/k2-vision-tools.git ~/Documents/Projects/k2-vision-tools
```

**`zotero-verify-api` fails or shows errors**
Check that your environment variables are set:
```bash
echo $ZOTERO_API_KEY
echo $ZOTERO_USER_ID
```
If they're empty, revisit Phase 1.6 and make sure you edited `~/.zshrc` and ran `source ~/.zshrc`.

**Obsidian "Trust author" prompt not appearing**
Close Obsidian completely and reopen it. Then open the vault again. The trust prompt appears the first time you open a vault that contains plugin configurations.

**Zotero Integration in Obsidian shows "No items found"**
Your Zotero library may be empty. Add a test item to Zotero first (try importing a paper by DOI in the Zotero desktop app: File --> Add by Identifier --> paste a DOI like `10.1038/d41586-023-00340-6`).

### Phase 5 Issues

**Skills not showing in `/skills`**
Check that the skill files are in the exact expected path. Each skill needs a `SKILL.md` file at:
```
~/.claude/skills/SKILLNAME/SKILL.md
```
Verify the structure:
```bash
ls ~/.claude/skills/*/SKILL.md
```

**Settings not taking effect**
Close your Claude Code session and start a new one. Settings are loaded at session start.

---

## Quick Reference Card

Bookmark this section for daily use.

| Tool | Command | What It Does |
|------|---------|-------------|
| uv | `uv run python script.py` | Run Python script |
| uv | `uv add package` | Add dependency to project |
| uv | `uv sync` | Install all project dependencies |
| Git | `git status` | Show changed files |
| Git | `git add -A && git commit -m "msg"` | Stage and commit |
| Git | `git push` | Push to remote |
| Claude Code | `claude` | Start interactive session |
| Claude Code | `/skills` | List available skills |
| Claude Code | `/lla` | Query prior learnings |
| Claude Code | `/llr` | Save session learnings |
| Claude Code | `/help` | Get help |
| Zotero CLI | `zotero-import-doi 10.xxx` | Import paper by DOI |
| Zotero CLI | `zotero-search-items "term"` | Search library |
| Zotero CLI | `zotero-verify-api` | Test API connection |
| Obsidian | `Cmd+P` | Command palette |
| Obsidian | `[@citekey` | Insert citation |
| VS Code | `Cmd+Shift+P` | Command palette |
| VS Code | `Cmd+J` | Toggle terminal |

---

## Appendix: .claude Customization Package (For Managers)

This section is for the manager preparing Jack's customization files. It documents what to package and how to adapt each file.

### Files to Package

| Item | Source | Adaptation Needed |
|------|--------|-------------------|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Strip personal "About Me" section (name, location, focus areas). Keep: communication style, quality standards, file naming, markdown standards, git conventions, Jupyter safety rules, Zotero CLI section, learning loop section. Replace "About Me" with intern's info. |
| `ZOTERO-CLI-REFERENCE.md` | `~/.claude/ZOTERO-CLI-REFERENCE.md` | Copy as-is (already generic) |
| Skill: `learning-loop/` | `~/.claude/skills/learning-loop/` | Copy directory structure but exclude `learnings/` content (those are personal session learnings). Include empty `learnings/` directory. |
| Skill: `lla/` | `~/.claude/skills/lla/` | Copy as-is (learning-loop shortcut) |
| Skill: `llr/` | `~/.claude/skills/llr/` | Copy as-is (learning-loop shortcut) |
| Skill: `jupyter-notebook-safety/` | `~/.claude/skills/jupyter-notebook-safety/` | Copy as-is |
| Skill: `obsidian-setup/` | `~/.claude/skills/obsidian-setup/` | Copy as-is |
| Skill: `obsidian-vault-keeper/` | `~/.claude/skills/obsidian-vault-keeper/` | Copy as-is |
| Skill: `citation-source-verification/` | `~/.claude/skills/citation-source-verification/` | Copy as-is |

**Why these 6 skills + 2 shortcuts?** The remaining skills are domain-specific (reaper, facebook-capture, marp, etc.), framework-level (superpowers plugin), or advanced workflows the intern doesn't need yet. These cover the core workflow: safe notebook editing, Obsidian vault management, citation workflow, and session learning.

**Excluded from package:**
- `settings.local.json` -- Auto-generated by Claude Code as the user approves/denies permissions. Do not pre-create.
- `mcp.json` -- MCP server connections are advanced. Set up later per-project as needed.
- `plugins/` -- Claude Code plugins (superpowers, context7, etc.) are installed via Claude Code commands, not file copy.

### Packaging Script

Run this from the manager's machine to create a distributable archive:

```bash
#!/bin/bash
# package-for-intern.sh
# Creates a tar.gz of .claude customizations for a new team member

set -e
PACKAGE_DIR=$(mktemp -d)/claude-starter-kit
mkdir -p "$PACKAGE_DIR/skills"

# Copy CLAUDE.md (manager should edit "About Me" section before distributing)
cp ~/.claude/CLAUDE.md "$PACKAGE_DIR/CLAUDE.md"

# Copy Zotero CLI reference (no changes needed)
cp ~/.claude/ZOTERO-CLI-REFERENCE.md "$PACKAGE_DIR/ZOTERO-CLI-REFERENCE.md"

# Copy skills
for skill in learning-loop lla llr jupyter-notebook-safety obsidian-setup obsidian-vault-keeper citation-source-verification; do
    if [ -d ~/.claude/skills/$skill ]; then
        cp -r ~/.claude/skills/$skill "$PACKAGE_DIR/skills/$skill"
    fi
done

# Remove personal learnings from learning-loop (keep directory structure)
rm -rf "$PACKAGE_DIR/skills/learning-loop/learnings/"*/*
mkdir -p "$PACKAGE_DIR/skills/learning-loop/learnings"

# Create the archive
tar -czf ~/Desktop/claude-starter-kit.tar.gz -C "$(dirname "$PACKAGE_DIR")" claude-starter-kit

echo "Package created at ~/Desktop/claude-starter-kit.tar.gz"
echo ""
echo "IMPORTANT: Edit CLAUDE.md in the archive to update the 'About Me' section"
echo "before sending to the intern."
```

### Installation Instructions for the Intern

After receiving `claude-starter-kit.tar.gz`:

```bash
# Extract the package
cd ~/Downloads
tar -xzf claude-starter-kit.tar.gz

# Install files
cp claude-starter-kit/CLAUDE.md ~/.claude/CLAUDE.md
cp claude-starter-kit/ZOTERO-CLI-REFERENCE.md ~/.claude/ZOTERO-CLI-REFERENCE.md
cp -r claude-starter-kit/skills/* ~/.claude/skills/

# Verify
ls ~/.claude/CLAUDE.md ~/.claude/ZOTERO-CLI-REFERENCE.md
ls ~/.claude/skills/*/SKILL.md
```

---

Last Updated: 2026-04-15
