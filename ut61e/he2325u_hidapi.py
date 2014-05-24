#!/usr/bin/env python

"""
Read from a Hoitek HE2325U or WCH CH9325 USB/HID adapter cable
using the HID-API provided by the operating system.
It relies on cython-hidapi: https://github.com/trezor/cython-hidapi
"""

import sys

BPS = 19200

def main():
    """
    Main function: Entry point if running this module from the command line.
    Prints messages to stdout.
    """
    import argparse
    from inspect import cleandoc
    parser = argparse.ArgumentParser(description=cleandoc(__doc__))
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    try:
        try:
            import hidraw as hid
        except ImportError:
            import hid
    except ImportError:
        parser.error("You need to install cython-hidapi first!")
    import logging
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format='%(message)s', level=loglevel)
    
    try:
        logging.info("Enumerating Devices")
        devices = hid.enumerate(0x1a86, 0xe008)
        if len(devices) == 0:
            raise NameError('No device found. Check your USB connection.')
        logging.info("Found {} devices: ".format(len(devices)))
        for dev in devices:
            name = dev['manufacturer_string'] + " " + dev['product_string']
            path = dev['path'].decode('ascii')
            logging.info("* {} [{}]".format(name, path))
        
        logging.info("Opening device")
        h = hid.device()
        try:
            h.open(0x1a86, 0xe008)
        except IOError as ex:
            raise NameError('Cannot open the device. Please check permissions.')
        
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
        logging.debug("Feature Report Sent")
        
        try:
            logging.debug("Start Reading Messages")
            while True:
                #answer = h.read(256)
                answer = h.read(256, timeout_ms=1000)
                if len(answer) < 1: continue
                nbytes = answer[0] & 0x7
                if nbytes > 0:
                    if len(answer) < nbytes+1:
                        raise NameError("More bytes announced then sent")
                    payload = answer[1:nbytes+1]
                    data = [b & ( ~(1<<7) ) for b in payload]
                    data = [chr(b) for b in data]
                    data = ''.join(data)
                    sys.stdout.write(data)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            logging.info("You pressed CTRL-C, stopping...")
        
        logging.debug("Closing device")
        h.close()
    
    except IOError as ex:
        logging.error(ex)
    except Exception as ex:
        logging.error(ex)

if __name__ == "__main__":
    main()
