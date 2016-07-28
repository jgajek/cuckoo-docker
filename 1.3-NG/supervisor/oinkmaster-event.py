# Oinkmaster event listener
import sys
from subprocess import call

CONFFILE = "/etc/oinkmaster.conf"
RULEPATH = "/etc/suricata/rules"
DUMPFILE = "/var/log/oinkmaster"

def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def update_rules(outfile):
    out = open(outfile, "w")
    call(["oinkmaster", "-C", CONFFILE, "-o", RULEPATH],
         stdout=out, stderr=out)
    out.close()

def main():
    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line
        line = sys.stdin.readline()

        # read event payload
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))

        # invoke oinkmaster
        update_rules(DUMPFILE)

        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')

if __name__ == '__main__':
    main()
