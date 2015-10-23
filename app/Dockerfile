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

# Permit capture capability for non-root users
RUN setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

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

# Create sandbox user and directory for Cuckoo
RUN useradd -p $(openssl passwd -1 'cuck00!') sandbox &&\
 usermod -G sandbox www-data &&\
 mkdir /home/sandbox &&\
 mkdir /opt/sandbox &&\
 chown sandbox:www-data /opt/sandbox

# Run this portion of the build as the sandbox user
USER sandbox

# Clone Cuckoo from Github repo
RUN cd /opt/sandbox &&\
 git clone https://github.com/brad-accuvant/cuckoo-modified.git

# Install community modules
RUN python /opt/sandbox/cuckoo-modified/utils/community.py -a -f

# Add volumes to allow persistent data storage
# The Cuckoo configuration (conf/ subdirectory) varies for each deployment and needs to be imported from another container
VOLUME ["/opt/sandbox/cuckoo-modified/storage", "/var/lib/mongodb"]

# Expose the Cuckoo network ports
EXPOSE 80 2042

# Run the default command as root
USER root

# Set the default command to run when starting the container
CMD ["/opt/sandbox/conf/startup.sh"]
