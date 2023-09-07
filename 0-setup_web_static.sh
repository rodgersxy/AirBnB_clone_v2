#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.
# Creates the folders where the static resources will be held
# creates placeholder files and symbolic links
# Update and install Nginx
apt-get update
apt-get install -y nginx

# Create necessary directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
printf %s "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>

" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ directory to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Configure Nginx
nginx_config="
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$hostname;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://github.com/rodgersxy/;
    }

    error_page 404 /404.html;
    location /404.html {
        root /var/www/html;
        internal;
    }
}"
echo "$nginx_config" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart
