import math
hueStepSize = 2.34   # 600 lumens divided into 8 bit

def hueValueTableIndex(xCoordinateInM,yCoordinateInM,roomSizeInFt):
        xCoordinateInFt = xCoordinateInM*3.28
        yCoordinateInFt = yCoordinateInM*3.28
        if math.floor(xCoordinateInFt) == 0 and math.floor(yCoordinateInFt) == 0:
                xCoorInFt = 0.00005
                yCoorInFt = 0.00005
        elif math.floor(xCoordinateInFt) == 0 and math.floor(yCoordinateInFt) != 0:
                xCoorInFt = 0.00005
                yCoorInFt = math.floor(yCoordinateInFt)
        elif math.floor(xCoordinateInFt) != 0 and math.floor(yCoordinateInFt) == 0:
                xCoorInFt = math.floor(xCoordinateInFt)
                yCoorInFt = 0.00005
        else:
                xCoorInFt = math.floor(xCoordinateInFt)
                yCoorInFt = math.floor(yCoordinateInFt)
               # print(xCoorInFt)
               # print(yCoorInFt)
        xCheck = divmod(xCoordinateInFt,xCoorInFt)
        yCheck = divmod(xCoordinateInFt,yCoorInFt)
        #print(xCheck)
        #print(yCheck)
        if xCheck[1] >= 0.5 and yCheck[1] >=0.5:
                xCoordinateInFt1 = math.ceil(xCoordinateInFt)
                yCoordinateInFt1 = math.ceil(yCoordinateInFt)
        elif xCheck[1] >= 0.5 and yCheck[1] < 0.5:
                xCoordinateInFt1 = math.ceil(xCoordinateInFt)
                yCoordinateInFt1 = math.floor(yCoordinateInFt)
        elif xCheck[1] < 0.5 and yCheck[1] >= 0.5:
                xCoordinateInFt1 = math.floor(xCoordinateInFt)
                yCoordinateInFt1 = math.ceil(yCoordinateInFt)
        else:
                xCoordinateInFt1 = math.floor(xCoordinateInFt)
                yCoordinateInFt1 = math.floor(yCoordinateInFt)
        tableIndex = (((roomSizeInFt-1)*(yCoordinateInFt1-1))+xCoordinateInFt1)-1
        return xCoordinateInFt1, yCoordinateInFt1, tableIndex

def hueInput(brightnessL1,brightnessL2,brightnessL3):
        brightL1 = divmod(brightnessL1,hueStepSize)
        brightL2 = divmod(brightnessL2,hueStepSize)
        brightL3 = divmod(brightnessL3,hueStepSize)          
        output2L1 = int(brightL1[0]+1)               
        output2L2 = int(brightL2[0]+1)               
        output2L3 = int(brightL3[0]+1)             
        return output2L1, output2L2, output2L3

