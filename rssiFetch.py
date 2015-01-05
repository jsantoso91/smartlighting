import sys
import os
import struct
import binascii
from array import array
from ctypes import (CDLL, get_errno)
from ctypes.util import find_library
from socket import (socket, AF_BLUETOOTH, SOCK_RAW, BTPROTO_HCI, SOL_HCI, HCI_FILTER,)

def fetchRSSI(nSample):
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

	running = True
	btdataCount = [0,0,0,0]
	garbageCount = 0
	RSSI = array('i',[0,0,0,0])
	bt1rssi = array('i',[ ])
	bt2rssi = array('i',[ ])
	bt3rssi = array('i',[ ])
	bt4rssi = array('i',[ ])
	distance = array('f',[0,0,0,0])

	while running:
		try:
                	data = sock.recv(1024)
                	btAddress = str(data[12:6:-1])
               		# print(btAddress)
               		# print(btAddress[4:6])
                	rssi = data[-1]-255
                	if btAddress[4:6] == "c2":
                        	btdataCount[0] = btdataCount[0]+1
                        	RSSI[0] = rssi
                        	bt1rssi.append(RSSI[0])
                	elif btAddress[4:6] == "f2":
                        	btdataCount[1] = btdataCount[1]+1
                        	RSSI[1] = rssi
                        	bt2rssi.append(RSSI[1])
                	elif btAddress[4:6] == "f4":
                        	btdataCount[2] = btdataCount[2]+1
                        	RSSI[2] = rssi
                        	bt3rssi.append(RSSI[2])
                	elif btAddress[4:6] == "d1":
                        	btdataCount[3] = btdataCount[3]+1
                        	RSSI[3] = rssi
                        	bt4rssi.append(RSSI[3])
                	else:
                     		garbageCount = garbageCount+1
                		#print('data1=' + repr(btdataCount[0]) + ' data2=' + repr(btdataCount[1]) + ' data3=' + repr(btdataCount[2]) + ' data4='+repr(btdataCount[3]));
                		#print(RSSI)
                	if btdataCount[0] >= nSample and btdataCount[1] >= nSample and btdataCount[2] >= nSample and btdataCount[3] >= nSample:
                        	bt1rssi = int(sum(bt1rssi)/len(bt1rssi))
                        	bt2rssi = int(sum(bt2rssi)/len(bt2rssi))
                        	bt3rssi = int(sum(bt3rssi)/len(bt3rssi))
                        	bt4rssi = int(sum(bt4rssi)/len(bt4rssi))
                        	running = False
                        	sock.close()
                        	#print(repr(bt1rssi) + repr(bt2rssi) + repr(bt3rssi) + repr(bt4rssi))
                        	#print(repr(btdataCount[0]) + '  ' + repr(btdataCount[1]) + '  ' + repr(btdataCount[2]) + '  ' + repr(btdataCount[3]))
                        	#sys.exit()
                	else:
                        	running = True 
		except KeyboardInterrupt:
			sock.close()
			running = False
			print('exit')
			sys.exit()
	return bt1rssi, bt2rssi, bt3rssi, bt4rssi
