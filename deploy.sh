#!/bin/bash
cd /var/www/community-site
git pull origin main
hugo --minify
sudo systemctl reload nginx
