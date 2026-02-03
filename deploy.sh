#!/bin/bash
cd /var/www/community-site

# Pull latest changes
git pull origin main 2>&1

# Build the site
hugo --minify 2>&1

# Reload nginx with sudo (now allowed without password)
sudo /bin/systemctl reload nginx 2>&1
