
def fix_none(s):
    if s.lower() == 'none':
        return None
    else:
        return s
        



def reduceAngle(a):
    return min(abs(360-a%360),a%360)


def sortObjects(list, order):
    pass

def feetToFloat(s):
    spl = s.split('_')
    dist = float(spl[0])
    if len(spl) == 2:
        dist = dist + float(spl[0])/12
    return dist


def shiftlist(l,n):
    l=list(l)
    Shifted=l[n:]+l[:n]
    return Shifted

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def inkscapePathToPolygon(s, scale=1):
    l = s.split()

    polygon = []                                

    # type points
    if l[0] == 'M': 
        for pair in l[1:]:
            if ',' in pair:
                point = pair.split(',')
                p1 = float(point[0])
                p2 = float(point[1])
                s1 = p1 * scale
                s2 = -p2 * scale
                polygon.append([p1, p2])

    # type path
    elif l[0] == 'm':
        current = [0,0]
        for pair in l[1:]:
            if ',' in pair:
                point = pair.split(',')
                p1 = float(point[0])
                p2 = float(point[1])
                s1 = p1 * scale + current[0]
                s2 = -p2 * scale + current[1]
                current = [s1,s2]
                polygon.append(current)
    
    else:
        print 'unknown path type'
    
    return polygon


def uniquify(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def rere(p):
    #print 'Reversing, Transposing the vertices:'
    num = len(p)
    #print num
    vr = []
    c = 0
    for v in p:
        transposed = []
        currentVerticy = p[num-c-1]
        transposed.append(currentVerticy[1])
        transposed.append(currentVerticy[0])
        vr.append(transposed)
        c += 1
    return vr


def angle(x1, y1, x2, y2):
    tan = math.degrees(math.atan((y2-y1)/(x2-x1)))
    if x1 > x2:
        a = 180. + tan
    else:
        a = tan
    return a

def translate(x1, y1, z1, x2, y2, z2, x, y): # translates x,y coordinate system to new vector (for roofs)
    x1 = float(x1)
    y1 = float(y1)
    z1 = float(z1)
    x2 = float(x2)
    y2 = float(y2)
    z2 = float(z2)
    x = float(x)
    y = float(y)
    
    debug('x1: %s' % x1)
    debug('y1: %s' % y1)
    debug('z1: %s' % z1)
    debug('x2: %s' % x2)
    debug('y2: %s' % y2)
    debug('z2: %s' % z2)
    
    debug('x: %s' % x)
    debug('y: %s' % y)
    
    va = angle(x1, y1, x2, y2)               # vector angle
    pa = angle(x1, y1, x, y)                 # point angle
    da = 90 - (va - pa)                      # translated angle

    pd = pointDistance([x1, y1], [x, y])     # point distance
    vd = pointDistance([x1, y1], [x2, y2])   # vector distance

    za = math.degrees(math.atan((z2-z1)/vd)) # translated angle

    xt = math.cos(math.radians(da)) * pd
    yt = math.sin(math.radians(da)) * pd / math.cos(math.radians(za))
    zt = z1 + (yt/vd) * (z2 - z1)
    t = math.degrees(math.atan((z2-z1)/vd))
    a = angle(x1,y1,x2,y2) - 90
    
    return xt, yt, zt, t, swapAngleType(a)
    

def getAngleCart(p1, p2):
    x1 = float(p1[0])
    y1 = float(p1[1])
    x2 = float(p2[0])
    y2 = float(p2[1])

    if (x2-x1)==0:
        if (y2-y1) > 0:
            a1 = 90
        else:
            a1 = 270
    elif (x2-x1) > 0:
        a1 = math.degrees(math.atan((y2-y1)/(x2-x1)))
    else:
        a1 = 180 + math.degrees(math.atan((y2-y1)/(x2-x1)))
    return(a1)

def getAngleSafe(p1, p2): # gets angle safely even when atan approached infinity
    x1 = float(p1[0])
    y1 = float(p1[1])
    x2 = float(p2[0])
    y2 = float(p2[1])

    if abs(x2-x1) > abs(y2-y1):
        baseAngle = math.degrees(math.atan(abs((y2-y1)/(x2-x1))))
    else:
        baseAngle = 90 - math.degrees(math.atan(abs((x2-x1)/(y2-y1))))

    if (x2 > x1):
        if (y2 > y1):
            a = baseAngle
        else:
            a = 360 - baseAngle
    else:
        if (y2 > y1):
            a = 180 - baseAngle
        else:
            a = 180 + baseAngle
    return(a)



def isCcw(poly):
    if isinstance((poly[0][0]), str):
        #print 'string poly', poly
        numPoly = []
        for v in poly:
            numPoly.append([float(v[0]), float(v[1])])
        poly = numPoly
        #print 'num poly', poly
    c = 0
    total = 0
    for point in poly[:-2]:
        #print '%s, %s > %s, %s' % (poly[c], poly[c+1], poly[c+1], poly[c+2])
        a1 = getAngleCart(poly[c], poly[c+1])
        a2 = getAngleCart(poly[c+1], poly[c+2])
        a = (a2 - a1)
        if a > 180:a = a - 360
        if a < - 180:a = a + 360
        total = total + a
        #print '   %s - %s = %s' % (a2, a1, a)
        #print '  ', total
        c +=1
    if total > 0:
        #print '  is ccw'
        return 1
    else:
        #print '  is cw'
        return 0


def eQuestToShapelyPoly(p):
    pnum = []
    for v in p:
        pnum.append([float(v[0]), float(v[1])])
    polyNum = Poly(pnum)
    return polyNum


def shapelyPolygonToShapelyLines(polygon):
    if type(polygon) == Poly:
         l = []
         n = len(polygon.exterior.coords)
         for c in range(0,n-1):
             l.append(LineString([polygon.exterior.coords[c],polygon.exterior.coords[c+1]]))
         return l
    else:
        print 'input to shapelyPolygonToShapelyLines() must be single polygon' 
        return None

def shapelyLineToRoundedVertices(line):
    if type(line) == LineString:
         l = []
         p = line.coords
         l.append([str(round(p[0][0],2)),str(round(p[0][1],2))])
         l.append([str(round(p[1][0],2)),str(round(p[1][1],2))])
         return l
    else:
        print 'input to shapelyLinesToShapelyVertices() must be single line' 
        return None


def shapelyLineStringAngle(ls):
    if type(ls) == LineString:
         c1 = ls.coords[0]
         c2 = ls.coords[1]
         a = getAngleCart(c1, c2)
         return a
    else:
        print 'input to shapelyLineStringAngle() must be LineString' 
        return None


def shapelyToEQuestPoly(obj):
    if type(obj) == MultiPolygon:
        m = []
        for polygon in obj.geoms:
            t = polygon.exterior.coords
            l = []
            for v in t:
                v0 = str(round(v[0],2))
                v1 = str(round(v[1],2))
                l.append([v0, v1])
            l = l[:-1]
            if not isCcw(l):
                l.reverse()
            m.append(l)
        
    elif type(obj) == Poly:
        m = []
        t = obj.exterior.coords
        l = []
        for v in t:
            v0 = str(round(v[0],2))
            v1 = str(round(v[1],2))
            l.append([v0, v1])
        l = l[:-1]
        if not isCcw(l):
            l.reverse()
        m.append(l)

    mNew  = []
    for p in m:
        pNew = []
        for c in range(0,len(p)):
            p1 = p[c]
            p2 = p[(c+1)%len(p)]
            #print c, p1, p2
            if p1 != p2:
                pNew.append(p[c])
        mNew.append(pNew)

    return mNew
    
        
        
    
    
    
        

    
def getSvgRectangles(file):
    colors = []
    f = open(file,'r')
    lines = f.readlines()
    f.close()

    rects = []
    curLineSet=[]
    state = 0
    
    for line in lines:
        if re.search('  \</rect', line):
           state = 0
           rects.append(curLineSet)
           curLineSet=[]
        if re.search('\/\>', line) and state:
           curLineSet.append(line[:-3].strip())
           state = 0
           rects.append(curLineSet)
        if state:
           curLineSet.append(line.strip())
        if re.search('  \<rect', line):
           state = 1
           curLineSet=[]
    
    r = []
    oc = 0
    sc = 0
    ox = 0
    oy = 0
     
    # look for origin and scale
    for rect in rects:
        x, y, h, w = 0,0,0,0
        for line in rect:
            if re.match('x=', line):
                x = float(re.findall('\-?\d+\.*\d*', line)[0])
            if re.match('y=', line):
                y = float(re.findall('\-?\d+\.*\d*', line)[0])
            if re.match('height=', line):
                h = round(float(re.findall('\d+\.*\d*', line)[0]))
            if re.match('width=', line):
                w = round(float(re.findall('\d+\.*\d*', line)[0]))
            if re.search('title', line):
                
                if re.findall('origin', line):
                    oxOrig = x
                    oyOrig = y
                    oc += 1

                s = re.findall('scale\[\d*\w\d*\]', line)
                if s:
                   nums = s[0][6:-1].split('_')
                   if len(nums) == 1:
                       feet = float(nums[0])
                   else:
                       feet = float(nums[0]) + float(nums[1])/12.
                   scale = feet/max(h, w)
                   sc +=1


    if oc == 0:
        print 'no origin found'
    elif oc != 1:
        print 'more than 1 origin found'
    elif sc == 0:
        print 'no scale found'
    elif sc != 1:
        print 'more than 1 scale found'
    else:
        print 'scale', scale
        print 'origin', oxOrig, oyOrig
        
        ox = round(oxOrig * scale,2)
        oy = round(oyOrig * scale,2)
        print 'ox %s (%s)' % (oxOrig, ox)
        print 'oy %s (%s)' % (oyOrig, oy)
        for rect in rects:
            color = None
            x1, y1, h, w, isOrigin, isScale, id = 0,0,0,0,0,0,"[none]"
            for line in rect:
                if re.match('x=', line):
                    x1 = round(float(re.findall('\-?\d+\.*\d*', line)[0])*scale,2)-ox
                if re.match('y=', line):
                    y2 = oy-round(float(re.findall('\-?\d+\.*\d*', line)[0])*scale,2)
                if re.match('height=', line):
                    h = round(float(re.findall('\d+\.*\d*', line)[0])*scale,2)
                if re.match('width=', line):
                    w = round(float(re.findall('\d+\.*\d*', line)[0])*scale,2)

                if 'id="' in line:
                    id = line.split('=')[1][1:-1]
                
                if re.match('style=', line):
                    try:
                        color = re.findall('fill:.......',line)[0][6:]
                        colors.append(color)
                    except:
                        print 'trouble finding color in style line\n   %s' % line 

                if re.search('title', line) and re.search('origin', line):
                    isOrigin = 1
                
                if re.search('title', line) and re.search('scale', line):
                    isScale = 1

            if not isOrigin and not isScale:
                x2 = x1 + w
                y1 = y2 - h
                xc = x1 + w/2.
                yc = y1 + h/2.
                r.append(['[no name]', x1, y1, x2, y2, w, h, xc, yc, color, id])
            
    return r, colors


#def getSvgScale(file):
#    f = open(file,'r')
#    lines = f.readlines()
#    f.close()
#
#    for line in lines:
#        if re.match('     d', line):
#            dLine = re.findall('".*"', line)[0][1:-1]
#            lineLenS = dLine.split(' ')[2]
#            lineLenCoords = lineLenS.split(',')
#            lineLen = ((float(lineLenCoords[0])**2)+(float(lineLenCoords[1])**2))**.5
#        
#        
#        s = re.findall('scale\w\d*\w\d*', line)
#        if s:
#           nums = s[0][6:].split('_')
#           if len(nums) == 1:
#               feet = float(nums[0])
#           else:
#               feet = float(nums[0]) + float(nums[1])/12.
#           
#    scale = feet/lineLen
#    return scale


def swapAngleType(a):
    return (180-a)%360


def fixInput(sTemp, s):
    if sTemp == '':
        return s
    else:
        try:
            return(float(sTemp))
        except:
            return '-'


def angleDistance(a, t):
    return min(abs(t-a), abs(t-360-a), abs(a-360-t))


def pointDistance(p1, p2):
    
    d = ((float(p1[0])-float(p2[0]))**2 + (float(p1[1])-float(p2[1]))**2)**.5
    return d


def oppositeAngleDistance(a, t):
    return abs(180-(abs(a%360-t%360)))

   
def dist(x, y, a, xt, yt):
    if a==90 or a==270:
        d = abs(x-xt)
    else:
        m = math.tan(math.radians(a))
        b = y-(m*x)
        A=m
        B=-1
        C=b        
        d = abs(A*xt + B*yt + C)/math.sqrt(A**2 + B**2)
    return d


def pdis(x1, y1, a, xt, yt, tol):  
    x2 = math.cos(math.radians(a)) + x1
    y2 = math.sin(math.radians(a)) + y1

    t = x2-x1, y2-x1           # Vector ab
    dd = math.sqrt(t[0]**2+t[1]**2)         # Length of ab
    t = t[0]/dd, t[1]/dd               # unit vector of ab
    n = -t[1], t[0]                    # normal unit vector to ab
    ac = xt-x1, yt-y1          # vector ac
    d = math.fabs(ac[0]*n[0]+ac[1]*n[1]) # Projection of ac to n (the minimum distance)
    if (d < tol):
        print '        %s is less than %s' % (d, tol)
        return True
    else:
        print '        %s is more than %s' % (d, tol)
        return False


def rotate(x, y, r):
    x = float(x)
    y = float(y)
    z = (x**2 + y**2)**.5
    
    if x==0:
        if y > 0:
            a1 = 90
        else:
            a1 = 270
    elif x > 0:
        a1 = math.degrees(math.atan(y/x))
    else:
        a1 = 180 + math.degrees(math.atan(y/x))
    
    a2 = (a1 + r)%360
    x2 = math.cos(math.radians(a2)) * z
    y2 = math.sin(math.radians(a2)) * z
    
    #print '[%s, %s]  (%s deg)' % (round(x,2), round(y,2), a1)
    #print 'rotated %s deg' % (r)
    #print '[%s, %s]  (%s deg)' % (round(x2,2), round(y2,2), a2)
    return x2, y2


def printActiveElements(elements):
    c = 0
    activeElements = []
    for element in elements:
        if elements[element].active == 1:
            activeElements.append(element)
    sortedElements = sortQuotedList(list(activeElements))
    for sortedElement in sortedElements:
        c = c + 1
        print '%s - %s' % (c, sortedElement)


def returnActiveElements(elements):
    c = 0
    activeElements = []
    for element in elements:
        if elements[element].active == 1:
            activeElements.append(element)
    sortedElements = sortQuotedList(list(activeElements))
    return sortedElements


def printActivePolygons(polygons):
    c = 0
    activePolygons = []
    for polygon in polygons:
        if polygons[polygon].active == 1:
            activePolygons.append(polygon)
    sortedPolygons = sortQuotedList(list(activePolygons))
    for sortedPolygon in sortedPolygons:
        c = c + 1
        print '%s - %s' % (c, sortedPolygon)


def returnActivePolygons(polygons):
    c = 0
    activePolygons = []
    for polygon in polygons:
        if polygons[polygon].active == 1:
            activePolygons.append(polygon)
    sortedPolygons = sortQuotedList(list(activePolygons))
    return sortedPolygons


def sortQuotedList (quotedList):
    c=0
    for item in quotedList:
        quotedList[c] = item[1:-1]
        c = c + 1
    quotedList.sort()
    c=0
    for item in quotedList:
        quotedList[c] = '"' + item + '"'
        c = c + 1
    return quotedList
  
    
def printChoices(choices):
    c = 0
    for choice in choices:
        
        c = c + 1
        print '%s - %s' % (c, choice)
    print '\n'


def procChoice(nAvail):
    passCheck=0
    
    while passCheck == 0:
        doChoice = raw_input('')
        if doChoice == 'q':
            break
        if doChoice == 'e':
            return('e')
        doChoice = int(doChoice)
        if doChoice > nAvail or doChoice <=0:
            print ('Out of Range - ("q" to quit)')
        else:
            passCheck = 1
    return doChoice

        
def printChoice(cNum, choices):
    c = 0
    for choice in choices:
        c = c + 1
        if c == cNum:
            print 'You Chose: %s - %s\n' % (c, choices[c-1])


def findProjectedDistance(a, xb, yb, x1, y1):
    d = dist(xb, yb, a, x1, y1)
    h = ((xb-x1)**2 + (yb-y1)**2)**.5
    x = (h**2 - d**2)**.5
    
    return x


def returnTrueCoords(o, p, rotate, scale=9):
    # for window fdf import
    if rotate == 'Rotate 270':
        x1 = (o[0] - float(p[3]))/scale
        y1 = (float(p[0]) - o[1])/scale
        x2 = (o[0] - float(p[1]))/scale
        y2 = (float(p[2]) - o[1])/scale
    else:
        print 'I do not recognize the rotate value'
    
    return [[x1, y1], [x2,y2]]


def getAngle(x1, y1, x2, y2):
    if x1 == x2:
        if y2>y1:
            direction = 90
        else:
            direction = 270
        
    elif y1 == y2:
        if x2>x1:
            direction = 180
        else:
            direction = 0
    else:
        atan = math.atan((y2-y1)/(x2-x1)) *180 / 3.14159
        if x2 > x1 and y2 > y1:
            direction = 180 - atan
        
        elif x2 < x1 and y2 > y1:
            direction = - atan
        
        elif x2 < x1 and y2 < y1:
            direction = 360 - atan
                
        
        elif x2 > x1 and y2 < y1:
            direction = 180 - atan

    if direction > 359:
        direction = 0

    return(direction)


def getAngleReal(x1, y1, x2, y2):
    if (x2-x1)==0:
        if (y2-y1) > 0:
            a1 = 90
        else:
            a1 = 270
    elif (x2-x1) > 0:
        a1 = math.degrees(math.atan((y2-y1)/(x2-x1)))
    else:
        a1 = 180 + math.degrees(math.atan((y2-y1)/(x2-x1)))

    return(a1)


def getAngleName(direction):
    if direction > 330:
        dirName = 'North'
    elif direction > 300:
        dirName = 'North West'
    elif direction > 240:
        dirName = 'West'
    elif direction > 210:
        dirName = 'South West'
    elif direction > 150:
        dirName = 'South'
    elif direction > 120:
        dirName = 'South East'
    elif direction > 60:
        dirName = 'East'
    elif direction > 30:
        dirName = 'North East'
    else: 
        dirName = 'North'
    return(dirName)


def getParams(s):
    bracket = s.find('[')
    p = []
    if bracket > 0:
        name = s[0:bracket]
        sFixed = s
        sFixed = sFixed.replace(';',' ')
        sFixed = sFixed.replace(',',' ')
        for pair in sFixed[bracket+1:-1].split():
            p.append(pair.split(':'))
    else:
        name = s
        p = []
    l = [name, p]
    return l
    
    
def rotateActivePolygons():

    print 'Rotating the polygon(s):'
    printActivePolygons(polygons)
    i2 = raw_input('deg/[q]')
    if i2=='' or i2=='q':
        print 'okay, aborting operation'

    else:

        try:
            a = float(i2)
            success = 1
        except:
             print 'oops, not a valid angle amount'

        if success:
            for polygon in polygons:
                if polygons[polygon].active == 1:
                    verticesNew = []
                    for verticy in polygons[polygon].vertices:
                        print verticy
                        (xNew, yNew) = rotate(verticy[0], verticy[1], a)
                        print xNew, yNew
                        verticesNew.append([str(round(xNew,2)), str(round(yNew,2))])
                    print polygons[polygon].vertices
                    polygons[polygon].vertices = verticesNew
                    print polygons[polygon].vertices
