#!/bin/bash

# Bin Collection Date Updater
# This script helps update bin collection dates by adding days to existing dates
# Usage: ./scripts/update-bin-dates.sh [days]
# Example: ./scripts/update-bin-dates.sh 7  (advances all dates by 7 days)

set -e

DAYS=${1:-7}
CONTENT_DIR="content/bin-collection"

echo "🗑️  Bin Collection Date Updater"
echo "================================"
echo ""
echo "This will advance all bin collection dates by $DAYS days."
echo "Current bin collection files:"
echo ""

# List current files and their next collection dates
for file in "$CONTENT_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        current_date=$(grep "^nextCollection:" "$file" | sed 's/nextCollection: "\(.*\)"/\1/' | tr -d '"')
        zone=$(grep "^zone:" "$file" | sed 's/zone: "\(.*\)"/\1/' | tr -d '"')
        waste=$(grep "^wasteType:" "$file" | sed 's/wasteType: "\(.*\)"/\1/' | tr -d '"')

        if [ -n "$current_date" ]; then
            echo "  📅 $zone - $waste: $current_date"
        fi
    fi
done

echo ""
read -p "Continue with update? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Update cancelled"
    exit 0
fi

echo ""
echo "Updating dates..."
echo ""

# Update each file
for file in "$CONTENT_DIR"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")

        # Extract current date
        current_date=$(grep "^nextCollection:" "$file" | sed 's/nextCollection: "\(.*\)"/\1/' | tr -d '"' | xargs)

        if [ -n "$current_date" ]; then
            # Calculate new date (works on Linux with GNU date)
            if date --version >/dev/null 2>&1; then
                # GNU date (Linux)
                new_date=$(date -d "$current_date + $DAYS days" "+%Y-%m-%dT%H:%M:%S%:z")
            else
                # BSD date (macOS)
                new_date=$(date -j -v+${DAYS}d -f "%Y-%m-%dT%H:%M:%S%z" "$current_date" "+%Y-%m-%dT%H:%M:%S%z" 2>/dev/null || echo "ERROR")
            fi

            if [ "$new_date" != "ERROR" ]; then
                # Update the file
                sed -i.bak "s|nextCollection: .*|nextCollection: \"$new_date\"|g" "$file"
                rm -f "$file.bak"

                zone=$(grep "^zone:" "$file" | sed 's/zone: "\(.*\)"/\1/' | tr -d '"')
                waste=$(grep "^wasteType:" "$file" | sed 's/wasteType: "\(.*\)"/\1/' | tr -d '"')

                echo "  ✅ Updated $zone - $waste: $current_date → $new_date"
            else
                echo "  ⚠️  Could not parse date for $filename"
            fi
        fi
    fi
done

echo ""
echo "✨ Update complete!"
echo ""
echo "Next steps:"
echo "1. Review the changes: git diff content/bin-collection/"
echo "2. Test the site: hugo server"
echo "3. Commit: git add content/bin-collection/ && git commit -m 'Update bin collection dates'"
echo "4. Push: git push origin main"
echo ""
