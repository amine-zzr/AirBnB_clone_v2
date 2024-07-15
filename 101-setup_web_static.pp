# Redoing the task 0 but by using Puppet
# Update package list and install Nginx
exec { 'apt-update':
  command => '/usr/bin/apt update',
  path    => '/usr/bin/',
  unless  => '/usr/bin/test -e /var/lib/apt/periodic/update-success-stamp',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-update'],
}

# Create necessary directories if they don't exist
file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  require => Package['nginx'],
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n<head>\n</head>\n<body>\n  ALX School\n</body>\n</html>\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  require => [
    File['/data/web_static/releases/test'],
    Package['nginx'],
  ],
}

# Create symbolic link and update ownership
file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => [
    File['/data/web_static/releases/test/index.html'],
    Package['nginx'],
  ],
}

# Configure Nginx to listen on port 80 and return "Hello World!"
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {\n    listen 80 default_server;\n    listen [::]:80 default_server;\n\n    root /var/www/html;\n    index index.html;\n\n    location /hbnb_static {\n        alias /data/web_static/current;\n        index index.html;\n    }\n}\n",
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  require => File['/data/web_static/current'],
  notify  => Service['nginx'],
}

# Restart Nginx to apply changes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
