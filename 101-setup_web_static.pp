# Nginx configuration file content
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
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
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Ensure Nginx is installed and configured
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

# Create necessary directories and files
file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  notify  => Service['nginx'],
}

# Remove the conflicting /data/ declaration

# Ensure web server directories are created
file { '/var/www':
  ensure  => 'directory',
}

file { '/var/www/html':
  ensure  => 'directory',
}

# Create index.html and 404.html for your web server
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n",
}

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
}

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
}

# Enable the Nginx site and restart Nginx
file { '/etc/nginx/sites-enabled/default':
  ensure  => 'link',
  target  => '/etc/nginx/sites-available/default',
  notify  => Service['nginx'],  # Ensure Nginx restarts when the site is enabled
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
}
