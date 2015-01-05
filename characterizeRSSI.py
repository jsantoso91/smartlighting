import sys
import os
import struct
import binascii
from time import sleep
from ctypes import (CDLL, get_errno)
from ctypes.util import find_library
from socket import (socket, AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI, SOL_HCI, HCI_FILTER,)

os.system("hciconfig hci0 down")
os.system("hciconfig hci0 up")

if not os.geteuid() == 0:
    sys.exit("script only works as root")

btlib = find_library("bluetooth")
if not btlib:
    raise Exception(
        "Can't find required bluetooth libraries"
        " (need to install bluez)"
    )
bluez = CDLL(btlib, use_errno=True)

dev_id = bluez.hci_get_route(None)

sock = socket(AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI)
sock.bind((dev_id,))

err = bluez.hci_le_set_scan_parameters(sock.fileno(), 0, 0x10, 0x10, 0, 0, 1000);
if err < 0:
    raise Exception("Set scan parameters failed")
    # occurs when scanning is still enabled from previous call

# allows LE advertising events
hci_filter = struct.pack(
    "<IQH", 
    0x00000010, 
    0x4000000000000000, 
    0
)
sock.setsockopt(SOL_HCI, HCI_FILTER, hci_filter)

err = bluez.hci_le_set_scan_enable(
    sock.fileno(),
    1,  # 1 - turn on;  0 - turn off
    0, # 0-filtering disabled, 1-filter out duplicates
    1000  # timeout
)
if err < 0:
    errnum = get_errno()
    raise Exception("{} {}".format(
        errno.errorcode[errnum],
        os.strerror(errnum)
    ))

distanceAway = 1  # distance away from the estimote beacon in meter
with open("RSSI_data" + str(distanceAway) + ".csv","w") as out_file:
	for x in range (1,100):
		data = sock.recv(1024)	
		RSSI = int(binascii.b2a_hex(data[-1]),16)-255
		out_string = ""
		out_string += str(RSSI)
		out_string += "\n"
		out_file.write(out_string)
	sock.close()
	sys.exit()
