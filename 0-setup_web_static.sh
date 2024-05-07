#!/usr/bin/env bash
# Update package list and install Nginx
apt update
apt install nginx -y

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link and update ownership
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to listen on port 80 and return "Hello World!"
echo 'server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By $hostname;

        root /var/www/html;
        index index.html;

        location /hbnb_static {
                alias /data/web_static/current;
                index index.html;
        }
}' > /etc/nginx/sites-available/default

#Restart Nginx to apply changes
service nginx restart
