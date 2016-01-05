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

# Fetch and install Tor
RUN echo "deb http://deb.torproject.org/torproject.org vivid main" > /etc/apt/sources.list.d/torproject.list &&\
 gpg --keyserver keys.gnupg.net --recv 886DDD89 &&\
 gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add - &&\
 apt-get update &&\
 apt-get install -y tor deb.torproject.org-keyring

# Fetch and install Suricata
RUN add-apt-repository ppa:oisf/suricata-beta &&\
 apt-get update &&\
 apt-get install -y libhtp1 suricata

# Replace the default Suricata configuration files
COPY suricata/suricata          /etc/default/suricata
COPY suricata/suricata.yaml     /etc/suricata/suricata.yaml
COPY suricata/cuckoo.rules      /etc/suricata/rules/cuckoo.rules
COPY oinkmaster/oinkmaster.conf	/etc/oinkmaster.conf

# Replace nginx default site
COPY nginx/nginx.conf           /etc/nginx/sites-enabled/default

# Create directory for Cuckoo
RUN useradd sandbox &&\
 usermod -G sandbox www-data &&\
 mkdir -p /opt/sandbox/suricata &&\
 chown sandbox:www-data /opt/sandbox

# Run this portion of the build as the sandbox user
USER sandbox

# Copy over configuration files
COPY supervisor/supervisord.conf  	/opt/sandbox/supervisor/supervisord.conf
COPY supervisor/oinkmaster-event.py	/opt/sandbox/supervisor/oinkmaster-event.py
COPY uwsgi/django.ini             	/opt/sandbox/uwsgi/django.ini
COPY uwsgi/api.ini                	/opt/sandbox/uwsgi/api.ini
COPY startup.sh                   	/opt/sandbox/startup.sh

# Clone Cuckoo from Github repo
RUN cd /opt/sandbox &&\
 git clone https://github.com/spender-sandbox/cuckoo-modified.git

# Install community modules
RUN python /opt/sandbox/cuckoo-modified/utils/community.py -a -f

# Copy binaries to the analyzer directory
COPY signtool.exe	/opt/sandbox/cuckoo-modified/analyzer/windows/bin/signtool.exe
COPY flashplayer.exe	/opt/sandbox/cuckoo-modified/analyzer/windows/bin/flashplayer.exe

# Clone routetor from Github repo
RUN cd /opt/sandbox &&\
 git clone http://github.com/jgajek/routetor.git

# Run this portion of the build as root
USER root

# Permit capture capability for non-root users
RUN chmod u+s `which tcpdump`

# Expose the Cuckoo network ports
EXPOSE 80 2042 5353 8090 9040

# Set the entry point
ENTRYPOINT ["/opt/sandbox/startup.sh"]
