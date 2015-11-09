#
# Configuration data volume for Cuckoo malware sandbox
#

FROM ubuntu:15.04
MAINTAINER Jacob Gajek <jacob.gajek@esentire.com>

COPY cuckoo/*.conf  /opt/sandbox/cuckoo-modified/conf/

VOLUME ["/opt/sandbox/cuckoo-modified/conf"]

CMD ["/bin/true"]
