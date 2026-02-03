# Skelton Gate CMS Editor Guide

Welcome! This guide will help you update the Skelton Gate community website using Decap CMS.

## Accessing the CMS

1. Visit: **https://skeltongate.homes/admin/**
2. Click "Login with GitHub"
3. Authorize the application (first time only)

You'll need GitHub access to the repository. Contact the site administrator if you don't have access.

## Content Types Overview

The CMS is organized into collections. Here's what each one is for:

### 📅 Events
Add community events, meetings, social gatherings.
- **Important:** Set the "Event Date" to when the event happens (used for calendar)
- **Tip:** Use "Featured Event" to highlight important events on homepage
- Set "Draft" to `false` to publish

### 📢 Notices
Post important announcements, alerts, or community news.
- **Priority:** Use "Urgent" for emergencies, "High" for important notices
- **Expiry Date:** Notice automatically disappears after this date
- Set "Draft" to `false` to publish

### 🏢 Local Businesses
Directory of businesses on or near the estate.
- **Category:** Choose appropriate type (Restaurant, Cafe, Shop, etc.)
- Include contact details and opening hours

### 🚶 Walking Routes
Scenic walks starting from Skelton Gate.
- Include distance, difficulty, and duration
- Upload route maps or GPX files if available

### 🛠️ Local Services
Services like plumbers, electricians, cleaners.
- Include category and contact details

### 📞 Contacts
Important contact information (management, council, utilities).
- **Category:** management, builders, council, utilities, emergency
- Include organization name and all available contact methods

### ❓ FAQs
Frequently asked questions organized by category.
- **Title:** The question (e.g., "How do I report a snagging issue?")
- **Body:** The answer with full details
- **Category:** snagging, parking, maintenance, utilities, management

### 📡 Broadband Providers
Compare internet providers available at Skelton Gate.
- Include speeds, technology type, and pricing information

### 🏪 Local Amenities
Nearby shops, restaurants, entertainment venues.
- **Distance:** How far from Skelton Gate (e.g., "2.5 miles")
- Include opening hours and key features

### 🚌 Transport & Travel
Bus routes, train stations, park & ride information.
- Include route numbers, frequencies, and nearest stops

### 🏫 Schools & Childcare
Local schools, nurseries, and childcare providers.
- **Ofsted Rating:** Keep this updated when new reports published
- Include age ranges and admissions info

### 🏥 Healthcare
GPs, dentists, pharmacies, opticians.
- **Accepting Patients:** Important for GPs - keep updated
- Include NHS service status

### 🗑️ Bin Collection
**MOST IMPORTANT TO KEEP UPDATED!**

This drives the homepage widget showing upcoming collections.
- **Next Collection:** ⚠️ Update this date after each collection
- **Zone:** Ensure you're updating the correct zone (A or B)
- Use the helper scripts (see below) to update multiple dates at once

## Common Tasks

### Publishing Content

1. Find the content in the left sidebar
2. Click "Edit" or "New [Content Type]"
3. Fill in all required fields
4. **Set "Draft" to `false`** to make it visible on website
5. Click "Save" (top right)
6. Click "Publish" → "Publish now"

### Updating Bin Collection Dates (Weekly Task)

**Option 1: Manual Update (via CMS)**
1. Go to "Bin Collection" in left sidebar
2. Edit each entry for your zone
3. Update the "Next Collection" date to the next scheduled date
4. Save and publish

**Option 2: Bulk Update (via script - requires terminal access)**
```bash
# Advance all dates by 7 days
python3 scripts/update-bin-dates.py --days 7

# See what dates are currently set
python3 scripts/update-bin-dates.py --list
```

### Adding a New Event

1. Click "Events" in left sidebar
2. Click "New Event"
3. Fill in:
   - **Title**: Event name
   - **Event Date**: When it happens ⚠️ (not "Date" at top)
   - **Event Time**: e.g., "7:00 PM - 9:00 PM"
   - **Location**: Where it takes place
   - **Description**: Full details
4. Set **Draft** to `false`
5. Save & Publish

### Editing Existing Content

1. Find the content in left sidebar
2. Click the item to edit
3. Make your changes
4. Click "Save"
5. Click "Publish" → "Publish now"

### Deleting Content

1. Open the content item
2. Click "Delete entry" (bottom of page)
3. Confirm deletion
4. Publish changes

## Important Tips

### ⚠️ Save Your Work!
- Click "Save" frequently while editing
- Don't close the tab until you see "Changes saved"

### 📱 Preview Not Available
- The CMS preview doesn't work perfectly with our theme
- After publishing, visit the actual website to see how it looks
- Test on: https://skeltongate.homes

### 📅 Dates Can Be Confusing
- **"Date"** at top = Creation date (auto-filled, ignore this)
- **"Event Date"** = When the event actually happens
- **"Next Collection"** = When bins are collected next

### 🔍 Finding Content
- Use browser search (Ctrl+F / Cmd+F) in the content list
- Content is sorted by date (newest first)

### ✏️ Markdown Formatting
For "Description" and "Body" fields, you can use:
- `**bold text**` for **bold**
- `*italic text*` for *italic*
- `[link text](https://url.com)` for links
- `- List item` for bullet points
- `1. List item` for numbered lists

### 🚫 What NOT to Touch
- "Type" field (hidden, auto-set)
- "Layout" field (hidden, auto-set)
- Anything in `static/admin/config.yml` (breaks the CMS)

## Troubleshooting

### "Cannot read property..."
- Refresh the page and try again
- Make sure all required fields are filled

### Changes not showing on website
1. Check "Draft" is set to `false`
2. Make sure you clicked "Publish"
3. Wait 1-2 minutes for deployment
4. Hard refresh the website (Ctrl+Shift+R / Cmd+Shift+R)

### "Authentication Error"
- Your GitHub access may have expired
- Log out and log back in
- Contact administrator if persists

### Can't find your content
- Check if "Draft" is set to `true` (means it's hidden)
- Look in the correct collection in left sidebar
- Use browser search to find it

## Getting Help

- **Technical Issues:** Check CLAUDE.md file in repository
- **Content Questions:** Contact estate management
- **Website Bugs:** Create GitHub issue in repository

## Quick Reference

| Task | Steps |
|------|-------|
| **Publish Event** | Events → New Event → Fill form → Draft=false → Save → Publish |
| **Update Bin Date** | Bin Collection → Edit entry → Update "Next Collection" → Save → Publish |
| **Post Notice** | Notices → New Notice → Set priority → Draft=false → Save → Publish |
| **Add Business** | Businesses → New Business → Fill details → Draft=false → Save → Publish |

---

**Remember:** Draft = false means "publish it", Draft = true means "hide it"

**Weekly Task:** Update bin collection dates every week after collection day!
