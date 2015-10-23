#!/bin/sh

# Replace nginx default site
cp /opt/sandbox/conf/nginx/nginx.conf /etc/nginx/sites-enabled/default

# Replace Cuckoo configuration
rm /opt/sandbox/cuckoo-modified/conf/*
cp /opt/sandbox/conf/cuckoo/* /opt/sandbox/cuckoo-modified/conf/

# Adjust ownership of mounted volumes
chown -R sandbox:sandbox /opt/sandbox

# Bring up malware network interface
ip address add 192.168.1.6/24 dev eth1
ip link set eth1 up
ip link set eth1 promisc on

# Execute the supervisor daemon
exec /usr/bin/supervisord -c /opt/sandbox/conf/supervisor/supervisord.conf
