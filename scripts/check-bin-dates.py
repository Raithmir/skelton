#!/usr/bin/env python3
"""
Bin Collection Date Checker
Checks if bin collection dates need updating

Usage:
    python3 scripts/check-bin-dates.py
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def parse_date(date_str):
    """Parse ISO 8601 date from frontmatter"""
    date_str = date_str.strip(' "\'')
    formats = [
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S.%f%z',
        '%Y-%m-%d',
    ]

    for fmt in formats:
        try:
            # Remove timezone for naive comparison
            dt = datetime.strptime(date_str, fmt)
            return dt.replace(tzinfo=None) if dt.tzinfo else dt
        except ValueError:
            continue

    return None

def check_bin_collections(content_dir='content/bin-collection'):
    """Check all bin collection dates and report status"""
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    collections = []

    for file_path in Path(content_dir).glob('*.md'):
        with open(file_path, 'r') as f:
            content = f.read()

        zone_match = re.search(r'^zone:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        waste_match = re.search(r'^wasteType:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        date_match = re.search(r'^nextCollection:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)

        if zone_match and waste_match and date_match:
            next_date = parse_date(date_match.group(1))
            if next_date:
                days_until = (next_date - now).days
                collections.append({
                    'zone': zone_match.group(1),
                    'waste': waste_match.group(1),
                    'date': next_date,
                    'days_until': days_until
                })

    return sorted(collections, key=lambda x: x['days_until'])

def main():
    print(f"\n{BOLD}🗑️  Bin Collection Date Checker{RESET}")
    print("=" * 50)
    print()

    collections = check_bin_collections()

    if not collections:
        print(f"{RED}❌ No bin collection files found{RESET}\n")
        return 1

    now = datetime.now()
    past_count = 0
    soon_count = 0
    ok_count = 0

    for c in collections:
        days = c['days_until']
        date_str = c['date'].strftime('%a, %d %b %Y')

        # Determine status
        if days < 0:
            status = f"{RED}⚠️  PAST DUE ({abs(days)} days ago){RESET}"
            past_count += 1
        elif days == 0:
            status = f"{YELLOW}📅 TODAY{RESET}"
            soon_count += 1
        elif days == 1:
            status = f"{YELLOW}📅 TOMORROW{RESET}"
            soon_count += 1
        elif days <= 3:
            status = f"{YELLOW}📅 in {days} days{RESET}"
            soon_count += 1
        elif days <= 7:
            status = f"{GREEN}✅ in {days} days{RESET}"
            ok_count += 1
        else:
            status = f"{GREEN}✅ in {days} days{RESET}"
            ok_count += 1

        print(f"  {c['zone']:8s} - {c['waste']:10s}: {date_str:20s} {status}")

    print()
    print(f"{BOLD}Summary:{RESET}")

    if past_count > 0:
        print(f"  {RED}⚠️  {past_count} collection(s) NEED UPDATING (date passed){RESET}")
    if soon_count > 0:
        print(f"  {YELLOW}📅 {soon_count} collection(s) coming up soon{RESET}")
    if ok_count > 0:
        print(f"  {GREEN}✅ {ok_count} collection(s) scheduled{RESET}")

    print()

    if past_count > 0:
        print(f"{BOLD}Action needed:{RESET}")
        print("  Update dates with: python3 scripts/update-bin-dates.py --days 7")
        print()
        return 1
    elif soon_count > 0:
        print(f"{BOLD}Reminder:{RESET}")
        print("  Update dates after collection day to keep the homepage widget current")
        print()
    else:
        print(f"{GREEN}All dates look good!{RESET}")
        print()

    return 0

if __name__ == '__main__':
    exit(main())
