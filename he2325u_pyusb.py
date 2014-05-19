#!/usr/bin/env python

# Helpful resources:
# * http://pyusb.sourceforge.net/docs/1.0/tutorial.html
# * https://github.com/walac/pyusb/blob/master/docs/tutorial.rst
# * http://ieee.students.mtu.edu/sites/default/files/USB%20Presentation.pdf
# * http://www.micahcarrick.com/credit-card-reader-pyusb.html
# * log output of `sudo tshark -i usbmon6 -V`

from __future__ import print_function
import usb.core
import usb.util
import sys

idVendor  = 0x1a86
idProduct = 0xe008

def pyus():
    join_int = lambda nums: int(''.join(str(i) for i in nums))


    try:
        dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)

        if dev is None:
            raise ValueError('Device not found')

        if dev.is_kernel_driver_active(0) is True:
            print("We need to detach kernel driver")
            dev.detach_kernel_driver(0)
        dev.set_configuration()

        #print(dev.bLength, dev.bNumConfigurations, dev.bDeviceClass)

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
        #print('packet details',ep.bEndpointAddress , ep.wMaxPacketSize)

        message = [0x00, 0x4b, 0x00, 0x00, 0x03]
        #dev.ctrl_transfer(bmRequestType, bmRequest, wValue, wIndex, payload)
        assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, message)

        try:
            while 1:
                answer = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize,256)
                #answer = answer.tolist()
                nbytes = answer[0] & 0x7
                if nbytes > 0:
                    if len(answer) < nbytes+1: raise NameError("More bytes announced then sent")
                    payload = answer[1:nbytes+1]
                    data = [b & ( ~(1<<7) ) for b in payload]
                    data = [chr(b) for b in data]
                    data = ''.join(data)
                    sys.stdout.write(data)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            #print("You pressed CTRL-C, stopping...")
            pass
    except usb.core.USBError as e:
        print("USB Error occured: ", e)

pyus()
