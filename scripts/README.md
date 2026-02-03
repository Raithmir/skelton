# Skelton Gate Utility Scripts

Helper scripts for maintaining the Skelton Gate community website.

## Bin Collection Scripts

### 1. Check Bin Dates (`check-bin-dates.py`)

**Purpose:** Quickly see the status of all bin collection dates.

**Usage:**
```bash
python3 scripts/check-bin-dates.py
```

**Output:**
- Shows all bin collection dates sorted by when they occur
- Highlights past-due dates in red
- Highlights upcoming dates (0-3 days) in yellow
- Shows future dates (4+ days) in green

**When to use:**
- Before updating the website
- Weekly check to see if dates need updating
- After making changes to verify they're correct

**Example Output:**
```
🗑️  Bin Collection Date Checker
==================================================

  Zone A   - general    : Wed, 05 Feb 2026      ⚠️  PAST DUE (2 days ago)
  Zone A   - recycling  : Wed, 12 Feb 2026      📅 in 7 days
  Zone B   - general    : Thu, 06 Feb 2026      📅 TOMORROW

Summary:
  ⚠️  1 collection(s) NEED UPDATING (date passed)
  📅 1 collection(s) coming up soon
  ✅ 1 collection(s) scheduled
```

---

### 2. Update Bin Dates (`update-bin-dates.py`)

**Purpose:** Bulk update all bin collection dates by adding days.

**Usage:**
```bash
# Advance all dates by 7 days (weekly update)
python3 scripts/update-bin-dates.py --days 7

# Advance all dates by 14 days (fortnightly)
python3 scripts/update-bin-dates.py --days 14

# Just list current dates without updating
python3 scripts/update-bin-dates.py --list
```

**What it does:**
1. Reads all bin collection markdown files
2. Extracts the `nextCollection` date from each
3. Adds the specified number of days
4. Updates the files with new dates
5. Shows what changed

**When to use:**
- Every week after collection day
- When starting a new collection cycle
- When dates need to be synchronized

**Example Output:**
```
🗑️  Bin Collection Date Updater
==================================================

Current collection dates:

  📅 Zone A   - general    : Wednesday, 05 February 2026
  📅 Zone A   - recycling  : Wednesday, 12 February 2026
  📅 Zone B   - general    : Thursday, 06 February 2026

This will advance all dates by 7 days.
Continue? (y/n): y

Updating dates...

  ✅ Zone A   - general    : 05/02/2026 → 12/02/2026
  ✅ Zone A   - recycling  : 12/02/2026 → 19/02/2026
  ✅ Zone B   - general    : 06/02/2026 → 13/02/2026

✨ Update complete!

Next steps:
  1. Review changes: git diff content/bin-collection/
  2. Test the site: hugo server
  3. Commit: git add content/bin-collection/ && git commit -m 'Update bin collection dates'
  4. Push: git push origin main
```

---

### 3. Update Bin Dates (Bash version) (`update-bin-dates.sh`)

**Purpose:** Same as Python version but uses Bash (for Linux/macOS terminal users).

**Usage:**
```bash
./scripts/update-bin-dates.sh 7   # Advance by 7 days
./scripts/update-bin-dates.sh 14  # Advance by 14 days
```

**Note:** Python version is recommended as it's more cross-platform compatible.

---

## Typical Weekly Workflow

**Every week after bin collection:**

1. **Check current status:**
   ```bash
   python3 scripts/check-bin-dates.py
   ```

2. **Update dates (if needed):**
   ```bash
   python3 scripts/update-bin-dates.py --days 7
   ```

3. **Review changes:**
   ```bash
   git diff content/bin-collection/
   ```

4. **Test locally:**
   ```bash
   hugo server
   # Visit http://localhost:1313 and check bin widget
   ```

5. **Commit and push:**
   ```bash
   git add content/bin-collection/
   git commit -m "Update bin collection dates for week of $(date +%d/%m/%Y)"
   git push origin main
   ```

6. **Deploy:**
   ```bash
   ./deploy.sh
   ```

---

## Automation Ideas

### Cron Job (Linux/macOS)

Run check script daily and email if dates are outdated:

```bash
# Add to crontab: crontab -e
0 9 * * * cd /var/www/community-site && python3 scripts/check-bin-dates.py | mail -s "Bin Date Status" admin@example.com
```

### GitHub Actions

Auto-update dates weekly:

```yaml
# .github/workflows/update-bin-dates.yml
name: Update Bin Dates
on:
  schedule:
    - cron: '0 2 * * 4'  # Every Thursday at 2am
  workflow_dispatch:  # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Update dates
        run: python3 scripts/update-bin-dates.py --days 7
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add content/bin-collection/
          git commit -m "Automated: Update bin collection dates" || echo "No changes"
          git push
```

---

## Troubleshooting

### "No bin collection files found"
- Check you're in the correct directory
- Verify `content/bin-collection/` exists
- Ensure markdown files exist in that directory

### Date parsing errors
- Check the date format in frontmatter is: `nextCollection: "2026-02-05T00:00:00+00:00"`
- Ensure dates are properly quoted
- Look for typos in the date string

### Script not executable
```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

### Python not found
```bash
# Install Python 3
sudo apt install python3  # Linux
brew install python3      # macOS
```

---

## Requirements

- **Python 3.6+** (for .py scripts)
- **Bash** (for .sh scripts)
- **Git** (for committing changes)
- **Hugo** (for testing changes)

No additional Python packages required - uses standard library only.

---

## Adding More Scripts

When adding new utility scripts:
1. Add them to this `scripts/` directory
2. Make them executable: `chmod +x scripts/your-script.py`
3. Add usage instructions to this README
4. Include helpful output with color coding
5. Add error handling and validation

---

## Questions?

See the main **CLAUDE.md** file for general site documentation, or **CMS-EDITOR-GUIDE.md** for CMS usage.
