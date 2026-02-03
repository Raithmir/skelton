#!/usr/bin/env python3
"""
Bin Collection Date Updater
Advances bin collection dates for all zones

Usage:
    python3 scripts/update-bin-dates.py              # Advance by 7 days (default)
    python3 scripts/update-bin-dates.py --days 14    # Advance by 14 days
    python3 scripts/update-bin-dates.py --list       # Just list current dates
"""

import os
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ANSI color codes for pretty output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def parse_frontmatter_date(date_str):
    """Parse ISO 8601 date from frontmatter"""
    # Remove quotes and whitespace
    date_str = date_str.strip(' "\'')

    # Try multiple formats
    formats = [
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%d',
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Could not parse date: {date_str}")

def format_date(dt):
    """Format date for frontmatter"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')

def get_bin_collections(content_dir):
    """Get all bin collection files and their current dates"""
    collections = []

    for file_path in Path(content_dir).glob('*.md'):
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract fields
        zone_match = re.search(r'^zone:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        waste_match = re.search(r'^wasteType:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        date_match = re.search(r'^nextCollection:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)

        if zone_match and waste_match and date_match:
            try:
                current_date = parse_frontmatter_date(date_match.group(1))
                collections.append({
                    'file': file_path,
                    'zone': zone_match.group(1),
                    'waste': waste_match.group(1),
                    'date': current_date,
                    'content': content
                })
            except ValueError as e:
                print(f"{YELLOW}⚠️  Warning: Could not parse date in {file_path.name}: {e}{RESET}")

    return sorted(collections, key=lambda x: (x['zone'], x['waste']))

def update_collection_dates(collections, days):
    """Update collection dates by adding specified days"""
    updated = []

    for collection in collections:
        new_date = collection['date'] + timedelta(days=days)

        # Update the content
        old_date_str = format_date(collection['date'])
        new_date_str = format_date(new_date)

        # Find and replace the date line
        pattern = r'(nextCollection:\s*["\']?)[^"\']+(["\']?)'
        new_content = re.sub(
            pattern,
            f'\\1{new_date_str}\\2',
            collection['content']
        )

        # Write back to file
        with open(collection['file'], 'w') as f:
            f.write(new_content)

        updated.append({
            'file': collection['file'].name,
            'zone': collection['zone'],
            'waste': collection['waste'],
            'old_date': collection['date'],
            'new_date': new_date
        })

    return updated

def main():
    parser = argparse.ArgumentParser(description='Update bin collection dates')
    parser.add_argument('--days', type=int, default=7, help='Number of days to advance (default: 7)')
    parser.add_argument('--list', action='store_true', help='List current dates without updating')
    parser.add_argument('--content-dir', default='content/bin-collection', help='Content directory')
    args = parser.parse_args()

    print(f"\n{BOLD}🗑️  Bin Collection Date Updater{RESET}")
    print("=" * 50)
    print()

    # Get current collections
    collections = get_bin_collections(args.content_dir)

    if not collections:
        print(f"{RED}❌ No bin collection files found in {args.content_dir}{RESET}")
        return 1

    # Display current dates
    print(f"{BOLD}Current collection dates:{RESET}\n")
    for c in collections:
        date_str = c['date'].strftime('%A, %d %B %Y')
        print(f"  {BLUE}📅 {c['zone']:8s} - {c['waste']:10s}{RESET}: {date_str}")

    if args.list:
        print()
        return 0

    print()
    print(f"This will advance all dates by {BOLD}{args.days} days{RESET}.")
    response = input("Continue? (y/n): ")

    if response.lower() != 'y':
        print(f"\n{YELLOW}❌ Update cancelled{RESET}\n")
        return 0

    # Update dates
    print(f"\n{BOLD}Updating dates...{RESET}\n")
    updated = update_collection_dates(collections, args.days)

    for u in updated:
        old = u['old_date'].strftime('%d/%m/%Y')
        new = u['new_date'].strftime('%d/%m/%Y')
        print(f"  {GREEN}✅ {u['zone']:8s} - {u['waste']:10s}{RESET}: {old} → {new}")

    print(f"\n{GREEN}✨ Update complete!{RESET}\n")
    print(f"{BOLD}Next steps:{RESET}")
    print("  1. Review changes: git diff content/bin-collection/")
    print("  2. Test the site: hugo server")
    print("  3. Commit: git add content/bin-collection/ && git commit -m 'Update bin collection dates'")
    print("  4. Push: git push origin main")
    print()

    return 0

if __name__ == '__main__':
    exit(main())
