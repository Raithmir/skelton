#!/bin/bash
# Check for files owned by root in the site directory
# These files will cause webhook deployments to fail

echo "Checking for root-owned files in /var/www/community-site..."
echo ""

ROOT_FILES=$(find /var/www/community-site -user root 2>/dev/null | grep -v ".git/objects/pack")

if [ -z "$ROOT_FILES" ]; then
    echo "✓ No root-owned files found. Permissions are correct."
    exit 0
else
    echo "⚠ WARNING: Found root-owned files that will cause deployment failures:"
    echo ""
    echo "$ROOT_FILES" | head -20
    echo ""
    echo "To fix, run:"
    echo "  sudo chown -R www-data:www-data /var/www/community-site"
    exit 1
fi
