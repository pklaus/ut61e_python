#!/usr/bin/env python

"""
Read from a Hoitek HE2325U or WCH CH9325 USB/HID adapter cable
using PyUSB/libusb. You need root access to get this to work.
"""

import sys

idVendor  = 0x1a86
idProduct = 0xe008
interface = 0

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
        import usb.core
        import usb.util
    except ImportError:
        parser.error("You need to install PyUSB first!")
    import logging
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format='%(message)s', level=loglevel)
    
    try:
        logging.info("Looking for the USB/HID Adapter")
        dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
        
        if dev is None:
            raise NameError('Device not found')
        
        lnd = (dev.bLength, dev.bNumConfigurations, dev.bDeviceClass)
        logging.debug("Length: {}, # configurations: {}, device class: {}".format(*lnd))
        
        if dev.is_kernel_driver_active(interface) is True:
            logging.info('Detaching kernel driver')
            dev.detach_kernel_driver(interface)
        dev.set_configuration()
        
        # get an endpoint instance
        cfg = dev.get_active_configuration()
        interface_number = cfg[(0,0)].bInterfaceNumber
        alternate_setting = usb.control.get_interface(dev,interface_number)
        intf = usb.util.find_descriptor(
            cfg, bInterfaceNumber = interface_number,
            bAlternateSetting = alternate_setting
        )
        
        ep = usb.util.find_descriptor(
            intf,
            # match the first IN endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN
        )
        
        assert ep is not None
        em = (ep.bEndpointAddress, ep.wMaxPacketSize)
        logging.debug("Endpoint Address: {}, Max Packet Size: {}".format(*em))
        
        message = [0x00, 0x4b, 0x00, 0x00, 0x03]
        #dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, payload)
        assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, message)
        logging.debug("Feature Report Sent")
        
        try:
            logging.info("Start Reading Messages")
            while True:
                answer = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize, timeout=1000)
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
        
        logging.info("Closing device")
        h.close()
    
    except usb.core.USBError as ex:
        logging.error("USB Error occured: " + str(ex))
    except Exception as ex:
        logging.error(ex)

if __name__ == "__main__":
    main()
