# Skelton Gate Community Website

Community website for the Skelton Gate housing estate, Leeds. Provides residents with local information including events, notices, businesses, amenities, healthcare, schools, transport, and practical resources.

**Live site:** https://skeltongate.homes
**Repository:** https://github.com/Raithmir/skelton

---

## Tech Stack

| Component | Details |
|-----------|---------|
| Static site generator | [Hugo](https://gohugo.io/) |
| Theme | [Blowfish v2](https://blowfish.page/) (Hugo module) |
| CMS | [Sveltia CMS](https://github.com/sveltia/sveltia-cms) |
| CMS auth | GitHub OAuth (via `base_url: https://skeltongate.homes`) |
| Maps | [Leaflet.js](https://leafletjs.com/) + OpenStreetMap / Nominatim geocoding |
| Hosting | nginx on Linux VPS |
| Deployment | Auto-deploy via webhook on push to `main` |

---

## Local Development

### Prerequisites

- Hugo extended v0.140+ (`hugo version`)
- Git

### Run locally

```bash
git clone https://github.com/Raithmir/skelton.git
cd skelton
hugo server
```

Open http://localhost:1313. Changes to content and layouts hot-reload automatically.

### Production build

```bash
hugo --minify
```

Output goes to `public/`. **Never run as root** — the deploy webhook runs as `www-data` and root-owned files in `public/` will break future deploys. If a manual build is needed on the server: `sudo -u www-data hugo --minify`.

---

## Deployment

Pushing to the `main` branch triggers an automatic deploy via webhook:

1. `git pull` — pulls latest changes
2. `hugo --minify` — builds to `public/`
3. `nginx reload` — reloads nginx to serve new files

The deploy script is at `deploy.sh`. Uncommitted files are not deployed.

---

## Content Management (Sveltia CMS)

The CMS provides a web interface for editors who don't want to work directly with Git and Markdown.

### Accessing the CMS

1. Go to the CMS login URL
2. Click **Login with GitHub**
3. Authorise the app — you must be a collaborator on the `Raithmir/skelton` repository

### Adding new content

1. In the left sidebar, click the collection you want (e.g. **Events**, **Businesses**)
2. Click the **New [item]** button (top right)
3. Fill in the fields — required fields are marked
4. Toggle **Draft** off when the entry is ready to go live
5. Click **Save** — this creates a commit directly to `main` and triggers a deploy

### Editing existing content

1. Click the collection in the sidebar
2. Find the entry (use search if needed)
3. Make changes and click **Save**

### Deleting content

Open the entry and click the **Delete** button (⋮ menu or bottom of the form).

### Draft entries

Set **Draft: true** to hide an entry from all listings without deleting it. Toggle it to false when ready to publish.

### Single pages

The **Single Pages** collection lets you edit the prose content of:
- About Skelton Gate
- Skelton Lake Services
- Welcome Pack
- Useful Links

---

## Content Types

### Events (`content/events/`)
Community events. Key fields:
- **Event Date** — ISO datetime, used for sorting and filtering (past events auto-hide from the homepage)
- **Event Time** — display string, e.g. "2pm – 5pm"
- **Location** — venue name/address (appears on detail page map)

Calendar feed: https://skeltongate.homes/events/calendar.ics

### Notices (`content/notices/`)
Community announcements. Key fields:
- **Priority** — `low`, `normal`, `high`, `urgent` (controls colour coding)
- **Expiry Date** — notices auto-hide after this date

### Walking Routes (`content/walks/`)
Local walking routes. Key fields: `distance`, `difficulty`, `duration`, `startPoint`.

### Businesses (`content/businesses/`)
Local businesses. Key fields: `category`, `address`, `phone`, `website`, `hours`.

### Services (`content/services/`)
Local service providers. Key fields: `category`, `contact`, `email`.

### Local Amenities (`content/amenities/`)
Nearby amenities (supermarkets, restaurants, leisure). Key fields: `category`, `address`, `postcode`, `distance`, `hours`.

### Healthcare (`content/healthcare/`)
GP surgeries, pharmacies, dentists. Key fields: `category`, `address`, `postcode`, `acceptingPatients` (shows badge), `nhsService`.

### Schools & Childcare (`content/schools/`)
Schools and nurseries. Key fields: `category`, `address`, `postcode`, `ofstedRating`, `ageRange`.

### Transport (`content/transport/`)
Bus routes, train services, Park & Ride. Key fields: `category`, `routeNumber`, `operator`, `frequency`, `nearestStop`.

### Broadband Providers (`content/broadband/`)
Broadband options. Key fields: `technology` (FTTP/FTTC/Cable), `maxSpeed`, `availability`.

### Contacts (`content/contacts/`)
Key contacts (management company, builders, council). Key fields: `category`, `organization`, `phone`, `email`.

### FAQs (`content/faqs/`)
Frequently asked questions. Key fields: `category`, `featured`, `weight` (sort order).

### Bin Collection (`content/bin-collection/`)
One entry per bin type (currently `black-bin.md` and `green-bin.md`). Key field:
- **Reference Date** — the date of a known past collection. The site calculates all future fortnightly dates from this. **Update this whenever the schedule shifts** (e.g. after a bank holiday delay).

Calendar feed: https://skeltongate.homes/bin-collection/calendar.ics

---

## Features

### Calendar Feeds (iCal / .ics)

Both the **Events** and **Bin Collection** pages expose a subscribe button. The `.ics` feeds can be added to Google Calendar, Apple Calendar, or Outlook as a live subscription that updates automatically.

- Events feed: `/events/calendar.ics` — all non-draft events
- Bin collection feed: `/bin-collection/calendar.ics` — ~26 fortnightly dates per bin type (~1 year ahead), calculated from `referenceDate`

### Estate Map (`/map/`)

Interactive map showing businesses, amenities, healthcare providers and schools. Accessible via **Directory → Estate Map**.

**How location coordinates work:**

Marker positions are pre-computed at build time from `data/geocache.json`. This means the map loads instantly for all visitors with no API calls required.

When new location content is added, run the geocoding script to update the cache (see [Scripts](#scripts) below), then commit `data/geocache.json`.

Locations not in the cache fall back to client-side Nominatim geocoding on the visitor's first view, then cache in their browser `localStorage`.

### Crime Stats Widget & Crime Map

The homepage sidebar includes a **Crime Stats widget** that fetches the most recent month of crime data from the [data.police.uk API](https://data.police.uk) and shows a breakdown by category for the area around Skelton Gate (~1 mile radius). Data is cached in `localStorage` for 24 hours.

The widget links to the **Local Crime Map** at `/crime-map/` — an interactive Leaflet map with colour-coded markers for all 14 crime categories, marker clustering (click to expand), category filter toggles, and individual popups showing crime type, street, and outcome status.

The crime map is not in the main navigation — it is accessed via the widget link only.

### Bin Collection Widget

The homepage sidebar shows the next 3 upcoming collections with a countdown for collections within 3 days ("Today!", "Tomorrow", "In X days"). Automatically calculated from `referenceDate` in each bin content file.

### Navigation

Five dropdown groups:

| Group | Items |
|-------|-------|
| About | About Skelton Gate, Skelton Lake Services |
| Community | Events, Notices, Walking Routes |
| Directory | Local Amenities, Local Businesses, Local Services, Contacts, Estate Map |
| Local Area | Healthcare, Schools & Childcare, Transport & Travel, Broadband Providers |
| Resources | Welcome Pack, Bin Collection, Useful Links, FAQs |

Menu items can be hidden without deleting them by setting `enabled = false` in `config/_default/menus.toml`.

---

## Scripts

### `scripts/geocode.py`

Pre-geocodes map location addresses and saves coordinates to `data/geocache.json`.

**When to run:** After adding or updating businesses, amenities, healthcare providers, or schools.

**How to run:**
```bash
python3 scripts/geocode.py
```

The script:
- Reads all content from `content/businesses/`, `content/amenities/`, `content/healthcare/`, `content/schools/`
- Skips entries already in `data/geocache.json`
- Calls Nominatim (OpenStreetMap) with a 1.2 second delay between requests
- Saves new results to `data/geocache.json`

After running, commit `data/geocache.json` and push:
```bash
git add data/geocache.json
git commit -m "Update geocache with new locations"
git push
```

If a location fails to geocode (vague or informal address), it will be listed at the end of the script output. You can add coordinates manually to `data/geocache.json`:
```json
{
  "My Business, Example Street, Leeds, UK": { "lat": 53.7950, "lng": -1.5479 }
}
```

---

## Regular Maintenance

### Bin collection dates

When the fortnightly schedule shifts (e.g. due to a bank holiday), update `referenceDate` in:
- `content/bin-collection/black-bin.md`
- `content/bin-collection/green-bin.md`

Set `referenceDate` to the date of a known upcoming or recent collection for that bin. The site calculates all subsequent fortnightly dates from this value.

### Events

Past events auto-hide from the homepage but remain accessible on the events page. Add new events via the CMS or by creating a file in `content/events/`.

### Placeholder content

Several sections contain placeholder data marked with *"This is placeholder content. Information will be updated soon."* Replace these with real information via the CMS when available.

---

## Project Structure

```
.
├── archetypes/          # Frontmatter templates for hugo new
├── assets/css/          # Custom CSS (custom.css)
├── config/_default/     # Hugo configuration
│   ├── menus.toml       # Navigation menu
│   └── params.toml      # Theme parameters
├── content/             # All site content (Markdown)
│   ├── amenities/
│   ├── bin-collection/
│   ├── businesses/
│   ├── events/
│   ├── faqs/
│   ├── healthcare/
│   ├── crime-map/       # Local crime map page
│   ├── map/             # Estate map page
│   ├── notices/
│   ├── schools/
│   ├── services/
│   ├── transport/
│   └── walks/
├── data/
│   └── geocache.json    # Pre-geocoded map coordinates
├── hugo.toml            # Hugo configuration
├── layouts/             # Custom layout templates (override Blowfish)
│   ├── events/
│   │   ├── calendar.ics   # iCal feed template
│   │   └── list.html
│   ├── bin-collection/
│   │   ├── calendar.ics   # iCal feed template
│   │   └── list.html
│   ├── crime-map/
│   │   └── list.html      # Crime map with Leaflet.js + markercluster
│   ├── map/
│   │   └── list.html      # Estate map with Leaflet.js
│   ├── partials/
│   │   ├── extend-head-uncached.html  # Injects Leaflet CSS into <head>
│   │   ├── menu.html                  # Custom nav with enable/disable
│   │   └── widgets/
│   │       ├── bin-collection.html    # Homepage bin widget
│   │       └── crime-stats.html       # Homepage crime stats widget
│   └── index.html       # Homepage
├── scripts/
│   └── geocode.py       # Map location geocoding script
└── static/
    └── admin/           # Sveltia CMS
        ├── config.yml   # CMS field definitions
        └── index.html   # CMS entry point
```
