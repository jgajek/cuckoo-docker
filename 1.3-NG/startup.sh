#!/bin/sh

exec /usr/bin/freshclam

exec /usr/bin/supervisord -c /opt/sandbox/supervisor/supervisord.conf
