
### ut61e (Python)

This is a Python package helping you to capture and interpret data from
the digital multimeter Uni-T UT61E. You can easily install it via `pip`.

#### Tools which this package provides:

##### `es51922.py` – Interprets the output of the ES51922 chip

This utility interprets data sent by the Cyrustek ES51922 chip
used in the Uni-Trend digital multimeter UT61E.
It reads lines from stdin, tries to interpret them as messages
from the chip and prints basic information on the stdout.
In addition it writes a CSV file with a lot more information
to the working directory.

##### `he2325u_hidapi.py` – Reads from the USB/HID adapter cable using HIDAPI

This tool tries to read from the adapter cable using the HID API
provided by the operating system. It relies on [cython-hidapi][].

The tool is called after the original chip from the USB/HID cables
which was the *Hoitek HE2325U*. Nowadays those cables come with a
newer chip called *WCH CH9325* but the way to get data out of them
didn't change.

This tool prints its output to stdout so that you can directly
pipe it into `es51922.py`.
Works on Linux and Mac OS X (Windows not tested) without root access.
On Linux you may have to [create a udev rule][] in order to get access
to the `/dev/hidrawX` device as a regular user.


##### `he2325u_pyusb.py` – Reads from the USB/HID adapter cable using PyUSB

This tool is very much similar to `he2325u_hidapi.py` as it also
allows to read from the USB/HID adapter cable. It also prints its
output to stdout. It uses PyUSB instead of HIDAPI which in turn uses
direct libusb calls to talk to the adapter. **Needs to be run as root.** 
Works on Linux only.

#### Installation

This Python package is registered on PyPI with the name
[ut61e](https://pypi.python.org/pypi/ut61e).
To install it, simply run

    pip instal ut61e

#### Usage

To read data from the USB/HID adapter cable and interpret
it as Cyrustek ES51922 information, you can do:

    he2325u_hidapi.py | es51922.py

#### Requirements

You need either Python2 or Python3 to run this software.

To analyze output using `es51922.py` you don't need any external modules.

If you want to run `he2325u_hidapi.py`, you need [cython-hidapi][].

If you want to run `he2325u_pyusb.py`, you need [PyUSB][].

#### Software using this Package

I also wrote a web interface for the display of the UT61E.
I put it in the repository [ut61e-web][]
on Github. It relies on the tools from this package.

#### Alternatives

There is also a C++ based software out there which can read and interpret
the data from the digital multimeter. The older version is called
*dmm_ut61e* and the newer version *ut61e-linux-sw*, both of which
you can find in my repository [ut61e_cpp][] on Github.

If you run Windows, you may be better off with
[DMM.exe](http://www-user.tu-chemnitz.de/~heha/hs/UNI-T/),
an open source tool provided by Henrik Haftmann.

#### History

The file es51922.py was originally written by Domas Jokubauskis ([1][])
and was reused in this project. I'm very grateful to his work and
the work of many others spent on analyzing the USB/HID interface and the
protocol, including Steffen Vogel ([2][]) and Henrik Haftmann ([3][]).

#### Licence and Authors

This software is licenced under the LGPL2+

Authors:

* Philipp Klaus (<philipp.l.klaus@web.de>)
* Domas Jokubauskis (<domas@jokubauskis.lt>)

[cython-hidapi]: https://github.com/trezor/cython-hidapi
[PyUSB]: https://github.com/walac/pyusb
[create a udev rule]: https://github.com/signal11/hidapi/blob/master/udev/99-hid.rules
[ut61e-web]: https://github.com/pklaus/ut61e-web/
[ut61e_cpp]: https://github.com/pklaus/ut61e_cpp
[1]: https://bitbucket.org/kuzavas/dmm_es51922/
[2]: http://www.noteblok.net/2009/11/29/uni-trend-ut61e-digital-multimeter/
[3]: http://www-user.tu-chemnitz.de/~heha/bastelecke/Rund%20um%20den%20PC/hid-ser
