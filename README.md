
### ut61e_python

Captures and Interprets Data from your Digital Multimeter Uni-T UT61E using Python.

#### Tools which ut61e_python provides

##### `es51922.py` – Interprets the output of the ES51922 chip

This utility interprets data sent by the Cyrustek ES51922 chip.
It reads lines from stdin, tries to interpret them as messages
from the chip and prints basic information on the stdout.
In addition it writes a CSV file with a lot more information
to the working directory.

##### `he2325u_hidapi.py` – Reads from the USB/HID adapter cable using HIDAPI

This tool tries to read from the adapter cable using the HID API
provided by the operating system. It relies on [cython-hidapi][].

This tool prints its output to stdout so that you can directly
pipe it into `./es51922.py`.
Works on Linux and Mac OS X (Windows not tested) without root access.
On Linux you may have to [create a udev rule][] in order to get access
to the `/dev/hidrawX` device as a regular user.


##### `he2325u_pyusb.py` – Reads from the USB/HID adapter cable using PyUSB

This tool is very much similar to `he2325u_hidapi.py` as it also
allows to read from the USB/HID adapter cable. It also prints its
output to stdout. It uses PyUSB instead of HIDAPI which in turn uses
direct libusb calls to talk to the adapter. **Needs to be run as root.** 
Works on Linux only.

#### Usage

To read data from the USB/HID adapter cable and interpret
it as Cyrustek ES51922 information, you can do:

    ./he2325u_hidapi.py | ./es51922.py

#### Requirements

This software is written in Python, so you obviously need this to run it.
Python2 and Python3 should both work.

To analyze output using `es51922.py` you don't need any other modules.

If you want to run `he2325u_hidapi.py`, you need [cython-hidapi][].

If you want to run `he2325u_pyusb.py`, you need [PyUSB][].

#### Licence and Authors

This software is licenced under the LGPL2+

Authors:

* Philipp Klaus (<philipp.l.klaus@web.de>)
* Domas Jokubauskis (<domas@jokubauskis.lt>)

[cython-hidapi]: https://github.com/trezor/cython-hidapi
[PyUSB]: https://github.com/walac/pyusb
[create a udev rule]: https://github.com/signal11/hidapi/blob/master/udev/99-hid.rules
