#!/bin/bash
# Obsidian + Zotero Integration Setup Verification Script
# Tests that the vault is properly configured and ready for use

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
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

# Function to run a test
run_test() {
    ((TESTS_RUN++))
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: $test_name... "
    if eval "$test_command" &> /dev/null; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Get vault path (current directory or specified)
VAULT_PATH="${1:-.}"
cd "$VAULT_PATH"
VAULT_PATH="$(pwd)"

print_header "Obsidian Vault Setup Verification"
print_info "Testing vault at: $VAULT_PATH"
echo

# Test 1: Check folder structure
print_header "Test 1: Folder Structure"

REQUIRED_FOLDERS=(
    "Literature"
    "Literature/attachments"
    "Synthesis"
    "Templates"
    "docs"
)

FOLDER_CHECK_PASS=true
for folder in "${REQUIRED_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        print_success "Found: $folder/"
    else
        print_error "Missing: $folder/"
        FOLDER_CHECK_PASS=false
    fi
done

# Test 2: Check required files
print_header "Test 2: Required Files"

FILE_CHECK_PASS=true

# Check template
if [ -f "Templates/Zotero-Literature-Note.md" ]; then
    print_success "Found: Templates/Zotero-Literature-Note.md"

    # Validate template has required Handlebars variables
    REQUIRED_VARS=("{{title}}" "{{authors}}" "{{itemKey}}" "{{citekey}}")
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "$var" "Templates/Zotero-Literature-Note.md"; then
            print_success "  Template contains: $var"
        else
            print_error "  Template missing: $var"
            FILE_CHECK_PASS=false
        fi
    done
else
    print_error "Missing: Templates/Zotero-Literature-Note.md"
    FILE_CHECK_PASS=false
fi

# Check README
if [ -f "README.md" ]; then
    print_success "Found: README.md"
else
    print_warning "Missing: README.md (optional but recommended)"
fi

# Check .gitignore
if [ -f ".gitignore" ]; then
    print_success "Found: .gitignore"
else
    print_warning "Missing: .gitignore (optional but recommended)"
fi

# Test 3: Check environment variables
print_header "Test 3: Zotero Credentials"

ENV_CHECK_PASS=true

if [ -n "$ZOTERO_API_KEY" ]; then
    print_success "ZOTERO_API_KEY is set"

    # Validate format (should be 24 alphanumeric characters)
    if [[ $ZOTERO_API_KEY =~ ^[A-Za-z0-9]{24}$ ]]; then
        print_success "  API key format is valid"
    else
        print_warning "  API key format may be incorrect (expected 24 characters)"
    fi
else
    print_error "ZOTERO_API_KEY not set"
    print_info "  Set with: export ZOTERO_API_KEY='your_key_here'"
    ENV_CHECK_PASS=false
fi

if [ -n "$ZOTERO_USER_ID" ]; then
    print_success "ZOTERO_USER_ID is set"

    # Validate format (should be numeric)
    if [[ $ZOTERO_USER_ID =~ ^[0-9]+$ ]]; then
        print_success "  User ID format is valid"
    else
        print_warning "  User ID format may be incorrect (expected numeric)"
    fi
else
    print_error "ZOTERO_USER_ID not set"
    print_info "  Set with: export ZOTERO_USER_ID='your_id_here'"
    ENV_CHECK_PASS=false
fi

# Test 4: Test Zotero API connection (if credentials available)
if [ "$ENV_CHECK_PASS" = true ]; then
    print_header "Test 4: Zotero API Connection"

    print_info "Testing connection to Zotero API..."

    # Try to fetch one item
    API_RESPONSE=$(curl -s -w "\n%{http_code}" \
        -H "Zotero-API-Key: $ZOTERO_API_KEY" \
        "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1" 2>&1)

    HTTP_CODE=$(echo "$API_RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "200" ]; then
        print_success "Zotero API connection successful"

        # Count items in library
        TOTAL_ITEMS=$(curl -s -I \
            -H "Zotero-API-Key: $ZOTERO_API_KEY" \
            "https://api.zotero.org/users/$ZOTERO_USER_ID/items" | \
            grep -i "Total-Results:" | awk '{print $2}' | tr -d '\r')

        if [ -n "$TOTAL_ITEMS" ]; then
            print_info "  Library contains $TOTAL_ITEMS items"
        fi
    else
        print_error "Zotero API connection failed (HTTP $HTTP_CODE)"
        print_info "  Verify your API key and User ID are correct"
    fi
else
    print_warning "Skipping API test - credentials not configured"
fi

# Test 5: Check Obsidian-specific files (optional)
print_header "Test 5: Obsidian Configuration (Optional)"

if [ -d ".obsidian" ]; then
    print_info "Found .obsidian/ directory"

    # Check for plugins
    if [ -d ".obsidian/plugins" ]; then
        print_info "  Plugins directory exists"

        # Check for Zotero Integration plugin
        if [ -d ".obsidian/plugins/obsidian-zotero-desktop-connector" ] || \
           [ -d ".obsidian/plugins/obsidian-zotero-integration" ]; then
            print_success "  Zotero Integration plugin detected"
        else
            print_warning "  Zotero Integration plugin not installed yet"
        fi
    fi

    # Check for community plugins enabled
    if [ -f ".obsidian/community-plugins.json" ]; then
        print_info "  Community plugins configuration exists"
    fi
else
    print_info "No .obsidian/ directory (will be created when opened in Obsidian)"
fi

# Test 6: Validate template syntax
print_header "Test 6: Template Validation"

if [ -f "Templates/Zotero-Literature-Note.md" ]; then
    TEMPLATE_VALID=true

    # Check for YAML frontmatter
    if grep -q "^---$" "Templates/Zotero-Literature-Note.md"; then
        print_success "Template has YAML frontmatter"
    else
        print_warning "Template missing YAML frontmatter"
        TEMPLATE_VALID=false
    fi

    # Check for common Handlebars patterns
    HANDLEBARS_COUNT=$(grep -c "{{" "Templates/Zotero-Literature-Note.md" || echo "0")
    if [ "$HANDLEBARS_COUNT" -gt 5 ]; then
        print_success "Template contains $HANDLEBARS_COUNT Handlebars variables"
    else
        print_warning "Template has few ($HANDLEBARS_COUNT) Handlebars variables"
    fi

    # Check for citation format
    if grep -q "{{citekey}}" "Templates/Zotero-Literature-Note.md"; then
        print_success "Template includes citation key field"
    else
        print_warning "Template missing citation key field"
    fi
fi

# Test 7: Check file permissions
print_header "Test 7: File Permissions"

PERMISSION_CHECK_PASS=true

# Check if we can write to Literature directory
if [ -w "Literature" ]; then
    print_success "Literature/ is writable"
else
    print_error "Literature/ is not writable"
    PERMISSION_CHECK_PASS=false
fi

# Check if we can write to Synthesis directory
if [ -w "Synthesis" ]; then
    print_success "Synthesis/ is writable"
else
    print_error "Synthesis/ is not writable"
    PERMISSION_CHECK_PASS=false
fi

# Summary
print_header "Verification Summary"

echo "Total Tests: $TESTS_RUN"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo

# Overall status
if [ "$FOLDER_CHECK_PASS" = true ] && [ "$FILE_CHECK_PASS" = true ] && [ "$PERMISSION_CHECK_PASS" = true ]; then
    echo -e "${GREEN}✓ Vault structure is READY${NC}"
else
    echo -e "${YELLOW}⚠ Vault structure has issues${NC}"
fi

if [ "$ENV_CHECK_PASS" = true ]; then
    echo -e "${GREEN}✓ Zotero credentials are CONFIGURED${NC}"
else
    echo -e "${YELLOW}⚠ Zotero credentials need configuration${NC}"
fi

echo
print_header "Next Steps"

if [ "$ENV_CHECK_PASS" = false ]; then
    echo "1. Set Zotero credentials:"
    echo "   export ZOTERO_API_KEY='your_key_here'"
    echo "   export ZOTERO_USER_ID='your_id_here'"
    echo
fi

echo "2. Open vault in Obsidian:"
echo "   File → Open folder as vault → Select: $VAULT_PATH"
echo

echo "3. Install Zotero Integration plugin:"
echo "   Settings → Community plugins → Browse → 'Zotero Integration'"
echo

echo "4. Configure plugin:"
echo "   Settings → Zotero Integration"
echo "   - Database Type: Web Library"
echo "   - User ID: $ZOTERO_USER_ID"
echo "   - API Key: ${ZOTERO_API_KEY:0:8}..."
echo "   - Literature Note Folder: Literature/"
echo "   - Template File: Templates/Zotero-Literature-Note.md"
echo

echo "5. Test the integration:"
echo "   Ctrl/Cmd + P → 'Zotero Integration: Create literature note'"
echo

print_header "Verification Complete"

# Exit with appropriate code
if [ "$FOLDER_CHECK_PASS" = true ] && [ "$FILE_CHECK_PASS" = true ]; then
    exit 0
else
    exit 1
fi
