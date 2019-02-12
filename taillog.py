import os
import string
import sys
import time

def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

while True:
	log = tail(open(sys.argv[1],'r'))
	for line in log:
		print line
