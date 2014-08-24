import ref
from collections import OrderedDict




         
     




def makeObjectTable(dict, methods, order, references):
    
    #headings = methods[:]
    headings = []
    dataTypes = []
     
     
    # loop through attributes of all items in dictionary, keep adding headings if they don't exist
    for item in sorted(dict.keys()):
        for attr, value in dict[item].__dict__.iteritems():
            if attr != 'catch':
                if attr not in headings:
                    headings.append(attr)
                    print attr, value, type(value)
                    dataTypes.append(re.findall("\'.*\'", str(type(value)))[0][1:-1])
            else:
                for caught in dict[item].catch:
                    if caught[0] not in headings:
                        headings.append(caught[0])
                        dataTypes.append(re.findall("\'.*\'", str(type(caught[1])))[0][1:-1])

    # append headings with desired methods
    if headings:
        headings = headings + methods[:]
    
    print len(headings)
    print dataTypes
    

    headingsOrdered = []
    dataTypesOrdered = []
    
    # add items only where order defined
    for item in order:
        if item in headings:
            headingsOrdered.append(item)
            dataTypesOrdered.append(dataTypes[headings.index(item)])


    # add remaining items not in defined order
    for item in headings:
        if not item in headingsOrdered:
            headingsOrdered.append(item)
            if item not in methods:
                dataTypesOrdered.append(dataTypes[headings.index(item)])

    l = len(headingsOrdered)

    subHeadingsOrdered = ([0]*l)

    for item in headingsOrdered:
        if item in references:
            subHeadingsOrdered[headingsOrdered.index(item)] = 'reference'
        elif item in methods:
            subHeadingsOrdered[headingsOrdered.index(item)] = 'method'
        else:
            subHeadingsOrdered[headingsOrdered.index(item)] = 'attribute'

    orderedTable = []      
    orderedTable.append(headingsOrdered)
    orderedTable.append(dataTypesOrdered)
    orderedTable.append(subHeadingsOrdered)

    print dataTypesOrdered


    for item in sorted(dict.keys()):
        tempList = ([0]*l)
        for attr, value in dict[item].__dict__.iteritems():
            if attr != 'catch':
                i = headingsOrdered.index(attr)
                tempList[i] = value
                
            else:
                for caught in dict[item].catch:
                    i = headingsOrdered.index(caught[0])
                    tempList[i] = caught[1]
 
        for method in methods:
            result = getattr(dict[item], method)()
            tempList[headingsOrdered.index(method)] = result
        orderedTable.append(tempList)
    
    print 'complete'
    return orderedTable       





    

def debug(s, f='debug.log', d=0, p=0):
    #print s
    s = " "*d + str(s)
    debug = open(f,'a')
    debug.write('%s\n' % s)
    debug.close()
    if p:
        print s





def spaceVerticalOverlap(space1, space2):
    l1 = (spaces[space1].trueZ())
    u1 = l1 + spaces[space1].trueHeight()
    l2 = (spaces[space2].trueZ())
    u2 = l2 + spaces[space2].trueHeight()
    u = min(u1, u2)
    l = max(l1, l2)
    ol = u - l
    return ol



    
    







def verifySpaces(vTol = 1, percent=2.):
    
    completedComparisons = []
    promblemSpaces = []
    total = len(spaces)
    c = 0
    for space in spaces:
        c +=1 
        debug('#############################', p=1)
        debug('  Space %s (%s of %s)' % (space, c, total), p=1)
        spaceZLow = spaces[space].trueZ()
        spaceZHigh = spaces[space].trueHeight() + spaceZLow
        spacePolygon = spaces[space].polygon
        spacePolygonVertices = polygons[spacePolygon].numericalVertices()
        spacePoly = Poly(spacePolygonVertices)
        spaceArea = spacePoly.area
        
        for space2 in spaces:
            pair = sorted([space,space2])
            
          
            if not space2 == space and not pair in completedComparisons:
                completedComparisons.append(pair)
                space2ZLow = spaces[space2].trueZ()
                space2ZHigh = spaces[space2].trueHeight() + space2ZLow
                maxLow = max(spaceZLow, space2ZLow)
                minHigh = min(spaceZHigh, space2ZHigh)
                
                if (minHigh - maxLow) > vTol:
                
                    space2Polygon = spaces[space2].polygon
                    space2PolygonVertices = polygons[space2Polygon].numericalVertices()
                    space2Poly = Poly(space2PolygonVertices)
                    space2Area = space2Poly.area
                    
                    minArea = min(spaceArea, space2Area) 

                    #d = spacePoly.distance(space2Poly)
                    intersection = spacePoly.intersection(space2Poly)
                    
                    a = intersection.area

                    aPercent = a/minArea/100.
                    

                    if a:
                        t =  '  Overlap between %s and %s\n' % (space, space2)
                        t += '  Type: %s\n' % type(intersection)
                        t += '  overlap : %s\n' % a
                        t += '  percent : %s\n' % aPercent
                        t += '  \n'
                        t += '    %s\n' % space 
                        t += '      zLow  : %s\n' % spaceZLow 
                        t += '      zHigh : %s\n' % spaceZHigh
                        #t += '    poly  : %s' % spacePolygonVertices
                        t += '    %s\n' % space2 
                        t += '      zLow  : %s\n' % space2ZLow 
                        t += '      zHigh : %s\n' % space2ZHigh
                        #t += '    poly  : %s' % space2PolygonVertices
                        t += '\n'
                        if aPercent > percent:
                            debug(t, p=1)
                            problemSpaces.append(t)
                        else:
                            debug(t)
    






             





##################################
######## Start Classes ###########
##################################

class Building(object):
    def __init__(self):
        self.object_list = []
        
    
    def set_parents(self):
    
        cur_parent = {}
        for o in self.object_list:
            cur_parent[o.type] = o
            if o.type in ref.parents.keys():
                o.parent = cur_parent[ref.parents[o.type]]
            else:
                o.parent = None
                
class Object(object):

    def __init__(self):
        self.is_default = 0
        self.attr = OrderedDict()

        
                
            
            
    

class FdfPolygon:
    def __init__(self, name='', vertices=''):
        self.name = name
        self.vertices = vertices

    def reverse(self, fdfPolygons):
        num = len(fdfPolygons[self.name].vertices)
        c = 0
        verticesNew = []
        for verticy in fdfPolygons[self.name].vertices:
            verticesNew.append(fdfPolygons[self.name].vertices[num-c-1])
            c = c + 1
        fdfPolygons[self.name].vertices = verticesNew


class FdfSpace:
    def __init__(self, name='', polygon='', type='CONDITIONED', floor='', z='', height='', hasPlenum='', plenumHeight='', activity=''):
        self.name = name
        self.polygon = polygon
        self.type = type
        self.floor = floor
        self.z = z
        self.height = height
        self.hasPlenum = hasPlenum
        self.plenumHeight = plenumHeight
        self.activity = activity


class FdfFloor:
    def __init__(self, name='', polygon='', scale='', direction='', origin='', z='', height='', p='', floorHeight='', spaceHeight='', plenumDefault=True, x=0, y=0, rotate=0):
        self.name = name
        self.scale = scale
        self.direction = direction
        self.origin = origin
        self.polygon = polygon
        self.x = x
        self.y = y
        self.z = z
        self.rotate = rotate
        self.floorHeight = floorHeight
        self.spaceHeight = spaceHeight
        self.plenumDefault = plenumDefault


class Polygon:
    def __init__(self, name='', vertices=''):
        self.name = name
        self.active = 1
        self.vertices = vertices

    def area(self):
        p = polygons[self.name].vertices
        pnum = []
        for v in p:
            pnum.append([float(v[0]), float(v[1])])
        polyNum = Poly(pnum)
        a = polyNum.area
        return a
    
    def delete(self, polygons, polygon):
        del polygons[polygon]

    def numericalVertices(self):
        nv = []
        for verticy in polygons[self.name].vertices:
            nv.append([float(verticy[0]), float(verticy[1])])
        return nv
    
    def reverse(self):
        num = len(polygons[self.name].vertices)
        verticesNew = []
        c = 0
        for verticy in polygons[self.name].vertices:
            verticesNew.append(polygons[polygon].vertices[num-c-1])
            c = c + 1
        polygons[self.name].vertices = verticesNew

    def changeVerticy(self, i, v):
        verticesNew = []
        c = 0
        for verticy in polygons[self.name].vertices:
            if c == i: 
                verticesNew.append(v)
            else:
                verticesNew.append(polygons[polygon].vertices[c])
            c += 1
        polygons[self.name].vertices = verticesNew

    def deleteDupes(self):
    
        verticesNew = []
        c = 0
        for verticy in polygons[self.name].vertices:
            if verticy in verticesNew:
                pass
                #print 'found dupe in %s' % self.name
            else:
                verticesNew.append(verticy)
        polygons[self.name].vertices = verticesNew

    def deleteSeqDupes(self, tol = 0.1):
       verticiesCurrent = polygons[self.name].vertices
       verticesNew = []
       verticesNew.append(verticiesCurrent[0])
       for i in range(1,len(verticiesCurrent)):
           if pointDistance(verticiesCurrent[i], verticiesCurrent[i-1]) > tol:
           #if verticiesCurrent[i] <> verticiesCurrent[i-1]:
               verticesNew.append(verticiesCurrent[i])
       
       while verticesNew[0] == verticesNew[-1]:
           verticesNew = verticesNew[0:-1]
       polygons[self.name].vertices = verticesNew
       #return verticesNew
        
    def spaceUse(self):
        s = []
        for space in spaces:
            if spaces[space].polygon == self.name:
                s.append(space)
    
        return s
      

class Floor:
    def __init__(self, name='', attributes=[]):
        self.name = name
        self.active = 1

        # define defaults
        self.shape = 'NO-SHAPE'
        self.floorHeight = ''
        self.spaceHeight = ''
        self.polygon = ''
        self.z = ''
        self.catch = []


        for attribute in attributes:
            found = 0
            if attribute[0]=='SHAPE':
                self.shape = attribute[1]
                found = 1
            if attribute[0]=='POLYGON':
                self.polygon = attribute[1]
                found = 1
            if attribute[0]=='FLOOR-HEIGHT':
                self.floorHeight = attribute[1]
                found = 1
            if attribute[0]=='SPACE-HEIGHT':
                self.spaceHeight = attribute[1]
                found = 1
            if attribute[0]=='Z':
                self.z = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)
            
        

    def listSpaces(self, spaces):
        for space in spaces:
            if spaces[space].floor == self.name:
                print space

    def returnSpaces(self, spaces):
        returnSpaces = []
        for space in spaces:
            if spaces[space].floor == self.name:
                returnSpaces.append(space)
        return(returnSpaces)

    def returnPolygons(self):
        returnPolygons = []
        for space in spaces:
            if spaces[space].floor == self.name:
                returnPolygons.append(spaces[space].polygon)
        return(returnPolygons)



    def listEWalls(self, eWalls):
        for eWall in eWalls:
            if eWalls[eWall].floor == self.name:
                print eWall
    def listUWalls(self, eWalls):
        for uWall in uWalls:
            if uWalls[uWall].floor == self.name:
                print uWall
    def listIWalls(self, iWalls):
        for iWall in iWalls:
            if iWalls[eWall].floor == self.name:
                print iWall
    def listWindows(self, windows):
        for window in windows:
            if windows[window].floor == self.name:
                print window


class Space:
    def __init__(self, name='', attributes=[], floor=''):
    #def __init__(self, name, attributes, floor):
        self.name = name
        self.active = 1
        self.floor = floor

        # define defaults
        self.x = ''
        self.y = ''
        self.z = ''
        self.shape = 'POLYGON'
        self.height = ''
        self.polygon = ''
        self.zoneType = ''
        self.activity = ''
        self.catch = []



        for attribute in attributes:
            found = 0
            if attribute[0]=='ZONE-TYPE':
                self.zoneType = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if attribute[0]=='POLYGON':
                self.polygon = attribute[1]
                found = 1
            if attribute[0]=='SHAPE':
                self.shape = attribute[1]
                found = 1
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='Z':
                self.z = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)
        
    
    def trueZ(self):
        if floors[self.floor].z != '':
            fz = float(floors[self.floor].z)
        else:
            fz = 0

        if spaces[self.name].z != '':
            sz = float(spaces[self.name].z)
        else:
            sz = 0
        
        if self.z != '':
            tz = float(self.z) + fz
        else:
            if self.zoneType != 'PLENUM':
                tz = fz
            else:
                tz = fz + float(floors[self.floor].spaceHeight)
        return tz
        

    def trueHeight(self):
        if self.height != '':
            th = float(self.height)
        elif self.zoneType != 'PLENUM':
            th = float(floors[self.floor].spaceHeight)
        else:
            th = float(floors[self.floor].floorHeight) - float(floors[self.floor].spaceHeight)
        return th


 
    def listEWalls(self, eWalls):
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                print eWall

    def countVertices(self):
        for polygon in polygons:
            if polygons[polygon].name == self.polygon:
                numberOfVertices = len(polygons[polygon].vertices)
        return(numberOfVertices)

    def returnVertices(self, polygons):
        vertices = []
        for polygon in polygons:
            if polygons[polygon].name == self.polygon:
                return polygons[polygon].vertices


    def returnEWalls(self, eWalls):
        returnEWalls = []
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                returnEWalls.append(eWalls[eWall].name)
        return(returnEWalls)

    def countEWalls(self):
        countEWalls = 0
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                countEWalls = countEWalls + 1
        return(countEWalls)

    def countUWalls(self):
        countUWalls = 0
        for uWall in uWalls:
            if uWalls[uWall].space == self.name:
                countUWalls = countUWalls + 1
        return(countUWalls)

    def countIWalls(self):
        countIWalls = 0
        for iWall in iWalls:
            if iWalls[iWall].space == self.name:
                countIWalls = countIWalls + 1
        return(countIWalls)

    def countWindows(self):
        countWindows = 0
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                for window in windows:
                    if windows[window].eWall == eWalls[eWall].name:
                        countWindows = countWindows + 1
        return(countWindows)


    def listUWalls(self, eWalls):
        for uWall in uWalls:
            if uWalls[uWall].space == self.name:
                print uWall

    def returnUWalls(self, uWalls):
        returnUWalls = []
        for uWall in uWalls:
            if uWalls[uWall].space == self.name:
                returnUWalls.append(uWall)
        return(returnUWalls)


    def listIWalls(self, iWalls):
        for iWall in iWalls:
            if iWalls[iWall].space == self.name or iWalls[iWall].nextTo == self.name:
                print iWall

    def returnIWalls(self, iWalls):
        returnIWalls = []
        for iWall in iWalls:
            if iWalls[iWall].space == self.name:
                returnIWalls.append(iWall)
        return(returnIWalls)

    def returnAllIWalls(self, iWalls): # include ones for which this is the other space
        returnIWalls = []
        for iWall in iWalls:
            if (iWalls[iWall].space == self.name) or (iWalls[iWall].nextTo == self.name):
                returnIWalls.append(iWall)
        return(returnIWalls)
        


    def listWindows(self, windows):
        print self
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                print '  %s' % wall
                for window in windows:
                    if windows[window].wall == eWalls[eWall].name:
                        print '    %s' % window

    def returnWindows(self, windows):
        returnWindows = []
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                for window in windows:
                    if windows[window].wall == eWalls[eWall].name:
                        returnWindows.append(window)
        return(returnWindows)


    def returnDoors(self, doors):
        returnDoors = []
        for eWall in eWalls:
            if eWalls[eWall].space == self.name:
                for door in doors:
                    if doors[door].wall == eWalls[eWall].name:
                        returnDoors.append(door)
        return(returnDoors)

    def returnZoneType(self):
        if self.zoneType =='':
            zt = 'CONDITIONED'
        else:
            zt = self.zoneType
        return zt
        


    def delete(self, eWalls, uWalls, iWalls, windows):

        for eWall in self.returnEWalls(eWalls):
            del eWalls[eWall]

        for iWall in self.returnIWalls(iWalls):
            del iWalls[iWall]

        for uWall in self.returnUWalls(uWalls):
            del uWalls[uWall]

        for window in self.returnWindows(windows):
            del windows[window]
        
        del spaces[self.name]

    def testSpace(self, polygons=None, floors=None, xMinO='-', xMaxO='-', yMinO='-', yMaxO='-', xMinI='-', xMaxI='-', yMinI='-', yMaxI='-', zMin='-', zMax='-', zThru='-', hMin='-', hMax='-', regex='-', isPlenum='-', isConditioned='-', isUnconditioned='-'): 
        result = True

        # gather info
        vertices = self.returnVertices(polygons)
        spaceXMin = ''
        spaceXMax = ''
        spaceYMin = ''
        spaceYMax = ''
  
        for verticy in vertices: 
            print verticy
            if spaceXMin == '':
                spaceXMin = float(verticy[0])
            elif float(verticy[0]) < float(spaceXMin):
                spaceXMin = float(verticy[0])

            if spaceXMax == '':
                spaceXMax = float(verticy[0])
            elif float(verticy[0]) > float(spaceXMax):
                spaceXMax = float(verticy[0])

            if spaceYMin == '':
                spaceYMin = float(verticy[1])
            elif float(verticy[1]) < float(spaceYMin):
                spaceYMin = float(verticy[1])

            if spaceYMax == '':
                spaceYMax = float(verticy[1])
            elif float(verticy[1]) > float(spaceYMax):
                spaceYMax = float(verticy[1])
                  
        spaceHeight = float(self.trueHeight())
        spaceZ = float(self.trueZ())
        if self.zoneType == 'PLENUM':
            zt = 'plenum'
        elif self.zoneType == 'UNCONDITIONED':
            zt = 'unconditioned'
        else:
            zt = 'conditioned'

        print self.name
        print '  xmin', spaceXMin
        print '  xmax', spaceXMax
        print '  ymin', spaceYMin
        print '  ymax', spaceYMax
        print '  z', spaceZ
        print '  h', spaceHeight
        print '  zt', zt


        
        # run tests  
        if not xMinO=='-': # O-types test for any intersection
            if (spaceXMax < xMinO):
                print '    failed xminO: %s < %s' % (spaceXMin, xMinO)
                result = False
        
        if not xMaxO=='-':
            if (spaceXMin > xMaxO):
                print '    failed xmaxO: %s > %s' % (spaceXMax, xMaxO)
                result = False

        if not yMinO=='-':
            if (spaceYMax < yMinO):
                print '    failed yminO: %s < %s' % (spaceYMin, yMinO)
                result = False
        
        if not xMaxO=='-':
            if (spaceYMin > yMaxO):
                print '    failed ymaxO: %s > %s' % (spaceYMax, yMaxO)
                result = False


        if not xMinI=='-':  # I types check for complete containment
            if (spaceXMin < xMinI):
                print '    failed xminI: %s !< %s' % (spaceXMin, xMinI)
                result = False
        
        if not xMaxI=='-':
            if (spaceXMax > xMaxI):
                print '    failed xmaxI: %s !> %s' % (spaceXMax, xMaxI)
                result = False

        if not yMinI=='-':
            if (spaceYMin < yMinI):
                print '    failed yminI: %s !< %s' % (spaceYMin, yMinI)
                result = False

        if not yMaxI=='-':
            if (spaceYMax > yMaxI):
                print '    failed ymaxI: %s !> %s' % (spaceYMax, yMaxI)
                result = False


        if not zMin=='-':
            if (spaceZ < zMin):
                print '    failed zmin: %s !< %s' % (spaceZ, zMin)
                result = False

        if not zMax=='-':
            if (spaceZ > zMax):
                print '    failed zmax: %s !> %s' % (spaceZ, zMax)
                result = False

        if not zThru=='-':
            if (spaceZ > zThru):
                print '    failed #1 zthru: %s !> %s' % (spaceZ, zThru)
            if  ((spaceZ + spaceHeight) < zThru):
                print '    failed #2 zthru: %s !> %s' % (spaceZ + spaceHeight, zThru)
                result = False


        if not hMin=='-':
            if (spaceHeight < hMin):
                print '    failed hmin: %s !< %s' % (spaceHeight, hMin)
                result = False

        if not hMax=='-':
            if (spaceHeight > hMax):
                print '    failed hmax: %s !> %s' % (spaceHeight, hMax)
                result = False

        if not isPlenum=='-':
            if isPlenum.lower() == 'n' and zt == 'plenum':
                print '    failed isPlenum, zonetype is %s' % zt
                result = False

        if not isConditioned=='-':
            if isConditioned.lower() == 'n' and zt == 'conditioned':
                print '    failed isConditioned, zonetype is %s' % zt
                result = False

        if not isUnconditioned=='-':
            if isUnconditioned.lower() == 'n' and zt == 'unconditioned':
                print '    failed isUnconditioned, zonetype is %s' % zt
                result = False
             
        if regex!='-':
            if not re.search(regex, self.name):
                print '    failed regex match of %s on %s' % (regex, self.name)
                result = False

        #if self.name == '"4-ATTIC_E"':
        #    sys.exit()

        return result    


    def findNextEWall(self, eWalls):
        spaceName = self.name[1:-1]
        print spaceName

        c = 1
        k = '"%s-E%s"' % (spaceName, c)

        while eWalls.has_key(k):
            c = c + 1
            k = '"%s-E%s"' % (spaceName, c)

        return k

    def findNextUWall(self, uWalls):
        spaceName = self.name[1:-1]
        print spaceName

        c = 1
        k = '"%s-U%s"' % (spaceName, c)

        while uWalls.has_key(k):
            c = c + 1
            k = '"%s-U%s"' % (spaceName, c)

        return k



class EWall:
    def __init__(self, name='', attributes=[], floor='', space=''):
    #def __init__(self, name, attributes, floor, space):
        self.name = name
        self.active = 1
        self.space = space
        self.floor = floor

        # define defaults
        self.location = ''
        self.construction = ''
        self.shape = ''
        self.polygon = ''
        self.x = ''
        self.y = ''
        self.z = ''
        self.tilt = ''
        self.width = ''
        self.height = ''
        self.tilt = ''
        self.azimuth = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='LOCATION':
                self.location = attribute[1]
                found = 1
            if attribute[0]=='CONSTRUCTION':
                self.construction = attribute[1]
                found = 1
            if attribute[0]=='SHAPE':
                self.shape = attribute[1]
                found = 1
            if attribute[0]=='POLYGON':
                self.polygon = attribute[1]
                found = 1
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='Z':
                self.z = attribute[1]
                found = 1
            if attribute[0]=='WIDTH':
                self.width = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if attribute[0]=='TILT':
                self.tilt = attribute[1]
                found = 1
            if attribute[0]=='AZIMUTH':
                self.azimuth = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)

    def listWindows(self, windows):
        for window in windows:
            if windows[window].wall == self.name:
                print window

    def returnWindows(self, windows):
        returnWindows = []
        for window in windows:
            if windows[window].wall == self.name:
                returnWindows.append(window)
        return(returnWindows)

    def returnDoors(self, windows):
        returnDoors = []
        for door in doors:
            if doors[door].wall == self.name:
                returnDoors.append(door)
        return(returnDoors)



    def countWindows(self):
        returnWindows = []
        for window in windows:
            if windows[window].wall == self.name:
                returnWindows.append(window)
        return(len(returnWindows))

    def countDoors(self):
        returnDoors = []
        for door in doors:
            if doors[door].wall == self.name:
                returnDoors.append(window)
        return(len(returnDoors))


    
    def returnTotalZ(self):
        wallZ = self.z
        spaceZ = spaces[self.space].z
        floorZ = floors[self.floor].z
        total = 0

        if spaces[self.space].zoneType == 'PLENUM':
            isPlenum = 1
        else:
            isPlenum = 0

        if wallZ:  # if the wall height is explicitly defined
            total+=float(wallZ)
        elif self.location == 'TOP':
            if isPlenum:
                total+=float(floors[self.floor].floorHeight)
            else:
                total+=float(floors[self.floor].spaceHeight)
        elif self.location == 'BOTTOM':
            if isPlenum:
                total+=float(floors[self.floor].spaceHeight)
        elif isPlenum:
            total += float(floors[self.floor].spaceHeight)
        
        if spaceZ: total+=float(spaceZ)
        if floorZ: total+=float(floorZ)
        
        return total

    def returnTilt(self):
        if self.tilt != '':
            tilt = float(self.tilt)
        elif self.location == 'TOP':
            tilt = 0
        elif self.location == 'BOTTOM':
            tilt = 180
        else:
            tilt = 90
        return tilt

    
    def returnCoords(self):
        space = self.space
        location = self.location
        currentPolygon = polygons[spaces[space].polygon].name
        currentPolygonvertices = polygons[currentPolygon].vertices
        polygonLength = len(polygons[currentPolygon].vertices)
        wallVerticy = location[7:]
        wallVerticyInteger = string.atoi(wallVerticy)
        if wallVerticyInteger == polygonLength:
            x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
            y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
            x2 = string.atof(currentPolygonvertices[0][0])
            y2 = string.atof(currentPolygonvertices[0][1])
        else:
            x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
            y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
            x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
            y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])

        return x1, x2, y1, y2

    def returnXMin(self):
        try:
            xMin = min(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMin = None
        return xMin

    def returnXMax(self):
        try:
            xMax = max(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMax = None
        return xMax

    def returnYMin(self):
        try:
            yMin = min(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMin = None
        return yMin

    def returnYMax(self):
        try:
            yMax = max(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMax = None
        return yMax

    def returnX1(self):
        try:
            x1 = float(self.returnCoords()[0])
        except:
            x1 = None
        return x1

    def returnX2(self):
        try:
            x2 = float(self.returnCoords()[1])
        except:
            x2 = None
        return x2

    def returnY1(self):
        try:
            y1 = float(self.returnCoords()[2])
        except:
            y1 = None
        return y1

    def returnY2(self):
        try:
            y2 = float(self.returnCoords()[3])
        except:
            y2 = None
        return y2

        

    def returnHeight(self):
        try:
            if self.polygon <> '' or self.location == 'TOP' or self.location == 'BOTTOM':
                return None
            elif self.height <> '':
                eWallHeight = self.height
            elif spaces[self.space].height <> '':
                eWallHeight = spaces[self.space].height
            else:
                if spaces[self.space].zoneType == 'PLENUM':
                    eWallHeight = (float(floors[self.floor].floorHeight) - float(floors[self.floor].spaceHeight))
                else:
                    if floors[self.floor].spaceHeight:
                        eWallHeight = floors[self.floor].spaceHeight
                    else: 
                        eWallHeight = floors[self.floor].floorHeight
            return float(eWallHeight)
        except:
            return None

    def returnWidth(self):
        try:
            if self.width <> '':
                eWallWidth = self.width
            else:
                space = self.space
                location = self.location
                currentPolygon = polygons[spaces[space].polygon].name
                currentPolygonvertices = polygons[currentPolygon].vertices
                polygonLength = len(polygons[currentPolygon].vertices)
                wallVerticy = location[7:]
                wallVerticyInteger = string.atoi(wallVerticy)
                if wallVerticyInteger == polygonLength:
                    x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
                    y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
                    x2 = string.atof(currentPolygonvertices[0][0])
                    y2 = string.atof(currentPolygonvertices[0][1])
                else:
                    x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
                    y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
                    x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
                    y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])
                eWallWidth = ((x2-x1)**2+(y2-y1)**2)**0.5
        except:
            eWallWidth = None

        return (eWallWidth)

    def area(self):
        if self.shape == 'POLYGON' or self.location == 'TOP' or self.location == 'BOTTOM' :
            if eWalls[self.name].polygon != '':
                p = eWalls[self.name].polygon
                area = polygons[p].area()
            else:
                s = eWalls[self.name].space
                p = spaces[s].polygon
                area = polygons[p].area()
        else:
            w = eWalls[self.name].returnWidth()
            h = eWalls[self.name].returnHeight()
            area = w * h
        return area

    
    
    def returnZoneType(self):
        space = self.space
        zt = spaces[space].returnZoneType()
        return zt
        


    def returnAngle(self, type='doe'):
        #print 'Determining Width from Polygon'
        space = self.space
        location = self.location
        tilt = self.returnTilt()
        if tilt == 180 or tilt == 0:
            angle = None
        else:
            currentPolygon = polygons[spaces[space].polygon].name
            currentPolygonvertices = polygons[currentPolygon].vertices
            polygonLength = len(polygons[currentPolygon].vertices)
            wallVerticy = location[7:]
            #print location
            #print wallVerticy
            wallVerticyInteger = string.atoi(wallVerticy)
            if wallVerticyInteger == polygonLength:
                x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
                y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
                x2 = string.atof(currentPolygonvertices[0][0])
                y2 = string.atof(currentPolygonvertices[0][1])
            else:
                x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
                y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
                x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
                y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])
            if type=='doe':
                angle = getAngle(x1, y1, x2, y2)
            else:
                angle = getAngleReal(x1, y1, x2, y2)
        
        return angle

    def testWall(self, x1='-', y1='-', aDoe='-', lTol='-', aTol='-', xMin='-', xMax='-', yMin='-', yMax='-', wMin='-', wMax='-', hMin='-', hMax='-', tMin='-', tMax='-', regex='-', verbose = 0): 
        result = True
        try:
            coords = self.returnCoords()
        except:
            coords = ''
        
        if (x1!='-' and y1!='-' and aDoe!='-' and lTol!='-' and aTol!='-'):

            aDoe = aDoe%360
            aTrue = swapAngleType(aDoe)
            eWallAngle = self.returnAngle()%360

            if angleDistance(aDoe, eWallAngle) <= aTol:
                if verbose:
                    print '    TRUE: %s is within %s of %s' % (aDoe, aTol, eWallAngle)
            else:
                if verbose:
                    print '    FALSE: %s is not within %s of %s' % (aDoe, aTol, eWallAngle)
                result = False
    
            if dist(x1, y1, aTrue, coords[0], coords[2]) <= lTol:
                if verbose:
                    print '    TRUE: (%s,%s) is within %s of (%s,%s) at angle %s' % (coords[0], coords[2], lTol, x1, y1, aTrue)
            else:
                if verbose:
                    print '    FALSE: (%s,%s) is not within %s of (%s,%s) at angle %s' % (coords[0], coords[2], lTol, x1, y1, aTrue)
                result = False
    
            if dist(x1, y1, aTrue, coords[1], coords[3]) <= lTol:
                if verbose:
                    print '    TRUE: (%s,%s) is within %s of (%s,%s) at angle %s' % (coords[1], coords[3], lTol, x1, y1, aTrue)
            else:
                if verbose:
                    print '    FALSE: (%s,%s) is not within %s of (%s,%s) at angle %s' % (coords[1], coords[3], lTol, x1, y1, aTrue)
                result = False
    
        if not xMin=='-':
            if (coords[0] >= xMin) and (coords[1] >= xMin):
                if verbose:
                    print '    TRUE: coords %s are > %s xMin ' % (coords, xMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s xMin ' % (coords, xMin)
                result = False

        if not xMax=='-':
            if (coords[0] <= xMax) and (coords[1] <= xMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s xMax ' % (coords, xMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s xMax ' % (coords, xMax)
                result = False

        if not yMin=='-':
            if (coords[2] >= yMin) and (coords[3] >= yMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s yMin ' % (coords, yMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s yMin ' % (coords, yMin)
                result = False

        if not yMax=='-':
            if (coords[2] <= yMax) and (coords[2] <= yMax):
                if verbose:
                    print '    TRUE: coords %s are < %s yMax ' % (coords, yMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s yMax ' % (coords, yMax)
                result = False

        if not hMin=='-':
            if (self.returnHeight() >= hMin):
                if verbose:
                    print '    TRUE: coords %s are > %s hMin ' % (coords, hMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s hMin ' % (coords, hMin)
                result = False

        if not hMax=='-':
            if (self.returnHeight() <= hMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s hMax ' % (coords, hMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s hMax ' % (coords, hMax)
                result = False

        if not wMin=='-':
            if (self.returnWidth() >= wMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s wMin ' % (coords, wMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s wMin ' % (coords, wMin)
                result = False

        if not wMax=='-':
            if (self.returnWidth() < wMax):
                if verbose:
                    print '    TRUE: coords %s are < %s wMax ' % (coords, wMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s wMax ' % (coords, wMax)
                result = False

        if not tMin=='-':
            tilt = round(float(self.returnTilt()),0)
            tMin = round(float(tMin),0)
            if (tilt >= tMin):
                if verbose:
                    print '    TRUE: tilt %s is >= %s tMin ' % (tilt, tMin)
            else:
                if verbose:
                    print '    FALSE: tilt %s is NOT >= %s tMin ' % (tilt, tMin)
                result = False

        if not tMax=='-':
            tilt = round(float(self.returnTilt()),0)
            tMax = round(float(tMax),0)
            if (self.returnTilt() <= tMax):
                if verbose:
                    print '    TRUE: tilt %s is <= %s tMax ' % (tilt, tMax)
            else:
                if verbose:
                    print '    FALSE: tilt %s is NOT <= %s tMax ' % (tilt, tMax)
                result = False


        if regex!='-':
            if re.search(regex, self.name):
                if verbose:
                    print '    TRUE: regex %s matches %s' % (regex, self.name)
            else:
                if verbose:
                    print '    FALSE: regex %s does not matche %s' % (regex, self.name)
                result = False

        return result

 
    def rotateWall(self, r):
        coords = self.returnCoords()
        print 'name: %s\n' % self.name
        if self.x:
            x = float(self.x)
        else:
            x = coords[0]

        if self.y:
            y = float(self.y)
        else:
            y = coords[2]

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
        
        
        if self.x:
            retX = x2
        else:
            retX = ''

        if self.y:
            retY = y2
        else:
            retY = ''

        if self.azimuth:
            aDoeOrig = float(self.azimuth)
            aRealOrig = swapAngleType(aDoeOrig)
            aRealNew = (aRealOrig+r)%360
            aDoeNew = swapAngleType(aRealNew)
            print '   Original Cardinal %s' % aDoeOrig
            print '   Original Real %s' % aRealOrig
            print '   Rotated %s REAL degrees' % (r)
            print '   New Real %s' % aRealNew
            print '   New Cardinal: %s\n' % aDoeNew
        else:
            aDoeNew = ''
                        


        print '   Coordinate: [%s, %s]' % (round(x,2), round(y,2))
        print '   Rotated %s deg' % (r)
        print '   New Coordinate: [%s, %s]\n' % (round(x2,2), round(y2,2))

        print '   Returning %s, %s, %s\n' % (retX, retY, aDoeNew)

        return retX, retY, aDoeNew

    def moveWall(self, x, y):

        newX = ''
        newY = ''

        if x == '':
            x = 0
        if y == '':
            y = 0

        if self.x:
            newX = float(self.x) + float(x)
        if self.y:
            newY = float(self.y) + float(y)

        return newX, newY



    def delete(self, eWalls, windows):
        for window in self.returnWindows(windows):
            del windows[window]

        for eWall in self.returnEWalls(eWalls):
            del eWalls[eWall]

     
        
class UWall:
    def __init__(self, name='', attributes=[], floor='', space=''):
    #def __init__(self, name, attributes, floor, space):
        self.name = name
        self.active = 1
        self.space = space
        self.floor = floor

        # define defaults
        self.location = ''
        self.construction = ''
        self.shape = ''
        self.polygon = ''
        self.x = ''
        self.y = ''
        self.z = ''
        self.tilt = ''
        self.width = ''
        self.height = ''
        self.azimuth = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='LOCATION':
                self.location = attribute[1]
                found = 1
            if attribute[0]=='CONSTRUCTION':
                self.construction = attribute[1]
                found = 1
            if attribute[0]=='SHAPE':
                self.shape = attribute[1]
                found = 1
            if attribute[0]=='POLYGON':
                self.polygon = attribute[1]
                found = 1
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='Z':
                self.z = attribute[1]
                found = 1
            if attribute[0]=='WIDTH':
                self.width = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if attribute[0]=='TILT':
                self.tilt = attribute[1]
                found = 1
            if attribute[0]=='AZIMUTH':
                self.azimuth = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)

    def returnTotalZ(self):
        wallZ = self.z
        spaceZ = spaces[self.space].z
        floorZ = floors[self.floor].z
        total = 0

        if spaces[self.space].zoneType == 'PLENUM':
            isPlenum = 1
        else:
            isPlenum = 0

        if wallZ:  # if the wall height is explicitly defined
            total+=float(wallZ)
        elif self.location == 'TOP':
            if isPlenum:
                total+=float(floors[self.floor].floorHeight)
            else:
                total+=float(floors[self.floor].spaceHeight)
        elif self.location == 'BOTTOM':
            if isPlenum:
                total+=float(floors[self.floor].spaceHeight)
        elif isPlenum:
            total += float(floors[self.floor].spaceHeight)
        
        if spaceZ: total+=float(spaceZ)
        if floorZ: total+=float(floorZ)
        
        return total

    def returnPolygon(self, spaces): # sometimes the polygon is defined with the SMirro convention
        if self.polygon != '':
            return self.polygon
        else:
            try:
                spacePoly = spaces[self.space].polygon
                if self.returnTilt() == 0:
                    return spacePoly
                elif self.returnTilt() == 180:
                    mPoly = spacePoly[:-1] + ' - SMirro' + '"'
                    return mPoly

            except:
                return None


    def returnTilt(self):
        if self.tilt != '':
            tilt = float(self.tilt)
        elif self.location == 'TOP':
            tilt = 0
        elif self.location == 'BOTTOM':
            tilt = 180
        else:
            tilt = 90
        return tilt
                
    
    def returnCoords(self):
        space = self.space
        location = self.location
        currentPolygon = polygons[spaces[space].polygon].name
        currentPolygonvertices = polygons[currentPolygon].vertices
        polygonLength = len(polygons[currentPolygon].vertices)
        wallVerticy = location[7:]
        wallVerticyInteger = string.atoi(wallVerticy)
        if wallVerticyInteger == polygonLength:
            x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
            y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
            x2 = string.atof(currentPolygonvertices[0][0])
            y2 = string.atof(currentPolygonvertices[0][1])
        else:
            x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
            y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
            x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
            y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])

        return x1, x2, y1, y2


    def returnXMin(self):
        try:
            xMin = min(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMin = None
        return xMin

    def returnXMax(self):
        try:
            xMax = max(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMax = None
        return xMax

    def returnYMin(self):
        try:
            yMin = min(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMin = None
        return yMin

    def returnYMax(self):
        try:
            yMax = max(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMax = None
        return yMax

    
    
    def returnX1(self):
        try:
            x1 = float(self.returnCoords()[0])
        except:
            x1 = None
        return x1

    def returnX2(self):
        try:
            x2 = float(self.returnCoords()[1])
        except:
            x2 = None
        return x2

    def returnY1(self):
        try:
            y1 = float(self.returnCoords()[2])
        except:
            y1 = None
        return y1

    def returnY2(self):
        try:
            y2 = float(self.returnCoords()[3])
        except:
            y2 = None
        return y2




    def returnHeight(self):
        try:
            if self.polygon <> '' or self.location == 'TOP' or self.location == 'BOTTOM':
                return None
            elif self.height <> '':
                uWallHeight = self.height
            elif spaces[self.space].height <> '':
                uWallHeight = spaces[self.space].height
            else:
                if spaces[self.space].zoneType == 'PLENUM':
                    uWallHeight = (float(floors[self.floor].floorHeight) - float(floors[self.floor].spaceHeight))
                else:
                    if floors[self.floor].spaceHeight:
                        uWallHeight = floors[self.floor].spaceHeight
                    else: 
                        uWallHeight = floors[self.floor].floorHeight
            return float(uWallHeight)
        except:
            return None


    def returnWidth(self):
        try:
            if self.polygon <> '' or self.location == 'TOP' or self.location == 'BOTTOM':
                return None
            if self.width <> '':
                uWallWidth = float(self.width)
            else:
                space = self.space
                location = self.location
                currentPolygon = polygons[spaces[space].polygon].name
                currentPolygonvertices = polygons[currentPolygon].vertices
                polygonLength = len(polygons[currentPolygon].vertices)
                wallVerticy = location[7:]
                wallVerticyInteger = string.atoi(wallVerticy)
                if wallVerticyInteger == polygonLength:
                    x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
                    y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
                    x2 = string.atof(currentPolygonvertices[0][0])
                    y2 = string.atof(currentPolygonvertices[0][1])
                else:
                    x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
                    y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
                    x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
                    y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])
                uWallWidth = ((x2-x1)**2+(y2-y1)**2)**0.5
        except:
            uWallWidth = None

        return (uWallWidth)

    def area(self):
        if self.shape == 'POLYGON' or self.location == 'TOP' or self.location == 'BOTTOM' :
            if uWalls[self.name].polygon != '':
                p = uWalls[self.name].polygon
                area = polygons[p].area()
            else:
                s = uWalls[self.name].space
                p = spaces[s].polygon
                area = polygons[p].area()
        else:
            w = uWalls[self.name].returnWidth()
            h = uWalls[self.name].returnHeight()
            area = w * h
        return area
    

    def returnZoneType(self):
        space = self.space
        zt = spaces[space].returnZoneType()
        return zt


    def returnAngle(self, type='doe'):

        space = self.space
        location = self.location
        tilt = self.returnTilt()
        if tilt == 180 or tilt == 0:
            angle = None
        else:
            #print 'Determining Width from Polygon'
            currentPolygon = polygons[spaces[space].polygon].name
            currentPolygonvertices = polygons[currentPolygon].vertices
            polygonLength = len(polygons[currentPolygon].vertices)
            wallVerticy = location[7:]
            #print location
            #print wallVerticy
            wallVerticyInteger = string.atoi(wallVerticy)
            if wallVerticyInteger == polygonLength:
                x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
                y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
                x2 = string.atof(currentPolygonvertices[0][0])
                y2 = string.atof(currentPolygonvertices[0][1])
            else:
                x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
                y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
                x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
                y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])
            if type=='doe':
                angle = getAngle(x1, y1, x2, y2)
            else:
                angle = getAngleReal(x1, y1, x2, y2)
            
        return angle

    def testWall(self, x1='-', y1='-', aDoe='-', lTol='-', aTol='-', xMin='-', xMax='-', yMin='-', yMax='-', wMin='-', wMax='-', hMin='-', hMax='-', tMin='-', tMax='-', regex='-', verbose = 0): 
        result = True
        try:
            coords = self.returnCoords()
        except:
            coords = ''
        
        if (x1!='-' and y1!='-' and aDoe!='-' and lTol!='-' and aTol!='-'):

            aDoe = aDoe%360
            aTrue = swapAngleType(aDoe)
            eWallAngle = self.returnAngle()%360

            if angleDistance(aDoe, eWallAngle) <= aTol:
                if verbose:
                    print '    TRUE: %s is within %s of %s' % (aDoe, aTol, eWallAngle)
            else:
                if verbose:
                    print '    FALSE: %s is not within %s of %s' % (aDoe, aTol, eWallAngle)
                result = False
    
            if dist(x1, y1, aTrue, coords[0], coords[2]) <= lTol:
                if verbose:
                    print '    TRUE: (%s,%s) is within %s of (%s,%s) at angle %s' % (coords[0], coords[2], lTol, x1, y1, aTrue)
            else:
                if verbose:
                    print '    FALSE: (%s,%s) is not within %s of (%s,%s) at angle %s' % (coords[0], coords[2], lTol, x1, y1, aTrue)
                result = False
    
            if dist(x1, y1, aTrue, coords[1], coords[3]) <= lTol:
                if verbose:
                    print '    TRUE: (%s,%s) is within %s of (%s,%s) at angle %s' % (coords[1], coords[3], lTol, x1, y1, aTrue)
            else:
                if verbose:
                    print '    FALSE: (%s,%s) is not within %s of (%s,%s) at angle %s' % (coords[1], coords[3], lTol, x1, y1, aTrue)
                result = False
    
        if not xMin=='-':
            if (coords[0] >= xMin) and (coords[1] >= xMin):
                if verbose:
                    print '    TRUE: coords %s are > %s xMin ' % (coords, xMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s xMin ' % (coords, xMin)
                result = False
 
        if not xMax=='-':
            if (coords[0] <= xMax) and (coords[1] <= xMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s xMax ' % (coords, xMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s xMax ' % (coords, xMax)
                result = False

        if not yMin=='-':
            if (coords[2] >= yMin) and (coords[3] >= yMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s yMin ' % (coords, yMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s yMin ' % (coords, yMin)
                result = False

        if not yMax=='-':
            if (coords[2] <= yMax) and (coords[2] <= yMax):
                if verbose:
                    print '    TRUE: coords %s are < %s yMax ' % (coords, yMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s yMax ' % (coords, yMax)
                result = False

        if not hMin=='-':
            if (self.returnHeight() >= hMin):
                if verbose:
                    print '    TRUE: coords %s are > %s hMin ' % (coords, hMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s hMin ' % (coords, hMin)
                result = False

        if not hMax=='-':
            if (self.returnHeight() <= hMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s hMax ' % (coords, hMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s hMax ' % (coords, hMax)
                result = False

        if not wMin=='-':
            if (self.returnWidth() >= wMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s wMin ' % (coords, wMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s wMin ' % (coords, wMin)
                result = False

        if not wMax=='-':
            if (self.returnWidth() < wMax):
                if verbose:
                    print '    TRUE: coords %s are < %s wMax ' % (coords, wMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s wMax ' % (coords, wMax)
                result = False

        if not tMin=='-':
            tilt = round(float(self.returnTilt()),0)
            tMin = round(float(tMin),0)
            if (tilt >= tMin):
                if verbose:
                    print '    TRUE: tilt %s is >= %s tMin ' % (tilt, tMin)
            else:
                if verbose:
                    print '    FALSE: tilt %s is NOT >= %s tMin ' % (tilt, tMin)
                result = False

        if not tMax=='-':
            tilt = round(float(self.returnTilt()),0)
            tMax = round(float(tMax),0)
            if (self.returnTilt() <= tMax):
                if verbose:
                    print '    TRUE: tilt %s is <= %s tMax ' % (tilt, tMax)
            else:
                if verbose:
                    print '    FALSE: tilt %s is NOT <= %s tMax ' % (tilt, tMax)
                result = False


        if regex!='-':
            if re.search(regex, self.name):
                if verbose:
                    print '    TRUE: regex %s matches %s' % (regex, self.name)
            else:
                if verbose:
                    print '    FALSE: regex %s does not matche %s' % (regex, self.name)
                result = False

        return result

 


class IWall:
    def __init__(self, name='', attributes=[], floor='', space=''):
        self.name = name
        self.active = 1
        self.space = space
        self.floor = floor

        # define defaults
        self.location = ''
        self.construction = ''
        self.shape = ''
        self.polygon = ''
        self.x = ''
        self.y = ''
        self.z = ''
        self.tilt = ''
        self.height = ''
        self.width = ''
        self.azimuth = ''
        self.nextTo = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='LOCATION':
                self.location = attribute[1]
                found = 1
            if attribute[0]=='CONSTRUCTION':
                self.construction = attribute[1]
                found = 1
            if attribute[0]=='SHAPE':
                self.shape = attribute[1]
                found = 1
            if attribute[0]=='POLYGON':
                self.polygon = attribute[1]
                found = 1
            if attribute[0]=='NEXT-TO':
                self.nextTo = attribute[1]
                found = 1
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='Z':
                self.z = attribute[1]
                found = 1
            if attribute[0]=='WIDTH':
                self.width = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if attribute[0]=='AZIMUTH':
                self.azimuth = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)
                
    def returnTotalZ(self):
        wallZ = self.z
        spaceZ = spaces[self.space].z
        floorZ = floors[self.floor].z
        total = 0

        if spaces[self.space].zoneType == 'PLENUM':
            isPlenum = 1
        else:
            isPlenum = 0

        if wallZ:  # if the wall height is explicitly defined
            total+=float(wallZ)
            #print type(debug)
            #debug('  returnTotalZ/wallZ %s' % wallZ)
        elif self.location == 'TOP':
            if isPlenum:
                total+=float(floors[self.floor].floorHeight)
            else:
                total+=float(floors[self.floor].spaceHeight)
        elif self.location == 'BOTTOM':
            if isPlenum:
                total+=float(floors[self.floor].spaceHeight)
        elif isPlenum:
            total += float(floors[self.floor].spaceHeight)
            #debug('  returnTotalZ/spaceheight %s' % float(floors[self.floor].spaceHeight))
        
        if spaceZ: total+=float(spaceZ)
        if floorZ: total+=float(floorZ)
        
        return total



    def returnCoords(self):
        space = self.space
        location = self.location
        currentPolygon = polygons[spaces[space].polygon].name
        currentPolygonvertices = polygons[currentPolygon].vertices
        polygonLength = len(polygons[currentPolygon].vertices)
        wallVerticy = location[7:]
        wallVerticyInteger = string.atoi(wallVerticy)
        if wallVerticyInteger == polygonLength:
            x1 = string.atof(currentPolygonvertices[polygonLength-1][0])
            y1 = string.atof(currentPolygonvertices[polygonLength-1][1])
            x2 = string.atof(currentPolygonvertices[0][0])
            y2 = string.atof(currentPolygonvertices[0][1])
        else:
            x1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][0])
            y1 = string.atof(currentPolygonvertices[wallVerticyInteger-1][1])
            x2 = string.atof(currentPolygonvertices[wallVerticyInteger][0])
            y2 = string.atof(currentPolygonvertices[wallVerticyInteger][1])

        return x1, x2, y1, y2
 
    
    def matchSpaces(self, regex, t='and'):
        if t == 'and':
            if re.findall(regex, self.space) and re.findall(regex, self.nextTo):
                return 1
        if t == 'or':
            if re.findall(regex, self.space) or re.findall(regex, self.nextTo):
                return 1
        return 0

    
    def returnWidth(self):
         coords = self.returnCoords()
         x1, x2, y1, y2 = coords
         iWallWidth = ((x2-x1)**2+(y2-y1)**2)**0.5
         return iWallWidth

 
    
    def returnXMin(self):
        try:
            xMin = min(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMin = None
        return xMin

    def returnXMax(self):
        try:
            xMax = max(float(self.returnCoords()[0]),float(self.returnCoords()[1]))
        except:
            xMax = None
        return xMax

    def returnYMin(self):
        try:
            yMin = min(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMin = None
        return yMin

    def returnYMax(self):
        try:
            yMax = max(float(self.returnCoords()[2]),float(self.returnCoords()[3]))
        except:
            yMax = None
        return yMax

    def returnTilt(self):
        if self.tilt != '':
            tilt = float(self.tilt)
        elif self.location == 'TOP':
            tilt = 0
        elif self.location == 'BOTTOM':
            tilt = 180
        else:
            tilt = 90
        return tilt

 
        
    def returnHeight(self):
        try:
            if self.polygon <> '' or self.location == 'TOP' or self.location == 'BOTTOM':
                return None
            elif self.height <> '':
                iWallHeight = self.height
            elif spaces[self.space].height <> '':
                iWallHeight = spaces[self.space].height
            else:
                if spaces[self.space].zoneType == 'PLENUM':
                    iWallHeight = (float(floors[self.floor].floorHeight) - float(floors[self.floor].spaceHeight))
                else:
                    if floors[self.floor].spaceHeight:
                        iWallHeight = floors[self.floor].spaceHeight
                    else: 
                        iWallHeight = floors[self.floor].floorHeight
            return float(iWallHeight)
        except:
            return None


    def testWall(self, xMin='-', xMax='-', yMin='-', yMax='-', wMin='-', wMax='-', hMin='-', hMax='-', regex='-', matchSpaces='-', verbose = 0): 
        result = True
        try:
            coords = self.returnCoords()
        except:
            coords = ''
        
        if not xMin=='-':
            if (coords[0] >= xMin) and (coords[1] >= xMin):
                if verbose:
                    print '    TRUE: coords %s are > %s xMin ' % (coords, xMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s xMin ' % (coords, xMin)
                result = False

        if not xMax=='-':
            if (coords[0] <= xMax) and (coords[1] <= xMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s xMax ' % (coords, xMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s xMax ' % (coords, xMax)
                result = False

        if not yMin=='-':
            if (coords[2] >= yMin) and (coords[3] >= yMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s yMin ' % (coords, yMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s yMin ' % (coords, yMin)
                result = False

        if not yMax=='-':
            if (coords[2] <= yMax) and (coords[2] <= yMax):
                if verbose:
                    print '    TRUE: coords %s are < %s yMax ' % (coords, yMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s yMax ' % (coords, yMax)
                result = False

        if not hMin=='-':
            if (self.returnHeight() >= hMin):
                if verbose:
                    print '    TRUE: coords %s are > %s hMin ' % (coords, hMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT > %s hMin ' % (coords, hMin)
                result = False

        if not hMax=='-':
            if (self.returnHeight() <= hMax):
                if verbose:
                    print '    TRUE: coords %s are <= %s hMax ' % (coords, hMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT <= %s hMax ' % (coords, hMax)
                result = False

        if not wMin=='-':
            if (self.returnWidth() >= wMin):
                if verbose:
                    print '    TRUE: coords %s are >= %s wMin ' % (coords, wMin)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT >= %s wMin ' % (coords, wMin)
                result = False

        if not wMax=='-':
            if (self.returnWidth() < wMax):
                if verbose:
                    print '    TRUE: coords %s are < %s wMax ' % (coords, wMax)
            else:
                if verbose:
                    print '    FALSE: coords %s are NOT < %s wMax ' % (coords, wMax)
                result = False



        if regex!='-':
            if re.search(regex, self.name):
                if verbose:
                    print '    TRUE: regex %s matches %s' % (regex, self.name)
            else:
                if verbose:
                    print '    FALSE: regex %s does not matche %s' % (regex, self.name)
                result = False

        if matchSpaces!='-':
            args = matchSpaces.split(',')
            if len(args) == 1 or args[1] == 'and':
                print args[0]
                if self.matchSpaces(args[0]):
                    print '    TRUE: regex %s space matched both %s and %s' % (self.name, self.space, self.nextTo)
                else:
                    print '    FALSE: regex %s did not match both %s and %s' % (self.name, self.space, self.nextTo)
                    result = False
            elif args[1] == 'or':
                if self.matchSpaces(args[0], t='or'):
                    print '    TRUE: regex %s space matched either %s or %s' % (self.name, self.space, self.nextTo)
                else:
                    print '    FALSE: regex %s space did not match either %s or %s' % (self.name, self.space, self.nextTo)
                    result = False
            else:
                print '    WARNING:: Did not understand args %s, no change administrered' % (','.join(args))
        

        return result
 





class Window:
    def __init__(self, name='', attributes=[], floor='', space='', wall=''):
    #def __init__(self, name, attributes, floor, space, wall):
        self.name = name
        self.active = 1
        self.wall = wall
        self.space = space
        self.floor = floor

        # define defaults
        self.glassType = ''
        self.x = ''
        self.y = ''
        self.width = ''
        self.height = ''
        self.frameWidth = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='GLASS-TYPE':
                self.glassType = attribute[1]
                found = 1
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='WIDTH':
                self.width = attribute[1]
                found = 1
            if attribute[0]=='FRAME-WIDTH':
                self.frameWidth = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)

    def returnTotalZ(self):
        wall = self.wall
        eWallHeight = eWalls[wall].returnTotalZ()
        eWallTilt = eWalls[wall].returnTilt()
        if self.y:
            y = float(self.y)
        else:
            y = 0
        z = eWallHeight + y * math.sin(math.radians(eWallTilt))
        return z

        
    def returnTotalX(self):
        space = self.space
        wall = self.wall
        wallWidth = eWalls[wall].returnWidth()
        wallX1 = eWalls[wall].returnX1()
        wallX2 = eWalls[wall].returnX2()
        if (wallX1 != None and wallX2 != None):
            if not self.x:
                xWin = 0.
            else:
                xWin = float(self.x)
            factor = xWin/wallWidth
            totalX = wallX1 + factor * (wallX2-wallX1)
            return totalX
        else:
            return None
        
        

    def returnTotalY(self):
            space = self.space
            wall = self.wall
            wallWidth = eWalls[wall].returnWidth()
            wallY1 = eWalls[wall].returnY1()
            wallY2 = eWalls[wall].returnY2()
            if (wallY1 != None and wallY2 != None):
                if not self.y:
                    yWin = 0.
                else:
                    yWin = float(self.y)
                factor = yWin/wallWidth
                totalY = wallY1 + factor * (wallY2-wallY1)
                return totalY
            else:
                return None

    def returnArea(self):
        try:
            area = float(self.height) * float(self.width)
            return area
        except:
            return None
        


    
    def returnTilt(self):
        wall = self.wall
        eWallTilt = eWalls[wall].returnTilt()
        return eWallTilt

    def returnAngle(self):
        wall = self.wall
        eWallAngle = eWalls[wall].returnAngle()
        return eWallAngle


    def moveWindow(self, x=0, y=0):

        if x:
            self.x = float(self.x) + float(x)
        if y:
            self.y = float(self.y) + float(y)

    def returnZoneType(self):
        space = self.space
        zt = spaces[space].returnZoneType()
        return zt



class Door:
    def __init__(self, name='', attributes=[], floor='', space='', wall=''):
    #def __init__(self, name, attributes, floor, space, wall):
        self.name = name
        self.active = 1
        self.wall = wall
        self.space = space
        self.floor = floor

        # define defaults
        self.glassType = ''
        self.x = ''
        self.y = ''
        self.width = ''
        self.height = ''
        self.frameWidth = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='X':
                self.x = attribute[1]
                found = 1
            if attribute[0]=='Y':
                self.y = attribute[1]
                found = 1
            if attribute[0]=='WIDTH':
                self.width = attribute[1]
                found = 1
            if attribute[0]=='HEIGHT':
                self.height = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)

    def returnTotalZ(self):
        wall = self.wall
        eWallHeight = eWalls[wall].returnTotalZ()
        eWallTilt = eWalls[wall].returnTilt()
        if self.y:
            y = float(self.y)
        else:
            y = 0
        z = float(eWallHeight) + y * math.sin(math.radians(eWallTilt))
        return z

    def returnTilt(self):
        wall = self.wall
        eWallTilt = eWalls[wall].returnTilt()
        return eWallTilt

    def returnAngle(self):
        wall = self.wall
        eWallAngle = eWalls[wall].returnAngle()
        return eWallAngle

    def returnArea(self):
        try:
            area = float(self.height) * float(self.width)
            return area
        except:
            return None

    def returnZoneType(self):
        space = self.space
        zt = spaces[space].returnZoneType()
        return zt

    def returnTotalX(self):
        try:
            space = self.space
            wall = self.wall
            wallWidth = eWalls[wall].returnWidth()
            wallX1 = eWalls[wall].returnX1()
            wallX2 = eWalls[wall].returnX2()
            if (wallX1 != None and wallX2 != None):
                if not self.x:
                    xWin = 0.
                else:
                    xWin = float(self.x)
                factor = xWin/wallWidth
                totalX = wallX1 + factor * (wallX2-wallX1)
                return totalX
            else:
                return None
        except:
            return None
        
        

    def returnTotalY(self):
        try:
            space = self.space
            wall = self.wall
            wallWidth = eWalls[wall].returnWidth()
            wallY1 = eWalls[wall].returnY1()
            wallY2 = eWalls[wall].returnY2()
            if (wallY1 != None and wallY2 != None):
                if not self.y:
                    yWin = 0.
                else:
                    yWin = float(self.y)
                factor = yWin/wallWidth
                totalY = wallY1 + factor * (wallY2-wallY1)
                return totalY
            else:
                return None
        except:
            return None


class Roof():

    def __init__(self):
        self.origin = 0

        self.azimuth = 0
        self.zMin = 0
        self.zMax = 0
        self.vertices = []
        self.tilt = 0



class System:
    def __init__(self, name='', attributes=[]):
        self.name = name
        self.active = 1

        # define defaults
        self.catch = []
        self.type = ''

        for attribute in attributes:
            found = 0
            if attribute[0]=='TYPE':
                self.type = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)
        
    def listZones(self, zones):
        for zone in zones:
            if zones[zone].system == self.name:
                print zone

    def returnZones(self, zones):
        returnZones = []
        for zone in zones:
            if zones[zone].system == self.name:
                returnZones.append(zone)
        return(returnZones)


class Zone:
    def __init__(self, name='', attributes=[], system=''):
        self.name = name
        self.active = 1
        self.system = system

        # define defaults
        self.type = ''
        self.catch = []

        for attribute in attributes:
            found = 0
            if attribute[0]=='TYPE':
                self.type = attribute[1]
                found = 1
            if attribute[0]=='SPACE':
                self.space = attribute[1]
                found = 1
            if found == 0:
                self.catch.append(attribute)
        