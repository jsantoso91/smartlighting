import xlrd
from time import sleep
from array import array
from localization import rssi2Distance, findIntersect
from lookupHueValue import hueValueTableIndex, hueInput
from phue import Bridge
from rssiFetch import fetchRSSI 

file = xlrd.open_workbook('hueLookupTable.xls')
b = Bridge('192.168.1.7')
lights = b.get_light_objects()

distance = array('f',[0,0,0,0])
xIntersect = array('f',[0,0,0,0])
yIntersect = array('f',[0,0,0,0])
nu = 2
rssiAtOneMeter = -74#-70 #the estimote website says -74 but from experiment it's around -86
rssiAtOneMeterForBT1 = -74
rssiAtOneMeterForBT4 = -69
bt1Position = [0,0]          # coordinate is in meter
bt2Position = [0,2.53]  # x = 4.75m, y=4.22m real room measurement, we will go with 16'x16'= 4.88m
bt3Position = [2.16,2.53] # 4.8 m = 16ft
bt4Position = [2.16,0]
bt1bt2intersect = array('f',[0,0])
bt2bt3intersect = array('f',[0,0])
bt3bt4intersect = array('f',[0,0])
bt4bt1intersect = array('f',[0,0])
userPosition = [0,0]
Xmax = 2.16
Ymax = 2.53
roomSizeInFt = 16
running = True
while running:
	try:
		RSSI = fetchRSSI(5)
		distance[0] = rssi2Distance(RSSI[0],rssiAtOneMeterForBT1,nu)
		distance[1] = rssi2Distance(RSSI[1],rssiAtOneMeter,nu)
		distance[2] = rssi2Distance(RSSI[2],rssiAtOneMeter,nu)
		distance[3] = rssi2Distance(RSSI[3],rssiAtOneMeterForBT4,nu)
		print('distance1=' + repr(distance[0]) + 'distance2=' + repr(distance[1]))
		bt1bt2intersect = findIntersect(bt1Position[0],bt1Position[1],distance[0],bt2Position[0],bt2Position[1],distance[1],Xmax,Ymax,1,2)
		bt2bt3intersect = findIntersect(bt2Position[0],bt2Position[1],distance[1],bt3Position[0],bt3Position[1],distance[2],Xmax,Ymax,2,3)
		bt3bt4intersect = findIntersect(bt3Position[0],bt3Position[1],distance[2],bt4Position[0],bt4Position[1],distance[3],Xmax,Ymax,3,4)
		bt4bt1intersect = findIntersect(bt4Position[0],bt4Position[1],distance[3],bt1Position[0],bt1Position[1],distance[0],Xmax,Ymax,4,1)
		print(repr(bt1bt2intersect[0]) + '  ' + repr(bt2bt3intersect[0]) +  '  '  +  repr(bt3bt4intersect[0]) + '  ' + repr(bt4bt1intersect[0]))
		print(repr(bt1bt2intersect[1]) + '  ' + repr(bt2bt3intersect[1]) +  '  '  +  repr(bt3bt4intersect[1]) + '  ' + repr(bt4bt1intersect[1]))
		userPosition[0] = (bt1bt2intersect[0]+bt2bt3intersect[0]+bt3bt4intersect[0]+bt4bt1intersect[0])/4
		userPosition[1] = (bt1bt2intersect[1]+bt2bt3intersect[1]+bt3bt4intersect[1]+bt4bt1intersect[1])/4
		#print(('distance1=' + str(distance[0]) + ' distance2=' + str(distance[1]) + ' distance3=' + str(distance[2]) + ' distance4=' + str(distance[3])) )
		print('X=' + str(userPosition[0]) + ' Y=' + str(userPosition[1]))
		print("\n")
		check = hueValueTableIndex(userPosition[0],userPosition[1],roomSizeInFt)
		print(str(check[0]),str(check[1]))
		if check[0]<8 and check[1]<8:
			state = 'normal'
			desiredLux = 2
		elif check[0]<8 and check[1]>8:
			state = 'sleep'
			desiredLux = 0.5
		elif check[0]>8 and check[1]<8:
			state = 'work'
			desiredLux = 4
		elif check[0]>8 and check[1]>8:
			state = 'entertainment'
			desiredLux = 1
		else:
			state = 'off'
			desiredLux = 0

		sheet = file.sheet_by_name(state)
		data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
		print('state=' + state)
		print('table index=' + str(check[2]))
		data1 = data[check[2]]
		hue = hueInput(data1[0],data1[1],data1[2])
		lights[0].on = True
		lights[1].on = True
		lights[2].on = True
		lights[0].brightness = hue[0]
		lights[1].brightness = hue[1]
		lights[2].brightness = hue[2]
		#lights[0].xy=[userPosition[0]/10,userPosition[1]/10]
		#hueVal = int(userPosition[0]+userPosition[1])*10
		print(hue)
		sleep(2)
	except KeyboardInterrupt:
		sock.close()
		running = False
		print('exit')
		sys.exit()
