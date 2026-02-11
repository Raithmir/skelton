#!/usr/bin/env python3
"""
Geocode map locations for the Skelton Gate community site.

Reads the current site content to build the list of location queries,
then geocodes any that aren't already in data/geocache.json using
Nominatim (OpenStreetMap). Results are cached so only new entries
are geocoded on subsequent runs.

Usage:
    python3 scripts/geocode.py

Run this whenever you add new businesses, amenities, healthcare
providers or schools to the site.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(SITE_ROOT, "data", "geocache.json")
USER_AGENT = "SkeltonGateCommunityMap/1.0 (skeltongate.homes)"
DELAY = 1.2  # seconds between requests (Nominatim ToS: max 1/sec)


def build_query(address, postcode=None):
    """Build a Nominatim search query from address fields."""
    if not address or address.strip().lower() in ("", "leeds"):
        return None
    if postcode:
        return f"{address.strip()} {postcode.strip()}, UK"
    return f"{address.strip()}, Leeds, UK"


def load_content_queries():
    """Walk content directories and build list of (query, meta) tuples."""
    import glob

    locations = []

    def read_frontmatter(filepath):
        """Extract YAML frontmatter from a markdown file."""
        try:
            import re
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not match:
                return {}
            # Simple YAML key: value parser (handles strings and booleans)
            result = {}
            for line in match.group(1).splitlines():
                kv = line.split(":", 1)
                if len(kv) == 2:
                    key = kv[0].strip()
                    val = kv[1].strip().strip("'\"")
                    result[key] = val
            return result
        except Exception:
            return {}

    content_types = {
        "businesses": lambda fm: build_query(fm.get("address"), None),
        "amenities":  lambda fm: build_query(fm.get("address"), fm.get("postcode")),
        "healthcare": lambda fm: build_query(fm.get("address"), fm.get("postcode")),
        "schools":    lambda fm: build_query(fm.get("address"), fm.get("postcode")),
    }

    for section, query_fn in content_types.items():
        pattern = os.path.join(SITE_ROOT, "content", section, "*.md")
        for filepath in sorted(glob.glob(pattern)):
            fm = read_frontmatter(filepath)
            if fm.get("draft", "").lower() == "true":
                continue
            query = query_fn(fm)
            if query:
                locations.append({
                    "query": query,
                    "title": fm.get("title", os.path.basename(filepath)),
                    "type": section.rstrip("s"),
                })

    return locations


def geocode(query):
    """Call Nominatim and return {lat, lng} or None."""
    url = ("https://nominatim.openstreetmap.org/search"
           f"?format=json&limit=1&q={urllib.parse.quote(query)}")
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept-Language": "en",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if data:
            return {"lat": float(data[0]["lat"]), "lng": float(data[0]["lon"])}
    except Exception as e:
        print(f"  ERROR: {e}")
    return None


def main():
    # Load existing cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            cache = json.load(f)
        print(f"Loaded {len(cache)} cached entries from {CACHE_FILE}")

    # Build query list from content
    locations = load_content_queries()
    print(f"Found {len(locations)} locations in content")

    # Find uncached queries
    to_geocode = [loc for loc in locations if loc["query"] not in cache]
    already_cached = len(locations) - len(to_geocode)

    if not to_geocode:
        print("All locations already cached — nothing to do.")
        return

    print(f"{already_cached} already cached, {len(to_geocode)} to geocode\n")

    # Geocode missing entries
    success = 0
    failed = []
    for i, loc in enumerate(to_geocode, 1):
        print(f"[{i}/{len(to_geocode)}] {loc['title']}")
        print(f"  query: {loc['query']}")
        coords = geocode(loc["query"])
        if coords:
            cache[loc["query"]] = coords
            print(f"  → {coords['lat']:.5f}, {coords['lng']:.5f}")
            success += 1
        else:
            print("  → no result")
            failed.append(loc)
        if i < len(to_geocode):
            time.sleep(DELAY)

    # Save updated cache
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {success} geocoded, {len(failed)} failed.")
    print(f"Cache saved to {CACHE_FILE}")

    if failed:
        print("\nFailed locations (add coordinates manually to data/geocache.json):")
        for loc in failed:
            print(f"  {loc['title']}: {loc['query']}")


if __name__ == "__main__":
    main()
