
### ut61e_python

Captures and Interprets Data from your Digital Multimeter Uni-T UT61E using Python.

#### The Tools

* `es51922.py` - Interprets the output of the ES51922 chip.
  Reads lines from stdin.
* `he2325u_hidapi.py` - Reads from the USB/HID adapter cable using HIDAPI.
  **Needs to be run as root.** This tool prints its output to stdout.
* `he2325u_pyusb.py` - Reads from the USB/HID adapter cable using PyUSB.
  **Needs to be run as root.** This tool prints its output to stdout.

#### Usage

To read data from the USB/HID adapter cable and interpret
it as Cyrustek ES51922 information, you can do:

    sudo python2 ./he2325u_pyusb.py | python2 ./es51922.py

#### Licence and Authors

This software is licenced under the LGPL2+

Authors:

* Philipp Klaus (<philipp.l.klaus@web.de>)
* Domas Jokubauskis (<domas@jokubauskis.lt>)

