#
# Docker container for Cuckoo malware sandbox
#

FROM ubuntu:15.04
MAINTAINER Jacob Gajek <jacob.gajek@esentire.com>

WORKDIR /tmp/docker/build

COPY packages.txt /tmp/
COPY requirements.txt /tmp/

# Install the dependencies
RUN apt-get update &&\
 xargs apt-get install -y < /tmp/packages.txt &&\
 rm /tmp/packages.txt &&\
 apt-get clean

# Install Python requirements
RUN pip install -r /tmp/requirements.txt &&\
 rm /tmp/requirements.txt

# Build and install yara
RUN wget https://github.com/plusvic/yara/archive/v3.4.0.tar.gz &&\
 tar xzf v3.4.0.tar.gz &&\
 cd yara-3.4.0 &&\
 ./bootstrap.sh &&\
 ./configure --with-crypto --enable-cuckoo --enable-magic &&\
 make &&\
 make install &&\
 cd yara-python &&\
 python setup.py build &&\
 python setup.py install &&\
 ldconfig &&\
 rm -rf /tmp/docker/build/*

# Build and install ssdeep
RUN wget http://downloads.sourceforge.net/project/ssdeep/ssdeep-2.13/ssdeep-2.13.tar.gz &&\
 tar xzf ssdeep-2.13.tar.gz &&\
 cd ssdeep-2.13 &&\
 ./bootstrap &&\
 ./configure &&\
 make &&\
 make install &&\
 git clone https://github.com/kbandla/pydeep.git &&\
 cd pydeep &&\
 python setup.py build &&\
 python setup.py install &&\
 ldconfig &&\
 rm -rf /tmp/docker/build/*

# Build and install volatility
RUN wget https://github.com/volatilityfoundation/volatility/archive/2.4.1.tar.gz &&\
 tar xzf 2.4.1.tar.gz &&\
 cd volatility-2.4.1 &&\
 python setup.py build &&\
 python setup.py install &&\
 ldconfig &&\
 rm -rf /tmp/docker/build/*

# Build and install libvirt with ESX driver
RUN wget http://libvirt.org/sources/libvirt-1.2.19.tar.gz &&\
 tar xzf libvirt-1.2.19.tar.gz &&\
 cd libvirt-1.2.19 &&\
 ./configure --with-esx &&\
 make &&\
 make install &&\
 git clone git://libvirt.org/libvirt-python.git &&\
 cd libvirt-python &&\
 git checkout -b v1.2.19 tags/v1.2.19 &&\
 python setup.py build &&\
 python setup.py install &&\
 ldconfig &&\
 rm -rf /tmp/docker/build/*

# Replace the default PostgreSQL configuration files
COPY postgres/pg_hba.conf       /etc/postgresql/9.4/main/pg_hba.conf
COPY postgres/postgresql.conf   /etc/postgresql/9.4/main/postgresql.conf

# Replace nginx default site
COPY nginx/nginx.conf           /etc/nginx/sites-enabled/default

# Run this portion of the build as the postgres user
USER postgres

# Start the PostgreSQL service and create the Cuckoo database
RUN service postgresql start &&\
 psql -c "CREATE USER sandbox PASSWORD 'cuck00!'" &&\
 psql -c "CREATE DATABASE cuckoo WITH TEMPLATE template0 ENCODING 'UTF-8'" &&\
 psql -c "GRANT ALL ON DATABASE cuckoo TO sandbox"

# Run this portion of the build as root
USER root

# Create directory for Cuckoo
RUN useradd sandbox &&\
 usermod -G sandbox www-data &&\
 mkdir /opt/sandbox &&\
 chown sandbox:www-data /opt/sandbox

# Run this portion of the build as the sandbox user
USER sandbox

# Copy over configuration files
COPY supervisor/supervisord.conf  /opt/sandbox/supervisor/supervisord.conf
COPY uwsgi/django.ini             /opt/sandbox/uwsgi/django.ini
COPY uwsgi/api.ini                /opt/sandbox/uwsgi/api.ini
COPY startup.sh                   /opt/sandbox/startup.sh

# Clone Cuckoo from Github repo
RUN cd /opt/sandbox &&\
 git clone https://github.com/brad-accuvant/cuckoo-modified.git

# Install community modules
RUN python /opt/sandbox/cuckoo-modified/utils/community.py -a -f

# Run this portion of the build as root
USER root

# Permit capture capability for non-root users
RUN chmod u+s `which tcpdump`

# Add volumes to allow persistent data storage
# The Cuckoo configuration (conf/ subdirectory) varies for each deployment and needs to be imported from another container
VOLUME ["/opt/sandbox/cuckoo-modified/storage", "/var/lib/mongodb", "/var/lib/postgresql"]

# Expose the Cuckoo network ports
EXPOSE 80 2042 5432 8090

# Set the entry point
ENTRYPOINT ["/opt/sandbox/startup.sh"]
