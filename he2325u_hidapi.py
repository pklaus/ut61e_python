#!/usr/bin/env python

# uses cython-hidapi: https://github.com/trezor/cython-hidapi
import hid
import time
import sys

BPS = 19200

try:
    print "Enumerating Devices"
    print hid.enumerate(0x1a86, 0xe008)

    print "Opening device"
    h = hid.device()
    h.open(0x1a86, 0xe008)

    buf = [0]*6
    buf[0] = 0x0 # report ID
    buf[1] = BPS & 0xFF
    buf[2] = ( BPS >>  8 ) & 0xFF
    buf[3] = ( BPS >> 16 ) & 0xFF
    buf[4] = ( BPS >> 24 ) & 0xFF
    buf[5] = 0x03 # 3 = enable?

    fr = h.send_feature_report(buf)
    if fr == -1:
        raise NameError("Sending Feature Report Failed")
    print "Feature Report Sent"

    time.sleep(1.0)

    try:
        print "Start Reading Messages"
        while True:
            #d = h.read(256)
            d = h.read(256, timeout_ms=1000)
            if len(d) < 1: continue
            payload = d[0] & 0x07
            if payload > 0:
                if len(d) < 1: raise NameError("More bytes announced then sent")
                data = d[1:payload+1]
                data = [b & ( ~(1<<7) ) for b in data]
                data = [chr(b) for b in data]
                data = ''.join(data)
                sys.stdout.write(data)
                sys.stdout.flush()
    except KeyboardInterrupt:
        print "You pressed CTRL-C, stopping..."

    print "Closing device"
    h.close()

except IOError, ex:
    print ex
except Exception, ex:
    print ex

print "Done"

