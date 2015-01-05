import math

def findIntersect(x1,y1,r1,x2,y2,r2,Xmax,Ymax,firstbtno,secondbtno):
        d = math.hypot(x2-x1,y2-y1)
        a = (pow(r1,2)-pow(r2,2)+pow(d,2))/(2*d)
        h = pow(r1,2)-pow(a,2)
        xmid = x1+(a*(x2-x1)/d)
        ymid = y1+(a*(y2-y1)/d)                                                         
        X1 = xmid+(h*(y2-y1)/d)                       
        Y1 = ymid-(h*(x2-x1)/d)                       
        X2 = xmid-(h*(y2-y1)/d)                       
        Y2 = ymid+(h*(x2-x1)/d)                       
        if (firstbtno == 1 and secondbtno == 2) or (firstbtno == 3 and secondbtno == 4):
                if X1>Xmax or X1<=0:
                        X = X2
                        Y = Y2
                elif X2>=Xmax or X2<=0:
                        X = X1
                        Y = Y1
                elif (X1<Xmax and X1>0) or (X2<Xmax and X2>0):
                        X = (X1+X2)/2
                        Y = (Y2+Y2)/2
                        print('hello')
        else:
                if Y1>=Ymax or Y1<=0:                         
                        X = X2                                
                        Y = Y2                                
       	        elif Y2>=Ymax or Y2<=0:                       
                        X = X1                                
                        Y = Y1                                
                elif (Y1<Ymax and Y1>0) or (Y2<Ymax and Y2>0):
                        X = (X1+X2)/2                        
                        Y = (Y1+Y2)/2                        
                        print('OOOOPS')
        return X,Y                                    
                                                      
def rssi2Distance(rssi,rssiAtOneMeter,nu):            
        dist = pow(10,(rssi-rssiAtOneMeter)/(-10*nu)) # RSSI = -(10*nu*log10(d)-RSSIatOneMeter)
        return dist                                                                            
