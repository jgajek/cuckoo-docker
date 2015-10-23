#
# Configuration container for Cuckoo malware sandbox
#

FROM ubuntu:15.04
MAINTAINER Jacob Gajek <jacob.gajek@esentire.com>

# Copy over configuration files
COPY conf/        /opt/sandbox/conf/
COPY startup.sh   /opt/sandbox/conf/startup.sh

# Add volumes to allow persistent data storage
VOLUME ["/opt/sandbox/conf"]

# Set the default command to run when starting the container
CMD ["/bin/true"]
