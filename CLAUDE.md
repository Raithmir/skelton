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

The site uses a nested dropdown menu system with 4 main categories:

- **About** - About Skelton Gate, Skelton Lake Services
- **Community** - Events, Notices, Walking Routes
- **Directory** - Local Businesses, Local Services, Contacts
- **Resources** - Welcome Pack, Local Amenities, Transport, Schools, Healthcare, Broadband, Links, Bin Collection, FAQs

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
| **Events** | `content/events/` | `eventDate`, `eventTime`, `location` | FullCalendar integration, filters future events |
| **Businesses** | `content/businesses/` | `category`, `address`, `phone` | Groups by category |
| **Services** | `content/services/` | `category`, `contact`, `email` | Groups by category |
| **Notices** | `content/notices/` | `priority`, `expiryDate` | Priority color-coding, auto-expiry |
| **Walks** | `content/walks/` | `distance`, `difficulty`, `duration` | Route metadata display |
| **Contacts** | `content/contacts/` | `category`, `organization`, `contactPerson` | Groups by category (management, builders, council, utilities, emergency) |
| **FAQs** | `content/faqs/` | `category`, `featured`, `weight` | Accordion-style, groups by category (snagging, parking, maintenance, utilities, management) |
| **Broadband** | `content/broadband/` | `technology`, `maxSpeed`, `availability` | Groups by technology (FTTP, FTTC, Cable), comparison-focused |
| **Amenities** | `content/amenities/` | `category`, `distance`, `postcode` | Groups by category (supermarket, restaurant, cafe, entertainment), distance badges |
| **Transport** | `content/transport/` | `category`, `routeNumber`, `operator` | Groups by category (bus, train, park-and-ride), route-focused |
| **Schools** | `content/schools/` | `category`, `ofstedRating`, `ageRange` | Groups by category (nursery, primary, secondary), Ofsted rating badges |
| **Healthcare** | `content/healthcare/` | `category`, `acceptingPatients`, `nhsService` | Groups by category (gp, dentist, pharmacy, optician), "accepting patients" badges |
| **Bin Collection** | `content/bin-collection/` | `zone`, `wasteType`, `nextCollection`, `color` | Groups by zone, color-coded by waste type, shows upcoming dates |

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
hugo new content/bin-collection/zone-a-general.md

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
- `hugo.toml` - Site configuration, theme settings
- `config/_default/menus.toml` - Navigation menu structure with enable/disable parameters
- `static/admin/config.yml` - CMS field definitions and collections (13 collections total)

### Layouts
- `layouts/index.html` - Homepage with featured notices, events, businesses, and bin collection widget
- `layouts/partials/menu.html` - Custom menu rendering with enable/disable filtering
- `layouts/partials/widgets/bin-collection.html` - Homepage widget showing next 3 bin collections
- `layouts/calendar.json` - Generates JSON feed for FullCalendar at `/events/calendar.json`
- `layouts/{type}/list.html` - List page templates for each content type

### Content Directories
- `content/` - All markdown content files organized by type
- `archetypes/` - Frontmatter templates for `hugo new` commands

## Frontmatter Notes

- **Events** use `eventDate` (ISO 8601 datetime) for scheduling, separate from `date` (creation date)
- **Notices** with `expiryDate` in the past are automatically hidden
- **Bin Collection** uses `nextCollection` (ISO 8601 date) for sorting and countdown display
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
- Filters to upcoming collections only
- Sorts by `nextCollection` date
- Shows countdown for collections within 3 days ("Today!", "Tomorrow", "X days")
- Color-coded by waste type (black, blue, green, brown)

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

## External Dependencies

- **FullCalendar v6.1.10** - CDN loaded in events list template for calendar view
- **Decap CMS** - Admin interface at `/admin/`, uses GitHub OAuth for authentication
- **Blowfish Theme** - Hugo module providing base styling and components

## Site Maintenance

### Regular Updates Needed

1. **Bin Collection Dates** - Update `nextCollection` dates in bin-collection content when schedules change
2. **Event Dates** - Add upcoming events, past events auto-hide from homepage
3. **Contact Information** - Verify phone numbers, emails, addresses remain current
4. **Amenity Hours** - Update opening hours, especially for seasonal changes
5. **School Information** - Update Ofsted ratings when reports are published
6. **Transport Schedules** - Update frequencies and operating hours when timetables change

### Content Review

Content marked with "This is placeholder content. Information will be updated soon." should be replaced with accurate information before going live.

## Development Notes

- Site uses Tailwind CSS via Blowfish theme
- Dark mode supported throughout via `dark:` class variants
- Responsive design with mobile-first breakpoints: `md:`, `lg:`
- SVG icons used for metadata (phone, email, location, etc.)
- All layouts include empty state fallbacks for sections with no content
