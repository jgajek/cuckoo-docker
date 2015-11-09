#!/bin/sh

# Adjust ownership of mounted volumes
chown -R sandbox:www-data /opt/sandbox

# Execute the supervisor daemon
exec /usr/bin/supervisord -c /opt/sandbox/supervisor/supervisord.conf
