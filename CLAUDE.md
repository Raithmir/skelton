# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site for the Skelton Gate community (skeltongate.homes). It uses the Blowfish theme (Hugo module) and Decap CMS (formerly Netlify CMS) for content management via GitHub backend.

**Purpose:** Community website providing residents with local information including events, businesses, services, amenities, transport links, healthcare providers, schools, and practical resources like bin collection schedules.

## Build Commands

```bash
hugo server              # Development server with live reload (http://localhost:1313)
hugo --minify            # Production build to public/
./deploy.sh              # Full deployment: git pull, build, reload nginx
```

## Navigation Structure

The site uses a nested dropdown menu system with 5 main categories:

- **About** - About Skelton Gate, Skelton Lake Services
- **Community** - Events, Notices, Walking Routes
- **Directory** - Local Amenities, Local Businesses, Local Services, Contacts, Estate Map
- **Local Area** - Healthcare, Schools & Childcare, Transport & Travel, Broadband Providers
- **Resources** - Welcome Pack, Bin Collection, Useful Links, FAQs

### Enabling/Disabling Sections

Sections can be toggled via `config/_default/menus.toml`:

```toml
[[main]]
  name = "Section Name"
  pageRef = "/section-path"
  [main.params]
    enabled = true    # Set to false to hide from navigation
```

The custom menu partial at `layouts/partials/menu.html` filters menu items based on the `enabled` parameter (defaults to `true` if omitted).

## Content Architecture

Content lives in `content/` with 13 content types, each with custom layouts in `layouts/`:

### List Content Types (with category grouping)

| Type | Directory | Key Fields | Template Features |
|------|-----------|------------|-------------------|
| **Events** | `content/events/` | `eventDate`, `eventTime`, `location` | Filters future events, detail page with add-to-calendar |
| **Businesses** | `content/businesses/` | `category`, `address`, `phone` | Category filter buttons, groups by category |
| **Services** | `content/services/` | `category`, `contact`, `email` | Groups by category |
| **Notices** | `content/notices/` | `priority`, `expiryDate` | Priority color-coding, auto-expiry |
| **Walks** | `content/walks/` | `distance`, `difficulty`, `duration` | Route metadata display |
| **Contacts** | `content/contacts/` | `category`, `organization`, `contactPerson` | Groups by category (management, builders, council, utilities, emergency) |
| **FAQs** | `content/faqs/` | `category`, `featured`, `weight` | Accordion-style, groups by category (snagging, parking, maintenance, utilities, management) |
| **Broadband** | `content/broadband/` | `technology`, `maxSpeed`, `availability` | Groups by technology (FTTP, FTTC, Cable), comparison-focused |
| **Amenities** | `content/amenities/` | `category`, `distance`, `postcode` | Category filter buttons, groups by category, distance badges |
| **Transport** | `content/transport/` | `category`, `routeNumber`, `operator` | Groups by category (bus, train, park-and-ride), route-focused |
| **Schools** | `content/schools/` | `category`, `ofstedRating`, `ageRange` | Category filter buttons, groups by category, Ofsted rating badges |
| **Healthcare** | `content/healthcare/` | `category`, `acceptingPatients`, `nhsService` | Category filter buttons, groups by category, "accepting patients" badges |
| **Bin Collection** | `content/bin-collection/` | `wasteType`, `referenceDate`, `color` | Color-coded by waste type, shows upcoming dates. One zone; black bin (general waste) and green bin (recycling) collected on alternate Tuesdays. |

### Single Page Content

| Page | Path | Purpose |
|------|------|---------|
| **About Skelton Gate** | `content/about/_index.md` | Estate history, development phases, community facilities |
| **Skelton Lake Services** | `content/skelton-lake-services/_index.md` | Nearby motorway services information |
| **Welcome Pack** | `content/welcome-pack/_index.md` | New resident onboarding guide |
| **Useful Links** | `content/links/_index.md` | Curated external resources (council, utilities, emergency services) |

## Creating Content

```bash
# List content types (auto-generates from archetype)
hugo new content/events/2026-01-15-event-name.md
hugo new content/contacts/contact-name.md
hugo new content/amenities/amenity-name.md
hugo new content/bin-collection/black-bin.md

# Single pages (edit directly)
# Edit content/about/_index.md, content/welcome-pack/_index.md, etc.
```

Archetypes in `archetypes/` define frontmatter templates for each content type.

## Layout Patterns

All list layouts follow a consistent pattern using Hugo's `GroupByParam` function:

```go
{{ $items := where .Pages ".Params.draft" "!=" true }}
{{ $itemsByCategory := $items.GroupByParam "category" }}

{{ range $itemsByCategory }}
  {{ $category := default "Other" .Key | title }}
  {{ range .Pages }}
    <!-- Render item -->
  {{ end }}
{{ end }}
```

This pattern is used in: businesses, contacts, amenities, transport, schools, healthcare, broadband, faqs, and bin-collection layouts.

## Key Files

### Configuration
- `hugo.toml` - Site configuration, theme settings, output formats (HTML/RSS/JSON/ICS)
- `config/_default/params.toml` - Theme params including `enableSearch = true`, `fuzzySearching = true`
- `config/_default/menus.toml` - Navigation menu structure with enable/disable parameters
- `static/admin/config.yml` - CMS field definitions and collections (13 collections total)
- `data/geocache.json` - Pre-computed lat/lng for all content locations (used by Leaflet map)
- `assets/css/custom.css` - Custom CSS: hero gradient, badge styles, print styles

### Layouts
- `layouts/index.html` - Homepage with featured notices, events, businesses, and bin collection widget
- `layouts/partials/menu.html` - Custom menu rendering with enable/disable filtering
- `layouts/partials/widgets/bin-collection.html` - Homepage widget showing next 3 bin collections
- `layouts/partials/documents.html` - Reusable downloads section (used on About, Welcome Pack, Useful Links)
- `layouts/{type}/list.html` - List page templates for each content type
- `layouts/map/list.html` - Interactive Leaflet.js map aggregating businesses, amenities, healthcare, schools
- `layouts/business/simple.html` - Detail page for businesses (image, address, phone, website, hours, map)
- `layouts/walk/simple.html` - Detail page for walks (difficulty/distance/duration badges, start point map, highlights, GPX download)
- `layouts/amenity/simple.html` - Detail page for amenities (contact info, features, map)
- `layouts/healthcare/simple.html` - Detail page for healthcare (badges, services, map)
- `layouts/school/simple.html` - Detail page for schools (Ofsted badge, admissions, map)
- `layouts/transport/simple.html` - Detail page for transport (route info, nearest stop, walking map)
- `layouts/event/simple.html` - Detail page for events (metadata, Google Calendar link, .ics download, map)

**Hugo layout resolution:** Single-page layouts are looked up by the `type` field in frontmatter (e.g. `type: business` → `layouts/business/`), NOT by the content directory name. List layouts use the content directory name. The Blowfish `simple` layout only renders `{{ .Content }}` — if frontmatter fields need to be shown on detail pages, a custom layout must be created in `layouts/{type}/simple.html`.

### Content Directories
- `content/` - All markdown content files organized by type
- `archetypes/` - Frontmatter templates for `hugo new` commands

## Frontmatter Notes

- **Events** use `eventDate` (ISO 8601 datetime) for scheduling, separate from `date` (creation date)
- **Notices** with `expiryDate` in the past are automatically hidden
- **Bin Collection** uses `referenceDate` (ISO 8601 date) — the list template calculates upcoming fortnightly Tuesdays from this anchor date
- **Healthcare** GPs use `acceptingPatients: true/false` for badge display
- **Schools** use `ofstedRating` with color-coded badges (Outstanding=green, Good=blue, etc.)
- All content types support `draft: true` to hide from listings
- All archetypes use YAML frontmatter (`---`)

## Homepage Widgets

The homepage sidebar (`layouts/index.html`) includes:

1. **Quick Links** - Section counts and navigation
2. **Bin Collection Widget** - Shows next 3 upcoming collections with color coding and countdown
3. **Upcoming Events** - Next 5 events with dates

The bin collection widget (`layouts/partials/widgets/bin-collection.html`):
- Calculates upcoming fortnightly Tuesdays from each bin type's `referenceDate`
- Shows next 3 upcoming collections across both bin types
- Shows countdown for collections within 3 days ("Today!", "Tomorrow", "X days")
- Color-coded by waste type (black, green)

## Dummy Content

Most content currently uses placeholder/dummy data with disclaimers. To update:

1. **Via CMS**: Navigate to `/admin/` and edit through web interface
2. **Via CLI**: Use `hugo new` or directly edit markdown files in `content/`
3. **Update dates**: Bin collection dates and event dates need regular updates to remain current

When adding real content, remove placeholder disclaimers from single pages.

## Theme

The site uses the **Blowfish v2 theme** as a Hugo module (not a git submodule). Update with:

```bash
hugo mod get -u github.com/nunocoracao/blowfish/v2
hugo mod tidy
```

Custom layouts in `layouts/` override theme templates. The custom menu partial is required for the enable/disable functionality.

## Already-Implemented Features

Do NOT suggest these as ideas — they are already built:

- **Search** — Fuse.js fuzzy search built into Blowfish (`enableSearch = true`). Search button in header on desktop and mobile. JSON index at `/index.json`.
- **Bin collection calendar** — `.ics` feed at `/bin-collection/calendar.ics` via Hugo output format. Subscribe/download buttons on the bin collection list page.
- **Events calendar** — `.ics` feed at `/events/calendar.ics`. Each event detail page also has an individual .ics download and Google Calendar link.
- **Interactive estate map** — Leaflet.js map at `/map/` aggregating all businesses, amenities, healthcare, schools. Markers colour-coded by type. Geocoding via Nominatim with results cached in `data/geocache.json` and localStorage.
- **Google Maps embeds** — Directions iframes on all 7 detail page types (event, business, amenity, healthcare, school, transport, walk).
- **GPX route download** — On walk detail pages.
- **FAQ attachments** — File attachments per FAQ entry.
- **Documents/downloads section** — Reusable partial on About, Welcome Pack, Useful Links pages.
- **Category filter buttons** — Client-side JS filtering on businesses, amenities, healthcare, schools.
- **Print styles** — In `assets/css/custom.css`.
- **Crime stats widget** — Homepage sidebar widget fetching from data.police.uk API. Shows crime counts by category for the most recent available month (~1 mile radius). Links to `/crime-map/` and police.uk Leeds East.
- **Local crime map** — Leaflet.js + Leaflet.markercluster at `/crime-map/`. Colour-coded markers (14 categories), category filter toggles, 24h localStorage cache (`crimeMapCache`). Linked from widget only (no nav entry). Data from data.police.uk `crimes-street/all-crime` endpoint.

## External Dependencies

- **Sveltia CMS** (Decap-compatible) - Admin interface at `/admin/`, uses GitHub OAuth for authentication; loads latest version from unpkg
- **Blowfish Theme** - Hugo module providing base styling and components
- **Leaflet.js** v1.9.4 (CDN) - Interactive map on `/map/` and `/crime-map/`
- **Leaflet.markercluster** v1.5.3 (CDN) - Marker clustering on `/crime-map/`
- **Fuse.js** - Full-text fuzzy search (bundled with Blowfish theme)
- **OpenStreetMap/Nominatim** - Geocoding for the estate map
- **Google Maps Embed API** - Used on detail pages for directions (origin: Beckside Crescent, Leeds)
- **data.police.uk API** - Crime data for homepage widget and `/crime-map/` (West Yorkshire Police, ~1 mile radius, most recent available month)

## Site Maintenance

### Regular Updates Needed

1. **Bin Collection Dates** - Update `nextCollection` dates in `content/bin-collection/black-bin.md` and `green-bin.md` when the fortnight rolls over. Black and green bins alternate weekly on Tuesdays.
2. **Event Dates** - Add upcoming events, past events auto-hide from homepage
3. **Contact Information** - Verify phone numbers, emails, addresses remain current
4. **Amenity Hours** - Update opening hours, especially for seasonal changes
5. **School Information** - Update Ofsted ratings when reports are published
6. **Transport Schedules** - Update frequencies and operating hours when timetables change

### Utility Scripts

The `scripts/` directory contains maintenance helpers:
- `update-bin-dates.py` / `update-bin-dates.sh` - Advance bin collection `referenceDate` by N weeks
- `check-bin-dates.py` - Verify current bin collection dates are still in the future
- `geocode.py` - Query Nominatim to build/update `data/geocache.json` for the estate map

### Content Review

Content marked with "This is placeholder content. Information will be updated soon." should be replaced with accurate information before going live.

## Development Notes

- Site uses Tailwind CSS via Blowfish theme
- **Tailwind CSS purge:** Only utility classes used by the Blowfish theme are available in the compiled CSS. Many standard Tailwind classes (e.g. `mr-6`, `gap-6`, `gap-8`) are purged and will silently have no effect. When a Tailwind class doesn't work, use inline `style=""` attributes instead. Available classes can be checked in the compiled CSS files in `public/css/`.
- Dark mode supported throughout via `dark:` class variants
- Responsive design with mobile-first breakpoints: `md:`, `lg:`
- SVG icons used for metadata (phone, email, location, etc.)
- All layouts include empty state fallbacks for sections with no content
- **Google Maps origin:** All detail page maps use `Beckside+Crescent,+Leeds` as the directions origin (not "Skelton Gate, LS9 0FN" which resolves to Skelton Crescent, off-estate)
