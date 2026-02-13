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

def next_fortnightly_date(reference_date, today):
    """Advance reference_date by 14-day increments until it's >= today"""
    d = reference_date
    while d < today:
        d += timedelta(days=14)
    return d


def check_bin_collections(content_dir='content/bin-collection'):
    """Check all bin collection dates and report status"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    collections = []

    for file_path in Path(content_dir).glob('*.md'):
        if file_path.name == '_index.md':
            continue
        with open(file_path, 'r') as f:
            content = f.read()

        title_match = re.search(r'^title:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        waste_match = re.search(r'^wasteType:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)
        date_match = re.search(r'^referenceDate:\s*["\']?([^"\']+)["\']?', content, re.MULTILINE)

        if waste_match and date_match:
            reference_date = parse_date(date_match.group(1))
            if reference_date:
                next_date = next_fortnightly_date(reference_date, today)
                days_until = (next_date - today).days
                collections.append({
                    'title': title_match.group(1) if title_match else file_path.stem,
                    'waste': waste_match.group(1),
                    'date': next_date,
                    'days_until': days_until,
                    'reference_date': reference_date,
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

    soon_count = 0
    ok_count = 0

    for c in collections:
        days = c['days_until']
        date_str = c['date'].strftime('%a, %d %b %Y')
        ref_str = c['reference_date'].strftime('%Y-%m-%d')

        if days == 0:
            status = f"{YELLOW}📅 TODAY{RESET}"
            soon_count += 1
        elif days == 1:
            status = f"{YELLOW}📅 TOMORROW{RESET}"
            soon_count += 1
        elif days <= 7:
            status = f"{YELLOW}📅 in {days} days{RESET}"
            soon_count += 1
        else:
            status = f"{GREEN}✅ in {days} days{RESET}"
            ok_count += 1

        print(f"  {c['title']:20s} ({c['waste']:10s}): next {date_str:20s} {status}")
        print(f"  {'':20s}  referenceDate: {ref_str}")
        print()

    print(f"{BOLD}Summary:{RESET}")
    if soon_count > 0:
        print(f"  {YELLOW}📅 {soon_count} collection(s) coming up within a week{RESET}")
    if ok_count > 0:
        print(f"  {GREEN}✅ {ok_count} collection(s) scheduled{RESET}")
    print()
    print("Dates are calculated fortnightly from referenceDate — no manual updates needed.")
    print()

    return 0

if __name__ == '__main__':
    exit(main())
