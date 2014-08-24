import math
from shapely.geometry import Polygon as Poly
from shapely.geometry import Point as Pt
from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString


def distance(p1, p2):
    return ((float(p1[0])-float(p2[0]))**2 + (float(p1[1])-float(p2[1]))**2)**.5

def reduce_angle(a):
    '''forces angle between 0 and 360'''
    return a%360

def swap_angle(a):
    return (180-a)%360

def get_angle(p1, p2, style='doe'):

    x1, y1 = [float(p) for p in p1]
    x2, y2 = [float(p) for p in p2]

    try:
        atan = math.atan((y2-y1)/(x2-x1)) *180 / 3.14159
    except ZeroDivisionError:
        atan = 90
        
    if x2 >= x1 and y2 >= y1:
        a = 180 - atan
    elif x2 <= x1 and y2 >= y1:
        a = - atan
    elif x2 <= x1 and y2 <= y1:
        a = 360 - atan
    elif x2 >= x1 and y2 <= y1:
        a = 180 - atan
    
    if style == 'doe':
        return a
    else:
        return swap_angle(a)

def get_angle_name(a):
    directions = ['North', 'North West', 'West', 'South West', 'South', 
        'South East', 'East', 'North East', 'North']
    index = int(rount(float(a)/8),0)
    return(directions[index])

def is_ccw(poly):
    c = 0
    total = 0
    for point in poly[:-2]:
        a1 = get_angle(poly[c], poly[c+1])
        a2 = get_angle(poly[c+1], poly[c+2])
        a = (a2 - a1)
        if a > 180:a = a - 360
        if a < - 180:a = a + 360
        total = total + a
        c +=1
    if total > 0:
        return 1
    else:
        return 0

def angle_distance(a, t):
    return min(abs(t-a), abs(t-360-a), abs(a-360-t))

def opposite_angle_distance(a, t):
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

def findProjectedDistance(a, xb, yb, x1, y1):
    d = dist(xb, yb, a, x1, y1)
    h = ((xb-x1)**2 + (yb-y1)**2)**.5
    return (h**2 - d**2)**.5
    
def rere(p):
    '''reverses and transposes polygon vertices'''
    p.reverse() 
    p = [[i[1], i[0]] for i in p]


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
    
    return x2, y2



def eQuest_to_shapely_poly(p):
    return Poly(p.vertices)

def shapely_polygon_to_shapely_lines(polygon):
     n = len(polygon.exterior.coords)
     return [(LineString(
            [polygon.exterior.coords[c],
            polygon.exterior.coords[c+1]])) 
            for c in range(0,n-1)]

def shapely_line_string_angle(ls):
     c1 = ls.coords[0]
     c2 = ls.coords[1]
     return get_angle(c1, c2)

def shapely_to_eQuest_poly(obj):
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
            if not is_ccw(l):
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
        if not is_ccw(l):
            l.reverse()
        m.append(l)

    mNew  = []
    for p in m:
        pNew = []
        for c in range(0,len(p)):
            p1 = p[c]
            p2 = p[(c+1)%len(p)]
            if p1 != p2:
                pNew.append(p[c])
        mNew.append(pNew)

    return mNew

def convert_feet(s):

    if '_' in s:
        f, i = [float(n) for n in s.split('_')]
    else:
        f, i = float(s), 0
    return (f + i/12)


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


    
    
