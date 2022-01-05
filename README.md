# Description
[Elmo Motion Controls](https://www.elmomc.com/) has  a nice portfolio for hardware, e.g. network servo based drives.

Many companies including [LAB Motion Systems](https://www.labmotionsystems.com/) incorporate Elmo's drives into their solutions.
We came across their DB3.6 controller. RS232 and USB communication protocols are not [very effective](https://www.tango-controls.org/developers/dsc/ds/2388/). 

Elmo provide a .NET library, which is nice but not very compatible with our [Tango Controls](https://www.tango-controls.org) environment run under Linux.
By the moment of the scrip writing I could not find any solution in Python.

The attached the [example script](example/DB_communication.py) written in Python demonstrating the basic communication capability via a UDP.
It creates a UDP server which performes communications with the controller. The proof of principle script can be easily transformed into a multithreading solution.
