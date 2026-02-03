# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site for the Skelton Gate community (skeltongate.homes). It uses the Ananke theme (git submodule) and Decap CMS (formerly Netlify CMS) for content management via GitHub backend.

## Build Commands

```bash
hugo server              # Development server with live reload (http://localhost:1313)
hugo --minify            # Production build to public/
./deploy.sh              # Full deployment: git pull, build, reload nginx
```

## Content Architecture

Content lives in `content/` with five main types, each with custom layouts in `layouts/`:

| Type | Directory | Key Fields | Template Features |
|------|-----------|------------|-------------------|
| **Events** | `content/events/` | `eventDate`, `eventTime`, `location` | FullCalendar integration, filters future events |
| **Businesses** | `content/businesses/` | `category`, `address`, `phone` | Groups by category |
| **Walks** | `content/walks/` | `distance`, `difficulty`, `duration` | Route metadata display |
| **Notices** | `content/notices/` | `priority`, `expiryDate` | Priority color-coding, auto-expiry |
| **Services** | `content/services/` | `category`, `contact`, `email` | Groups by category |

### Creating Content

```bash
hugo new content/events/2026-01-15-event-name.md    # Uses archetypes/events.md template
hugo new content/businesses/business-name.md        # Uses archetypes/businesses.md template
```

Archetypes in `archetypes/` define frontmatter templates for each content type.

## Key Files

- `hugo.toml` - Site configuration, menu structure
- `static/admin/config.yml` - CMS field definitions and collections
- `layouts/calendar.json` - Generates JSON feed for FullCalendar at `/events/calendar.json`
- `layouts/index.html` - Homepage showing featured notices, events, businesses

## Frontmatter Notes

- Events use `eventDate` (ISO 8601 datetime) for scheduling, separate from `date` (creation date)
- Notices with `expiryDate` in the past are automatically hidden
- All content types support `draft: true` to hide from listings
- Archetypes use YAML frontmatter (`---`) except `default.md` which uses TOML (`+++`)

## Theme

The Ananke theme is a git submodule at `themes/ananke/`. Update with:

```bash
git submodule update --remote themes/ananke
```

Custom layouts in `layouts/` override theme templates.

## External Dependencies

- **FullCalendar v6.1.10** - CDN loaded in events list template
- **Decap CMS** - Admin interface at `/admin/`, uses GitHub OAuth
