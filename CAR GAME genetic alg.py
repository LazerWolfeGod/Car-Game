import pygame,time,random,math,os,copy
import carAIv3 as carAI
pygame.init()

def text_objects(text, font, col):
    textSurface = font.render(text, True, col)
    return textSurface, textSurface.get_rect()

def write(x,y,text,col,size,screen,center):
    largeText = pygame.font.SysFont("impact", size)
    TextSurf, TextRect = text_objects(text, largeText, col)
    if center:
        TextRect.center = (int(x),int(y))
    else:
        TextRect.x = int(x)
        TextRect.y = int(y)
    screen.blit(TextSurf, TextRect)

def typeing(textinput,event):
    text = textinput[0]
    caps = textinput[1]
    item = ''
    remove = False
    esc = False
    enter = False
    if event.type == pygame.KEYDOWN:
        kprs = pygame.key.get_pressed()
        if event.key<1000 and event.key>15:
            if (caps or kprs[pygame.K_LSHIFT]) and (event.key>96 and event.key<121):
                item = chr(event.key-32)
            else:
                item = chr(event.key)
        if kprs[pygame.K_BACKSPACE]:
            item = ''
            remove = True
        if kprs[pygame.K_ESCAPE]:
            esc = True
        if kprs[pygame.K_RETURN]:
            enter = True
        if event.key == 1073741881:
            if caps:
                caps = False
            else:
                caps = True
    if item != '':
        text = text+item
    if remove:
        text = text[:-1]
    textinput[0] = text
    textinput[1] = caps
    return textinput,esc,enter

def drawtypeing(text,typeline,screen,inptype,w,h):
    if typeline>40:
        ntext = text+'|'
    else:
        ntext = text
    pygame.draw.rect(screen,(245,246,247),pygame.Rect(w*0.3,50,w*0.4,140))
    pygame.draw.rect(screen,(225,226,227),pygame.Rect(w*0.3,50,w*0.4,140),4)
    if inptype[0]:
        write(w/2,90,'Save',(0,0,0),50,screen,True)
    else:
        write(w/2,90,'Open',(0,0,0),50,screen,True)
    write(w/2,150,ntext,(0,0,0),50,screen,True)
    #typeline+=1
    if typeline == 80:
        typeline = 0
    return typeline

def linecross(L1,L2):
    #print(L1,L2)
##    x1,x2,x3,x4,y1,y2,y3 ,y4 = L1[0][0],L1[1][0],L2[0][0],L2[1][0],L1[0][1],L1[1][1],L2[0][1],L2[1][1]
##    xcross = (x1*(x3*(-2*y1+y2+2*y3-y4)+x4*(2*y1-y2-y3))+x2*(x3*(y1-2*y3+y4)+x4*(y3-y1)))/(y3*(x1-x2)+y4*(x2-x1)+y1*(x4-x3)+y2*(x3-x4))
    a,b,c,d,e,f,g,h = L1[0][0],L1[1][0],L2[0][0],L2[1][0],L1[0][1],L1[1][1],L2[0][1],L2[1][1]
    try:
        xcross = (a*(c*(h-f)+d*(f-g))+b*(c*(e-h)+d*(g-e)))/((g*(b-a)+h*(a-b)+e*(c-d)+f*(d-c)))
        if abs(a-b) < 0.001:
            ycross = (xcross-c)*((g-h)/(c-d))+g
        else:
            ycross = ((e-f)*(xcross-a))/(a-b)+e

        dis = 0.1
        if a<b:
            if xcross<a-dis or xcross>b+dis:
                return False,1
        elif b<a:
            if xcross<b-dis or xcross>a+dis:
                return False,2
        if c<d:
            if xcross<c-dis or xcross>d+dis:
                return False,3
        elif d<c:
            if xcross<d-dis or xcross>c+dis:
                return False,4
        if e<f:
            if ycross<e-dis or ycross>f+dis:
                return False,5
        elif f<e:
            if ycross<f-dis or ycross>e+dis:
                return False,6
        if g<h:
            if ycross<g-dis or ycross>h+dis:
                return False,7
        elif h<g:
            if ycross<h-dis or ycross>g+dis:
                return False,8

        return True,xcross,ycross
    except:
        return False,9

def linecirclecross(L1,L2):
    #print(L1,L2)
    a,b,c,d = -L1[0][0],-L1[1][0],-L1[0][1],-L1[1][1]
    p,q,r = L2[0][0],L2[0][1],L2[1]
    if c-d == 0:
        m = 0
        i = m*a-c
        A = (m**2+1)
        B = 2*(m*i-m*q-p)
    elif a-b == 0:
        m = 1000000000
        i = a
        A = 1
        B = 2*p
    else:
        m = (c-d)/(a-b)
        i = m*a-c
        A = (m**2+1)
        B = 2*(m*i-m*q-p)
    C = (q**2-r**2+p**2-2*i*q+i**2)
    print(B**2-4*A*C,A,B,C)
    if B**2-4*A*C<0:
        return False,2
##    ycross1 = (m*(((-B)+math.sqrt(B**2-4*A*C))/(2*A))+i)
##    ycross2 = (m*(((-B)-math.sqrt(B**2-4*A*C))/(2*A))+i)
    xcross1 = (((-B)+math.sqrt(B**2-4*A*C))/(2*A))
    xcross2 = (((-B)-math.sqrt(B**2-4*A*C))/(2*A))
    ycross1 = (m*xcross1+i)
    ycross2 = (m*xcross2+i)
    print(xcross1,xcross2,ycross1,ycross2)
    dis = 0
    passed = [True,True]
    a,b,c,d = -a,-b,-c,-d
    if a<b:
        if xcross1<a-dis or xcross1>b+dis:
            passed[0] = False
    elif b<a:
        if xcross1<b-dis or xcross1>a+dis:
            passed[0] = False
    if c<d:
        if ycross1<c-dis or ycross1>d+dis:
            passed[0] = False
    elif d<c:
        if ycross1<d-dis or ycross1>c+dis:
            passed[0] = False
    if a<b:
        if xcross2<a-dis or xcross2>b+dis:
            passed[1] = False
    elif b<a:
        if xcross2<b-dis or xcross2>a+dis:
            passed[1] = False
    if c<d:
        if ycross2<c-dis or ycross2>d+dis:
            passed[1] = False
    elif d<c:
        if ycross2<d-dis or ycross2>c+dis:
            passed[1] = False
    if passed[0] == True:
        return True,[xcross1,ycross1]
    if passed[1] == True:
        return True,[xcross2,ycross2]
    return False,0

def pointangles(p):
    if p[0][1]-p[1][1] == 0:
        return math.pi/4
    return math.atan((p[0][0]-p[1][0])/(p[0][1]-p[1][1]))

def point3angles(ap,bp,cp):
    a = math.sqrt((bp[0]-cp[0])**2+(bp[1]-cp[1])**2)
    b = math.sqrt((ap[0]-cp[0])**2+(ap[1]-cp[1])**2)
    c = math.sqrt((bp[0]-ap[0])**2+(bp[1]-ap[1])**2)
    if a*b*c == 0:
        A = 0
    else:
        A = math.acos((b**2+c**2-a**2)/(2*b*c))
    
    return A

def pointtranslate(tpoint,camcords,zoom):
    point = [tpoint[0]-camcords[0],tpoint[1]-camcords[1]]
    try:
        polarangle = math.atan((point[1]-camcords[4])/(point[0]-camcords[3]))
    except:
        if point[1]>camcords[4]: polarangle = math.pi*0.5
        else: polarangle = math.pi*1.5
    if point[0]<camcords[3]: polarangle+=math.pi
    polardis = math.sqrt((point[0]-camcords[3])**2+(point[1]-camcords[4])**2)
    endpoint = [(camcords[3])+(polardis*math.cos(polarangle-camcords[2])*zoom),(camcords[4])+(polardis*math.sin(polarangle-camcords[2])*zoom)]
    return endpoint

def pointtranslatedraw(point,camcords,zoom):
    try:
        polarangle = math.atan((point[1]-camcords[4])/(point[0]-camcords[3]))
    except:
        if point[1]>camcords[4]: polarangle = math.pi*0.5
        else: polarangle = math.pi*1.5
    if point[0]<camcords[3]: polarangle+=math.pi
    polardis = math.sqrt((point[0]-camcords[3])**2+(point[1]-camcords[4])**2)
    endpoint = [(camcords[3])+(polardis*math.cos(polarangle+camcords[2])/zoom),(camcords[4])+(polardis*math.sin(polarangle+camcords[2])/zoom)]
    return endpoint


def polyescape(center,poly):
    dis = 100000
    searchdetail = 4
    usedangles = []
    inc = 1
    while searchdetail!=0:
        for a in range(inc):
            angle = int(360/inc*a)
            if not(angle in usedangles):
                usedangles.append(angle)
                awayline = [center,[(center[0])+(dis*math.cos(angle/180*math.pi)),(center[1])+(dis*math.sin(angle/180*math.pi))]]
                escaped = True
                for b in range(len(poly)):
                    collide = linecross(awayline,[poly[b],poly[b-1]])
                    if collide[0]:
                        escaped = False
                    
                if escaped:
                    return False
        inc*=2
        searchdetail-=1
        angle = 0
    return True
def simplepolycollision(poly,point,center):
    x = point[0]
    y = point[1]
    inside = True
    for a in range(len(poly)):
        if (poly[a-1][0]-poly[a][0]) == 0:
            term = ((poly[a-1][1]-poly[a][1])/(poly[a-1][0]-poly[a][0]))*(y-poly[a-1][1])-poly[a-1][0]
        else: term = poly[a-1][0]
        if (poly[a-1][0]-poly[a][0]) == 0:
            cterm = ((poly[a-1][1]-poly[a][1])/(poly[a-1][0]-poly[a][0]))*(center[1]-poly[a-1][1])-poly[a-1][0]
        else: cterm = poly[a-1][0]
        if center[0]<cterm:
            if x>term:
##                print(a,':',x,'>',term,center[0],'<',cterm)
                inside = False
        else:
            if x<term:
##                print(a,':',x,'<',term,center[0],'>',cterm)
                inside = False
##    print(poly,point,center,inside)
##    print('------------')
    return inside
def distancebetween(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
def perimiterlength(point,corners,origin):
    if point[2] == -1:
        return 10000
    centerTL = corners[0][1]
    width = corners[1][1][0]-corners[0][1][0]
    height = corners[2][1][1]-corners[1][1][1]
    if point[2] == 0:
        perim =  point[0]-centerTL[0]
    elif point[2] == 1:
        perim =  point[1]-centerTL[1]+width
    elif point[2] == 2:
        perim =  -point[0]+centerTL[0]+width*2+height
    elif point[2] == 3:
        perim = -point[1]+centerTL[1]+height*2+width*2
    if origin == 0:
         return perim
    elif origin == 1:
        perim-=width
        return perim%(width*2+height*2)
    elif origin == 2:
        perim-=(width+height)
        return perim%(width*2+height*2)
    else:
        perim-=(width*2+height)
        return perim%(width*2+height*2)
def cornerinclude(seppoly,npoly,corners):
    for c in range(len(corners)):
        if corners[c][0]:
            closest = [0,0]
            minn = 1000000000
            for a in range(len(seppoly)):
                for b in range(2):
                    tperim = perimiterlength(seppoly[a][1][b*-1],corners,c)
                    if minn>tperim:
                        minn = tperim
                        closest = [a,b*-1]
            try:
                seppoly[closest[0]][closest[1]].append([corners[c][1][0],corners[c][1][1],c,minn])
            except:
                pass
    altru = True
    for d in corners:
        if not d[0]:
            altru = False
    if seppoly == []:
        if altru:
            seppoly.append([[],[],[]])
            for e in range(4):
                seppoly[-1][1].append([corners[e][1][0],corners[e][1][1],e])
                #print('error - no edge detected by corner',closest,c,minn,seppoly,corners)
    for a in range(len(seppoly)):
        for b in range(2):
            if seppoly[a][b*2] != []:
                if b == 0:
                    seppoly[a][b*2] = sorted(seppoly[a][b*2],key=lambda x:x[3],reverse = True)
                else:
                    seppoly[a][b*2] = sorted(seppoly[a][b*2],key=lambda x:x[3])
    return seppoly
def polygonlimit(poly,camcords,zoom,tab):
##    cenx = camcords[0]+camcords[3]
##    ceny = camcords[1]+camcords[4]
##    screenangle = math.atan(tab[3]/tab[2])
##    screenlen = math.sqrt((tab[2]/2)**2+(tab[3]/2)**2)
##    screencorners = [[cenx-screenlen*math.cos(screenangle+camcords[2]),ceny-screenlen*math.sin(screenangle+camcords[2])],[cenx+screenlen*math.sin(math.pi/2-screenangle+camcords[2]),ceny-screenlen*math.cos(math.pi/2-screenangle+camcords[2])],[cenx+screenlen*math.cos(screenangle+camcords[2]),ceny+screenlen*math.sin(screenangle+camcords[2])],[cenx-screenlen*math.sin((math.pi/2-screenangle)+camcords[2]),ceny+screenlen*math.cos((math.pi/2-screenangle)+camcords[2])]]
##    screenlines = [[screencorners[0],screencorners[1]],[screencorners[1],screencorners[2]],[screencorners[2],screencorners[3]],[screencorners[3],screencorners[0]]]
## 
    
    screenTL = [camcords[0]+camcords[3]-camcords[3]/zoom,camcords[1]+camcords[4]-camcords[4]/zoom]
    width = tab[2]/zoom
    height = tab[3]/zoom
    screenlines = [[[screenTL[0],screenTL[1]],[screenTL[0]+width,screenTL[1]]],[[screenTL[0]+width,screenTL[1]],[screenTL[0]+width,screenTL[1]+height]],[[screenTL[0]+width,screenTL[1]+height],[screenTL[0],screenTL[1]+height]],[[screenTL[0],screenTL[1]+height],[screenTL[0],screenTL[1]]]]
    screenrect = pygame.Rect(screenTL[0],screenTL[1],width,height)
    pattern = []
    for a in range(len(poly)):
        if poly[a][0]>screenTL[0] and poly[a][0]<screenTL[0]+width and poly[a][1]>screenTL[1] and poly[a][1]<screenTL[1]+height:#simplepolycollision(screencorners,poly[a],[cenx,ceny]):
            pattern.append(True)
        else:
            pattern.append(False)
    npoly = []
    screencross = []
    npattern = []
##    print('-------')
    for b in range(len(pattern)):
        if pattern[b]!=pattern[b-1]:
            for c in range(len(screenlines)):
                crossing = linecross(screenlines[c],[poly[b],poly[b-1]])
##                print(crossing,screenlines[c],[poly[b],poly[b-1]],b,c)
                if crossing[0]:
                    npoly.append([crossing[1],crossing[2],c])
                    npattern.append(True)
                    if pattern[b]:
                        screencross.append([[b,b-1],[crossing[1],crossing[2]],len(npoly)+1,c,True])
                    else:
                        screencross.append([[b,b-1],[crossing[1],crossing[2]],len(npoly)+1,c,False])
        if not(pattern[b] or pattern[b-1]):
            crossnum = 0
            for c in range(len(screenlines)):
                crossing = linecross([poly[b],poly[b-1]],screenlines[c])
                if crossing[0]:  
                    crossnum+=1
                    if crossnum == 1:
                        screencross.append([[b,b-1],[crossing[1],crossing[2]],len(npoly)+1,c])
                    elif crossnum == 2:
                        screencross.append([[b,b-1],[crossing[1],crossing[2]],len(npoly)+1,c])
            if crossnum == 2:
                if distancebetween(poly[b],screencross[-2][1])>distancebetween(poly[b],screencross[-1][1]):
                    screencross[-2].append(True)
                    screencross[-1].append(False)
                else:
                    screencross[-1].append(True)
                    screencross[-2].append(False)
                if screencross[-2][4]:
                    npoly.append([screencross[-2][1][0],screencross[-2][1][1],screencross[-2][3]])
                    npattern.append(True)
                    npoly.append([screencross[-1][1][0],screencross[-1][1][1],screencross[-1][3]])
                    npattern.append(True)
                    screencross[-1][2]+=1
                else:
                    npoly.append([screencross[-1][1][0],screencross[-1][1][1],screencross[-1][3]])
                    npattern.append(True)
                    npoly.append([screencross[-2][1][0],screencross[-2][1][1],screencross[-2][3]])
                    npattern.append(True)
                    screencross[-2][2]+=1
        if pattern[b]:
            npoly.append([poly[b][0],poly[b][1],-1])
        npattern.append(pattern[b])
        
    seppoly = []
    string = 0
    index = 0
    npattern.append(0)
    for a in range(len(npattern)):
        if not npattern[a]:
            if string>0:
                seppoly.append([])
                seppoly[-1].append([])
                seppoly[-1].append([])
                for b in range(string):
                    seppoly[-1][-1].append(npoly[index])
                    index+=1
                seppoly[-1].append([])
            string = 0
        else:
            string+=1
    if npattern[0] and npattern[-2] and len(seppoly)>1:
        seppoly[0][1] = seppoly[-1][1]+seppoly[0][1]
        del seppoly[-1]
    cornerdraw = []
    for d in range(len(screenlines)):
        if polyescape(screenlines[d][0],poly):
            cornerdraw.append([True,screenlines[d][0]])
        else:
            cornerdraw.append([False,screenlines[d][0]])
            
    seppoly = cornerinclude(seppoly,npoly,cornerdraw)
    combine = True
    combinel = []
    lrdata = []
    completeshape = []
    cornersused = []
    if len(seppoly)>1:
        for a in seppoly:
            lrdata.append([])
            lrdata[-1].append([ a[1][-1][2],'edge'])
            lrdata[-1].append([a[1][0][2],'edge'])
            
        for a in range(len(lrdata)):
            cornersused.append([])
            for b in range(len(seppoly[a][0])):
                cornersused[-1].append(seppoly[a][0][b][2])
            for b in range(len(seppoly[a][2])):
                cornersused[-1].append(seppoly[a][2][b][2])
                
            if lrdata[a][0][0] == lrdata[a][1][0] and len(cornersused)>0:
                completeshape.append(False)
            else:
                comp = 0
                for direction in range(-1,3,2):
                    inc = max([direction,0])
                    while (lrdata[a][0][0]+inc)%4 in cornersused[-1]:
                        if (lrdata[a][0][0]+inc+min([direction,0]))%4 == lrdata[a][1][0]:
                            comp = True
                        else:
                            cornersused[-1].remove((lrdata[a][0][0]+inc)%4)
                        inc+=direction
                    if len(cornersused[-1]) == 0 and comp == 0:
                        comp = False
                completeshape.append(comp)


##    print(completeshape,lrdata,cornersused)
##    #print('---------------')
    if len(completeshape)>0 and (sum(completeshape))/len(completeshape):
        combine = False
    if combine: fpoly = [[]]
    else: fpoly = []
    for a in seppoly:
        if not combine: fpoly.append([])
        for b in a:
            for c in b:
                fpoly[-1].append([c[0],c[1]])
    #print('output',fpoly)
    return fpoly
    
    
class CAR:
    def __init__(self,x,y,col,length,width,mass,grip,engine,aero,brakeforce,materials,image,carid,controlkeys):
        self.imageoriginal = pygame.image.load(os.path.abspath(os.getcwd())+'\\'+image).convert_alpha()
        self.imageoriginal.set_colorkey((255,255,255))
        self.controlkeys = controlkeys
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.angle = 0
        self.col = col
        self.carid = carid
        self.prevstate = [x,y,0,0,0]
        self.lightangle = math.atan((self.width/3)/(self.length/2))
        self.cornerangle = math.atan((self.width/2)/(self.length/2))
        self.cornerlength = math.sqrt((self.width/2)**2+(self.length/2)**2)
        self.cornerfind()
        self.debug = False
        self.accelerating = False
        self.braking = False
        self.powerkey = 100
        self.turning = 0
        self.turnvel = 0
        self.velocity = [0.0000001,math.pi*2]
        self.gear = 1
        self.gearratio = [0.5,0.8,1.2,1.5,1.8,2.3]
        self.cameravelocity = [0,0,0]
        self.carcenterdis = [0,0]
        self.markpoint = []
        self.marklines = []
        self.collisiontangent = []
        self.bouncevector = [1,0]
        self.distancelines = []
    
        self.racedata = [False,0,1,[]]
        self.checkpointdata = [self.x,self.y,self.angle,self.velocity[:]]
        self.trackstartdata = [self.x,self.y,self.angle,self.velocity[:]]
        self.readypressed = False
        self.readysequence = -1
        self.datarecorder = [False,[]]

        self.mass = mass
        self.grip = grip
        self.engine = engine
        self.aero = aero
        self.brakeforce = brakeforce
        self.materials = materials
        self.material = materials[0]
        self.materialspin = self.material[1]
        self.materialgrip = self.material[2]
        self.materialdrag = self.material[3]
        self.materialslip = self.material[4]
##        self.x = 9366.59081050297
##        self.y = 4388.038592974806
##        self.angle = 8.893500817331454
##        self.velocity = [7.818608393394042e-40, 12.035093400776278]


        self.maxspeedsim()
        
    def cornerfind(self):        
        self.hitboxpoints = [[self.x-self.cornerlength*math.cos(self.cornerangle+self.angle),self.y-self.cornerlength*math.sin(self.cornerangle+self.angle)],[self.x+self.cornerlength*math.sin(math.pi/2-self.cornerangle+self.angle),self.y-self.cornerlength*math.cos(math.pi/2-self.cornerangle+self.angle)],[self.x+self.cornerlength*math.cos(self.cornerangle+self.angle),self.y+self.cornerlength*math.sin(self.cornerangle+self.angle)],[self.x-self.cornerlength*math.sin((math.pi/2-self.cornerangle)+self.angle),self.y+self.cornerlength*math.cos((math.pi/2-self.cornerangle)+self.angle)]]
    def cornerfinddraw(self,camcords,zoom):        
        self.hitboxpoints = [[self.x-(self.cornerlength*math.cos(self.cornerangle+self.angle-camcords[2]))*zoom,self.y-(self.cornerlength*math.sin(self.cornerangle+self.angle-camcords[2]))*zoom],[self.x+(self.cornerlength*math.sin(math.pi/2-self.cornerangle+self.angle-camcords[2]))*zoom,self.y-(self.cornerlength*math.cos(math.pi/2-self.cornerangle+self.angle-camcords[2]))*zoom],[self.x+(self.cornerlength*math.cos(self.cornerangle+self.angle-camcords[2]))*zoom,self.y+(self.cornerlength*math.sin(self.cornerangle+self.angle-camcords[2]))*zoom],[self.x-(self.cornerlength*math.sin((math.pi/2-self.cornerangle)+self.angle-camcords[2]))*zoom,self.y+(self.cornerlength*math.cos((math.pi/2-self.cornerangle)+self.angle-camcords[2]))*zoom]]

    def draw(self,screen,camcords,zoom,checkpointnum,tab,cars,aicars):

        w = tab[2]
        h = tab[3]
        radius = math.sqrt((w/2)**2+(h/2)**2)
        disloc = [self.x+tab[0]-camcords[0],self.y+tab[1]-camcords[1]]
        for a in range(len(cars)):
            img = pygame.transform.scale(cars[a].imageoriginal,(int(cars[a].length*zoom),int(cars[a].width*zoom)))
            img = pygame.transform.rotate(img,180-(cars[a].angle-camcords[2])/math.pi*180)
            img.set_colorkey((255,255,255))
            point = pointtranslate([cars[a].x,cars[a].y],camcords,zoom)
            if pygame.Rect(tab).colliderect(pygame.Rect(point[0]+tab[0]-img.get_rect().center[0],point[1]+tab[1]-img.get_rect().center[1],img.get_width(),img.get_height())):
                if a == self.carid: disloc = [point[0]+tab[0],point[1]+tab[1]]
                screen.blit(img,[point[0]+tab[0]-img.get_rect().center[0],point[1]+tab[1]-img.get_rect().center[1]])

        self.cornerfinddraw(camcords,zoom)
        if self.debug:
            pygame.draw.line(screen,(255,0,0),disloc,(disloc[0]+40*zoom*math.cos(self.velocity[1]-camcords[2]),disloc[1]+40*zoom*math.sin(self.velocity[1]-camcords[2])),3)
            pygame.draw.line(screen,(0,0,255),disloc,(disloc[0]+5*self.velocity[0]*zoom*math.cos(self.velocity[1]-camcords[2]),disloc[1]+5*self.velocity[0]*zoom*math.sin(self.velocity[1]-camcords[2])),3)
            pygame.draw.line(screen,(0,255,0),disloc,(disloc[0]+5*self.bouncevector[0]*zoom*math.cos(self.bouncevector[1]-camcords[2]),disloc[1]+5*self.bouncevector[0]*zoom*math.sin(self.bouncevector[1]-camcords[2])),3)
            p = []
            for a in self.hitboxpoints:
                p.append(pointtranslate(a,camcords,zoom))

            pygame.draw.polygon(screen,(0,0,255),p,2)
            for a in range(len(self.distancelines)):
                col = (255,255,255)
                lw = 3
                ang = (math.pi+math.pi/self.aidetail)*(a/self.aidetail)-math.pi/2+self.angle
                pygame.draw.line(screen,col,(disloc),(disloc[0]+zoom*(1-self.distancelines[a])*2*radius*math.cos(ang),disloc[1]+zoom*(1-self.distancelines[a])*2*radius*math.sin(ang)),lw)
        if self.datarecorder[0]:
            pygame.draw.circle(screen,(255,0,0),(tab[0]+40,tab[1]+tab[3]/2),20)
        for a in self.markpoint:
            pygame.draw.circle(screen,(0,255,0),(a[0]+tab[0],a[1]+tab[1]),5)
        for a in self.marklines:
            pygame.draw.line(screen,(0,255,0),a[0],a[1],3)
        #hud
        write(10+tab[0],5+tab[1],str(int(self.velocity[0]*1000)/1000),(255,255,255),45,screen,False)
        write(10+tab[0],55+tab[1],str(self.gear),(255,255,255),45,screen,False)
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(10+tab[0],110+tab[1],104,30))
        pygame.draw.rect(screen,(200,150,150),pygame.Rect(12+tab[0],112+tab[1],self.powerkey,26))
        if self.racedata[0]:
            write(10+tab[0],h-100+tab[1],str(round(self.racedata[1]/60,2)),(255,255,255),40,screen,False)
            write(40+tab[0],h-30+tab[1],str(len(self.racedata[3]))+'/'+str(self.racedata[2]),(255,255,255),40,screen,True)
            
    def readyseqfunction(self,screen,w,h,tab,checkpointnum):
        self.readysequence-=1
        if self.readysequence>0:
            rite = str(int((self.readysequence+40)/60))
            if rite == '0':
                rite = 'GO'
            else:
                self.resetcheckpoint(self.trackstartdata)
            if self.readysequence < 21 and not self.racedata[0]:
                self.racedata = [True,0,checkpointnum,[]]
            write(w/2+tab[0],h/2+tab[1],rite,(255,0,0),int(h/3),screen,True)

        
    def applyforce(self,scale,direc):
        C = (math.pi-(self.velocity[1]-direc))
        C = abs(C%(math.pi*2))
        b = scale
        a = self.velocity[0]
        c = math.sqrt(a**2+b**2-2*a*b*math.cos(C))
        try:
            hgushg = (a**2+c**2-b**2)/(2*a*c)
        except:
            print(c,a)
        if (a**2+c**2-b**2)/(2*a*c)>1:
            B = math.acos(1)
        elif (a**2+c**2-b**2)/(2*a*c)<-1:
            B = math.cos(-1)
        else:
            B = math.acos((a**2+c**2-b**2)/(2*a*c))
        self.velocity[0] = c
        if C>math.pi:
            self.velocity[1] += B
        if C<math.pi:
            self.velocity[1] -= B
            
    def setmat(self,mat):
        self.material = mat
        self.materialspin = mat[1]
        self.materialgrip = mat[2]
        self.materialdrag = mat[3]
        self.materialslip = mat[4]
        
    def checkmat(self,mats,ground,screenmat):
        self.setmat(self.pointmat([self.x,self.y],mats,ground,screenmat))
    def pointmat(self,point,mats,ground,screenmat):
        maton = screenmat
        for a in ground:
            if a.material[0]!='wall':
                if a.shape == 'rect':
                    if pygame.Rect(a.x-a.width/2,a.y-a.height/2,a.width,a.height).collidepoint(point[0],point[1]):
                        maton = a.material
                elif a.shape == 'cricle':
                    if math.sqrt((a.x-point[0])**2+(a.y-point[1])**2)<a.radius:
                        maton = a.material
        return maton

    def collidecheck(self,ground):
        self.markpoint = []
        self.marklines = []
        self.collisionpoints = []
        for a in ground:
            if a.material[0] == 'wall':
                if a.shape == 'rect' or a.shape == 'poly':
                    self.collisionpoints = []
                    for c in range(len(a.displaypoly[self.carid])):
                        for rec in range(len(a.displaypoly[self.carid][c])):
                            for ca in range(len(self.hitboxpoints)):
    ##                            self.marklines.append([(a.cornerpoints[rec-1][0],a.cornerpoints[rec-1][1]),(a.cornerpoints[rec][0],a.cornerpoints[rec][1])])
    ##                            self.marklines.append([(self.hitboxpoints[ca-1][0],self.hitboxpoints[ca-1][1]),(self.hitboxpoints[ca][0],self.hitboxpoints[ca][1])])
                                #print(a.displaypoly,rec,self.hitboxpoints,ca)
                                temp = linecross([(a.displaypoly[self.carid][c][rec-1][0],a.displaypoly[self.carid][c][rec-1][1]),(a.displaypoly[self.carid][c][rec][0],a.displaypoly[self.carid][c][rec][1])],[(self.hitboxpoints[ca-1][0],self.hitboxpoints[ca-1][1]),(self.hitboxpoints[ca][0],self.hitboxpoints[ca][1])])
                                if temp[0]!=False:
                                    self.collisionpoints.append([temp[1],temp[2]])
                                    self.markpoint.append([temp[1],temp[2]])
                    if self.collisionpoints!=[]:
                        break
                elif a.shape == 'cricle':
                    self.collisionpoints = []
                    for ca in range(len(self.hitboxpoints)):
                        temp = linecirclecross([(self.hitboxpoints[ca-1][0],self.hitboxpoints[ca-1][1]),(self.hitboxpoints[ca][0],self.hitboxpoints[ca][1])],[(a.x,a.y),a.radius])
                        if temp[0]!=False:
                            self.collisionpoints.append(temp[1])
                            self.markpoint.append(temp[1])
                    if self.collisionpoints!=[]:
                        break
        if len(self.markpoint)>0:
            return True
        return False
    
    def checkpointcollide(self,ground,checkpointnum):
        for a in ground:
            if a.shape == 'checkpoint':
                if self.readysequence>20:
                    self.racedata = [False,self.racedata[1],checkpointnum,[]]
                else:
                    exi = False
                    for rec in range(len(a.cornerpoints)):
                        for ca in range(len(self.hitboxpoints)):
                            temp = linecross([(a.cornerpoints[rec-1][0],a.cornerpoints[rec-1][1]),(a.cornerpoints[rec][0],a.cornerpoints[rec][1])],[(self.hitboxpoints[ca-1][0],self.hitboxpoints[ca-1][1]),(self.hitboxpoints[ca][0],self.hitboxpoints[ca][1])])
                            if temp[0]!=False:
                                exi = True
                                break
                        if exi:break
                    if exi:
                        if (a.material[0] == 'finish' or a.material[0] == 'startfinish') and (self.racedata[0]) and len(self.racedata[3])==self.racedata[2]:
                            if self.racedata[1]/60>0.1: print('car',self.carid,'got time:',self.racedata[1]/60)
                            self.racedata = [False,self.racedata[1],checkpointnum,[]]
                            self.drivingdata[2]+=1
                        elif a.material[0] == 'checkpoint':
                            if not(a.checkpointnum in self.racedata[3]):
                                if self.racedata[1]/60>0.1: print('car',self.carid,'got checkpoint at '+str(a.checkpointnum+1)+':',self.racedata[1]/60)
                                self.racedata[3].append(a.checkpointnum)
                                self.checkpointdata = [self.x,self.y,self.angle,self.velocity[:]]
                                self.drivingdata[2]+=1

    def reaction(self):
        if len(self.collisionpoints)==2:
            print('boom')
            if (self.collisionpoints[0][0]-self.collisionpoints[1][0])==0:
                coltangm = 100000
            else:
                coltangm = (self.collisionpoints[0][1]-self.collisionpoints[1][1])/(self.collisionpoints[0][0]-self.collisionpoints[1][0])
            coltangmid = [(self.collisionpoints[0][0]+self.collisionpoints[1][0])/2,(self.collisionpoints[0][1]+self.collisionpoints[1][1])/2]
            self.collisiontangent = [(self.collisionpoints[0][0],self.collisionpoints[0][1]),(self.collisionpoints[1][0],self.collisionpoints[1][1])]
            self.collisioncomtocol = [[self.x,self.y],coltangmid]
            self.collisiontheta1 = pointangles(self.collisioncomtocol)-pointangles(self.collisiontangent)
            self.collisiontheta2 = pointangles(self.collisioncomtocol)-pointangles([[self.x,self.y],[self.x+self.velocity[0]*math.cos(self.velocity[1]),self.y+self.velocity[0]*math.sin(self.velocity[1])]])
##            print(self.collisiontheta1,self.collisiontheta2)
            tempvel = self.velocity
            self.applyforce(math.sin(self.collisiontheta1)**2*math.cos(self.collisiontheta2)*tempvel[0],pointangles(self.collisioncomtocol)+math.pi)
            self.bouncevector = [math.sin(self.collisiontheta1)**2*math.cos(self.collisiontheta2)*tempvel[0],pointangles(self.collisioncomtocol)+math.pi]
            self.turnvel+=math.cos(self.collisiontheta1)*math.sin(self.collisiontheta1)*math.cos(self.collisiontheta2)*tempvel[0]*0.05
            print(math.sin(self.collisiontheta1)**2*math.cos(self.collisiontheta2)*tempvel[0])
        else:
            self.collisiontangent = []
    def randomparticlespawn(self,particles,wheelmats,wheelcords,particlequantity,a,wheelspawnvolume,velmod,timemod,colmod,colrange):
        loop = random.randint(wheelspawnvolume[a][0],wheelspawnvolume[a][1])
        for b in range(loop):
            if random.random()<particlequantity:
                colran = (random.gauss(colmod,0.1))
                if colran<colrange[0] or colran>colrange[1]:
                    colran = colmod
                col = [wheelmats[a][-1][0]*colran,wheelmats[a][-1][1]*colran,wheelmats[a][-1][2]*colran]
                particles.append(['particle',random.gauss(time.time()+timemod,2.5),[(((self.maxspeeds[self.gear-1])*-0.1)+random.gauss(-self.maxspeeds[self.gear-1]/3,1))*velmod,self.angle+random.gauss(0,0.3)],col,wheelcords[a][:]])

    def particlegen(self,particles,mats,matcols,screen,camcords,particlequantity,tab,movetype):
        wheeldis = self.cornerlength*0.7
        wheelcords = [[self.x-wheeldis*math.cos(self.cornerangle+self.angle),self.y-wheeldis*math.sin(self.cornerangle+self.angle)],[self.x-wheeldis*math.sin((math.pi/2-self.cornerangle)+self.angle),self.y+wheeldis*math.cos((math.pi/2-self.cornerangle)+self.angle)],[self.x+wheeldis*math.sin(math.pi/2-self.cornerangle+self.angle),self.y-wheeldis*math.cos(math.pi/2-self.cornerangle+self.angle)],[self.x+wheeldis*math.cos(self.cornerangle+self.angle),self.y+wheeldis*math.sin(self.cornerangle+self.angle)]]
        oldwheelcords = [[self.prevstate[0]-wheeldis*math.cos(self.cornerangle+self.prevstate[2]),self.prevstate[1]-wheeldis*math.sin(self.cornerangle+self.prevstate[2])],[self.prevstate[0]-wheeldis*math.sin((math.pi/2-self.cornerangle)+self.prevstate[2]),self.prevstate[1]+wheeldis*math.cos((math.pi/2-self.cornerangle)+self.prevstate[2])],[self.prevstate[0]+wheeldis*math.sin(math.pi/2-self.cornerangle+self.prevstate[2]),self.prevstate[1]-wheeldis*math.cos(math.pi/2-self.cornerangle+self.prevstate[2])],[self.prevstate[0]+wheeldis*math.cos(self.cornerangle+self.prevstate[2]),self.prevstate[1]+wheeldis*math.sin(self.cornerangle+self.prevstate[2])]]
        wheelmats = []
        for a in range(len(wheelcords)):
            try:
                wheelmats.append(mats[matcols.index(screen.get_at((int(wheelcords[a][0]+tab[0]-camcords[0]),int(wheelcords[a][1]+tab[1]-camcords[1]))))])
            except:
                wheelmats.append(['road',0.77,0.99,0.995,30,(100,100,100)])
        if not(movetype == 'accelerate' or movetype == 'reverse'):
            for a in range(2):
                if wheelmats[a][0] == 'road':
                    particles.append(['tiremark',time.time()+7+random.random(),[oldwheelcords[a][0],oldwheelcords[a][1]],(0,0,0),wheelcords[a]])
                 
        for a in range(len(wheelmats)):
            if movetype == 'braking': velmod = random.gauss(-0.3,0.3)
            elif movetype == 'reverse': velmod = -1
            else: velmod = 1
            
            if wheelmats[a][0] == 'dirt':
                self.randomparticlespawn(particles,wheelmats,wheelcords,particlequantity,a,[[1,2],[1,2],[0,0],[0,0]],velmod,3,0.7,[0.5,1])
            elif wheelmats[a][0] == 'gravel':
                self.randomparticlespawn(particles,wheelmats,wheelcords,particlequantity,a,[[1,2],[1,2],[0,1],[0,1]],velmod,0,0.7,[0.5,1])
            elif wheelmats[a][0] == 'ice':
                self.randomparticlespawn(particles,wheelmats,wheelcords,particlequantity,a,[[1,2],[1,2],[1,2],[1,2]],velmod,0,0.9,[0.8,1])
            elif wheelmats[a][0] == 'grass':
                self.randomparticlespawn(particles,wheelmats,wheelcords,particlequantity,a,[[1,2],[1,2],[0,0],[0,0]],0.5,0,0.9,[0.8,1])
            elif wheelmats[a][0] == 'sand':
                self.randomparticlespawn(particles,wheelmats,wheelcords,particlequantity,a,[[1,2],[1,2],[1,2],[1,2]],0.8,0,0.9,[0.8,1])
                
        return particles
    
    def maxspeedsim(self):
        maxspeeds = [0 for a in range(len(self.gearratio))]
        for g in range(len(self.gearratio)):
            speed = 0
            for l in range(1000):
                speed+=self.engine/self.mass*self.materialgrip*self.gearratio[g]
                airres = (0.99)**((speed*4)/self.aero)
                speed = (speed)*(airres)*self.materialdrag
            maxspeeds[g] = speed
        for b in range(len(maxspeeds)):
            for c in range(b):
                maxspeeds[c]*=(1-(len(maxspeeds)-c)/1000)
        maxspeeds[0]*=0.7
        self.maxspeeds = maxspeeds
        self.dropspeedsp = copy.copy(self.maxspeeds)
        self.dropspeedsp.insert(0,0)
        self.dropspeeds = [0 for a in range(len(self.maxspeeds))]
        for a in range(len(self.dropspeeds)):
            self.dropspeeds[a] = self.dropspeedsp[a]+0.8*(self.dropspeedsp[a+1]-self.dropspeedsp[a])
                
    def move(self,tab,ground,particles,mats,matcols,screen,camcords,particlequantity):
        if self.racedata[0]: self.racedata[1]+=1
        self.prevstate = [self.x,self.y,self.angle,self.x-self.prevstate[0],self.y-self.prevstate[1]]

        angledif = abs(self.angle%(2*math.pi)-self.velocity[1]%(2*math.pi))
        if angledif>math.pi: angledif = 2*math.pi-angledif
        if angledif>math.pi/2: angledif = abs(angledif-math.pi)
        
        vel = self.velocity[0]
        airres = (0.99)**((self.velocity[0]*4)/self.aero)
        friction = (1-(angledif/self.materialslip)/1.8)
        self.velocity[0] = (self.velocity[0])*(airres)*friction*self.materialdrag
        gr = (abs(self.mass*self.velocity[0]-(self.mass*self.velocity[0]*math.cos(self.turning*0.01*abs(self.velocity[0]))))/self.grip+1)
     
        self.x+=self.velocity[0]*math.cos(self.velocity[1])
        self.kickout('self.x',self.velocity[0]*math.cos(self.velocity[1]),ground)
        self.y+=self.velocity[0]*math.sin(self.velocity[1])
        self.kickout('self.y',self.velocity[0]*math.sin(self.velocity[1]),ground)

        self.velocity[1]+=self.turning*0.001*math.sqrt(self.velocity[0]/gr**2)
        self.turnvel+=(self.turning*(self.powerkey/100)*0.001*abs(self.velocity[0])/gr)*((2-self.materialspin)**4)
        self.turnvel*=self.materialspin
        self.angle+=self.turnvel
        self.kickout('self.angle',self.turnvel,ground)
        
        if self.gear<len(self.gearratio) and self.velocity[0]>self.maxspeeds[self.gear-1]:
            self.gear+=1
        elif self.gear>1 and self.velocity[0]<self.dropspeeds[self.gear-2]:
            self.gear-=1
            
##        if gr>1.05:
##            particles = self.particlegen(particles,mats,matcols,screen,camcords,particlequantity,tab,'turning')
##            
        if self.accelerating>0:
            self.applyforce(self.engine/self.mass*self.materialgrip*self.gearratio[self.gear-1]*self.accelerating,self.angle)
            #particles = self.particlegen(particles,mats,matcols,screen,camcords,particlequantity,tab,'accelerate')
        if self.braking>0:
            angledif = abs(self.angle%(2*math.pi)-self.velocity[1]%(2*math.pi))
            if angledif>math.pi: angledif = 2*math.pi-angledif
            if angledif>math.pi/2:
                self.applyforce(self.engine/self.mass*self.materialgrip*self.gearratio[0]*self.braking,self.angle+math.pi)
                angledif = abs(angledif-math.pi)
                #particles = self.particlegen(particles,mats,matcols,screen,camcords,particlequantity,tab,'reverse')
            else:
                self.applyforce(self.brakeforce/self.mass*self.materialgrip*self.braking,self.angle+math.pi) 
                #particles = self.particlegen(particles,mats,matcols,screen,camcords,particlequantity,tab,'braking')
        return particles

    def camerafollow(self,camcords,anglec,dynamiccamera,tab,zoom):
        w = tab[2]
        h = tab[3]
        if dynamiccamera:
            camvio = 0.1
            followvio = 20
            camwobble = 0.5
            aof = (self.angle-self.prevstate[2])*10
            camc2 = [0,0,camcords[2],0,0]
            point = pointtranslate([((self.x-self.prevstate[0])-self.prevstate[3]),((self.y-self.prevstate[1])-self.prevstate[4])],camc2,zoom)
            point = [point[0]*followvio,point[1]*followvio]
            self.carcenterdis = [self.carcenterdis[0]+point[0]+self.cameravelocity[0],self.carcenterdis[1]+point[1]+self.cameravelocity[1]]
            self.cameravelocity[0]-=self.carcenterdis[0]*camvio
            self.cameravelocity[1]-=self.carcenterdis[1]*camvio
            self.cameravelocity[2]-=aof*camvio
            for a in range(len(self.cameravelocity)):
                self.cameravelocity[a]*=camwobble
        else:
            cardis = [0,0]
        if anglec:
            return [self.x-camcords[3],self.y-camcords[4],self.angle+math.pi*0.5+self.cameravelocity[2],w/2+self.cameravelocity[0]+self.carcenterdis[0],h/2+self.cameravelocity[1]+self.carcenterdis[1]]
        else:
            return [self.x-camcords[3],self.y-camcords[4],0,w/2+self.cameravelocity[0]+self.carcenterdis[0],h/2+self.cameravelocity[1]+self.carcenterdis[1]]
    
    def kickout(self,datatype,kicksize,ground):
        self.cornerfind()
        count = 0
        exec('orig = '+datatype)
        if self.collidecheck(ground):
            #self.reaction()
##            if datatype == 'self.angle': self.turnvel*=0.1
##            else:
##                self.velocity[1]+=math.pi
##                self.velocity[0]*=0.1
            while self.collidecheck(ground):
                exec(datatype+'-=kicksize*0.1')
                self.cornerfind()
                count+=1
                if count>100:
                    print(self.velocity)
                    exec(datatype+'=orig')
                    break
##        if count>0:
##            print(count,datatype)
    def resetcheckpoint(self,data):
        self.x = data[0]
        self.y = data[1]
        self.angle = data[2]
        self.velocity = data[3][:]
        self.prevstate = [self.x,self.y,self.angle,0,0]
        self.velocity[0] = 0.00001
        
    def gendrivedata(self,inpu):
        if self.datarecorder[0]:
            output = [((self.accelerating-self.braking)+1)/2,(self.turning+1)/2]
            self.datarecorder[1].append([inpu,output])
        self.drivingdata[0]+=1
        self.drivingdata[1]+=self.velocity[0]
        
            
    def control(self,prsd,ground,tab,camcords,zoom):
        
        if prsd[self.controlkeys[0]]: self.accelerating = 1
        else: self.accelerating = 0
        if prsd[self.controlkeys[1]]: self.braking = 1
        else: self.braking = 0
        if prsd[self.controlkeys[2]] and prsd[self.controlkeys[3]]: self.turning = 0
        elif prsd[self.controlkeys[2]]: self.turning = -1
        elif prsd[self.controlkeys[3]]: self.turning = 1
        else: self.turning = 0
        
        if self.carid == 0:
            if prsd[pygame.K_0]: self.powerkey = 100
            elif prsd[pygame.K_1]: self.powerkey = 10
            elif prsd[pygame.K_2]: self.powerkey = 20
            elif prsd[pygame.K_3]: self.powerkey = 30
            elif prsd[pygame.K_4]: self.powerkey = 40
            elif prsd[pygame.K_5]: self.powerkey = 50
            elif prsd[pygame.K_6]: self.powerkey = 60
            elif prsd[pygame.K_7]: self.powerkey = 70
            elif prsd[pygame.K_8]: self.powerkey = 80
            elif prsd[pygame.K_9]: self.powerkey = 90
        else:
            if prsd[pygame.K_z]: self.powerkey = 10
            elif prsd[pygame.K_x]: self.powerkey = 30
            elif prsd[pygame.K_c]: self.powerkey = 50
            elif prsd[pygame.K_v]: self.powerkey = 75
            elif prsd[pygame.K_b]: self.powerkey = 100

        if prsd[pygame.K_RETURN]: self.resetcheckpoint(self.checkpointdata)
        if prsd[pygame.K_r]: self.readypressed = True
        if self.readypressed and not prsd[pygame.K_r]:
            self.readysequence = 200
            self.readypressed = False
            self.resetcheckpoint(self.trackstartdata)
        

class AIPOWEREDCAR(CAR):
    def __init__(self,x,y,col,length,width,mass,grip,engine,aero,brakeforce,materials,image,carid,controlkeys,tab):
        super().__init__(x,y,col,length,width,mass,grip,engine,aero,brakeforce,materials,image,carid,controlkeys)
        self.aidetail = 23
        #displayx,displayy,displaywidth,displayheight,nodesperlayer,inputnodes,outputnodes,hiddenlayertotal
        self.net = carAI.AI(tab[0]+200,tab[1]+10,200,200,20,self.aidetail+3,2,1,'attempt 10')
        try:
            self.net = self.net.rednet
        except:
            pass
        self.distancelines = [0 for a in range(self.aidetail)]
        self.drivingdata = [0,0,0,0]
        self.datarecorder = [False,[]]
        
    def control(self,prsd,ground,tab,camcords,zoom):    
        self.distancelines = self.calcAIinput(ground,tab,camcords,0.5)
        inwall,inpu = self.distancelines
        self.distancelines = copy.copy(self.distancelines[1])
        if inwall:
            self.resetcheckpoint(self.checkpointdata)
            self.drivingdata[3]+=1
            print('car',self.carid,'hit wall at',self.racedata[1]/60)
        
        inpu.append(self.velocity[0]/self.maxspeeds[len(self.gearratio)-1])
        angleof = ((self.velocity[1]-self.angle)%(math.pi*2))/(math.pi*2)
        if angleof>0.5:
            angleofl = min([((1-angleof)*4),1.0])
            angleofr = 0
        else:
            angleofl = 0
            angleofr = min([((angleof)*4),1.0])
        inpu.append(angleofl)
        inpu.append(angleofr)
        self.gendrivedata(inpu)
        output = self.net.processinput(inpu)
        self.accelerating = max([(output[0]-0.5)*2,0])
        self.braking = min([(output[0]-0.5)*2,0])
        self.turning = (output[1]-0.5)*2+random.gauss(0,0.1)

##        if prsd[pygame.K_0]: self.powerkey = 100
##        elif prsd[pygame.K_1]: self.powerkey = 10
##        elif prsd[pygame.K_2]: self.powerkey = 20
##        elif prsd[pygame.K_3]: self.powerkey = 30
##        elif prsd[pygame.K_4]: self.powerkey = 40
##        elif prsd[pygame.K_5]: self.powerkey = 50
##        elif prsd[pygame.K_6]: self.powerkey = 60
##        elif prsd[pygame.K_7]: self.powerkey = 70
##        elif prsd[pygame.K_8]: self.powerkey = 80
##        elif prsd[pygame.K_9]: self.powerkey = 90
##        if prsd[self.controlkeys[0]]: self.accelerating = 1
##        else: self.accelerating = 0
##        if prsd[self.controlkeys[1]]: self.braking = 1
##        else: self.braking = 0
##        if prsd[self.controlkeys[2]] and prsd[self.controlkeys[3]]: self.turning = 0
##        elif prsd[self.controlkeys[2]]: self.turning = -1*(self.powerkey/100)
##        elif prsd[self.controlkeys[3]]: self.turning = 1*(self.powerkey/100)
##        else: self.turning = 0
        
        
    def calcAIinput(self,ground,tab,camcords,zoom):
##        start = time.time()
        inpu = [0 for a in range(self.aidetail)]
        screenTL = [camcords[0]+camcords[3]-camcords[3]/zoom,camcords[1]+camcords[4]-camcords[4]/zoom]
        width = tab[2]/zoom
        height = tab[3]/zoom
        radius = math.sqrt((width/2)**2+(height/2)**2)
        screenlines = [[[screenTL[0],screenTL[1]],[screenTL[0]+width,screenTL[1]]],[[screenTL[0]+width,screenTL[1]],[screenTL[0]+width,screenTL[1]+height]],[[screenTL[0]+width,screenTL[1]+height],[screenTL[0],screenTL[1]+height]],[[screenTL[0],screenTL[1]+height],[screenTL[0],screenTL[1]]]]
        for ln in range(self.aidetail):
            searchangle = ((math.pi+math.pi/self.aidetail)/self.aidetail)*ln+self.angle-math.pi/2
            predis = radius
            mindissand = predis
            mindiswall = predis
            for a in range(len(ground)):
                if ground[a].material[0] == 'sand' or ground[a].material[0] == 'grass':# or ground[a].material[0] == 'wall':
                    predis = 1000000
                    if ground[a].shape == 'poly' or ground[a].shape == 'rect':
                        if polyescape([self.x,self.y],ground[a].cornerpoints):
                            return True,[0 for a in range(self.aidetail)]
                            predis = 0
                        else:
                            for c in range(len(ground[a].displaypoly[self.carid])):
    ##                                print('-----------')
    ##                                print(ground[a].displaypoly[c])
    ##                                print(ground[a].cornerpoints)
                                for b in range(len(ground[a].displaypoly[self.carid][c])):
                                    point = linecross([[self.x,self.y],[self.x+100000*math.cos(searchangle),self.y+100000*math.sin(searchangle)]],[ground[a].displaypoly[self.carid][c][b-1],ground[a].displaypoly[self.carid][c][b]])
                                    if point[0]:
                                        if math.sqrt((self.x-point[1])**2+(self.y-point[2])**2)<predis: predis = math.sqrt((self.x-point[1])**2+(self.y-point[2])**2)

                    elif ground[a].shape == 'cricle':
                        point = linecirclecross([[self.x,self.y],[self.x+100000*math.cos(searchangle),self.y+100000*math.sin(searchangle)]],[[ground[a].x,ground[a].y],ground[a].radius])
                        if point[0]:
                            if math.sqrt((self.x-point[1][0])**2+(self.y-point[1][1])**2)<predis: predis = math.sqrt((self.x-point[1][0])**2+(self.y-point[1][1])**2)
                    if ground[a].material[0] == 'sand' or ground[a].material[0] == 'grass':
                        if mindissand>predis: mindissand = predis
                    elif ground[a].material[0] == 'wall':
                        if mindiswall>predis: mindiswall = predis
    ##            if mindissand == 1000000:mindissand = 0
    ##            if mindiswall == 1000000:mindiswall = 0
            inpu[ln] = 1-mindissand/radius
            #inpu[ln] = mindiswall
    ##        print('calculate ai lines',time.time()-start)
        return False,inpu
    

class surface:
    def __init__(self,x,y,shape,width,height,material):
        self.x = x
        self.y = y
        self.shape = shape
        self.material = material
        self.height = height
        self.width = width
        self.radius = height
        self.points = height
        
        self.angle = 0
        self.selected = False
        self.cornerpoints = []
        self.displaypoly = [[] for a in range(20)]
        self.setvalues()
    def setvalues(self):
##        try:
            if self.shape == 'poly': self.cornerpoints = self.points
            else:
                try:
                    self.cornerlength = math.sqrt((self.height/2)**2+(self.width/2)**2)
                    self.cornerangle = math.atan((self.height/2)/(self.width/2))
                    self.cornerpoints = [[self.x-self.cornerlength*math.cos(self.cornerangle+self.angle),self.y-self.cornerlength*math.sin(self.cornerangle+self.angle)],[self.x+self.cornerlength*math.sin(math.pi/2-self.cornerangle+self.angle),self.y-self.cornerlength*math.cos(math.pi/2-self.cornerangle+self.angle)],[self.x+self.cornerlength*math.cos(self.cornerangle+self.angle),self.y+self.cornerlength*math.sin(self.cornerangle+self.angle)],[self.x-self.cornerlength*math.sin((math.pi/2-self.cornerangle)+self.angle),self.y+self.cornerlength*math.cos((math.pi/2-self.cornerangle)+self.angle)]]
                except:
                    pass
            if self.shape == 'checkpoint':
                self.checkpointpoly = []
                if self.material[0]!='checkpoint':
                    flip = 1
                    for a in range(int(self.height//self.width)):
                        if a%2 == 0: flip = 1
                        else: flip = -1
                        self.checkpointpoly.append([self.x+self.width/2*flip,self.y+self.width/2*a])
                        self.checkpointpoly.append([self.x+self.width/2*flip,self.y+self.width/2*(a+1)])
                        self.checkpointpoly.insert(0,[self.x-self.width/2*flip,self.y-self.width/2*a])
                        self.checkpointpoly.insert(0,[self.x-self.width/2*flip,self.y-self.width/2*(a+1)])

                    flip*=-1
                    a = int(self.height//self.width)
                    self.checkpointpoly.append([self.x+self.width/2*flip,self.y+self.width/2*a])
                    self.checkpointpoly.append([self.x+self.width/2*flip,self.y+self.width/2*(a+(self.height%self.width)/self.width)])
                    self.checkpointpoly.append([self.x,self.y+self.width/2*(a+(self.height%self.width)/self.width)])
                    self.checkpointpoly.insert(0,[self.x-self.width/2*flip,self.y-self.width/2*a])
                    self.checkpointpoly.insert(0,[self.x-self.width/2*flip,self.y-self.width/2*(a+(self.height%self.width)/self.width)])
                    self.checkpointpoly.insert(0,[self.x,self.y-self.width/2*(a+(self.height%self.width)/self.width)])
                    for a in range(len(self.checkpointpoly)):
                        cam2 = [0,0,-self.angle,0,0]
                        ncord = pointtranslate([self.checkpointpoly[a][0]-self.x,self.checkpointpoly[a][1]-self.y],cam2,1)
                        self.checkpointpoly[a] = [ncord[0]+self.x,ncord[1]+self.y]
##        except:
##            self.cornerlength = 0
##            self.cornerangle = 0
    def polylimit(self,carid,camcords,zoom,tab):
        if self.shape == 'rect' or self.shape == 'poly':
            tpoints = [copy.deepcopy(self.cornerpoints)]
            tpoints = polygonlimit(copy.deepcopy(tpoints)[0],camcords,zoom,tab)
            self.displaypoly[carid] = copy.deepcopy(tpoints)
            return tpoints
    def draw(self,screen,camcords,zoom,tab,polyeff,tabrect,carid):
        if self.shape == 'rect' or self.shape == 'poly':
            tpoints = [copy.deepcopy(self.cornerpoints)]
            if polyeff:
                tpoints = polygonlimit(copy.deepcopy(tpoints)[0],camcords,zoom,tab)
            self.displaypoly[carid] = copy.deepcopy(tpoints)
            for p in tpoints: 
                if len(p) == 0:
                    return
                else:
                    while len(p)<3: p.append(copy.copy(p[-1]))
                for a in range(len(p)):
                    p[a] = pointtranslate(p[a],camcords,zoom)
                if tab[0]+tab[1] != 0:
                    for b in p:
                        b[0]+=tab[0]
                        b[1]+=tab[1]
                pygame.draw.polygon(screen,self.material[-1],p)
        elif self.shape == 'cricle':
            p = pointtranslate([self.x,self.y],camcords,zoom)
            p[0]+=tab[0]
            p[1]+=tab[1]
            dra = False
            nrect = copy.deepcopy(tabrect)
            nrect.x-=self.radius
            nrect.y-=self.radius
            nrect.width+=self.radius*2
            nrect.height+=self.radius*2
            if nrect.collidepoint(p):
                if self.selected: pygame.draw.circle(screen,(0,0,0),p,(self.radius+3)*zoom)
                pygame.draw.circle(screen,self.material[-1],p,self.radius*zoom)

        elif self.shape == 'checkpoint':
            self.setvalues()
            plim = polygonlimit(self.cornerpoints,camcords,zoom,tab)
            plim = copy.copy(plim[0])
            if len(plim)>2:
                p = []
                for a in range(len(plim)):
                    p.append(pointtranslate(plim[a],camcords,zoom))
                for a in range(len(p)):
                    p[a][0]+=tab[0]
                    p[a][1]+=tab[1]
                pygame.draw.polygon(screen,self.material[-1],p)
                if len(self.checkpointpoly)>2:
                    plim = polygonlimit(self.checkpointpoly,camcords,zoom,tab)
                    plim = copy.copy(plim[0])
                    if len(plim)>2:
                        p2 = []
                        for a in range(len(plim)):
                            p2.append(pointtranslate(plim[a],camcords,zoom))
                        for a in range(len(p2)):
                            p2[a][0]+=tab[0]
                            p2[a][1]+=tab[1]
                        pygame.draw.polygon(screen,self.material[-2],p2)

        
def inbetweenangles(an1,an2,anb):
    if an1>an2:
        if anb<an1 and anb>an2:
            return False
        else:
            return True
    else:
        if anb>an1 and anb<an2:
            return True
        else:
            return False


class MAIN:
    def __init__(self,screenw,screenh,cameraangled,efficientpolygons,dynamiccamera,particlequantity,frameskip,playernum,aicarid,aicarnum):
        self.screenw = screenw
        self.screenh = screenh
        self.screen = pygame.display.set_mode((screenw,screenh))
        self.clock = pygame.time.Clock()
        w = screenw
        h = screenh
        screendata = [[[0,0,w,h]],
                      [[0,0,w/2,h],[w/2,0,w/2,h]],
                      [[0,0,w,h/2],[0,h/2,w/2,h/2],[w/2,h/2,w/2,h/2]],
                      [[0,0,w/2,h/2],[w/2,0,w/2,h/2],[0,h/2,w/2,h/2],[w/2,h/2,w/2,h/2]]]
        tablinedata = [[],
                       [[(w/2,0),(w/2,h)]],
                       [[(0,h/2),(w,h/2)],[(w/2,h/2),(w/2,h)]],
                       [[(0,h/2),(w,h/2)],[(w/2,0),(w/2,h)]]]
        keydata = [[pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT],
                   [pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d],
                   [pygame.K_i,pygame.K_k,pygame.K_j,pygame.K_l],
                   [pygame.K_t,pygame.K_g,pygame.K_f,pygame.K_h]]
        imagedata = ['car.png','car2.png','car3.png','car4.png','car5.png','car6.png','car7.png','car8.png','car9.png','car10.png','car11.png']
        self.trainingtracks = ['track 1','track 2','track 3','track 4','training','training 2']
        self.tabs = screendata[playernum-1]
        for a in range(aicarnum): self.tabs.append(self.tabs[0])
        self.tabrects = [pygame.Rect(self.tabs[a][0],self.tabs[a][1],self.tabs[a][2],self.tabs[a][3]) for a in range(len(self.tabs))]
        self.tablines = tablinedata[playernum-1]
        self.camcords = [[0,0,0,self.tabs[a][2]/2,self.tabs[a][3]/2] for a in range(playernum)]
        for a in range(aicarnum): self.camcords.append([0,0,0,self.tabs[0][2]/2,self.tabs[0][3]/2])
        self.editmode = False
        self.cameraangled = cameraangled
        self.efficientpolygons = efficientpolygons
        self.particlequantity = particlequantity
        self.dynamiccamera = dynamiccamera
        self.playernum = playernum
        self.frameskip = frameskip
        self.aicarid = aicarid
        self.aicarnum = aicarnum
        self.drawmat  = 0
        self.drawshape = 0
        self.editclick = False
        self.editclickspace = False
        self.editclickb = False
        self.tempground = 0
        self.textinput = ['',False,0]
        self.saving = False
        self.opening = False
        self.zoom = 1
        #spin grip drag slip
        self.materials = [['road',0.77,0.99,0.995,30,(100,100,100)],['ice',0.96,0.5,1,1000,(207,241,255)],['dirt',0.85,0.7,0.99,70,(108,101,55)],['sand',0.72,0.2,0.95,10,(227,218,119)],['wall',0.77,0.99,0.995,30,(0,0,0)],['grass',0.93,0.7,0.96,10,(42,156,2)],['gravel',0.87,0.9,0.99,200,(160,160,160)]]
        self.checkpointmats = [['start',0.77,0.99,0.995,30,(255,0,0),(0,0,255)],['finish',0.77,0.99,0.995,30,(0,0,0),(255,255,255)],['startfinish',0.77,0.99,0.995,30,(0,0,0),(0,0,255)],['checkpoint',0.77,0.99,0.995,30,(0,0,255),(0,0,255)]]
        self.materialcols = [self.materials[a][-1] for a in range(len(self.materials))]
        self.checkpointnum = 0
        self.gameclock = 0
        self.gen = 0
        self.aicontrolcount = 0
        self.ground = []
        self.particles = []
        self.screenmat = self.materials[0]
        self.ground.append(surface(400,200,'rect',700,300,self.materials[2]))
        self.ground.append(surface(1200,100,'cricle',0,100,self.materials[1]))
        self.cars = []
        #x,y,col,length,width,mass,grip,engine,aero,brakeforce,materials,image
        for a in range(playernum):
            if a in self.aicarid:
                self.cars.append(AIPOWEREDCAR(200,200+a*100,(255,0,0),100,50,1000,1000,500,100,500,self.materials,imagedata[a%(len(imagedata))],a,keydata[a],self.tabs[a]))
            else:   
                self.cars.append(CAR(200,200+a*100,(255,0,0),100,50,1000,1000,500,100,500,self.materials,imagedata[a%4],a,keydata[a]))
        for a in range(aicarnum):
            self.cars.append(AIPOWEREDCAR(200,200+(a+playernum+1)*100,(255,0,0),100,50,1000,1000,500,100,500,self.materials,imagedata[(a+1)%(len(imagedata))],len(self.cars),keydata[2],self.tabs[a]))

        self.prevtimes = []
    def main(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.KEYDOWN and not self.saving and not self.opening:
                    if event.key == pygame.K_ESCAPE:
                        return 0
                    elif event.key == pygame.K_F5:
                        if self.editmode: self.editmode = False
                        else: self.editmode = True
                    elif event.key == pygame.K_F3:
                        for a in self.cars:
                            if a.debug: a.debug = False
                            else: a.debug = True
                    elif event.key == pygame.K_r:
                        for a in self.cars:
                            a.readysequence = 200
                            a.readypressed = False
                            a.resetcheckpoint(a.trackstartdata)
                    elif event.key == pygame.K_BACKSPACE and len(self.ground)>0:
                        del self.ground[-1]
                    elif event.key == pygame.K_n:
                        self.zoom/=1.1
                    elif event.key == pygame.K_m:
                        self.zoom*=1.1
                    elif event.key == pygame.K_t:
                        for a in self.cars:
                            if a.datarecorder[0]:
                                self.datastore(a.datarecorder[1])
                                a.datarecorder = [False,[]]
                            else: a.datarecorder[0] = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3: self.drawshape+=1
                    self.drawshape = (self.drawshape+4)%4
                    if event.button == 4: self.drawmat+=1
                    elif event.button == 5: self.drawmat-=1
                    if self.drawshape!=3:
                        self.drawmat = (self.drawmat+len(self.materials))%len(self.materials)
                    else:
                        self.drawmat = (self.drawmat+len(self.checkpointmats))%len(self.checkpointmats)
                if self.saving:
                    self.textinput,esc,enter = typeing(self.textinput,event)
                    if esc: self.saving = False
                    if enter:
                        self.storeground()
                        self.saving = False
                        self.textinput[0] = ''
                if self.opening:
                    self.textinput,esc,enter = typeing(self.textinput,event)
                    if esc: self.opening = False
                    if enter:
                        if self.loadground(self.textinput[0]):
                            self.opening = False
                            self.textinput[0] = ''
                            
                            
            kprs = pygame.key.get_pressed()
            if kprs[pygame.K_LCTRL] and kprs[pygame.K_s]:
                self.saving = True
                self.opening = False
                self.textinput = ['',False,0]
            if kprs[pygame.K_LCTRL] and kprs[pygame.K_o]:
                self.opening = True
                self.saving = False
                self.textinput = ['',False,0]
                
            self.screen.fill(self.screenmat[5])
            self.aicontrolcount += 1
            if not(self.saving or self.opening):
                if self.aicontrolcount%1 == 0:
                    for a in range(len(self.cars)):
                        self.cars[a].control(pygame.key.get_pressed(),self.ground,self.tabs[a],self.camcords[a],self.zoom)
                
            for a in range(self.frameskip):
                for b in range(self.playernum+self.aicarnum):
                    self.camcords[b] = self.cars[b].camerafollow(self.camcords[b],self.cameraangled,self.dynamiccamera,self.tabs[b],self.zoom)
                    
            for c in range(self.playernum):
                pygame.draw.rect(self.screen,self.screenmat[5],self.tabrects[c])
                for a in self.ground:
                    a.draw(self.screen,self.camcords[c],self.zoom,self.tabs[c],self.efficientpolygons,self.tabrects[c],c)
            for a in self.ground:
                for b in range(self.playernum,self.aicarnum+self.playernum):
                     a.polylimit(b,self.camcords[b],self.zoom,self.tabs[0])
                    
            for a in range(len(self.cars)):
                try:
                    self.cars[a].setmat(self.materials[self.materialcols.index(self.screen.get_at((int(self.camcords[a][3]+self.tabs[a][0]),int(self.camcords[a][4]+self.tabs[a][1]))))])
                except:
                    self.cars[a].setmat(['road',0.77,0.99,0.995,30,(100,100,100)])
                    
            for a in range(self.frameskip):
                for c in range(len(self.cars)):
                    if c<self.playernum: self.particles = self.cars[c].move(self.tabs[c],self.ground,self.particles,self.materials,self.materialcols,self.screen,self.camcords[c],self.particlequantity)
                    else: self.particles = self.cars[c].move(self.tabs[c],self.ground,self.particles,self.materials,self.materialcols,self.screen,self.camcords[0],self.particlequantity)
                    
            for c in range(len(self.tabs)):
                if self.tempground != 0:
                    self.tempground[1].draw(self.screen,self.camcords[c],self.zoom,self.tabs[c],self.efficientpolygons,self.tabrects[c],c)
                    
            for c in range(len(self.cars)):
                self.cars[c].checkpointcollide(self.ground,self.checkpointnum)
                
            for a in range(self.frameskip): self.particlesslide()
            self.particlesdraw()
            
            for a in range(self.playernum):
                self.cars[a].draw(self.screen,self.camcords[a],self.zoom,self.checkpointnum,self.tabs[a],self.cars,self.aicarid)
                if a in self.aicarid:
                    self.cars[a].net.displaynetwork(self.screen,[0,0,0,0])
            for f in range(self.frameskip):
                for a in range(len(self.cars)):
                    self.cars[a].readyseqfunction(self.screen,self.screenw,self.screenh,self.tabs[a],self.checkpointnum)

            for a in self.tablines:
                pygame.draw.line(self.screen,(50,50,50),a[0],a[1],5)
            if self.saving or self.opening:
                self.textinput[2] = drawtypeing(self.textinput[0],self.textinput[2],self.screen,[self.saving,self.opening],self.screenw,self.screenh)
            elif self.editmode:
                self.mapedit()
            write(self.screenw-15,self.screenh-15,str(int(self.clock.get_fps())),(150,150,150),20,self.screen,True)
            pygame.display.flip()
            self.clock.tick(int(60/self.frameskip))
            self.darwinism()
            
    def darwinism(self):
        self.gameclock+=1
        if self.gameclock%(int(60/self.frameskip)*12) == 0:
            self.gen+=1
            top = 1
            changesize = 1
            print('----------------------------- gen number',self.gen,'----------------------------')
##            print([[self.cars[a].drivingdata,self.cars[a].carid] for a in range(len(self.cars))])
            dd = [[self.cars[a].drivingdata[1]/self.cars[a].drivingdata[0]+self.cars[a].drivingdata[2]*10-self.cars[a].drivingdata[3]*7,self.cars[a].carid] for a in range(len(self.cars))]
            dd.sort(key = lambda x : (x[0]),reverse = True)
            print('gen data',dd)
            dd = dd[:top]
            ncars = []
            for a in range(len(dd)):
                ncars.append(self.cars[dd[a][1]])
            nets = []
            for a in range(top):
                for b in ncars[a].net.evolve(int(len(self.cars)/top)-1,changesize):
                    nets.append(b)
            nets.insert(0,copy.deepcopy(self.cars[dd[0][1]].net))
            self.cars.sort(key = lambda x : x.carid)

            self.loadground(self.trainingtracks[random.randint(0,len(self.trainingtracks)-1)])
            
            for n in range(len(nets)):
                self.cars[n].net = nets[n]
            
                self.cars[n].readysequence = 25
                self.cars[n].readypressed = False
                self.cars[n].resetcheckpoint(self.cars[n].trackstartdata)
                self.cars[n].checkpointdata = self.cars[n].trackstartdata[:]
                self.cars[n].drivingdata = [0,0,0,0]
            


    def particlesdraw(self):
        #write(200,50,str(len(self.particles)),(255,255,255),50,self.screen,True)
        for c in range(self.playernum):
            for a in range(len(self.particles),0,-1):
                if self.particles[a-1][0] == 'particle':
                    p = pointtranslate([self.particles[a-1][4][0],self.particles[a-1][4][1]],self.camcords[c],self.zoom)
                    if self.tabrects[c].collidepoint((p[0]+self.tabs[c][0],p[1]+self.tabs[c][1])):
                        pygame.draw.circle(self.screen,self.particles[a-1][3],(p[0]+self.tabs[c][0],p[1]+self.tabs[c][1]),(0.5*abs(time.time()-self.particles[a-1][1]-3.5)+2)*self.zoom)
                else:
                    p1 = pointtranslate([self.particles[a-1][4][0],self.particles[a-1][4][1]],self.camcords[c],self.zoom)
                    p2 = pointtranslate([self.particles[a-1][2][0],self.particles[a-1][2][1]],self.camcords[c],self.zoom)
                    if self.tabrects[c].collidepoint((p1[0]+self.tabs[c][0],p1[1]+self.tabs[c][1])) and self.tabrects[c].collidepoint((p2[0]+self.tabs[c][0],p2[1]+self.tabs[c][1])):
                        pygame.draw.line(self.screen,self.particles[a-1][3],(p1[0]+self.tabs[c][0],p1[1]+self.tabs[c][1]),(p2[0]+self.tabs[c][0],p2[1]+self.tabs[c][1]),int((0.5*abs(time.time()-self.particles[a-1][1]-3.5)+2)*self.zoom))
                if time.time()-self.particles[a-1][1] > 3.5:
                    del self.particles[a-1]
    def particlesslide(self):
        for a in self.particles:
            if a[0] == 'particle':
                a[4][0]+=a[2][0]*math.cos(a[2][1])
                a[4][1]+=a[2][0]*math.sin(a[2][1])
                a[2][0]*=0.95
    def mapedit(self):
        kprs = pygame.key.get_pressed()
        mprs = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        #mpos = copy.copy([mpos[0]+self.camcords[0],mpos[1]+self.camcords[1]])
        mpos = pointtranslatedraw(copy.copy(mpos),self.camcords[0],self.zoom)
        mpos = copy.copy([mpos[0]+self.camcords[0][0],mpos[1]+self.camcords[0][1]])
        if kprs[pygame.K_BACKSPACE]:
            self.tempground = 0
            self.editclick = False
        shapesize = 60
        
        if self.drawshape == 2:
            pygame.draw.circle(self.screen,(0,0,0),(self.screenw-shapesize/2,shapesize/2),shapesize/2)
            pygame.draw.circle(self.screen,self.materials[self.drawmat][5],(self.screenw-shapesize/2,shapesize/2),shapesize/2-4)
            if mprs[0] and self.editclick == False:
                self.tempground = [mpos,surface(mpos[0],mpos[1],'cricle',10,10,self.materials[self.drawmat])]
                self.tempground[1].selected = True
                self.editclick = True
            if mprs[0] and self.editclick:
                 self.tempground[1].radius = math.sqrt((self.tempground[0][0]-mpos[0])**2+(self.tempground[0][1]-mpos[1])**2)
                 self.tempground[1].height = math.sqrt((self.tempground[0][0]-mpos[0])**2+(self.tempground[0][1]-mpos[1])**2)

        elif self.drawshape == 0:
            pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.screenw-shapesize,0,shapesize,shapesize))
            pygame.draw.rect(self.screen,self.materials[self.drawmat][5],pygame.Rect(self.screenw-(shapesize-4),4,shapesize-8,shapesize-8))
            if mprs[0] and self.editclick == False:
                self.tempground = [mpos,surface(mpos[0],mpos[1],'rect',10,10,self.materials[self.drawmat])]
                self.tempground[1].selected = True
                self.editclick = True
            if mprs[0] and self.editclick:
                self.tempground[1].width = abs(self.tempground[0][0]-mpos[0])*2
                self.tempground[1].height = abs(self.tempground[0][1]-mpos[1])*2
                self.tempground[1].setvalues()

        elif self.drawshape == 1:
            pygame.draw.polygon(self.screen,(0,0,0),((self.screenw-(shapesize*3/4),0),(self.screenw-(shapesize*1/4),0),(self.screenw,shapesize/2),(self.screenw-(shapesize*1/4),shapesize),(self.screenw-(shapesize*3/4),shapesize),(self.screenw-shapesize,shapesize/2)))
            pygame.draw.polygon(self.screen,self.materials[self.drawmat][5],((self.screenw-(shapesize*3/4)+2.3,4),(self.screenw-(shapesize*1/4)-2.3,4),(self.screenw-4,shapesize/2),(self.screenw-(shapesize*1/4)-2.3,shapesize-4),(self.screenw-(shapesize*3/4)+2.3,shapesize-4),(self.screenw-shapesize+4,shapesize/2)))
            if mprs[0] and self.editclick == False:
                self.tempground = [mpos,surface(mpos[0],mpos[1],'poly',10,[copy.copy(mpos),copy.copy(mpos)],self.materials[self.drawmat])]
                self.tempground[1].selected = True
                self.editclick = True
            if mprs[0] and self.editclick:
                self.tempground[1].points[-1] = copy.copy(mpos)

            if mprs[0] and self.editclick and not(self.editclickspace )and (kprs[pygame.K_SPACE] or kprs[pygame.K_RETURN]):
                self.tempground[1].points.append(copy.copy(self.tempground[1].points[-1]))
                self.editclickspace = True
            if mprs[0] and self.editclick and not(self.editclickb) and kprs[pygame.K_b]:
                if len(self.tempground[1].points)>2:
                    del self.tempground[1].points[-2]
                self.editclickb = True
            if not(kprs[pygame.K_SPACE] or kprs[pygame.K_RETURN]):
                self.editclickspace = False
            if not(kprs[pygame.K_b]):
                self.editclickb = False
        elif self.drawshape == 3:
            pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.screenw-shapesize,0,shapesize,shapesize),4,10)
            pygame.draw.rect(self.screen,self.checkpointmats[self.drawmat][5],pygame.Rect(self.screenw-(shapesize-4),4,shapesize/2-4,shapesize/2-4))
            pygame.draw.rect(self.screen,self.checkpointmats[self.drawmat][6],pygame.Rect(self.screenw-(shapesize/2),4,shapesize/2-4,shapesize/2-4))
            pygame.draw.rect(self.screen,self.checkpointmats[self.drawmat][6],pygame.Rect(self.screenw-(shapesize-4),shapesize/2,shapesize/2-4,shapesize/2-4))
            pygame.draw.rect(self.screen,self.checkpointmats[self.drawmat][5],pygame.Rect(self.screenw-(shapesize/2),shapesize/2,shapesize/2-4,shapesize/2-4))
            pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.screenw-shapesize,0,shapesize,shapesize),4,10)
            if mprs[0] and self.editclick == False:
                self.tempground = [mpos,surface(mpos[0],mpos[1],'checkpoint',40,20,self.checkpointmats[self.drawmat])]
                self.tempground[1].selected = True
                self.editclick = True
            if mprs[0] and self.editclick:
                try:
                    self.tempground[1].angle = math.atan((self.tempground[1].y-mpos[1])/(self.tempground[1].x-mpos[0]))+math.pi/2
                except:
                    self.tempground[1].angle = math.pi/2
                if mpos[0]<self.tempground[1].x:
                    self.tempground[1].angle+=math.pi
                self.tempground[1].height = math.sqrt((self.tempground[1].y-mpos[1])**2+(self.tempground[1].x-mpos[0])**2)*2
                self.tempground[1].setvalues()

                
        if not (mprs[0]) and self.editclick:
            if self.tempground[1].material[0] == 'checkpoint':
                self.tempground[1].checkpointnum = self.checkpointnum
                self.checkpointnum+=1
            self.tempground[1].selected = False
            self.ground.append(self.tempground[1])
            self.tempground = 0
            self.editclick = False
    def storeground(self):
        path = os.path.abspath(os.getcwd())+'\\'+str(self.textinput[0])+'.txt'
        grounddata = []
        for a in self.ground:
            grounddata.append([a.shape,a.material,a.x,a.y,a.height,a.width,a.angle])
        dstr = str(grounddata)
        with open(path,'w') as f:
            f.write(dstr)
##            f.write('\nFalse')
        return grounddata
        self.grounddata = grounddata
        
    def loadground(self,name):
        print('loading track:',name,end='')
        self.particles = []
        path = os.path.abspath(os.getcwd())+'\\'+str(name)+'.txt'
        try:
            with open(path,'r') as f:
                lin = f.readlines()
                exec('grounddataloading = '+str(lin[0]),globals())
        except:
            print('invalid file name')
            return False
        self.ground = []
        self.checkpointnum = 0
        cpdata = []
        for a in grounddataloading:
            h = a[4]
            self.ground.append(surface(a[2],a[3],a[0],a[5],h,a[1]))
            if a[1][0] == 'checkpoint':
                self.ground[-1].checkpointnum = self.checkpointnum
                self.checkpointnum+=1
                cpdata.append(a)
            if a[1][0] == 'start' or a[1][0] == 'startfinish':
                cpdata.append(a)
            try:
                self.ground[-1].angle = a[6]
            except:
                pass
        cpnum = random.randint(0,len(cpdata)-1)
        facing = random.randint(0,1)*math.pi
        print(' at checkpoint',cpnum)
        a = cpdata[cpnum]
        for c in range(len(self.cars)):
            self.cars[c].trackstartdata = [a[2]+60*math.cos(a[6]),a[3]+60*math.sin(a[6]),a[6]+facing,[0.0000001,a[6]+facing]]
            self.cars[c].checkpointdata = [a[2]+60*math.cos(a[6]),a[3]+60*math.sin(a[6]),a[6]+facing,[0.0000001,a[6]+facing]]
        return True
    def datastore(self,data):
        name = 'car data '
        num = 0
        while 1:
            if num == 10:
                break
            try:
                with open(name+str(num)+'.txt','r'):
                    num+=1
            except:
                break
        with open(name+str(num)+'.txt','w') as f:
            for a in data:
                f.write(str(a))
                f.write('\n')
        
            
        
        



#width,height,cameraangled,efficientpolygons,dynamiccamera,particlequantity,frameskip,playernum,ai car id,aicarnum
main = MAIN(1600,1000,False,True,True,0,3,1,[0],10)
main.main()
pygame.quit()

