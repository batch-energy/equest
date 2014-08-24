# test2

# writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, elemToSystemSection, systems, zones, endingSection): 
def writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection): 
    print '\nwriting file...'
    
    ####################
    ## Write Out File ##
    ####################

    fout = open(inpFile, "w")

    
    for line in beginingSection:
        fout.write(line)
    
    for polygon in sorted(polygons.keys()):
        #write name
        writeLine = ('%s = POLYGON\n') % (polygons[polygon].name)
        fout.write(writeLine)
    
        #write vertices
        currentVerticy = 1
        for verticy in polygons[polygon].vertices:
            fout.write('   V%s = ( %s, %s )\n' % (currentVerticy, verticy[0], verticy[1]))
            currentVerticy = currentVerticy + 1
    
        #write delimeter
        polygonWriteLine ='   ..\n'
        fout.write(polygonWriteLine)
    
    
    #write polygon to element section
    for line in polyToElemSection:
        fout.write(line)

    
    
    #write elements
    
    #write floors
    for floor in sorted(floors.keys()):
    #for floor in floors:
        
        writeLine = ('%s = FLOOR\n' % floors[floor].name)
        fout.write(writeLine)
    
        if floors[floor].z <> '':
            writeLine = ('   Z                = %s\n') % floors[floor].z
            fout.write(writeLine)
        if floors[floor].shape <> '':
            writeLine = ('   SHAPE            = %s\n') % (floors[floor].shape)
            fout.write(writeLine)
        if floors[floor].floorHeight <> '':
            writeLine = ('   FLOOR-HEIGHT     = %s\n') % floors[floor].floorHeight
            fout.write(writeLine)
        if floors[floor].spaceHeight <> '':
            writeLine = ('   SPACE-HEIGHT     = %s\n') % floors[floor].spaceHeight
            fout.write(writeLine)
        if floors[floor].polygon <> '':
            writeLine = ('   POLYGON          = %s\n') % floors[floor].polygon
            fout.write(writeLine)
        if floors[floor].catch <> []:
            for caught in floors[floor].catch:
                writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                fout.write(writeLine)
        fout.write('   ..\n')
    
        # write spaces
        floorSpaces = floors[floor].returnSpaces(spaces)
        floorSpacesSorted = sorted(floorSpaces)
        #print floorSpacesSorted
        #for space in sorted(floorSpaces.keys()):
        for space in floorSpacesSorted:
            #print space
            writeLine = ('%s = SPACE\n') % spaces[space].name
            fout.write(writeLine)
    
            if spaces[space].shape <> '':
                writeLine = ('   SHAPE            = %s\n') % spaces[space].shape
                fout.write(writeLine)
            if spaces[space].zoneType <> '':
                writeLine = ('   ZONE-TYPE        = %s\n') % spaces[space].zoneType
                fout.write(writeLine)
            if spaces[space].polygon <> '':
                writeLine = ('   POLYGON          = %s\n') % spaces[space].polygon
                fout.write(writeLine)
            if spaces[space].x <> '':
                writeLine = ('   X                = %s\n') % spaces[space].x
                fout.write(writeLine)
            if spaces[space].y <> '':
                writeLine = ('   Y                = %s\n') % spaces[space].y
                fout.write(writeLine)
            if spaces[space].height <> '':
                writeLine = ('   HEIGHT           = %s\n') % spaces[space].height
                fout.write(writeLine)
            if spaces[space].z <> '':
                writeLine = ('   Z                = %s\n') % spaces[space].z
                fout.write(writeLine)
            if spaces[space].activity <> '':
                writeLine = ('   C-ACTIVITY-DESC  = %s\n') % spaces[space].activity
                fout.write(writeLine)
            if spaces[space].catch <> []:
                for caught in spaces[space].catch:
                    writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                    fout.write(writeLine)
            fout.write('   ..\n')
    
    
            #write exterior walls
            spaceEWalls = spaces[space].returnEWalls(eWalls) 
            spaceEWallsSorted = sorted(spaceEWalls)
            #for eWall in sorted(spaceEWalls.keys()):
            for eWall in spaceEWallsSorted:
                writeLine = ('%s = EXTERIOR-WALL\n') % eWalls[eWall].name
                fout.write(writeLine)
    
                if eWalls[eWall].x <> '':
                    writeLine = ('   X                = %s\n') % eWalls[eWall].x
                    fout.write(writeLine)
                if eWalls[eWall].y <> '':
                    writeLine = ('   Y                = %s\n') % eWalls[eWall].y
                    fout.write(writeLine)
                if eWalls[eWall].z <> '':
                    writeLine = ('   Z                = %s\n') % eWalls[eWall].z
                    fout.write(writeLine)
                if eWalls[eWall].width <> '':
                    writeLine = ('   WIDTH            = %s\n') % eWalls[eWall].width
                    fout.write(writeLine)
                if eWalls[eWall].construction <> '':
                    writeLine = ('   CONSTRUCTION     = %s\n') % eWalls[eWall].construction
                    fout.write(writeLine)
                if eWalls[eWall].location <> '':
                    writeLine = ('   LOCATION         = %s\n') % eWalls[eWall].location
                    fout.write(writeLine)
                if eWalls[eWall].polygon <> '':
                    writeLine = ('   POLYGON          = %s\n') % eWalls[eWall].polygon
                    fout.write(writeLine)
                if eWalls[eWall].shape <> '':
                    writeLine = ('   SHAPE            = %s\n') % eWalls[eWall].shape
                    fout.write(writeLine)
                if eWalls[eWall].tilt <> '':
                    writeLine = ('   TILT             = %s\n') % eWalls[eWall].tilt
                    fout.write(writeLine)
                if eWalls[eWall].height <> '':
                    writeLine = ('   HEIGHT           = %s\n') % eWalls[eWall].height
                    fout.write(writeLine)
                if eWalls[eWall].azimuth <> '':
                    writeLine = ('   AZIMUTH          = %s\n') % eWalls[eWall].azimuth
                    fout.write(writeLine)
                if len(eWalls[eWall].catch) > 0:
                    for caught in eWalls[eWall].catch:
                        writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                        fout.write(writeLine)
                fout.write('   ..\n')
                        
                #write windows
                eWallWindows = eWalls[eWall].returnWindows(windows) 
                #for window in sorted(eWallWindows.keys()):
                eWallWindowsSorted = sorted(eWallWindows)
                for window in eWallWindowsSorted:
                    writeLine = ('%s = WINDOW\n') % (windows[window].name)
                    fout.write(writeLine)
                    #print window width : %s % 
    
    
                    if windows[window].x <> '':
                        writeLine = ('   X                = %s\n') % windows[window].x
                        fout.write(writeLine)
                    if windows[window].y <> '':
                        writeLine = ('   Y                = %s\n') % windows[window].y
                        fout.write(writeLine)
                    if windows[window].width <> '':
                        writeLine = ('   WIDTH            = %s\n') % windows[window].width
                        fout.write(writeLine)
                    if windows[window].height <> '':
                        writeLine = ('   HEIGHT           = %s\n') % windows[window].height
                        fout.write(writeLine)
                    if windows[window].glassType <> '':
                        writeLine = ('   GLASS-TYPE       = %s\n') % windows[window].glassType
                        fout.write(writeLine)
                    if windows[window].frameWidth <> '':
                        writeLine = ('   FRAME-WIDTH      = %s\n') % windows[window].frameWidth
                        fout.write(writeLine)
                    if windows[window].catch <> []:
                        for caught in windows[window].catch:
                            writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                            fout.write(writeLine)
                    fout.write('   ..\n')


                #write doors
                eWallDoors = eWalls[eWall].returnDoors(doors) 
                #for door in sorted(eWallDoors.keys()):
                eWallDoorsSorted = sorted(eWallDoors)
                for door in eWallDoorsSorted:
                    writeLine = ('%s = DOOR\n') % (doors[door].name)
                    fout.write(writeLine)
                    #print door width : %s % 
    
    
                    if doors[door].x <> '':
                        writeLine = ('   X                = %s\n') % doors[door].x
                        fout.write(writeLine)
                    if doors[door].y <> '':
                        writeLine = ('   Y                = %s\n') % doors[door].y
                        fout.write(writeLine)
                    if doors[door].width <> '':
                        writeLine = ('   WIDTH            = %s\n') % doors[door].width
                        fout.write(writeLine)
                    if doors[door].height <> '':
                        writeLine = ('   HEIGHT           = %s\n') % doors[door].height
                        fout.write(writeLine)
                    if doors[door].catch <> []:
                        for caught in doors[door].catch:
                            writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                            fout.write(writeLine)
                    fout.write('   ..\n')

    
    
            #write underground walls
            spaceUWalls = spaces[space].returnUWalls(uWalls) 
            #for uWall in sorted(spaceUWalls.keys()):
            spaceUWallsSorted = sorted(spaceUWalls)
            for uWall in spaceUWallsSorted:
                writeLine = ('%s = UNDERGROUND-WALL\n') % uWalls[uWall].name
                fout.write(writeLine)
    
                if uWalls[uWall].width <> '':
                    writeLine = ('   WIDTH            = %s\n') % uWalls[uWall].width
                    fout.write(writeLine)
                if uWalls[uWall].construction <> '':
                    writeLine = ('   CONSTRUCTION     = %s\n') % uWalls[uWall].construction
                    fout.write(writeLine)
                if uWalls[uWall].location <> '':
                    writeLine = ('   LOCATION         = %s\n') % uWalls[uWall].location
                    fout.write(writeLine)
                if uWalls[uWall].polygon <> '':
                    writeLine = ('   POLYGON          = %s\n') % uWalls[uWall].polygon
                    fout.write(writeLine)
                if uWalls[uWall].shape <> '':
                    writeLine = ('   SHAPE            = %s\n') % uWalls[uWall].shape
                    fout.write(writeLine)
                if uWalls[uWall].x <> '':
                    writeLine = ('   X                = %s\n') % uWalls[uWall].x
                    fout.write(writeLine)
                if uWalls[uWall].y <> '':
                    writeLine = ('   Y                = %s\n') % uWalls[uWall].y
                    fout.write(writeLine)
                if uWalls[uWall].z <> '':
                    writeLine = ('   Z                = %s\n') % uWalls[uWall].z
                    fout.write(writeLine)
                if uWalls[uWall].tilt <> '':
                    writeLine = ('   TILT             = %s\n') % uWalls[uWall].tilt
                    fout.write(writeLine)
                if uWalls[uWall].height <> '':
                    writeLine = ('   HEIGHT           = %s\n') % uWalls[uWall].height
                    fout.write(writeLine)
                if uWalls[uWall].azimuth <> '':
                    writeLine = ('   AZIMUTH          = %s\n') % uWalls[uWall].azimuth
                    fout.write(writeLine)
                if len(uWalls[uWall].catch) > 0:
                    for caught in uWalls[uWall].catch:
                        writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                        fout.write(writeLine)
                fout.write('   ..\n')
    
    
            #write interior walls
            spaceIWalls = spaces[space].returnIWalls(iWalls) 
            spaceIWallsSorted = sorted(spaceIWalls)
            for iWall in spaceIWallsSorted:
                writeLine = ('%s = INTERIOR-WALL\n') % iWalls[iWall].name
                fout.write(writeLine)
    
                if iWalls[iWall].width <> '':
                    writeLine = ('   WIDTH            = %s\n') % iWalls[iWall].width
                    fout.write(writeLine)
                if iWalls[iWall].construction <> '':
                    writeLine = ('   CONSTRUCTION     = %s\n') % iWalls[iWall].construction
                    fout.write(writeLine)
                if iWalls[iWall].location <> '':
                    writeLine = ('   LOCATION         = %s\n') % iWalls[iWall].location
                    fout.write(writeLine)
                if iWalls[iWall].polygon <> '':
                    writeLine = ('   POLYGON          = %s\n') % iWalls[iWall].polygon
                    fout.write(writeLine)
                if iWalls[iWall].shape <> '':
                    writeLine = ('   SHAPE            = %s\n') % iWalls[iWall].shape
                    fout.write(writeLine)
                if iWalls[iWall].x <> '':
                    writeLine = ('   X                = %s\n') % iWalls[iWall].x
                    fout.write(writeLine)
                if iWalls[iWall].y <> '':
                    writeLine = ('   Y                = %s\n') % iWalls[iWall].y
                    fout.write(writeLine)
                if iWalls[iWall].z <> '':
                    writeLine = ('   Z                = %s\n') % iWalls[iWall].z
                    fout.write(writeLine)
                if iWalls[iWall].tilt <> '':
                    writeLine = ('   TILT             = %s\n') % iWalls[iWall].tilt
                    fout.write(writeLine)
                if iWalls[iWall].height <> '':
                    writeLine = ('   HEIGHT           = %s\n') % iWalls[iWall].height
                    fout.write(writeLine)
                if iWalls[iWall].azimuth <> '':
                    writeLine = ('   AZIMUTH          = %s\n') % iWalls[iWall].azimuth
                    fout.write(writeLine)
                if iWalls[iWall].nextTo <> '':
                    writeLine = ('   NEXT-TO          = %s\n') % iWalls[iWall].nextTo
                    fout.write(writeLine)
                if len(iWalls[iWall].catch) > 0:
                    for caught in iWalls[iWall].catch:
                        writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                        fout.write(writeLine)
                fout.write('   ..\n')

    for line in elemToSystemSection:
        fout.write(line)


    for system in sorted(systems.keys()):
        #print systems.keys()        
        writeLine = ('%s = SYSTEM\n' % systems[system].name)
        fout.write(writeLine)
    
        if systems[system].type <> '':
            writeLine = ('   TYPE             = %s\n') % systems[system].type
            fout.write(writeLine)    
        if len(systems[system].catch) > 0:
            for caught in systems[system].catch:
                writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                fout.write(writeLine)
        fout.write('   ..\n')
    
        systemZones = systems[system].returnZones(zones)
        #print systemZones
        systemZoneSorted = sorted(systemZones)
        for zone in systemZoneSorted:
            # test for instances
            try:
                if zones[zone].type <> '':
                    pass
                if zones[zone].space <> '':
                    pass
                if len(zones[zone].catch) > 0:
                    pass

                writeLine = ('%s = ZONE\n') % zones[zone].name
                fout.write(writeLine)

                if zones[zone].type <> '':
                    writeLine = ('   TYPE             = %s\n') % zones[zone].type
                    fout.write(writeLine)    
                if zones[zone].space <> '':
                    writeLine = ('   SPACE            = %s\n') % zones[zone].space
                    fout.write(writeLine)    
                if len(zones[zone].catch) > 0:
                    for caught in zones[zone].catch:
                        writeLine = ('   %s %s = %s\n') % (caught[0], (15 - len(caught[0]))*' ',  caught[1])
                        fout.write(writeLine)
                fout.write('   ..\n')
            except:
                pass
            

    
    
    #write end section
    for line in endingSection:
        fout.write(line)

    fout.close()

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

def writeXlFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection): 
    print '\nwriting excel file...'
    
    
    ####################
    ## Write Out File ##
    ####################

    xlFile = inpFile[:-4] + '.xls'
    if os.path.exists(xlFile):
        try:
            os.remove(xlFile)
        except:
            print 'cannot delete file %s' % xlFile
            sys.exit()

    print xlFile
    wb = xlwt.Workbook()
    
    wsText = wb.add_sheet('text')
    wsPolygons = wb.add_sheet('polygons')
    wsFloors = wb.add_sheet('floors')
    wsSpaces = wb.add_sheet('spaces')
    wsEWalls = wb.add_sheet('eWalls')
    wsIWalls = wb.add_sheet('iWalls')
    wsUWalls = wb.add_sheet('uWalls')
    wsWindows = wb.add_sheet('windows')
    wsDoors = wb.add_sheet('doors')
    wsZones = wb.add_sheet('zones')
    wsSystems = wb.add_sheet('systems')
    
    ### Write Plain Text ###

    c = 0
    for line in beginingSection:
        wsText.write(c,0,line)
        c += 1

    wsText.write(c,0,'>< delimiter ><')
    c+=1
        
    for line in polyToElemSection:
        wsText.write(c,0,line)
        c += 1
    
    wsText.write(c,0,'>< delimiter ><')
    c+=1

    for line in elemToSystemSection:
        wsText.write(c,0,line)
        c += 1

    wsText.write(c,0,'>< delimiter ><')
    c+=1

    for line in endingSection:
        wsText.write(c,0,line)
        c += 1

    ### Write Polygons ###

    c = 0    
    for polygon in sorted(polygons.keys()):
        
        wsPolygons.write(c,0,'%s' % (polygons[polygon].name))
        c += 1
    
        #write vertices
        currentVerticy = 1
        for verticy in polygons[polygon].vertices:
            wsPolygons.write(c,0, verticy[0])
            wsPolygons.write(c,1, verticy[1])
            c += 1
            currentVerticy = currentVerticy + 1
    
    ### Write Floors ###
    
    # sample write:  wsSpaces.write(r, headings.index(attr), value)
    
    order = ['name', 'floor', 'space', 'wall', 'spaceHeight', 'floorHeight', 'location', 'nextTo', 'x', 'y', 'z', 'height', 'width', 'construction', 'glassType']
    
    ### Write Floors ###

    methods = []
    #order = ['name', 'z', 'spaceHeight', 'floorHeight']
    references = []
    t = makeObjectTable(floors, methods, order, references)
    shoot(wsFloors, t) 

    ### Write Spaces ###
    
    #order = ['name', 'trueZ', 'trueHeight']
    methods = ['trueZ', 'trueHeight', 'countVertices', 'countEWalls', 'countUWalls', 'countIWalls']  
    references = []
    t = makeObjectTable(spaces, methods, order, references)
    shoot(wsSpaces, t) 

    
    ### Write Ewalls ###
    
    #order = ['name']
    methods = ['countWindows', 'countDoors', 'returnTotalZ', 'returnTilt', 'returnXMin', 'returnXMax', 'returnYMin', 'returnYMax', 'returnHeight', 'returnWidth', 'area', 'returnAngle', 'returnZoneType']
    references = ['floor']
    t = makeObjectTable(eWalls, methods, order, references)
    shoot(wsEWalls, t) 

    ### Write Iwalls ###

    #order = ['name']
    methods = ['returnTotalZ', 'returnHeight', 'returnTilt', 'returnXMin', 'returnXMax', 'returnYMin', 'returnYMax']
    references = ['floor']
    t = makeObjectTable(iWalls, methods, order, references)
    shoot(wsIWalls, t) 


    ### Write Uwalls ###

    #order = ['name']
    methods = ['returnTotalZ', 'returnTilt', 'returnXMin', 'returnXMax', 'returnYMin', 'returnYMax', 'returnHeight', 'returnWidth', 'area', 'returnAngle', 'returnZoneType']   
    references = ['floor']
    t = makeObjectTable(uWalls, methods, order, references)
    shoot(wsUWalls, t) 

    ### Write Windows ###
    
    #order = ['name']
    methods = ['returnTotalZ', 'returnTilt', 'returnAngle', 'returnZoneType', 'returnTotalX', 'returnTotalY', 'returnArea']
    references = ['floor', 'space', 'eWall']
    t = makeObjectTable(windows, methods, order, references)
    shoot(wsWindows, t) 

    ### Write Doors ###

    #order = ['name']
    methods = ['returnTotalZ', 'returnTilt', 'returnAngle', 'returnZoneType', 'returnTotalX', 'returnTotalY', 'returnArea']
    references = ['floor', 'space', 'eWall']
    t = makeObjectTable(doors, methods, order, references)
    shoot(wsDoors, t) 

    ### Write Systmes ###
    
    #order = ['name']
    methods = []
    references = []
    t = makeObjectTable(systems, methods, order, references)
    shoot(wsSystems, t) 

    ### Write Zones ###
    
    #order = ['name']
    methods = []
    references = []
    t = makeObjectTable(zones, methods, order, references)
    shoot(wsZones, t) 

    wb.save(xlFile)



def readXlFile(inpFile):
    xlFile = inpFile[:-4] + '.xls'
    if not os.path.exists(xlFile):
        print 'no file found'
        sys.exit()
    
    f = 'BatchDemo.xls'
    wb = xlrd.open_workbook(f)    

    for sheet in wb.sheets():
        if sheet.name == 'text':
            t = ''
            for rx in range(sheet.nrows):
                t += sheet.row(rx)[0].value
            beginingSection, polyToElemSection, elemToSystemSection, endingSection = t.split('>< delimiter ><')
        
        elif sheet.name == 'polygons':
            c = 0
            for rx in range(sheet.nrows):
            
                l = sheet.row(rx)[0].value
            
                if l.find(sheet.row(rx)[0].value) > -1:
                    # append PREVIOUS polygon
                    if c != 0:
                        polygons[polygonName]=Polygon(name=polygonName, vertices=vertices)
                    vertices=[]
                    polygonName = sheet.row(rx)[0].value
                else:
                    verticyX = sheet.row(rx)[0].value
                    verticyY = sheet.row(rx)[1].value
                    verticy = [verticyX, verticyY]
                    vertices.append(verticy)
                c += 1
            polygons[polygonName]=Polygon(name=polygonName, vertices=vertices)
            
      
        else:
            sheetName = sheet.name
            headings = []
            dataTypes = []
            for heading in sheet.row(0):
                 headings.append(heading.value)
            for dataType in sheet.row(1):
                 dataTypes.append(dataType.value)
            c = 0
            print
            print sheetName
            print headings
            print dataTypes

            r = 0
            for rx in range(sheet.nrows):
            
                if r != 0 and r != 1:
                     cellValues = []
                     for cell in sheet.row(rx):
                         cellValues.append(cell.value)
                     
                     c = 0
                     name = cellValues[headings.index('name')]
                     objName = sheetName[0].upper() + sheetName[1:-1]
                     
                     cmd = '%s[%s]=%s(name=%s)' % (sheetName, name, objName, name)
                     print cmd

                     exec cmd
                     for cellValue in cellValues:
                         attr = headings[c]
                         dt = dataTypes[c]
                         if dt == 'reference' or dt == 'attribute' and cellValue and attr != 'name':
                             try:
                                 cmd = "%s[%s].%s='%s'" % (sheetName, name, attr, str(cellValue))
                                 print 'trying %s' % cmd
                                 exec cmd
                                 print '  success', cmd
                             except:
                                 print '  catching...'
                                 temp = [attr, cellValue]
                                 print '   ', temp
                                 exec '%s[%s].catch.append(%s)' % (sheetName, name, temp)
                         c+=1
                r += 1
      

         
     


def shoot(sheet, t):
    rc = 0
    for r in t:
        cc = 0
        for c in r:
            sheet.write(rc, cc, c)
            cc += 1
        rc += 1
    


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





def parseInp(inpFile):
    f = open(inpFile, "r")
    file = f.readlines()
    
    ####################
    ## Read and Parse ##
    ####################
    
    lineNumber = 0
    startLookingForFloors = 0
    startLookingForSystems = 0
    for line in file:
    
        lineNumber += 1
    
        #Polygon Start
        if line == '$              Polygons\n':
            polyStart = (lineNumber + 2)
    
        #Polygon End
        if line == '$              Wall Parameters\n':
            polyEnd = (lineNumber - 2)
    
        #Element Start
        if line == '$ **      Floors / Spaces / Walls / Windows / Doors      **\n':
            startLookingForFloors = 1
            defaultElementStart = (lineNumber + 2)
        if (startLookingForFloors ==1) and (line.strip()[-7:] == '= FLOOR'):
            elementStart = (lineNumber - 1)
            startLookingForFloors = 0
            
        #Element End
        if line == '$ **                Performance Curves                   **\n':
            elementEnd = (lineNumber - 3)
    
        #System Start
        if line == '$ **               HVAC Systems / Zones                  **\n':
            startLookingForSystems = 1
        if (startLookingForSystems ==1) and (line.strip()[-8:] == '= SYSTEM'):
            systemStart = (lineNumber - 1)
            startLookingForSystems = 0
            
        #System End
        if line == '$ **                Metering & Misc HVAC                 **\n':
            systemEnd = (lineNumber - 3)
    
    beginingSection = file[:polyStart]
    polygonSection = file[polyStart:polyEnd]
    polyToElemSection = file[polyEnd:elementStart]
    elementSection = file[elementStart:elementEnd]
    elemToSystemSection = file[elementEnd:systemStart]
    systemSection = file[systemStart:systemEnd]
    endingSection = file[systemEnd:]
    elementDefaultSection = file[defaultElementStart:elementStart]  #non contiguous, auxilary sections
    
    return [beginingSection, polygonSection, polyToElemSection, elementSection, elemToSystemSection, systemSection, endingSection, elementDefaultSection]
    

def debug(s, f='debug.log', d=0, p=0):
    #print s
    s = " "*d + str(s)
    debug = open(f,'a')
    debug.write('%s\n' % s)
    debug.close()
    if p:
        print s


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


def spaceVerticalOverlap(space1, space2):
    l1 = (spaces[space1].trueZ())
    u1 = l1 + spaces[space1].trueHeight()
    l2 = (spaces[space2].trueZ())
    u2 = l2 + spaces[space2].trueHeight()
    u = min(u1, u2)
    l = max(l1, l2)
    ol = u - l
    return ol




def createHorizontalInteriorWalls():
    activeSpaces = returnActiveElements(spaces)
    floorMatchTolerance = 1
    minimumArea = 3
    for activeSpace in sorted(activeSpaces):                        
        iWallNum = 0
        activeSpaceVertices = polygons[spaces[activeSpace].polygon].numericalVertices()
        activeSpacePolygon = Poly(activeSpaceVertices)
        for otherSpace in spaces:
            if abs((spaces[activeSpace].trueZ() + spaces[activeSpace].trueHeight()) - spaces[otherSpace].trueZ()) < floorMatchTolerance:
                otherSpaceVertices = polygons[spaces[otherSpace].polygon].numericalVertices()
                otherSpacePolygon = Poly(otherSpaceVertices)
                
                try:
                    intersection = activeSpacePolygon.intersection(otherSpacePolygon)
                except:
                    debug('ERROR: could not properly compare %s to %s' % (activeSpace, otherSpace))
                    debug(traceback.print_exc())
                    #time.sleep(2)

                polyList = []
                #debug('') 
                #debug(activeSpace)
                if type(intersection) == MultiPolygon:
                    for poly in intersection.geoms:
                        if poly.area > minimumArea:
                            polyList.append(poly)
                        else:
                            debug('INFO: polygon too small to count %s x %s' % (activeSpace, otherSpace))
                        
        
                elif type(intersection) == Poly:
                    if intersection.area > minimumArea:
                        polyList.append(intersection)
                    else:
                        debug('INFO: polygon too small to count %s x %s' % (activeSpace, otherSpace))
        
                else:
                    debug(  '\n   No polygon intersection')
                    debug(  '   %s' % otherSpace)
                
                for poly in polyList:
                    iWallNum += 1
                    name = '"%s-IT+B-%s"' % (spaces[activeSpace].name[1:-1], iWallNum)
                    
                    if spaces[activeSpace].floor == spaces[otherSpace].floor:
                        attributes = [['CONSTRUCTION', '"INTERIOR CEILING CONSTRUCTION"']]
                    else:
                        attributes = [['CONSTRUCTION', '"INTERIOR SLAB CONSTRUCTION"']]

                    iWalls[name]=IWall(name=name, attributes=attributes, floor=spaces[activeSpace].floor, space=spaces[activeSpace].name)
                    iWalls[name].location = 'TOP'
                    iWalls[name].nextTo = otherSpace 
                    debug(  '   create iwall %s next to %s' % (activeSpace, otherSpace))
                    
                    p = shapelyToEQuestPoly(poly)[0]
                    polygon = '"%s POLY"' % (name[1:-1])
                    polygons[polygon]=Polygon(name=polygon, vertices=p)
                    iWalls[name].polygon = polygon
                    debug(  '   create polygon %s' % polygon)
    
    



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



def splitInteriorWalls():
    print '\nsplitting interior walls...'
    activeSpaces = returnActiveElements(spaces)
    minimumVerticalOverlap = 1
    pointLineDistance = 1
    newPoints = []
    for space in activeSpaces:
        polygon = spaces[space].polygon
        shPolygon = eQuestToShapelyPoly(polygons[polygon].vertices)
        shLines = shapelyPolygonToShapelyLines(shPolygon)
        v = 0
        for otherSpace in activeSpaces:
            ol = spaceVerticalOverlap(space, otherSpace)        
            if ol > minimumVerticalOverlap:
                polygon2 = spaces[otherSpace].polygon
                v = 0
                for line in shLines:
                    shPoints = line.coords
                    p1 = Point(shPoints[0])
                    p2 = Point(shPoints[1])
                    v += 1
                    for v2 in polygons[polygon2].vertices:
                        v2p = Point(float(v2[0]),float(v2[1]))
                        dLine = line.distance(v2p)
                        d1 = p1.distance(v2p)
                        d2 = p2.distance(v2p)
                        dPoints = min(d1, d2)
                        
                        if dLine < pointLineDistance and dPoints > pointLineDistance:
                            #newPoints.append([v, d1, polygon, v2, polygon2, u1, l1, u2, l2])
                            newPoints.append([v, d1, polygon, v2, polygon2])

    newPoints.sort()
    if newPoints:
        last = newPoints[-1]
        for i in range(len(newPoints)-2, -1, -1):
            if last == newPoints[i]:
                del newPoints[i]
            else:
                last = newPoints[i]
        newPoints.sort(key=lambda x:x[1] )
        newPoints.sort(key=lambda x:x[0] )
        newPoints.reverse()
        newPoints.sort(key=lambda x:x[2] )
        

        for newPoint in newPoints:
            #print newPoint[0], newPoint[1], newPoint[2], newPoint[3]
            #print 'adding %s to %s at %s because of %s (%s, %s))' % (newPoint[3],newPoint[2],newPoint[0],newPoint[4],newPoint[5],newPoint[6])
            polygons[newPoint[2]].vertices.insert(newPoint[0],newPoint[3])

        for polygon in polygons:
           polygons[polygon].deleteSeqDupes()



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
    


def combineCloseVerticies():
    print '\ncombining close vertices...'
    
    #t = 1.2
    t = 2.0
    cols = {}
    c = 0
    combineColumns = []
    
    # loop through polys's vertices, check against existing dictionaries of coincident points
    for polygon in polygons:
        if polygons[polygon].active == 1:
            vNum = 0
            for v in polygons[polygon].vertices:
                foundCols = []
                for col in cols:
                    d = 9999
                    for colV in cols[col]:
                        d = min(pointDistance(v, colV[2]), d)
                    if d < t:
                        cols[col].append([polygon,vNum,v])
                        foundCols.append(col)
                if not foundCols:
                    c += 1
                    cols[c] = ([[polygon,vNum,v],])
                vNum += 1
                if len(foundCols) > 1:
                    #print '%s %s %s in more than one column' % (polygon,vNum,v)
                    combineColumns.append(foundCols)
                    #for foundCol in foundCols:
                        #print '   %s' % foundCol

    #for c in combineColumns:
    #   print c
    
    # combine cols with coincedent points
    for c in combineColumns:
        #print
        #print c
        if cols.has_key(c[1]):
            for colV in cols[c[1]]:
                #print colV
                if not colV in cols[c[0]]:
                    cols[c[0]].append(colV)
                    #print 'appended \n   %s to col %s\n   (%s)' % (colV, c[0], cols[c[0]])
                else:
                    pass
                    #print '%s already in col %s\n   (%s)' % (colV, col, cols[c[0]])
            #print 'deleting column %s\n   %s' % (c[1], cols[c[1]])
            del cols[c[1]]
    
    
    # move points to average
    f = open('debug.log', 'a')
    for col in cols:
        l = len(cols[col])
        if l > 1:
            x = 0
            y = 0
            for colV in cols[col]:
                x += float(colV[2][0])/float(l)
                y += float(colV[2][1])/float(l)
            
            cols[col].insert(0,[x,y])
            for colV in cols[col][1:]:
                newVerticy = cols[col][0]
                currentPolygon = colV[0]
                verticyNumber = colV[1]
                newVerticy = [x,y]
                currentVerticy = colV[2]
                for polygon in polygons:
                    if polygon == currentPolygon:
                        if currentVerticy != newVerticy:
                            polygons[polygon].vertices[verticyNumber] = newVerticy
                            f.write('changed %s(v%s) from %s to %s\n' % (currentPolygon, verticyNumber+1, currentVerticy, newVerticy))
                            f.write('   %s\n' % col)
                            for c in cols[col]:
                               f.write('   %s\n' % c)

    f.close()

    print '\ndeleting duplicate vertices...'
    
    #check for dupes
    for polygon in polygons:
       polygons[polygon].deleteDupes()

def combineCloseVerticies2(tol=1, minimumVerticalOverlap=1.0):
#    print '\ncombining close vertices...'
#    
#    # remove close vertices within polygons #THIS WAS ALREADY DONE IN POLGON CREATION
#    for polygon in polygons:
#    
#        vs = polygons[polygon].vertices
#        l = len(vs)
#        c = 0
#        popList = []
#        print polygon
#        print '  length %s' % l
#        for c in range(0,l-1):
#            v1 = vs[c]
#            v2 = vs[c+1]
#            if pointDistance(v1, v2) < tol:
#                popList.append(c)
#                print '  %s and %s close' % (c, c+1)
#        v1 = vs[c+1]
#        v2 = vs[0]
#        if pointDistance(v1, v2) < tol:
#            print '  %s and %s close' % (c+1, 0)
#            popList.append(c+1)
#        popList.sort()
#        popList.reverse()
#        for popItem in popList:
#            print 'removing verticy %s from %s' % (popItem, polygon)
#            polygons[polygon].vertices.pop(popItem)

    
    
    a = 1
    polyPairs = []
    donePolygons = []
    
    # find close polygons
    for polygon1 in polygons:
        donePolygons.append(polygon1)
        sPoly1 = eQuestToShapelyPoly(polygons[polygon1].vertices)
        for polygon2 in polygons:
            if (not polygon2 in donePolygons):
                sPoly2 = eQuestToShapelyPoly(polygons[polygon2].vertices)
                d = sPoly1.distance(sPoly2)
                if d < tol:
                    space1s = polygons[polygon1].spaceUse()
                    space2s = polygons[polygon2].spaceUse()
                    polysHaveOverlappingSpaces = 0
                    maxOverlap = 0
                    for space1 in space1s:
                        for space2 in space2s:
                            ol = spaceVerticalOverlap(space1, space2)
                            if ol > minimumVerticalOverlap:
                                 maxOverlap = max(ol, maxOverlap)
                                 polysHaveOverlappingSpaces = 1
                    if polysHaveOverlappingSpaces:
                        polyPairs.append([polygon1, polygon2])
                        print polygon1, polygon2

    # remove close vertices across polygons
    verticyStrings = []
    l = len(polyPairs)
    a = 1
    conflicts = []
    vPairs = []
    while a == 1:
        a = 0
        c = 0
        for polyPair in polyPairs:
            c += 1
            polygon1 = polyPair[0]
            polygon2 = polyPair[1]
            vNum1 = 0
            for v1 in polygons[polygon1].vertices:
                str1 = '%s:%s' % (polygon1, vNum1)
                vNum2 = 0
                for v2 in polygons[polygon2].vertices:
                    str2 = '%s:%s' % (polygon2, vNum2)
                    vd = pointDistance(v1, v2)
                    if vd < tol and vd > 0.001:
                        print '   combining %s:%s with %s:%s due to distance %s (%s/%s)' % (polygon1, vNum1+1, polygon2, vNum2+1, vd, c, l)
                        if str1 in verticyStrings and str2 in verticyStrings:
                            print '   conflict'
#                            xs = []
#                            ys = []
#                            updatePoints = []
#                            updatePoints.append(str1)
#                            updatePoints.append(str2)
#                            print '      searching through history for related points'
#                            for vPair in vPairs:
#                                
#                                vPairPoly1, vPairVert1 = vPair[0].split(':')
#                                vPairPoly2, vPairVert2 = vPair[1].split(':')
#
#                                if vPairPoly1 == polygon1 or vPairPoly1 == polygon2:
#                                    print '      found %s' % vPairPoly1
#                                    xs.append(polygons[vPairPoly1].vertices[vPairVert1][0])
#                                    ys.append(polygons[vPairPoly1].vertices[vPairVert1][1])
#                                    updatePoints.append(vPair[1])
#                                    print '      will update %s' % vPair[1]
#                                if vPairPoly2 == polygon1 or vPairPoly2 == polygon2:
#                                    print '      found %s' % vPairPoly2
#                                    xs.append(polygons[vPairPoly2].vertices[vPairVert2][0])
#                                    ys.append(polygons[vPairPoly2].vertices[vPairVert2][1])
#                                    updatePoints.append(vPair[0])
#                                    print '      will update %s' % vPair[0]
#                                    
#                                
#                            x = float(sum(xs)) / len(xs)
#                            y = float(sum(ys)) / len(ys)
#                            print '     new x for all: %s ' % x
#                            print '     new y for all: %s ' % y
#                            for updatePoint in updatePoints:
#                                print '     updating %s' % updatePoint
#                                p, v = updatePoint.split(':')
#                                polygons[p].vertices[v][0] = x
#                                polygons[p].vertices[v][1] = y
#
                        else:
                            #vPairs.append(str1, str2)
                            if str1 in verticyStrings:
                                xNew = polygons[polygon1].vertices[vNum1][0]
                                yNew = polygons[polygon1].vertices[vNum1][1]
                                verticyStrings.append(str2)

                            elif str2 in verticyStrings:
                                xNew = polygons[polygon2].vertices[vNum2][0]
                                yNew = polygons[polygon2].vertices[vNum2][1]
                                verticyStrings.append(str1)
                            else:
                                xNew = (float(v1[0]) + float(v2[0]))/2
                                yNew = (float(v1[1]) + float(v2[1]))/2
                                verticyStrings.append(str1)
                                verticyStrings.append(str2)
                            polygons[polygon1].vertices[vNum1][0] = xNew
                            polygons[polygon2].vertices[vNum2][0] = xNew
                            polygons[polygon1].vertices[vNum1][1] = yNew
                            polygons[polygon2].vertices[vNum2][1] = yNew
                        a = 1
                    vNum2 += 1
                if a == 1:
                    break
                vNum1 += 1
            if a == 1:
                break
    
    for conflict in conflicts:
        print conflict

    for polygon in polygons:
       polygons[polygon].deleteDupes()

def adjacentSpaces(space=None, tol=1, vTol=1):

    adjacentSpaces = []

    spaceZLow = spaces[space].trueZ()
    spaceZHigh = spaces[space].trueHeight() + spaceZLow
    spacePolygon = spaces[space].polygon
    spacePolygonVertices = polygons[spacePolygon].numericalVertices()
    spacePoly = Poly(spacePolygonVertices)

    for space2 in spaces:
        if space != space2:
            space2ZLow = spaces[space2].trueZ()
            space2ZHigh = spaces[space2].trueHeight() + space2ZLow
            space2Polygon = spaces[space2].polygon
            space2PolygonVertices = polygons[space2Polygon].numericalVertices()
            space2Poly = Poly(space2PolygonVertices)
    
            maxLow = max(spaceZLow, space2ZLow)
            minHigh = min(spaceZHigh, space2ZHigh)
            d = spacePoly.distance(space2Poly)
            
            if ((minHigh - maxLow) > vTol) and (d < tol):
                adjacentSpaces.append(space2)

    return adjacentSpaces

                                         
def combineCloseVerticies3(tol=1.25, vTol = 1):
    c = 0
    
    spaceGroups = []
    #spacesUsed = []

    spaceList = sorted(spaces.keys())
    print spaceList
    
    # go through all spaces as base space
    debug('Start combine clost vertices 3')
    spacesUsed =[]
    
    # loop to determine groups of space which share walls
    for space1 in spaceList:
        thisGroup = []
        workingList = []
        if space1 in spacesUsed:
            debug('Base space already used: %s' % space1, p=0) 
        else:
            debug('Base space being investigated: %s' % space1, p=0) 
            #spacesUsed.append(space1)
            workingList.append(space1)

            while len(workingList):
                debug('Current workingList: %s' % (workingList), d=2, p=0)
                workingSpace = workingList[0]
                thisGroup.append(workingSpace)
                debug('First space added to thisGroup: %s' % (workingSpace), d=2, p=0)
                workingList.remove(workingSpace)
                debug('Remaining working list: %s' % (workingList), d=2, p=0)
                adjacents = adjacentSpaces(workingSpace)
                debug('Found %s new adjacents to %s' % (len(adjacents), workingSpace), d=2, p=0)
                for adjacent in adjacents:
                    if not (adjacent in thisGroup) and not (adjacent in workingList):
                        workingList.append(adjacent)
            
            spaceGroups.append(thisGroup)
            
        spacesUsed += thisGroup
    
    # print spaces with shared walls
    c = 0
    for spaceGroup in spaceGroups:
        c += 1
        debug('Space Group %s' % c, p=0)
        for space in spaceGroup:
            debug('Space %s' % space, p=0, d=1)

    # create polygon groups
    polygonGroups = []
    for spaceGroup in spaceGroups:
        polygonGroup = []
        for space in spaceGroup:
            polygonGroup.append(spaces[space].polygon)
        polygonGroup = list(set(polygonGroup))
        polygonGroups.append(polygonGroup)
        
    
    polygonGroupNumber = 0
    # loop through polygon groups to fix clost vertices
    for polygonGroup in polygonGroups:
        polygonGroupNumber += 1
        debug('\n\n###################################\n')
        comboSets = {}
        
        for polygon in polygonGroup:
            debug('Looking at Polygon %s' % polygon, d=2, p=0)
            vNum = 1
            for verticy in polygons[polygon].vertices:
                addPoint = '%s:%s' % (polygon, vNum)
                addSet = []
                debug('Looking at Verticy %s' % addPoint, d=4, p=0)
                
                # loop through all comboSets
                for comboSet in comboSets:
                    debug('Comparing to ComboSet %s' % comboSet, d=6)
                    # loop through all  points in this combo set to see if we can add this point          
                    for comboPoint in comboSets[comboSet]:
                        debug('Comparing to ComboPoint %s' % comboPoint, d=8)
                        vd = pointDistance(verticy, comboSets[comboSet][comboPoint])
                        # add to combo set
                        if vd < tol:
                            foundComboSet = 1
                            addSet.append(comboSet)
                            debug('Found Matching ComboSet "%s" for %s' % (comboSet, addPoint), d=10)
                            break

    
                # if this piont can't be added, make a new set
                if len(addSet) > 1:
                    debug('Multiple ComboSets found for %s' % (addPoint), d=6, p=0)
                    
                elif len(addSet) == 1:
                     theAddSet = addSet[0]
                     comboSets[theAddSet][addPoint] = verticy
                     debug('Adding point %s to new  set "%s"\n   %s' % (addPoint, theAddSet, verticy), d=6, p=0)
                
                else:
                    c += 1
                    newSetName = 'set %s' % c
                    debug('Making new set "%s" ' % newSetName, d=6)
                    addPoint = '%s:%s' % (polygon, vNum)
                    comboSets[newSetName] = {}
                    debug('  adding point %s to new cobmo set\n   %s' % (addPoint, verticy), d=6, p=0)
                    comboSets[newSetName][addPoint] = verticy
    
                vNum +=1
         
        debug('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        debug('Changing vertices for polygon group %s' % polygonGroupNumber)
        for comboSet in comboSets:
            debug('Working with set %s' % comboSet, d=2)
            xTotal = 0.
            yTotal = 0.
            for verticy in comboSets[comboSet]:
                debug('adding contribution from %s' % verticy, d=4, p=0)
                x = float(comboSets[comboSet][verticy][0])
                y = float(comboSets[comboSet][verticy][1])
                xTotal += x
                yTotal += y
                debug('%s, %s, %s ' % (verticy, x, y), d=6, p=0)
            xAvg = xTotal/len(comboSets[comboSet])
            yAvg = yTotal/len(comboSets[comboSet])

            debug('-- Set average: %s, %s ' % (xAvg, yAvg) , d=4, p=0)
    
            debug('Changing vertices for polygon group %s' % polygonGroupNumber)
            
            for verticy in comboSets[comboSet]:
                debug('Changing vertices for polygon group %s, verticy %s' % (polygonGroupNumber, verticy))
                polygon = verticy.split(':')[0]
                vNum = int(verticy.split(':')[1])
                polygons[polygon].vertices[vNum-1][0] = xAvg
                polygons[polygon].vertices[vNum-1][1] = yAvg
    
    for polygon in polygons:
        polygons[polygon].deleteSeqDupes()        

             


def createZones():
    print '\ncreating zones...'

    activeSpaces = returnActiveElements(spaces)
    addedZone = []
    for space in activeSpaces:
        zoneName = '"%s ZONE"' % space[1:-1]
        #print '----------------'
        #print 'Adding zone %s' % (zoneName)
        #print '----------------'                        
        zones[zoneName]=Zone(zoneName, '', '"Dummy System"')
        #print 'System: %s' % zones[zoneName].system
        if spaces[space].zoneType == 'PLENUM':
            zones[zoneName].type = 'PLENUM'
            #print 'Type: PLENUM'
        else:
            zones[zoneName].type = 'CONDITIONED'
            #print 'Type: CONDITIONED'
        zones[zoneName].space = '%s' % space
        #print 'Space: %s' % space

def createInteriorAndExteriorWalls(ugThreshold=''):
    print '\ncreating interior and exterior walls...'
    minimumVerticalOverlap = 1
    maximumHorizontalDistance = 1
    minimumLineDistance = 1
    maximumPointDifferenceTolerance = 1
    badSpaces = []
    intWalls = []
    sameSpaceWalls = []
    reverseIntWall = []
    intWallsShort = []
    extWalls = []
    # angleTolerance = 2.5 # controled by formula below
    activeElements = returnActiveElements(spaces)
    
    # determining which space edges have interior walls
    
    # loop through spaces
    for space in activeElements:
        #loop through other spaces
        for otherSpace in spaces:
            #get global upper and lower vertical for spaces
            
            
            u = min((spaces[space].trueZ() + spaces[space].trueHeight()),(spaces[otherSpace].trueZ() + spaces[otherSpace].trueHeight()))
            l = max((spaces[space].trueZ()),(spaces[otherSpace].trueZ()))
            
            # ##### u and l not calculating properly!
            
            #loop only if the spaces overlap vertically
            if (u - l) > minimumVerticalOverlap:
                
                # nitty gritty details
                spaceVerticesEquest = polygons[spaces[space].polygon].vertices
                otherSpaceVerticesEquest = polygons[spaces[otherSpace].polygon].vertices
                spacePolygonShapely = eQuestToShapelyPoly(spaceVerticesEquest)
                otherSpacePolygonShapely = eQuestToShapelyPoly(otherSpaceVerticesEquest)
                polygonDistance = spacePolygonShapely.distance(otherSpacePolygonShapely)

                # loop only if spaces are close 
                if polygonDistance < maximumHorizontalDistance:
                
                    spaceLSs = shapelyPolygonToShapelyLines(spacePolygonShapely)
                    otherSpaceLSs = shapelyPolygonToShapelyLines(otherSpacePolygonShapely)
                    l1 = 0

                    # loop through space linestrings
                    for spaceLS in spaceLSs:
                        l1 += 1
                        spaceLSAngle = shapelyLineStringAngle(spaceLS)
                        l2 = 0

                        # loop through other space linestrings
                        for otherSpaceLS in otherSpaceLSs:
                            l2 += 1
                            otherSpaceLSAngle = shapelyLineStringAngle(otherSpaceLS)
                            d = spaceLS.distance(otherSpaceLS)
                            angleTolerance = (2./max(d,1))**0.5*10.
                            oad = oppositeAngleDistance(spaceLSAngle,otherSpaceLSAngle)
                            # see if the walls and angles are withing tolerance
                            if (oad < angleTolerance) and (d < minimumLineDistance):
                                # make sure the walls are actually adjacent, not just coincidnet in one point
                                if not (min(pointDistance(spaceLS.coords[0], otherSpaceLS.coords[0]),pointDistance(spaceLS.coords[1], otherSpaceLS.coords[1])) < maximumPointDifferenceTolerance):
                                #if not (min(pointDistance(spaceLS.coords[0], otherSpaceLS.coords[1]),pointDistance(spaceLS.coords[1], otherSpaceLS.coords[0])) < maximumPointDifferenceTolerance):
                                    maxPointDistance = max(pointDistance(spaceLS.coords[0], otherSpaceLS.coords[1]),pointDistance(spaceLS.coords[1], otherSpaceLS.coords[0]))
                                    # see if there the walls are exhustive of each others coincidence
                                    if maxPointDistance > maximumPointDifferenceTolerance:
                                        reverseSpace = [otherSpace[1:-1], l2, space[1:-1], l1]
                                        # don't want to count errors twice!
                                        if reverseSpace in badSpaces:
                                            pass
                                            #print '    skipping %s:%s  %s:%s because it already exists\n' % (space, l1, otherSpace, l2)
                                        else:
                                            badSpaces.append([space[1:-1], l1, otherSpace[1:-1], l2])
                                            print '  %s/%s' % (space, otherSpace)
                                            print '  %s to %s' % (l1, l2)
                                            print '    dist = %s' % (d)
                                            print '    oad = %s' % (oad)
                                            print '    l1 = %s,%s  %s,%s  %s' % (shapelyLineToRoundedVertices(spaceLS)[0][0], shapelyLineToRoundedVertices(spaceLS)[0][1], shapelyLineToRoundedVertices(spaceLS)[1][0], shapelyLineToRoundedVertices(spaceLS)[1][1], spaceLSAngle)
                                            print '    l2 = %s,%s  %s,%s  %s' % (shapelyLineToRoundedVertices(otherSpaceLS)[0][0], shapelyLineToRoundedVertices(otherSpaceLS)[0][1], shapelyLineToRoundedVertices(otherSpaceLS)[1][0], shapelyLineToRoundedVertices(otherSpaceLS)[1][1], otherSpaceLSAngle)
                                            print '    max pt dist = %s' % maxPointDistance
                                            print '    u = %s' % u
                                            print '    l = %s\n' % l
                                    else:
                                        # don't want to count walls twice!
                                        reverseIntWall = [otherSpace, l2, space, l1, u, l]
                                        if reverseIntWall in intWalls:
                                            pass
                                            #print  '    skipping %s:%s  %s:%s because it already exists\n' % (space, l1, otherSpace, l2)
                                        else:
                                            # no interior walls between a space and itself
                                            if space == otherSpace:
                                                sameSpaceWalls.append([space, l1])
                                                sameSpaceWalls.append([otherSpace, l2])
                                            # append interior wall list
                                            else:
                                                intWalls.append([space, l1, otherSpace, l2, u, l])

    if badSpaces:
        print '\n*** found bad spaces ***'
        time.sleep(3)
        for badSpace in badSpaces:
            print '%s:%s  %s:%s' % (badSpace[0],badSpace[1],badSpace[2],badSpace[3])
        print '\n bad spaces must be fixed to continue...'
        time.sleep(3)

        sys.exit()
    else:
        
        #### NEED TO CREATE ALL INTERIOR WALLS TO SEE WHERE REMAINING EXTERIOR WALLS WILL FALL
        ## create exterior walls where interior walls do not exist
        #for space in activeElements:
        #    print 'space', space
        #    c = spaces[space].countVertices()
        #    print c
        #    for v in range(1,c+1):
        #        found = 0
        #        for intWall in intWalls:
        #            if ((intWall[0] == space) and (intWall[1] == v)) or ((intWall[2] == space) and (intWall[3] == v)):
        #                found = 1
        #                print '   found interior wall on %s: %s'  % (v, intWall)
        #        if not found and ([space, v] not in sameSpaceWalls):
        #            extWalls.append([space,v])
        #            print '   no interior wall on %s'  % v
        
        tol = 1                        
     
        #makeInteriorWalls = raw_input('   make interior walls? [y]/n')   # use this later to delete
        newIWalls = []
        
        IWallNum = 0
        for intWall in intWalls:
            space = intWall[0]
            spaceZ = spaces[space].trueZ()
            spaceH = spaces[space].trueHeight()
            zoneType = spaces[space].zoneType
            wallZ = intWall[5]
            wallZRel = intWall[5] - spaceZ
            wallH = intWall[4] - intWall[5]
            location = 'SPACE-V%s' % intWall[1]
            nextTo = intWall[2]
            nextToZoneType = spaces[nextTo].zoneType
            IWallNum += 1
            iWall = '"%s-I%s+%s-%s"' % (space[1:-1], intWall[1], intWall[3], IWallNum)
            newIWalls.append(iWall)

            if zoneType == 'PLENUM' and nextToZoneType == 'PLENUM':
                attributes = [['CONSTRUCTION', '"AIR WALL CONSTRUCTION"']]
            else:
                attributes = [['CONSTRUCTION', '"INTERIOR WALL CONSTRUCTION"']]
            
            #debug('IW\n  iwall %s\n  space %s\n  spaceZ %s\n  spaceH %s\n  wallZ %s\n  wallRel %s\n  wallH %s\n\n' % (iWall, space, spaceZ, spaceH, wallZ, wallZRel, wallH))
            
            iWalls[iWall]=IWall(name=iWall,attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
            
            iWalls[iWall].location = location
            iWalls[iWall].nextTo = nextTo

            if not (abs(wallZ-spaceZ) < tol):
                iWalls[iWall].z = wallZRel

            if not (abs(wallH-spaceH) < tol):
                iWalls[iWall].height = wallH

           
        newEWalls = []
        for space in activeElements:
            
            c = spaces[space].countVertices()
            for v in range(1,c+1):
                debug('\n-----------------\n%s' % space)
                allIWalls = []
                for iWall in iWalls:
                    vs = re.findall('\d+\+\d+', iWall)[0]
                    v1, v2 = vs.split('+')
                    if ( (iWalls[iWall].space == space and str(v) == v1) or ((iWalls[iWall].nextTo == space) and str(v) == v2)):
                        #debug('   %s %s %s %s %s\n' % (iWall, iWalls[iWall].nextTo, v, v1, v2))
                        allIWalls.append(iWall)
                    
                

                #debug('   v %s\n  allIWalls %s\n' % (v, allIWalls))
                if not len(allIWalls):
                    newEWalls.append([space,v,None,None])
                    #debug('   appended new ewalls with [%s, %s, %s, %s]\n' % (space,v,None,None))
                else:
                    tol = 1
                    allIWallsHeight = 0
                    for allIWall in allIWalls:
                        allIWallsHeight += iWalls[allIWall].returnHeight()
                    
                    if abs(allIWallsHeight - spaces[space].trueHeight()) < tol:
                        debug('%s-%s exhausted by %s \n' % (space, v, allIWalls))
                    else:
                        debug('%s-%s not exhausted by %s \n' % (space, v, allIWalls))
                        spaceZ = spaces[space].trueZ()
                        iWallSpans = []
                        eWallSpans = []
                        for allIWall in allIWalls:
                            iWallH = iWalls[allIWall].returnHeight()
                            iWallZ = iWalls[allIWall].returnTotalZ()
                            iWallSpan = [iWallZ - spaceZ, iWallZ + iWallH - spaceZ]
                            iWallSpans.append(iWallSpan)
                            
                            debug('  allIWall %s\n  iWallH %s\n  iWallZ %s\n  spaceZ %s' % (allIWall, iWallH, iWallZ, spaceZ))
                            debug('  iWallSpan %s' % (iWallSpan))

                        
                        iWallSpans.sort()
                        debug('iWallSpans %s' % (iWallSpans))
                        spaceHeight = spaces[space].trueHeight()
                        lowEWall = [0,iWallSpans[0][0]]
                        highEWall = [iWallSpans[-1][1],spaceHeight]
                        eWallSpans = [lowEWall, highEWall]
                        c = 0
                        if len(iWallSpans) > 1:
                            for c in range(1,len(iWallSpans)):
                                eWallSpans.append([iWallSpans[c-1][1],iWallSpans[c][0]])
                        debug('eWallSpans %s' % (eWallSpans))
                        for eWallSpan in eWallSpans:
                            if (eWallSpan[1] - eWallSpan[0]) > tol:
                                newEWalls.append([space,v,eWallSpan[0], eWallSpan[1] - eWallSpan[0]])
                                debug('  new ewall %s' % eWallSpan)
        
        
        
        if ugThreshold == '':
            i4 = raw_input('   underground threshohold [0]')
        try:
            ugThreshold = round(float(i4),2)
        except:
            ugThreshold = 0
        #print 'exterior/underground walls'
        for newEWall in newEWalls:
            space = newEWall[0]
            location = 'SPACE-V%s' % newEWall[1]
            eWall = '"%s-E%s"' % (space[1:-1], newEWall[1])
            uWall = '"%s-U%s"' % (space[1:-1], newEWall[1])
            

            
            
            if not newEWall[2]:
                z = spaces[space].trueZ()
            else:
                z = spaces[space].trueZ() + float(newEWall[2])

            if not newEWall[3]:
                h = spaces[space].trueHeight()
            else:
                h = float(newEWall[3])

            debug('%s %s %s %s %s' % (space, location, newEWall, z, h))

            # if the ewall Z is above the underground threshold, make an exterior wall
            tol = 1
            
            if z >= ugThreshold:
                debug('created %s' % eWall)
                attributes = [['CONSTRUCTION', '"EXTERIOR WALL CONSTRUCTION"']]
                eWalls[eWall]=EWall(name=eWall, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                eWalls[eWall].location = location
                
                if newEWall[2]:
                    eWalls[eWall].z = newEWall[2] 
                if newEWall[2]:
                    eWalls[eWall].height = newEWall[3] 


            # if the ewall Z + height is below the underground threshold, make an underground wall
            elif (z+h) <= ugThreshold:
                uWalls[uWall]=UWall(name=uWall, floor=spaces[space].floor, space=spaces[space].name)
                uWalls[uWall].location = location
                
                if newEWall[2]:
                    uWalls[uWall].z = newEWall[2] 
                if newEWall[2]:
                    uWalls[uWall].height = newEWall[3] 

            # otherwise, split the wall into an ewall and a uwall
            else:
                uWallHeight = ugThreshold - z
                eWallZ = uWallHeight
                eWallHeight = h - eWallZ

                attributes = [['CONSTRUCTION', '"EXTERIOR WALL CONSTRUCTION"']]
                eWalls[eWall]=EWall(name=eWall,  attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                debug('created %s' % eWall) 
                eWalls[eWall].height = eWallHeight
                eWalls[eWall].z = eWallZ
                eWalls[eWall].location = location
                
                attributes = [['CONSTRUCTION', '"UNDERGROUND WALL CONSTRUCTION"']]
                uWalls[uWall]=UWall(name=uWall, floor=spaces[space].floor, space=spaces[space].name)
                uWalls[uWall].height = uWallHeight
                uWalls[uWall].location = location


def advancedCreateFloors():
    print '\ncreating floors and overhangs...'

    floorMatchTolerance = 1
    minArea = 10
    maxArea = 40
    askRatio = .02
    passRatio = .02
    useSpacePolygonThreshold = .98
    smallestAreaIntersection = 1

    activeElements = returnActiveElements(spaces)
    for space in activeElements:
        runningVerts = polygons[spaces[space].polygon].numericalVertices()
        runningPoly = Poly(runningVerts)
        debug('') 
        debug(space)

        for otherSpace in spaces:
            if abs((spaces[space].trueZ()) - ((spaces[otherSpace].trueHeight()) + spaces[otherSpace].trueZ())) < floorMatchTolerance:
                otherSpaceVerts = polygons[spaces[otherSpace].polygon].numericalVertices()
                otherSpacePoly = Poly(otherSpaceVerts)
                
                try:
                    intersection = runningPoly.intersection(otherSpacePoly)
                    if intersection.area > smallestAreaIntersection:
                        runningPoly = runningPoly.difference(otherSpacePoly)
                        debug('    Subtracted %s from %s' % (otherSpace, space))
                except:
                    debug('    ERROR: could not properly compare %s to %s' % (space, otherSpace))

        polyList = []
        if type(runningPoly) == MultiPolygon:
            for poly in runningPoly.geoms:
                polyList.append(poly)

        elif type(runningPoly) == Poly:
            polyList.append(runningPoly)

        else:
            debug(  '\n   No polygon remaining from differences')
            debug(  '   %s' % runningPoly)
        
        floorNum = 0
        for poly in polyList:
            debug(    '\n    area:    %s' % poly.area)
            debug(    '    length:  %s' % poly.length)
            r = (poly.area/poly.length)**2.
            debug(    '    ratio:   %s' % r)
            makeFloor = 0
            if (r > passRatio and poly.area > minArea) or (poly.area > maxArea):
                debug(  '        passed!   ')
                p = shapelyToEQuestPoly(poly)[0]
                for v in p:
                    debug(  '        %s' % v)
                makeFloor = 1
            elif (r > askRatio) and (poly.area > minArea):
                p = shapelyToEQuestPoly(poly)[0]
                for v in p:
                    debug(  '        %s' % v)
                debug(  '\n        make floor for %s ' % space)
                mr = raw_input('        [n] >')
                if len(mr) > 0:
                    if mr.lower()[0] == 'y':
                        makeFloor = 1
            else:
                debug(  '        skipped   ')

            if makeFloor:
                    
                if spaces[space].trueZ() <= 3:
                    floorType = 'u'
                else:
                    floorType = 'e'
                    
                spaceArea = polygons[spaces[space].polygon].area()
                floorPolyNum = eQuestToShapelyPoly(p)
                floorArea = floorPolyNum.area

                floorNum += 1
                name = '"%s-FLOOR%s"' % (spaces[space].name[1:-1], floorNum)
                
                if floorType == 'e':
                    attributes = [['CONSTRUCTION','"EXTERIOR FLOOR CONSTRUCTION"']]
                    eWalls[name]=EWall(name=name, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                    eWalls[name].location = 'BOTTOM'
                else:
                    attributes = [['CONSTRUCTION','"SUBGRADE SLAB CONSTRUCTION"']]
                    uWalls[name]=UWall(name=name, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                    uWalls[name].location = 'BOTTOM'
                debug(  '   create floor %s' % name)


                if (floorArea/spaceArea) < useSpacePolygonThreshold: # else use space poly by default
                    pnew = rere(p)
                    polygon = '"%s POLY"' % (name[1:-1])
                    polygons[polygon]=Polygon(name=polygon, vertices=pnew)
                    if floorType == 'e':
                        eWalls[name].polygon = polygon
                    else:
                        uWalls[name].polygon = polygon
                    debug(  '   create polygon %s' % polygon)


def advancedCreateRoofs():
    print '\ncreating roofs...'

    # finding roofs and overhangs
    floorMatchTolerance = 1
    minArea = 10
    maxArea = 40
    askRatio = .02
    passRatio = .02
    useSpacePolygonThreshold = .98
    smallestAreaIntersection = 1
    #otherSpaces = spaces[:]
    
    dl = 'debug.log'
    
    #roofs
    #makeRoofs(spaces, floors)
    
    activeElements = returnActiveElements(spaces)
    for space in activeElements:
        runningVerts = polygons[spaces[space].polygon].numericalVertices()
        runningPoly = Poly(runningVerts)
        for otherSpace in spaces:
            if abs((spaces[space].trueZ() + spaces[space].trueHeight()) - spaces[otherSpace].trueZ()) < floorMatchTolerance:
                otherSpaceVerts = polygons[spaces[otherSpace].polygon].numericalVertices()
                otherSpacePoly = Poly(otherSpaceVerts)
                
                try:
                    runningPoly = runningPoly.difference(otherSpacePoly)
                except:
                    debug('ERROR: could not properly compare %s to %s' % (space, otherSpace))

        polyList = []
        debug('') 
        debug(space)
        if type(runningPoly) == MultiPolygon:
            for poly in runningPoly.geoms:
                polyList.append(poly)

        elif type(runningPoly) == Poly:
            polyList.append(runningPoly)

        else:
            debug(  '\n   No polygon remaining from differences')
            debug(  '   %s' % runningPoly)
        
        roofNum = 0
        for poly in polyList:
            debug(    '\n    area:    %s' % poly.area)
            debug(    '    length:  %s' % poly.length)
            r = (poly.area/poly.length)**2.
            debug(    '    ratio:   %s' % r)
            makeRoof = 0
            if (r > passRatio and poly.area > minArea) or (poly.area > maxArea):
                debug(  '        passed!   ')
                p = shapelyToEQuestPoly(poly)[0]
                for v in p:
                    debug(  '        %s' % v)
                makeRoof = 1
            elif (r > askRatio) and (poly.area > minArea):
                p = shapelyToEQuestPoly(poly)[0]
                for v in p:
                    debug(  '        %s' % v)
                debug(  '\n        make roof for %s ' % space)
                mr = raw_input('        [n] >')
                if len(mr) > 0:
                    if mr.lower()[0] == 'y':
                        makeRoof = 1
            else:
                debug(  '        skipped   ')

            if makeRoof:
                if (spaces[space].trueZ() + spaces[space].trueHeight()) >= 0:
                    roofType = 'e'
                else:
                    roofType = 'u'
                    
                spaceArea = polygons[spaces[space].polygon].area()
                roofPolyNum = eQuestToShapelyPoly(p)
                roofArea = roofPolyNum.area

                roofNum += 1
                name = '"%s-ROOF%s"' % (spaces[space].name[1:-1], roofNum)
                if roofType == 'e':
                    attributes = [['CONSTRUCTION','"EXTERIOR ROOF CONSTRUCTION"']]
                    eWalls[name]=EWall(name=name, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                    eWalls[name].location = 'TOP'
                else:
                    attributes = [['CONSTRUCTION','"UNDERGROUND ROOF CONSTRUCTION"']]
                    uWalls[name]=UWall(name=name, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                    uWalls[name].location = 'TOP'
                debug(  '   create roof %s' % name)

                if (roofArea/spaceArea) < useSpacePolygonThreshold: # else use space poly by default
                    polygon = '"%s POLY"' % (name[1:-1])
                    polygons[polygon]=Polygon(name=polygon, vertices=p)
                    if roofType == 'e':
                        eWalls[name].polygon = polygon
                    else:
                        uWalls[name].polygon = polygon
                    debug(  '   create polygon %s' % polygon)



##################################
######## Start Classes ###########
##################################


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
        

####################################################    Start Code     ##########################################################

####################
## Initialization ##
####################

try:

    errorNumber = 1


    from shapely.geometry import Polygon as Poly
    from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString
    import math, sys, operator
    import string
    import sys
    import re
    import os
    import time
    import shutil
    import traceback
    import math
    import xlwt
    import xlrd
    import subprocess
    import copy
    
    
    polygons = {}
    floors = {}
    spaces = {}
    eWalls = {}
    iWalls = {}
    uWalls = {}
    windows = {}
    doors = {}
    systems = {}
    zones = {}
    elementDefaults = {}
    
    f = open('debug.log', 'w')
    f.close()

    windowNumber = 0  # set here to avoid duplication

    
    vertices = []
    attributes = []
    
    seedPath = 'E:\\Files\\Documents\\Jared\\Work\\DMI\\eQuest\\Scripts\\'
    pd2Seed = 'E:\\Files\\Documents\\Jared\\Work\\DMI\\eQuest\\Scripts\\seed.pd2'
    
    #############################
    #### Get Input file Name ####
    #############################



    defaultProject = os.getcwd().split("\\")[-1]
    inpFile = defaultProject + '.inp'
    
    print '\nWill write to %s\n' % inpFile
    
    print 'Detecting pd2 file...\n'

    pd2 = inpFile[:-4] + '.pd2'
    if os.path.exists(pd2):
        print 'pd2 file found\n'
    else:
        print 'No pd2 file...copying in pd2 template'
        if os.path.exists(pd2Seed):
            f = open(pd2Seed,'r')
            pd2SeedLines = f.readlines()[1:]
            fw = open(pd2,'w')
            fw.write('Proj   "%s" \n' % inpFile[:-4])
            for line in pd2SeedLines:
                fw.write(line)
            f.close()
            fw.close()
        else:
            print 'Cannot locate pd2 seed file %s\n' % pd2seed

    #############################
    ####    Make    Backup   ####
    #############################

    if os.path.exists(inpFile):
        if not os.path.exists('backup'):
            os.mkdir('backup')
        bfile = os.path.join('backup',inpFile + '_' + time.strftime('%y%m%d-%H%M%S'))
        shutil.copyfile(inpFile, bfile)
        print 'Creating backup\n'
        print '   backing up\n      %s\n   to      \n      %s' % (inpFile, bfile)


    #############################
    ####   Big     Loop      ####
    #############################
    
    i = ''
    while i != 'q':

        
        if i == 'f':
            print 'Reading fdf\n'
            fdfFiles = []
            for file in os.listdir('.'):
                if file[-3:] == 'fdf':
                    fdfFiles.append(file)
            if not fdfFiles:
                print 'No FDF files in directory\n'
            else:
                c = 0
                for file in fdfFiles:
                    c += 1
                    print c, '-', file

                print
                i2 = raw_input('which fdf? ')
                print
                file = fdfFiles[int(i2)-1]
                
                defaultPlenumInput = raw_input('plenum by default? [y]/n').lower()
                if len(defaultPlenumInput) == 0:
                    defaultPlenum = True
                elif defaultPlenumInput.lower()[0] == 'n':
                    defaultPlenum = False
                else:
                    defaultPlenum = True
                   
                
                
                #instantiate dics, lists
                errors = []
                fdfPolygons = {}
                fdfFloors = {}
                fdfSpaces = {}

                
                fdf = open(file, 'r')
                lines = fdf.read().split("endobj")
                fdf.close()
                
                nameList = []
                duplicateNameList = []
                
                scales = []
                origins = []
                
                # find scale and north
                print '\n\n########## Looking for scales ##########\n'
                for line in lines:
                    sInput = 0
                    scales = re.findall('scale\-.+?\)', line, re.IGNORECASE)
                    if len(scales) > 1:
                        errors.append('found more than one "scale" in line %s' % line)
                    elif len(scales) == 1:
                        scale = scales[0]

                        # check for format: scale-1[30_0]
                        if not re.search('scale\-.*?\[.*?\]', scale, re.IGNORECASE):
                            errors.append('scale %s is malformed' % scale)

                        # find floor
                        f = '"' + re.findall('scale\-.*?\[', scale, re.IGNORECASE)[0][6:-1] + '"'
                        
                        # find scale
                        scaleString = re.findall('\[.*?\]', scale, re.IGNORECASE)

                        #scaleSplit = scaleString[0][2:-1].split('_')
                        scaleSplit = scaleString[0][1:-1].split('_')
                        sInput += float(scaleSplit[0])
                        if len(scaleSplit) > 1:
                            sInput += float(scaleSplit[1])/12

                        #get endpoints and direction
                        n = re.findall('l\[.+?\]', line, re.IGNORECASE)[0][2:-1].split()
                        if abs(float(n[0]) - float(n[2])) < 1:
                            sPdf = abs(float(n[1])-float(n[3]))
                            if float(n[1])>float(n[3]):
                                d = 'north'
                            else:
                                d = 'south'
                        elif abs(float(n[1]) - float(n[3])) < 1:
                            sPdf = abs(float(n[0])-float(n[2]))
                            if float(n[0])>float(n[2]):
                                d = 'west'
                            else:
                                d = 'east'
                        else:
                            errors.append('Could not determine direction from scaleString %s' % scaleString)

                        s = sInput/sPdf
                        
                        # check for existing floors
                        found = 0
                        for existingFloor in fdfFloors.keys():
                            if existingFloor.lower() == f.lower():
                                found = 1
                                errors.append('ERROR - Duplicate name %s' % f)
                        if not found:
                            fdfFloors[f]=FdfFloor(f, scale=s, direction=d)
                            print '\nfound scale line with text match "%s"' % scales[0] 
                            print '  floor     %s' % f
                            print '  d         %s' % d
                            print '  s         %s' % s


                #print fdfFloors 
                # find origins  (format origin-B[Z:-2.5;FH:21.5;HP:Y;PH:7.5;R:7.5;X:100_11;Y:10]
                print 'Origin Input Type'
                print '1 - In FDF (default)'
                print '2 - In Text File named origin.txt'
                
                originInputType = raw_input()
                
                if (not originInputType) or (originInputType == '1'):
                
                    print '\n\n########## Looking for origins ##########\n'
                    for line in lines:
                        origins = re.findall('origin.+?\)', line, re.IGNORECASE)
                        if len(origins) > 1:
                            errors.append('ERROR - Found multiple origins on line %s' % line)
                        elif len(origins):
                            originSplit = getParams(origins[0][7:-1])
                            f = '"' + originSplit[0] + '"'
                            params = originSplit[1]
                            
                            # check for scale
                            if not fdfFloors.has_key(f):
                                errors.append('ERROR - Cannot create origin, no scale found for %s' % f)
                            else:
                                # get origin numbers
                                n = re.findall('rect\[.+?\]', line, re.IGNORECASE)[0][5:-1].split()
                                if fdfFloors[f].direction == 'north':
                                    o = [min(float(n[0]), float(n[2])), min(float(n[1]), float(n[3]))]
                                    fdfFloors[f].origin = o
                                elif fdfFloors[f].direction == 'east':
                                    o = [min(float(n[1]), float(n[3])), max(float(n[0]), float(n[2]))]
                                    fdfFloors[f].origin = o
                                elif fdfFloors[f].direction == 'south':
                                    o = [min(float(n[0]), float(n[2])), min(float(n[1]), float(n[3]))]
                                    fdfFloors[f].origin = o
                                
                                elif fdfFloors[f].direction == 'west':  # funny one
                                    o = [max(float(n[1]), float(n[3])), min(float(n[0]), float(n[2]))]
                                    fdfFloors[f].origin = o
                                
                                else:
    
                                    errors.append('ERROR - No floor direction definition for %s' % f)
    
                                fdfFloors[f].plenumDefault = defaultPlenum
                                ph = 0
                                rotateOffset = 0
                                xOffset = 0
                                yOffset = 0
                                hasPlenum = defaultPlenum
                                height = 0
                                z = 0
                                print params
                                for p in params:
                                    if p[0].lower() == 'hp':
                                        if p[1].lower() == 'y':
                                            hasPlenum = True
                                        if p[1].lower() == 'n':
                                            hasPlenum = False
    
                                    elif p[0].lower() == 'ph':
                                        n = p[1].split('_')
                                        ph = float(n[0])
                                        if len(n) == 2:
                                             ph +=float(n[1])/12
    
                                    elif p[0].lower() == 'h':
                                        n = p[1].split('_')
                                        height = float(n[0])
                                        if len(n) == 2:
                                            height +=float(n[1])/12
    
                                    elif p[0].lower() == 'z':
                                        print p
                                        n = p[1].split('_')
                                        z = float(n[0])
                                        if len(n) == 2:
                                            z +=float(n[1])/12
    
                                    elif p[0].lower() == 'x':
                                        n = p[1].split('_')
                                        xOffset = float(n[0])
                                        if len(n) == 2:
                                            xOffset += float(n[0])
    
                                    elif p[0].lower() == 'y':
                                        n = p[1].split('_')
                                        yOffset = float(n[0])
                                        if len(n) == 2:
                                            yOffset += float(n[0])
    
                                    elif p[0].lower() == 'r':
                                        n = p[1].split('_')
                                        rotateOffset = float(n[0])
     
                                    else:
                                        errors.append('WARNING - unknown option %s in %s... skipping' % (p, f))
    
                                if (xOffset or yOffset) and (rotateOffset):
                                
                                    errors.append('ERROR - Cannot rotate AND offset.. setting rotate to 0')
                                    rotateOffset = 0
    
                                fdfFloors[f].x = xOffset
                                fdfFloors[f].y = yOffset
                                fdfFloors[f].z = z
                                fdfFloors[f].floorHeight = height
                                fdfFloors[f].rotate = rotateOffset
                                fdfFloors[f].plenumDefault = hasPlenum
                                
    
                                print f
                                print fdfFloors[f].floorHeight
                                print ph
                                fdfFloors[f].spaceHeight = fdfFloors[f].floorHeight - ph
    
                                print '\nfound origin line with text match "%s"' % origins[0] 
                                print '  floor     %s' % f
                                print '  params    %s' % params
                                
                elif (originInputType=='2'):
                    fOrigin = open('origin.txt', 'r')
                    originLines = fOrigin.readlines()
                    fOrigin.close()

                    ph = 0
                    rotateOffset = 0
                    xOffset = 0
                    yOffset = 0
                    hasPlenum = defaultPlenum
                    height = 0
                    z = 0

                    #requiredHeadings = ['floor', 'z', 'fh', 'hp', 'ph', 'x', 'y']
                    fileHeadings = originLines[0].lower().split()
                    floorIndex = fileHeadings.index('floor')
                    zIndex = fileHeadings.index('z')
                    fhIndex = fileHeadings.index('fh')
                    hpIndex = fileHeadings.index('hp')
                    phIndex = fileHeadings.index('ph')
                    xIndex = fileHeadings.index('x')
                    yIndex = fileHeadings.index('y')
                    
                    floorIndex = 0
                   
                    titleLine = originLines
                   
                else:
                    print 'bad choice'
                             
                
                PolyRenameList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P']
                # find polygons
                print '\n\n########## Looking for polygons ##########\n'
                for line in lines:
                    thisLineError = 0
                    if '/Subtype/Polygon/' in line and not 'PolygonCloud' in line:
                        # find name (where the name is defined)
                        stringMatch = re.findall('\)\/T\(.*?\)\/Subj\(', line, re.IGNORECASE)
                        #print line
                        #print stringMatch
                        if not '-' in stringMatch[0]:
                            stringMatch = re.findall('\/Contents\(.*?\)\/', line, re.IGNORECASE)
                        
                        # subject strings for C-ACTIVITY-DESC
                        activity = ''
                        subjectStrings =re.findall('\/Subj\(.*?\)\/', line, re.IGNORECASE)
                        if not subjectStrings:
                            errors.append('ERROR - No Subject line found in line %s' % line)
                        elif len(subjectStrings) > 1:
                            errors.append('ERROR - Multiple Subject Names Found in line %s' % line)
                        else:
                            subjectString = subjectStrings[0]
                            #print '      ', subjectString
                            #print '   subject string: %s' % subjectString
                            if 'polygon' not in subjectString.lower():
                                activity = '*' + subjectString[6:-2] + '*'
                        

                        #print stringMatch
                        #time.sleep(.1)
                        if len(stringMatch) > 1:
                            errors.append('ERROR - Multiple Polygon Names Found in line %s' % line)
                        elif len(stringMatch):
                            #print stringMatch
                            if not 'Subj' in stringMatch[0] and not 'Contents' in stringMatch[0]:
                                errors.append('ERROR - Unknown Polygon Naming Type %s' % stringMatch[0])
                            else:
                                if 'Subj' in stringMatch[0]:
                                    polySplit = getParams(stringMatch[0][4:-7])
                                else:
                                    polySplit = getParams(stringMatch[0][10:-2])

                                name = polySplit[0]
                                params = polySplit[1]
    
                                # check for dupe
                                if name in fdfPolygons.keys():
                                    errors.append('ERROR - Duplicate Name Found %s' % name)
                                else:
                                     
                                    polyError = 0
                                    
                                    # create floor polygon, assign floor params
                                    #if name.count('-') == 0:
                                    #    floor = '"' + name + '"'
                                    #    polyName = '"' + name + ' poly' + '"'
                                    #    if not fdfFloors.has_key(floor):
                                    #        errors.append('ERROR - No floor %s for floor polygon %s.  Check scale and origin' % (name, name))
                                    #        polyError = 1
                                    #    else:
                                    #        
                                    #        found = 0
                                    #        for existingPolygon in fdfPolygons.keys():
                                    #            if existingPolygon.lower() == polyName.lower():
                                    #                found = 1
                                    #                errors.append('ERROR - Duplicate polygon name %s' % polyName)
                                    #        if not found:
                                    #            fdfPolygons[polyName] = FdfPolygon(name=polyName)
                                    #        
                                    #        fdfFloors[floor].polygon = polyName
    
                                    #        for p in params:
                                    #            if p[0].lower() == 'p':
                                    #                n = p[1].split('_')
                                    #                fdfFloors[floor].spaceHeight = float(n[0])
                                    #                if len(n) == 2:
                                    #                    fdfFloors[floor].spaceHeight +=float(n[1])/12
                                    #            elif p[0].lower() == 'h':
                                    #                n = p[1].split('_')
                                    #                fdfFloors[floor].floorHeight = float(n[0])
                                    #                if len(n) == 2:
                                    #                    fdfFloors[floor].floorHeight +=float(n[1])/12
                                    #            elif p[0].lower() == 'z':
                                    #                n = p[1].split('_')
                                    #                fdfFloors[floor].z = float(n[0])
                                    #                if len(n) == 2:
                                    #                    fdfFloors[floor].z +=float(n[1])/12
                                    #            else:
                                    #                errors.append('WARNING - unknown option %s in %s... skipping' % (p ,floor))
                                        
                                    # create space polygon
                                    if name.count('-') == 1:
                                        floor = '"' + name.split('-')[0]+ '"'
                                        space = '"' + name + '"'
                                        if not fdfFloors.has_key(floor):
                                            errors.append('ERROR - No floor %s for space polygon %s.  Check scale and origin' % (floor, space))
                                            polyError = 1
     
                                        else:
                                            #check for existing Spaces
                                            fdfSpacesSet = set(k.lower() for k in fdfSpaces)
                                            
                                            if space.lower() in fdfSpacesSet:
                                                changeCount = 1 
                                                spaceNew = '"%s%s"' % (space[1:-1], changeCount)
                                                while ('"%s%s"' % (space[1:-1], changeCount) in fdfSpacesSet):
                                                    changeCount+=1
                                                    spaceNew = '"%s%s"' % (space[1:-1], changeCount)
                                                errors.append('WARNING - Duplicate space %s - renamed to %s' % (space, spaceNew))
                                                space = spaceNew
                                            fdfSpaces[space] = FdfSpace(space)
                                            
                                            #check for existing namesPolygon, rename if necessary
                                            polyName = '"' + space[1:-1] + ' poly' + '"'
                                            fdfPolygons[polyName] = FdfPolygon(polyName)
        


    
                                            fdfSpaces[space].floor = floor
                                            fdfSpaces[space].polygon = polyName
                                            fdfSpaces[space].hasPlenum = fdfFloors[floor].plenumDefault
                                            fdfSpaces[space].activity = activity
                                            
                                            for p in params:
    
                                                # institute default plenum
                                                
                                                if p[0].lower() == 'hp':
                                                    if p[1][0].lower()== 'y':
                                                        fdfSpaces[space].hasPlenum = True
                                                    if p[1][0].lower()== 'n':
                                                        fdfSpaces[space].hasPlenum = False
                                                
                                                elif p[0].lower() == 'ph':
                                                    n = p[1].split('_')
                                                    fdfSpaces[space].plenumHeight = float(n[0])
                                                    if len(n) == 2:
                                                        fdfSpaces[space].plenumHeight +=float(n[1])/12
    
                                                elif p[0].lower() == 'z':
                                                    n = p[1].split('_')
                                                    fdfSpaces[space].z = float(n[0])
                                                    if len(n) == 2:
                                                        fdfSpaces[space].z +=float(n[1])/12
                                                
                                                elif p[0].lower() == 'h':
                                                    n = p[1].split('_')
                                                    fdfSpaces[space].height = float(n[0])
                                                    if len(n) == 2:
                                                        fdfSpaces[space].height +=float(n[1])/12
                                                else:
                                                    errors.append('WARNING - unknown option %s in %s... skipping' % (p ,space))
                                            
                                            #print '\nfound space line with text match "%s"' % stringMatch[0]
                                            #print '  floor    %s' % floor
                                            #print '  space    %s' % space
                                            #print '  params   %s' % params
                                            #print '  activity %s' % activity

                                    
                                    
                                    
                                    else:
                                        errors.append('ERROR - polygon name must have one hyphen in its name: %s' % name)
                                    
                                         
                                    if not polyError:
                                        # find associated origin
                                        direction = fdfFloors[floor].direction
                                        scale = fdfFloors[floor].scale
                                        origin = fdfFloors[floor].origin
                                        xOffset = fdfFloors[floor].x
                                        yOffset = fdfFloors[floor].y
                                        rotateOffset = fdfFloors[floor].rotate
                                    
                                        if (not direction): 
                                            errors.append('ERROR - Floor %s is missing direction' % floor)
                                            del fdfPolygons[polyName]
                                        elif (not scale): 
                                            errors.append('ERROR - Floor %s is missing scale' % floor)
                                            del fdfPolygons[polyName]
                                        elif (not origin):
                                            errors.append('ERROR - Floor %s is missing origin' % floor)
                                            del fdfPolygons[polyName]
        
                                        else:
                                            #Find vertices definition
                                            s = line.find('Vertices[') + 9 
                                            e = line[s:].find(']')
                                            verticesString = line[s:e+s]
                                        
                                            # Parse vertices Numbers
                                            verticyNumbers = verticesString.split(' ')
                                            # group numbers into pairs
                                            vPaired = zip(verticyNumbers[::2], verticyNumbers[1::2])
                                            polygonVertices = []
                                            #print 'space %s ' % name
                                            #print '   origin %s' % origin
                                            
                                            for p1, p2 in vPaired:
                                                if direction == 'north':
                                                    x = str(round((float(p1) - origin[0])*scale,2))
                                                    y = str(round((float(p2) - origin[1])*scale,2))
                                                elif direction == 'east':
                                                    x = str(round((float(p2) - origin[0])*scale,2))
                                                    y = str(round((origin[1] - float(p1))*scale ,2))
                                                elif direction == 'south':
                                                    #print '   v%s abs        (%s,%s)' % (vertCount, str(round(float(p1),0)), str(round(float(p2),0)))
                                                    x = str(round((float(p1) - origin[0])*scale,2))
                                                    y = str(round((float(p2) - origin[1])*scale,2))
                                                    #xx = str(round((float(p1) - origin[0]),0))
                                                    #yy = str(round((float(p2) - origin[1]),0))
                                                    #print '   v%s rel        (%s,%s)' % (vertCount, xx, yy)
                                                    #print '   v%s rel scaled (%s,%s)' % (vertCount, x, y)
    
                                                elif direction == 'west': # funny west one, should normally look like east
                                                    x = str(round((origin[0] - float(p2))*scale,2))
                                                    y = str(round((float(p1) - origin[1])*scale ,2))
    
                                                    
                                                else:
                                                    errors.append('ERROR - No definition for %s' % floors[floor]['direction'])
                                
                                                polygonVertices.append([x,y])
                            
                                            # Remove last verticy if it matches first verticy
                                            if polygonVertices[:1] == polygonVertices[-1:]:
                                                del polygonVertices[-1:]
                                            
                                            # check to see if any veritcies are in a straight line
                                            delPoints = []
                                            pvl = len(polygonVertices)  # polygon verticy length
                                            for c in range(0,pvl-1):
                                                ptA1 = polygonVertices[(c-1)%pvl]
                                                ptA2 = polygonVertices[(c)%pvl]
                                                ptB1 = polygonVertices[(c)%pvl]
                                                ptB2 = polygonVertices[(c+1)%pvl]
                                                
                                                #print ####################
                                                #print ptA1, ptA2
                                                #print ptB1, ptB2
                                                #print ####################

                                                a1 = getAngleCart(ptA1, ptA2)
                                                a2 = getAngleCart(ptB1, ptB2)
                                                if (abs(a1-a2) < 4) or (360-(abs(a1-a2)) < 2):
                                                   delPoints.append(c)

                                            # delete points if they are in a straight line
                                            delPoints.sort()
                                            delPoints.reverse()
                                            for delPoint in delPoints:
                                                errors.append('WARNING - Verticy %s in %s is superfluous because it forms a striaght line. It has been deleted' % (delPoint+1, polyName))
                                                del polygonVertices[delPoint]

                                            # check if any verticies are too close
                                            minDist = 1.25
                                            mNew = []
                                            c1 = 0
                                            for p1 in polygonVertices:
                                                c1 += 1
                                                c2 = 0
                                                for p2 in polygonVertices:
                                                    c2 += 1 
                                                    if c1 < c2 and pointDistance(p1,p2) < minDist:
                                                        errors.append('WARNING - Vertices %s and %s in %s are too close' % (c1, c2, polyName))
                                            
                                            # create polygon
                                            fdfPolygons[polyName].vertices = polygonVertices
                                            if not isCcw(fdfPolygons[polyName].vertices):
                                                #for v in fdfPolygons[polyName].vertices:
                                                #    print v
                                                errors.append('WARNING - Found CW polygon %s and reversed the vertices' % polyName)
                                                fdfPolygons[polyName].reverse(fdfPolygons)
                                                #print 'reversing....'
                                                #for v in fdfPolygons[polyName].vertices:
                                                #    print v

                                            # offset or rotate
                                            if xOffset or yOffset:
                                                verticesNew = []                                               
                                                for verticy in fdfPolygons[polyName].vertices:
                                                    #print verticy
                                                    (xNew, yNew) = (verticy[0]+xOffset, verticy[1]+yOffset)
                                                    #print xNew, yNew
                                                    verticesNew.append([str(round(xNew,2)), str(round(yNew,2))])
                                                #print polygons[polygon].vertices
                                                fdfPolygons[polyName].vertices = verticesNew
                                            
                                            if rotateOffset:
                                                verticesNew = []
                                                for verticy in fdfPolygons[polyName].vertices:
                                                    print rotateOffset
                                                    debug('rotating %s by %s' % (polyName, rotateOffset))
                                                    #print verticy
                                                    (xNew, yNew) = rotate(verticy[0], verticy[1], rotateOffset)
                                                    #print xNew, yNew
                                                    verticesNew.append([str(round(xNew,2)), str(round(yNew,2))])
                                                #print polygons[polygon].vertices
                                                fdfPolygons[polyName].vertices = verticesNew
                                                #print polygons[polygon].vertices

                                            
    
                
                eCount = 0
                if errors:
                    for error in errors:
                        debug(error, p=1)
                        if 'ERROR' in errors:
                            eCount += 1
                            time.sleep(1)
                    print 'Fatal errors: %s' % eCount
                    prompt = '\nContinue y/[n]'
                    default = 'n'
                else:
                    print '\nNo Errors'
                    prompt = 'Continue [y]/n'
                    default = 'y'
                print

                print prompt
                i2 = raw_input('     >')
                if i2.lower() == 'n' or (i2=='' and default == 'n'):
                    print 'exiting....'
                    time.sleep(2)
                    sys.exit()
                else:
                    
                    print 'which client?:'
                    print '1 - DMI'
                    print '2 - TNZ'
                    
                    clientNumber = raw_input()
                    if clientNumber == '1':
                       seedFile = os.path.join(seedPath, 'seed_dmi.inp')
                    elif clientNumber == '2':
                       seedFile = os.path.join(seedPath, 'seed_tnz.inp')
                    else:
                        'no matching seed file'
                        system.exit()
                    
                    
                    parsedSeed = parseInp(seedFile)
                    i2 = ''
                    try:
                        contentExists = (len(beginingSection)>0)
                    except:
                        contentExists = False
                    
                    if contentExists:
                        print 'Overwrite existing dead info? [y]/n'
                        i2 = raw_input('     >')

                    if i2.lower() != 'n' or not contentExists:
                        beginingSection = parsedSeed[0]
                        polyToElemSection = parsedSeed[2]
                        elemToSystemSection = parsedSeed[4]
                        systemSection = parsedSeed[5]
                        endingSection = parsedSeed[6]

                        #####################
                        ## Define Systems  ##  # note since systems are not in fdf file
                        #####################
                        
                        for elementLine in systemSection:
                        
                            # find line with system definition
                            if elementLine[:1]=='"':
                                active = 1
                                elementName = elementLine[:elementLine.find('=')-1].strip()
                                elementType = elementLine[elementLine.find('=')+1:].strip()
                        
                            # form list of attribute pairs
                            elif elementLine.find('=') > 0 and active == 1:
                                attribute = ([elementLine[0:elementLine.find('=')-1].strip(), elementLine[elementLine.find('=')+1:].strip()])
                                attributes.append(attribute)    
                                
                            # done gathering info, defining instance
                            elif elementLine.find('..') > 0:
                                foundElement = 0
                        
                                if elementType == 'SYSTEM':
                                    systems[elementName]=System(elementName, attributes)
                                    foundElement = 1
                                    currentSystem = systems[elementName].name
                        
                                elif elementType == 'ZONE':
                                    zones[elementName]=Zone(elementName, attributes, currentSystem)
                                    foundElement = 1
                        
                                attributes = []
                                active=0



                    else:
                        print 'Preserving Existing Content'
                    
                    handle = 'k'

                    #convert fdf objects to normal objects


                    #convert fdf polygons to normal polygons
                    for polyName in sorted(fdfPolygons.keys()):
                        w = 1
                        if polygons.has_key(polyName): 
                            if handle=='ka':
                                w = 0
                            elif handle=='oa':
                                w = 1
                            else:
                                print 'polygon %s exists\n  [k] - keep\n   o - overwrite\n   ka - keep all\n   oa - overwrite all\n' % polyName
                                handle = raw_input('   >')
                                if i2[0] == 'o':
                                    w = 1
                                else:
                                    w = 0
                        if w:
                            polygons[polyName] = Polygon(name=polyName, vertices=fdfPolygons[polyName].vertices)

                    
                    
                    handle = 'k'

                    #convert fdf floors to normal floors
                    for floorName in sorted(fdfFloors.keys()):
                        w = 1
                        if floors.has_key(floorName): 
                            if handle=='ka':
                                w = 0
                            elif handle=='oa':
                                w = 1
                            else:
                                print 'floor %s exists\n  [k] - keep\n   o - overwrite\n   ka - keep all\n   oa - overwrite all\n' % floor
                                handle = raw_input('   >')
                                if i2[0] == 'o':
                                    w = 1
                                else:
                                    w = 0
                        if w:
                            floors[floorName] = Floor(name=floorName)
                            floors[floorName].z = fdfFloors[floorName].z
                            floors[floorName].floorHeight = fdfFloors[floorName].floorHeight
                            floors[floorName].spaceHeight = fdfFloors[floorName].spaceHeight
                            #floors[floorName].polygon = fdfFloors[floorName].polygon
                        
                    #convert fdf spaces to normal spaces
                    for spaceName in sorted(fdfSpaces.keys()):
                        w = 1
                        if spaces.has_key(spaceName): 
                            if handle=='ka':
                                w = 0
                            elif handle=='oa':
                                w = 1
                            else:
                                print 'space %s exists\n  [k] - keep\n   o - overwrite\n   ka - keep all\n   oa - overwrite all\n' % space
                                handle = raw_input('   >')
                                if i2[0] == 'o':
                                    w = 1
                                else:
                                    w = 0

                        if w:
                            spaces[spaceName] = Space(name=spaceName)
                            spaces[spaceName].z = fdfSpaces[spaceName].z
                            spaces[spaceName].height = fdfSpaces[spaceName].height
                            spaces[spaceName].floor = fdfSpaces[spaceName].floor
                            spaces[spaceName].polygon = fdfSpaces[spaceName].polygon
                            spaces[spaceName].activity = fdfSpaces[spaceName].activity
                            if not fdfSpaces[spaceName].hasPlenum:
                                if not spaces[spaceName].height:
                                    spaces[spaceName].height = floors[spaces[spaceName].floor].floorHeight
                            
                        #create plenum if necessary
                        if fdfSpaces[spaceName].hasPlenum:
                            psn = spaceName[:-1] + '_P' + '"'
                            w = 1
                            if spaces.has_key(psn): 
                                if handle=='ka':
                                    w = 0
                                elif handle=='oa':
                                    w = 1
                                else:
                                    print 'space %s exists\n  [k] - keep\n   o - overwrite\n   ka - keep all\n   oa - overwrite all\n' % space
                                    handle = raw_input('   >')
                                    if i2[0] == 'o':
                                        w = 1
                                    else:
                                        w = 0
                            if w:
                                spaces[psn] = Space(name=psn)
                                spaces[psn].zoneType = 'PLENUM'
                                spaces[psn].floor = fdfSpaces[spaceName].floor
                                spaces[psn].polygon = fdfSpaces[spaceName].polygon
                                
                                if fdfSpaces[spaceName].activity:
                                    spaces[psn].activity = '*Plenum*'

                                sh = fdfSpaces[spaceName].height
                                ph = fdfSpaces[spaceName].plenumHeight
                                z = spaces[spaceName].z
                                if not z:
                                    z = 0
                                z = float(z)
                                
                                debug('space %s ' % spaceName)
                                
                                if sh and ph:
                                    debug('  xxx (1) if sh and ph %s' % spaceName)
                                    pz = sh - ph + z
                                    #pz = sh - ph
                                    spaces[spaceName].height = sh - ph
                                    spaces[psn].z = pz
                                    spaces[psn].height = ph

                                if sh and not ph:
                                    #print spaceName
                                    #print floors[spaces[spaceName].floor].floorHeight
                                    #print floors[spaces[spaceName].floor].spaceHeight
                                    debug('  xxx (2) if sh and not ph %s' % spaceName)
                                    ph = floors[spaces[spaceName].floor].floorHeight - floors[spaces[spaceName].floor].spaceHeight
                                    pz = sh - ph + z
                                    spaces[spaceName].height = sh - ph
                                    spaces[psn].z = pz
                                    spaces[psn].height = ph


                                if not sh and ph:
                                    debug('  xxx (3) if not sh and ph %s' % spaceName)
                                    sh = floors[spaces[spaceName].floor].floorHeight
                                    pz = sh - ph + z
                                    spaces[spaceName].height = sh - ph
                                    spaces[psn].z = pz
                                    spaces[psn].height = ph
                                
                                debug('  z: ......................... %s' % z)
                                debug('  sh: ........................ %s' % sh)
                                debug('  ph: ........................ %s' % ph)
                                debug('  spaces[spaceName].height ... %s' % spaces[spaceName].height)
                                debug('  spaces[psn].z .............. %s' % spaces[psn].z)
                                debug('  spaces[psn].height ......... %s' % spaces[psn].height)
                    
                    
                    
                    debug('  deleting dupes', p=1)
                    for polygon in polygons:
                        polygons[polygon].deleteSeqDupes(tol=.3)
                        
                    print 'done creating spaces and polygons... Note, this process no longer creates any walls.  Please see "work with spaces" for that'
                                    

        elif i == 'i':
            print 'Importing input file\n'
            importFiles = []
            for file in os.listdir('.'):
                if file[-3:] == 'inp':
                    importFiles.append(file)
            
            if not importFiles:
                print 'No input files in directory, skipping import'
            else:
                if len(importFiles) == 1:
                    importFile = importFiles[0]
                else:
                    c = 0
                    for file in importFiles:
                        c += 1
                        print c, '-', file
                    i2 = raw_input('\nwhich inp? ')
                    print ''
                    importFile = importFiles[int(i2)-1]
        
                print 'Reading inp file %s' % importFile
                
                depth = {'FLOOR':0, 'SPACE':1, 'EXTERIOR-WALL':2, 'INTERIOR-WALL':2, 'UNDERGROUND-WALL':2, 'WINDOW':3, 'DOOR':3}
                parentLookup = {0:'empty', 1:'empty', 2:'empty', 3: 'empty'}
                
    
                f = open(importFile, "r")
                file = f.readlines()
                errors = []
                
                ####################
                ## Read and Parse ##
                ####################
                
    
                parsedInp = parseInp(importFile)
                beginingSection = parsedInp[0]
                polygonSection = parsedInp[1]
                polyToElemSection = parsedInp[2]
                elementSection = parsedInp[3]
                elemToSystemSection = parsedInp[4]
                systemSection = parsedInp[5]
                endingSection = parsedInp[6]
                elementDefaultSection = parsedInp[7]        
                
                #####################
                ## Define Polygons ##
                #####################
                
                active = 0
                lineNumber = 0
                for polygonLine in polygonSection:
                    #lineNumber = lineNumber + 1
                    if polygonLine.find('POLYGON') > 0:
                        active = 1
                        polygonName = polygonLine[:polygonLine.find('=')-1].strip()
                
                    elif polygonLine.find('=') > 0 and active == 1:
                        verticyX = polygonLine[polygonLine.find('(')+1:polygonLine.find(',')].strip()
                        verticyY = polygonLine[polygonLine.find(',')+1:polygonLine.find(')')].strip()
                        verticy = [verticyX, verticyY]
                        vertices.append(verticy)
                
                    elif polygonLine.find('..') > 0:
                        active=0
                        polygons[polygonName]=Polygon(name=polygonName, vertices=vertices)
                        vertices=[]
                
                ##############################
                ## Define Elements Defaults ##
                ##############################
                
                specialSection = 0 # added

                for elementDefaultLine in elementDefaultSection:
                    #print 'looking at line %s' % elementDefaultLine 
                    # find line with element type 
                    if elementDefaultLine[:16]=='SET-DEFAULT FOR ':
                        active = 1
                        elementType = elementDefaultLine[16:].strip()
                        #print 'searching through defaults for element type %s' % elementType
                        
                    # form list of attribute pairs
                    elif specialSection == 1:
                        attributeValue = attributeValue + '\n' + elementDefaultLine[:-1]
                        if '}' in elementDefaultLine:
                            specialSection = 0
                            elementDefaults[elementType, attributeName] = attributeValue

                    elif elementDefaultLine.find('=') > 0 and active == 1:
                        attributeName = elementDefaultLine[0:elementDefaultLine.find('=')-1].strip()
                        attributeValue = elementDefaultLine[elementDefaultLine.find('=')+1:].strip()

                        if (not len(attributeValue)) or attributeValue=='(':
                            specialSection = 1
                            print 'entered special section for element defaults'
                            #time.sleep(.3)
                        else:
                            #define element defaults in format elementdefaults[FLOOR, SPACE-HEIGHT]=10
                            elementDefaults[elementType, attributeName] = attributeValue

                        
                    # done gathering info, defining instance
                    elif elementDefaultLine.find('..') > 0:
                        foundElement = 0
                
                #####################
                ## Define Elements ##
                #####################
                
                currentDepth = 0
                specialSection = 0 # added
                for elementLine in elementSection:
                    
                    if specialSection == 1:
                        attribute[1] = attribute[1] + '\n' + elementLine[:-1]
                        if '}' in elementLine:
                            specialSection = 0
                            attributes.append(attribute)

                    elif elementLine[:1]=='"':
                        active = 1
                
                        elementName = elementLine[:elementLine.find('=')-1].strip()
                        elementType = elementLine[elementLine.find('=')+1:].strip()
                        elementDepth = depth[elementType]
                        
                        #define parent lookup for this elements children
                        parentLookup[elementDepth] = elementName
                
                    # form list of attribute pairs
                    elif elementLine.find('=') > 0 and active == 1:
                        attribute = ([elementLine[0:elementLine.find('=')-1].strip(), elementLine[elementLine.find('=')+1:].strip()])

                        if (not len(attribute[1])) or (attribute[1]=='(') or ('{' in attribute[1] and not '}' in attribute[1] ) :
                            specialSection = 1
                            print 'entered special section'
                            #time.sleep(.3)
                        else:
                            attributes.append(attribute)

                    # find line with element definition
                        
                    # done gathering info, defining instances
                    elif elementLine.find('..') > 0:
                        
                        # close previous attribute

                        #attribute = ''

                        foundElement = 0
                
                        if elementType == 'FLOOR':
                            floors[elementName]=Floor(name=elementName, attributes=attributes)
                            foundElement = 1
                
                        elif elementType == 'SPACE':
                            foundElement = 1
                            spaces[elementName]=Space(name=elementName, attributes=attributes, floor=parentLookup[0])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of space %s' % (parentLookup[0], elementName))

                        elif elementType == 'EXTERIOR-WALL':
                            foundElement = 1
                            eWalls[elementName]=EWall(name=elementName, attributes=attributes, floor=parentLookup[0], space=parentLookup[1])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of exterior wall %s' % (parentLookup[0], elementName))
                            if not (parentLookup[1][:-1] + '-') in elementName:
                                errors.append('Malformed space %s of exterior wall %s' % (parentLookup[1], elementName))
                
                        elif elementType == 'UNDERGROUND-WALL':
                            foundElement = 1
                            uWalls[elementName]=UWall(name=elementName, attributes=attributes, floor=parentLookup[0], space=parentLookup[1])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of underground wall %s' % (parentLookup[0], elementName))
                            if not (parentLookup[1][:-1] + '-') in elementName:
                                errors.append('Malformed space %s of underground wall %s' % (parentLookup[1], elementName))
                
                        elif elementType == 'INTERIOR-WALL':
                            foundElement = 1
                            iWalls[elementName]=IWall(name=elementName, attributes=attributes, floor=parentLookup[0], space=parentLookup[1])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of interior wall %s' % (parentLookup[0], elementName))
                            if not (parentLookup[1][:-1] + '-') in elementName:
                                errors.append('Malformed space %s of interior wall %s' % (parentLookup[1], elementName))
                
                        elif elementType == 'WINDOW':
                            foundElement = 1
                            windows[elementName]=Window(name=elementName, attributes=attributes, floor=parentLookup[0], space=parentLookup[1], wall=parentLookup[2])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of window %s' % (parentLookup[0], elementName))
                            if not (parentLookup[1][:-1] + '-') in elementName:
                                errors.append('Malformed space %s of window %s' % (parentLookup[1], elementName))
                            if not (parentLookup[2][:-1] + '-') in elementName:
                                errors.append('Malformed exterior wall %s of window %s' % (parentLookup[2], elementName))
                
                        elif elementType == 'DOOR':
                            foundElement = 1
                            doors[elementName]=Door(name=elementName, attributes=attributes, floor=parentLookup[0], space=parentLookup[1], wall=parentLookup[2])
                            if not (parentLookup[0][:-1] + '-') in elementName:
                                errors.append('Malformed parent floor %s of door %s' % (parentLookup[0], elementName))
                            if not (parentLookup[1][:-1] + '-') in elementName:
                                errors.append('Malformed space %s of door %s' % (parentLookup[1], elementName))
                            if not (parentLookup[2][:-1] + '-') in elementName:
                                errors.append('Malformed exterior wall %s of door %s' % (parentLookup[2], elementName))
                
                        if foundElement == 0:
                            errors.append('Unknown Element %s' % elementType)
                
                        attributes = []
                        active=0    
    

                
                    

                


                #####################
                ## Define Systems  ##
                #####################
                
                specialSection = 0 # added
                for elementLine in systemSection:
                    
                    if specialSection == 1:
                        attribute[1] = attribute[1] + '\n' + elementLine[:-1]
                        if '}' in elementLine:
                            specialSection = 0
                            attributes.append(attribute)
                
                    # find line with system definition
                    elif elementLine[:1]=='"':
                        active = 1
                        elementName = elementLine[:elementLine.find('=')-1].strip()
                        elementType = elementLine[elementLine.find('=')+1:].strip()
                
                    # form list of attribute pairs
                    elif elementLine.find('=') > 0 and active == 1:
                        attribute = ([elementLine[0:elementLine.find('=')-1].strip(), elementLine[elementLine.find('=')+1:].strip()])

                        if (not len(attribute[1])) or attribute[1]=='(':
                            specialSection = 1
                            print 'entered special section for system'
                            #time.sleep(.3)
                        else:
                            attributes.append(attribute)

                    # done gathering info, defining instance
                    elif elementLine.find('..') > 0:
                        foundElement = 0
                
                        if elementType == 'SYSTEM':
                            systems[elementName]=System(elementName, attributes)
                            foundElement = 1
                            currentSystem = systems[elementName].name
                
                        elif elementType == 'ZONE':
                            zones[elementName]=Zone(elementName, attributes, currentSystem)
                            foundElement = 1
                
                        attributes = []
                        active=0
    
                print
                
                for error in errors:
                    print error
                        
            
        elif i == 'ixl':
            importFiles = []
            for file in os.listdir('.'):
                if file[-3:] == 'xls':
                    importFiles.append(file)
            
            if not importFiles:
                print 'No excel files in directory, skipping import'
            else:
                if len(importFiles) == 1:
                    importFile = importFiles[0]
                else:
                    c = 0
                    for file in importFiles:
                        c += 1
                        print c, '-', file
                    i2 = raw_input('\nwhich inp? ')
                    print ''
                    importFile = importFiles[int(i2)-1]
        
                print 'Reading xls file %s' % importFile
                   


        elif i == 'p':
            #for polygon in polygons:
            #    polygons[polygon].active = 1
            #printActivePolygons(polygons)

            i2 = ''
            while i2 != 'q':
    
                #list active
                if i2 == 'l':
                    printActivePolygons(polygons)
    
                if i2 == 'regex':
                    i3 = raw_input('regex: ')
                    activePolygons = returnActivePolygons(polygons)
                    sortedPolygons = sortQuotedList(activePolygons)
                    for sortedPolygon in sortedPolygons:
                        if re.findall(i3, sortedPolygon):
                            polygons[sortedPolygon].active = 1
                        else:
                            polygons[sortedPolygon].active = 0
                        print sortedPolygon, polygons[sortedPolygon].active, i3

                if i2 == 'dp':
                    activePolygons = returnActivePolygons(polygons)
                    sortedPolygons = sortQuotedList(activePolygons)
                    for sortedPolygon in sortedPolygons:
                        del polygons[sortedPolygon]
                
                
                if i2 =='wf':
                    print 'writing file'
                    writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
    
                #select by number
                if i2[:2] == 's ':
                    print 'running select'
                    nums = i2[1:].split()
                    activePolygons = returnActivePolygons(polygons)
                    #for polygon in activePolygons:
                    #    polygons[polygon].active = 0
                    c = 0
                    sortedPolygons = sortQuotedList(activePolygons)
                    for sortedPolygon in sortedPolygons:
                        c = c + 1
                        isSelected = 0
                        for num in nums:
                            #print 'compare %s to %s' % (num, c)
                            if num == '%s' % c:
                                isSelected = 1
                        if isSelected == 1:
                            #print 'keeping %s -----------------------' % polygons[sortedPolygon].name
                            polygons[sortedPolygon].active = 1
                        else:
                            #print 'setting %s to inactive' % polygons[sortedPolygon].name
                            polygons[sortedPolygon].active = 0

                    printActivePolygons(polygons)


    
                #rename
                if i2 == 'r':
                    print 'Renaming polygons above'
                    print 's to skip'
                    for polygon in returnActivePolygons(polygons):
                        print 'Renaming %s' % polygon
                        i2 = raw_input('to: ')
                        if i2 <> 's' and i2 <> '':
                            duplicateFound = 0
                            newName = i2
                            if newName[:1]<>'"':
                                newName = '"' + newName + '"'
                            if newName[-5:-1]<>'POLY':
                                newName = newName[:-1] + ' POLY' + '"'
                            for polygonCheck in polygons:
                                if newName == polygonCheck:
                                    duplicateFound = 1
                            if duplicateFound==1:
                                print 'Duplicate name found. Skipping'
                            else:
                                # create new
                                polygons[newName]=Polygon(name=newName, vertices=polygons[polygon].vertices)
    
                                # destroy old
                                del polygons[polygon]
                                print 'renamed polygon to %s' % newName
                                # migrate references
                                for floor in floors:
                                    if floors[floor].polygon == polygon:
                                        floors[floor].polygon = newName
                                for eWall in eWalls:
                                    if eWalls[eWall].polygon == polygon:
                                        eWalls[eWall].polygon = newName
                                for iWall in iWalls:
                                    if eWalls[eWall].polygon == polygon:
                                        eWalls[eWall].polygon = newName
                                for uWall in uWalls:
                                    if eWalls[eWall].polygon == polygon:
                                        eWalls[eWall].polygon = newName


                
                #reverse verticy order
                if i2 == 're':
                    print 'Reversing the polygon(s):'
                    printActivePolygons(polygons)
                    i2 = raw_input('yes/[n]')
                    if i2 == 'yes':
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                num = len(polygons[polygon].vertices)
                                verticesNew = []
                                c = 0
                                for verticy in polygons[polygon].vertices:
                                    verticesNew.append(polygons[polygon].vertices[num-c-1])
                                    c = c + 1
                                polygons[polygon].vertices = verticesNew
                    else:
                        print 'okay, aborting operation'


                #reverse verticy order
                if i2 == 'xyswap':
                    print 'Reversing the polygon(s):'
                    printActivePolygons(polygons)
                    i2 = raw_input('yes/[n]')
                    if i2 == 'yes':
                        negX = 0
                        negY = 0
                        QNegX = raw_input('negate new X? yes/[n]')
                        if QNegX == 'yes':
                            negX = 1
                        QNegY = raw_input('negate new Y? yes/[n]')
                        if QNegY == 'yes':
                            negY = 1
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                num = len(polygons[polygon].vertices)
                                print num
                                verticesNew = []
                                c = 0
                                for verticy in polygons[polygon].vertices:
                                    newX = verticy[1]
                                    newY = verticy[0]
                                    print newX
                                    print newY
                                    if negX:
                                        if newX[0] == '-':
                                            newX = newX[1:]
                                        else:
                                            newX = '-' + newX
                                    if negY:
                                        if newY[0] == '-':
                                            newY = newY[1:]
                                        else:
                                            newY = '-' + newY
                                    newVerticy = [newX, newY]
                                    verticesNew.append(newVerticy)
                                    c = c + 1
                                polygons[polygon].vertices = verticesNew
                                print polygons[polygon].vertices
                    else:
                        print 'okay, aborting operation'


    
                if i2 == 'rere':
                    print 'Reversing, Transposing the polygon(s):'
                    printActivePolygons(polygons)
                    i2 = raw_input('yes/[n]')
                    if i2 == 'yes':
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                num = len(polygons[polygon].vertices)
                                print num
                                verticesReversed = []
                                c = 0
                                for verticy in polygons[polygon].vertices:
                                    currentVerticyTransposed = []
                                    currentVerticy = polygons[polygon].vertices[num-c-1]
                                    currentVerticyTransposed.append(currentVerticy[1])
                                    currentVerticyTransposed.append(currentVerticy[0])
                                    verticesReversed.append(currentVerticyTransposed)
                                    c = c + 1
                                print polygons[polygon].vertices
                                polygons[polygon].vertices = verticesReversed
                                print polygons[polygon].vertices
                    else:
                        print 'okay, aborting operation'
    

                #move x coordinate           
                if i2 == 'mv':
                    print 'Moving Coordinates in the polygon(s):'
                    printActivePolygons(polygons)
                    print 'Moving Coordinates in the polygon(s) above:'
                    i2 = raw_input('yes/[n]')
                    if i2 == 'yes':
                        xMoveInput = raw_input('translate x')
                        yMoveInput = raw_input('translate y')
                        xMove = string.atof(xMoveInput)
                        yMove = string.atof(yMoveInput)
                        #scale = raw_input('scale')
                        
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                num = len(polygons[polygon].vertices)
                                print num
                                verticesNew = []
                                for verticy in polygons[polygon].vertices:
                                    verticyNew = []
                                    print xMove
                                    oldX = string.atof(verticy[0])
                                    newX = round(oldX + xMove,2)
                                    oldY = string.atof(verticy[1])
                                    newY = round(oldY + yMove,2)
                                    verticyNew.append(newX)
                                    verticyNew.append(newY)
                                    verticesNew.append(verticyNew)
                                print 'translated:'
                                for verticy in polygons[polygon].vertices:
                                    print ('%s, %s') % (verticy[0], verticy[1])
                                print 'to:'
                                for verticy in verticesNew:
                                    print ('%s, %s') % (verticy[0], verticy[1])
                                polygons[polygon].vertices = verticesNew
                    else:
                        print 'okay, aborting operation'
    

                if i2 == 'scale':
                    print 'Scaling  Coordinates in the polygon(s):'
                    printActivePolygons(polygons)
                    print 'Scaling Coordinates in the polygon(s) above:'
                    i2 = raw_input('yes/[n]')
                    if i2 == 'yes':
                        scaleInput = raw_input('scale')
                        scale = string.atof(scaleInput)
                        
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                num = len(polygons[polygon].vertices)
                                print num
                                verticesNew = []
                                for verticy in polygons[polygon].vertices:
                                    verticyNew = []
                                    oldX = string.atof(verticy[0])
                                    newX = round(oldX * scale, 2)
                                    oldY = string.atof(verticy[1])
                                    newY = round(oldY * scale,2)
                                    verticyNew.append(newX)
                                    verticyNew.append(newY)
                                    verticesNew.append(verticyNew)
                                print 'scaled:'
                                for verticy in polygons[polygon].vertices:
                                    print ('%s, %s') % (verticy[0], verticy[1])
                                print 'to:'
                                for verticy in verticesNew:
                                    print ('%s, %s') % (verticy[0], verticy[1])
                                polygons[polygon].vertices = verticesNew
                    else:
                        print 'okay, aborting operation'


                if i2 == 'rotate':
                    rotateActivePolygons()



    
                # filter            
                if i2[:1] == 'f':
                    if len(i2)==1:
                        print 'filter requires argument'
                    else:
                        subs = i2[1:].split()
                        print subs
                        for polygon in polygons:
                            if polygons[polygon].active==1:
                                active = 0
                                for sub in subs:
                                    #print 'looking for %s' % sub
                                    if string.find(polygons[polygon].name, sub) >= 0:
                                        active = active + 1
                                if active > 0:
                                    pass
                                    #print 'keeping %s' % polygons[polygon].name
                                else: 
                                    #print 'reomving %s' % polygons[polygon].name
                                    polygons[polygon].active=0
                    printActivePolygons(polygons)

                # find space polygons only
                if i2 == 'sp':
                    for polygon in polygons:
                        if polygons[polygon].active==1:
                            print '\ninspecting %s ' % polygon
                            if len(re.findall("\S\-", polygon)) == 1:
                                polygons[polygon].active = 1
                            else:
                                polygons[polygon].active = 0
                            print '   %s ' % len(re.findall("\S\-", polygon))
                    printActivePolygons(polygons)
    
                
                
                if i2 == 'a':
                    for polygon in polygons:
                        polygons[polygon].active = 1
                    activePolygons = sortQuotedList(list(polygons))
                    printChoices(activePolygons)
    
                
                
                #orphans
                if i2 == 'po':
                    for polygon in polygons:
                        if polygons[polygon].active == 1:
                            orphaned = 1
                            for floor in floors:
                                if floors[floor].polygon == polygon:
                                    orphaned = 0
                            for eWall in eWalls:
                                if eWalls[eWall].polygon == polygon:
                                    orphaned = 0
                            for iWall in iWalls:
                                if iWalls[iWall].polygon == polygon:
                                    orphaned = 0
                            for uWall in uWalls:
                                if uWalls[uWall].polygon == polygon:
                                    orphaned = 0
                            if orphaned == 0:
                                polygons[polygon].active == 1
                            else:
                                polygons[polygon].active == 1
                    printActivePolygons(polygons)
    

                #parents
                if i2 == 'pp':
                    for polygon in polygons:
                        if polygons[polygon].active == 1:
                            print ('Listing Parents of %s') % polygon
                            orphaned = 1
                            for floor in floors:
                                if floors[floor].polygon == polygon:
                                    print floors[floor]
                                    orphaned = 0
                            for eWall in eWalls:
                                if eWalls[eWall].polygon == polygon:
                                    print eWalls[eWall]
                                    orphaned = 0
                            for iWall in iWalls:
                                if iWalls[iWall].polygon == polygon:
                                    print iWalls[iWall]
                                    orphaned = 0
                            for uWall in uWalls:
                                if uWalls[uWall].polygon == polygon:
                                    print uWalls[uWall]
                                    orphaned = 0
                            if orphaned == 1:
                                print 'orphan'

                if i2 == 'pv':
                        for polygon in polygons:
                            if polygons[polygon].active == 1:
                                print 
                                print polygon
                                for v in polygons[polygon].vertices:
                                    print v

                if i2 == 'cc':
                    combineCloseVerticies()

                if i2 == 'cc2':
                    combineCloseVerticies2()
                        
                if i2 == 'cc3':
                    combineCloseVerticies3()

                                




                
                    
    
                print 'Top'
                print '  |'
                print '  +--Working with Polygons:'
                print
                print '   a  - expend current selection to all'
                print '   l  - list current selection'
                print '   f  - filter'
                print '   s  - select'
                print '   ds  - delete selected polyogns'
                print '   sp  - filter space polygons only'
                print '   po  - print orphans'
                print '   pp  - print parents'
                print '   pp  - print vertices'
                print '   regex - select by regular expression'
                print '   r  - rename'
                print '   rotate - rotate vertices'
                print '   scale  - scale vertices'
                print '   mv  - move vertices'
                print '   xyswap - swap x/y vertices'
                print '   rere - reverse, transpose vertices'
                print '   re - reverse vertices, transpose to maintain ccw'
                print '   cc1 - combine close vertices 1'
                print '   cc2 - combine close vertices 2'
                print '   cc3 - combine close vertices 3'
                print 
                print '   wf - write file'
                print '   q  - quit up to Top menu'
                print
                i2 = raw_input('   >')

            
        elif i == 's':
            i2 = ''
            while i2 != 'q':

                if i2 == 'wf':
                    writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)    

                if i2 == 'l':                
                    printActiveElements(spaces)
    
                if i2[:2] == 's ':
                    if len(i2)==1:
                        print 'select requres argument'
                    else:
                        nums = i2[1:].split()
                        activeElements = returnActiveElements(spaces)
                        c = 0
                        sortedElements = sortQuotedList(activeElements)
                        for sortedElement in sortedElements:
                            c = c + 1
                            isSelected = 0
                            for num in nums:
                                #print 'compare %s to %s' % (num, c)
                                if num == '%s' % c:
                                    isSelected = 1
                            if isSelected == 1:
                                #print 'keeping %s -----------------------' % elements[sortedElement].name
                                spaces[sortedElement].active = 1
                            else:
                                #print 'setting %s to inactive' % elements[sortedElement].name
                                spaces[sortedElement].active = 0
                        print '\n'
                        printActiveElements(spaces)
    


                if i2[:2] == 'f ':
                    if len(i2)==1:
                        print 'filter requires argument'
                    else:
                        subs = i2[1:].split()
                        print subs
                        for space in spaces:
                            if spaces[space].active==1:
                                active = 0
                                for sub in subs:
                                    #print 'looking for %s' % sub
                                    if string.find(spaces[space].name, sub) >= 0:
                                        active = active + 1
                                if active > 0:
                                    pass
                                    #print 'keeping %s' % elements[element].name
                                else: 
                                    #print 'reomving %s' % elements[element].name
                                    spaces[space].active=0
                    printActiveElements(spaces)
    


                if i2 == 'i':
                    for space in spaces:
                        if spaces[space].active==1:
                            spaces[space].active=0
                        else:
                            spaces[space].active=1
                    printActiveElements(spaces)



                                

                if i2 == 'a':
                    for space in spaces:
                        spaces[space].active = 1
                    activeElements = sortQuotedList(list(spaces))
                    print len(activeElements)
                    printChoices(activeElements)


                if i2 == 'c':
                    activeElements = returnActiveElements(spaces)
                    numSpaces = len(spaces)
                    numEWalls = len(eWalls)
                    numUWalls = len(uWalls)
                    numIWalls = len(iWalls)
                    numWindows = len(windows)
                    numPolygons = len(polygons)
                    
                    print 'Spaces: %s' % numSpaces
                    print 'EWalls: %s' % numEWalls
                    print 'UWalls: %s' % numUWalls
                    print 'IWalls: %s' % numIWalls
                    print 'Windows: %s' % numWindows
                    print 'Polygons: %s' % numPolygons
            
                if i2 == 'urep':
                    activeElements=returnActiveElements(spaces)
                    perim = 0
                    floorArea = 0
                    roofArea = 0
                    print 'wall|tilt|location|area|length|width|z|perimeter|note'

                    for space in activeElements:
                        childUWalls = spaces[space].returnUWalls(uWalls)
                        for childUWall in childUWalls:
                            debug('%s' % (childUWall))
                            note = ''
                            t = uWalls[childUWall].returnTilt()
                            l = uWalls[childUWall].location
                            h = uWalls[childUWall].returnHeight()
                            w = uWalls[childUWall].returnWidth()
                            a = uWalls[childUWall].area()
                            z = uWalls[childUWall].returnTotalZ()
                            p = 0
                            if t == 180:
                                floorArea += a
                                poly = uWalls[childUWall].returnPolygon(spaces)
                                vs = polygons[poly].vertices
                            elif t == 0:
                                roofArea += a
                            elif t == 90:
                                p = w
                            
                            debug('%s|%s|%s|%s|%s|%s|%s|%s|%s' % (childUWall, t, l, a, h, w, z, p, note))
                                                
                                                
                                            
                                            

                                        
                                        
                                        



                    print ''
                    print 'Perimeter:  %s' % perim
                    print 'Floor Area: %s' % floorArea
                    print 'Roof Area: %s' % roofArea
                            

                if i2 == 'rep':
                    reportFile = '%s.rep' % (inpFile[-4:])    
                    activeElements = returnActiveElements(spaces)
                    
                    # define attributes from defaults 
                    defaultWindowHeight = ''
                    defaultWindowWidth = ''
                    defaultEWallHeight = ''
                    defaultEWallWidth = ''
                    defaultSpaceHeight = ''
                    defaultFloorFloorHeight = ''
                    defaultFloorSpaceHeight = ''
                    if elementDefaults.has_key(('WINDOW', 'HEIGHT')):
                        defaultWindowHeight = elementDefaults['WINDOW', 'HEIGHT']
                    if elementDefaults.has_key(('WINDOW', 'WIDTH')):
                        defaultWindowWidth = elementDefaults['WINDOW', 'WIDTH']
                    if elementDefaults.has_key(('EXTERIOR-WALL', 'HEIGHT')):
                        defaultEWallHeight = elementDefaults['EXTERIOR-WALL', 'HEIGHT']
                    if elementDefaults.has_key(('EXTERIOR-WALL', 'WIDTH')):
                        defaultEWallWidth = elementDefaults['EXTERIOR-WALL', 'WIDTH']
                    if elementDefaults.has_key(('SPACE', 'HEIGHT')):
                        defaultSpaceHeight = elementDefaults['SPACE', 'HEIGHT']
                    if elementDefaults.has_key(('FLOOR', 'FLOOR-HEIGHT')):
                        defaultFloorFloorHeight = elementDefaults['FLOOR', 'FLOOR-HEIGHT']
                    if elementDefaults.has_key(('FLOOR', 'SPACE-HEIGHT')):
                        defaultFloorSpaceHeight = elementDefaults['FLOOR', 'SPACE-HEIGHT']
    
                    # iterate through spaces
                    totalEWallArea = 0
                    totalWindowArea = 0
                    for space in activeElements:
                        # check - determinte number of Ewalls
                        numberOfEWalls = spaces[space].countEWalls()
                        print spaces[space].polygon
                        print ('%s       %s/%s') % (space, numberOfEWalls, spaces[space].countVertices())
    
                        #define space/floor attributes
                        spaceHeight = spaces[space].height
                        floorFloorHeight = floors[spaces[space].floor].floorHeight
                        floorSpaceHeight = floors[spaces[space].floor].spaceHeight
                        
                        childEWalls = spaces[space].returnEWalls(eWalls)
    
                        # iterate though ewall for space
                        for childEWall in childEWalls:
                            location = eWalls[childEWall].location
                            # exclude floors and ceilings
                            if location <> 'TOP' and location <> 'BOTTOM':
                                # check - print ewall
                                print '--------------------------------'
                                print '  %s' % childEWall
                                floor = eWalls[childEWall].floor
                                eWallHeight = eWalls[childEWall].height
                                eWallWidth = eWalls[childEWall].width
                                print '--------------------------------'
                                print 'FLOOR: %s' % floor
                                print ' FLOOR-HEIGHT: %s' % floorFloorHeight
                                print ' SPACE-HEIGHT: %s' % floorSpaceHeight
                                print ' DEFAULT FLOOR-HEIGHT: %s' % defaultFloorFloorHeight
                                print ' DEFAULT SPACE-HEIGHT: %s' % defaultFloorSpaceHeight
                                print 'SPACE: %s' % space
                                print ' HEIGHT: %s' % spaceHeight
                                print ' DEFAULT HEIGHT: %s' % defaultSpaceHeight
                                print 'EWALL: %s' % childEWall
                                print ' LOCATION: %s' % location
                                print ' HEIGHT: %s' % eWallHeight
                                print ' WIDTH: %s' % eWallWidth
                                print ' DEFAULT HEIGHT: %s' % defaultEWallHeight
                                print ' DEFAULT WIDTH: %s' % defaultEWallWidth
                                print '--------------------------------'
        
                                # DETERMINE HEIGHT
                                # if height not explicitly defined:
                                # 1) check if user-defined default ewall height exists (very unusual), if not 
                                # 2) check if space height is explicitly defined, if not 
                                # 3) check if user-defined default space height exists (very unusual), if not 
                                # For non plenum
                                # 4a) check if floor's Space-Height is explicitly defined, use floor's Space Height 
                                # 4a) check if floor's Floor-Height is explicitly defined, use floor's Space Height 
                                # 4b) see if floor's defaultSpaceHeight is defined, use
                                # 4c) see if floor's defaultFloorHeight is defined, use
                                # 4d) skip
                                #
                                # For non plenum
                                # 5a) check if floor's Floor-Height is explicitly defined, use floor's Floor-Height minus Space-Height
                                # 5b) see if floor's defaultFloor is defined, use DefaultFloor-Height minus DefaultSpace-Height
                                # 5c) skip
                                
                                if eWallHeight <> '':
                                    eWallHeight = eWallHeight
                                    print 'using explicit ewall height %s' % eWallHeight
                                # 1) check if user-defined default ewall height exists (very unusual)
                                elif defaultEWallHeight <> '':
                                    print 'using default ewall height %s' % defaultEWallHeight
                                    eWallHeight = defaultEWallHeight
                                # 2) check if space height is explicitly defined, if not 
                                elif spaceHeight <> '':
                                    print 'using explicit space height %s' % spaceHeight
                                    eWallHeight = spaceHeight
                                # 3) check if user-defined default space height exists (very unusual)
                                elif spaceHeight <> '':
                                    print 'using default space height %s' % defaultSpaceHeight
                                    eWallHeight = defaultSpaceHeight
                                # 4) height base on floor, non-plenum
                                elif spaces[space].zoneType <> 'PLENUM':
                                    print 'Space is NOT plenum'
                                    # floorSpaceHeight, defaultFloorSpaceHeight, floorFloorHeight, defaultfloorFloorHeight
                                    if floorSpaceHeight <> '':
                                        eWallHeight = floorSpaceHeight
                                        print 'using floor space height %s' % floorSpaceHeight
                                    elif defaultFloorSpaceHeight <> '':
                                        eWallHeight = defaultFloorSpaceHeight
                                        print 'using default floor space height %s' % defaultFloorSpaceHeight
                                    elif floorFloorHeight <> '':
                                        eWallHeight = floorFloorHeight
                                        print 'using floor floor height %s' % floorFloorHeight
                                    elif defaultFloorFloorHeight <> '':
                                        eWallHeight = defaultFloorFloorHeight
                                        print 'using default floor floor height %s' % defaultFloorFloorHeight
                                    else:
                                        print 'skipping, setting height to 0'
                                        eWallHeight = 0
                                # heigth based on floor - plenum
                                else:
                                    print 'Space is plenum'
                                    if floorSpaceHeight == '':
                                        floorSpaceHeight = defaultFloorSpaceHeight
                                    if floorFloorHeight == '':
                                        floorFloorHeight = defaultFloorFloorHeight
                                    if string.atof(floorSpaceHeight) >= string.atof(floorFloorHeight) or floorSpaceHeight=='' or floorFloorHeight=='':
                                        print 'floor space height %s' % floorSpaceHeight
                                        print 'floor floor height %s' % floorFloorHeight
                                        print 'skipping, setting height to 0'
                                        eWallHeight = 0
                                    else:
                                        eWallHeight = string.atof(floorFloorHeight) - string.atof(floorSpaceHeight)
                                        print 'floor space height %s' % floorSpaceHeight
                                        print 'floor floor height %s' % floorFloorHeight
                                        print 'height %s' % eWallHeight
                                        
                                    
    
                                # DETERMINE Width
                                # if width not explicitly defined:
                                # 1) use polygon branch
        
                                if eWallWidth <> '':
                                    eWallWidth = eWallWidth
                                    print 'using explicit ewall width %s' % eWallWidth
                                else:
                                    currentPolygon = polygons[spaces[space].polygon].name
                                    print currentPolygon
                                    currentPolygonvertices = polygons[currentPolygon].vertices
                                    print currentPolygonvertices
                                    polygonLength = len(polygons[currentPolygon].vertices)
                                    wallVerticy = location[7:]
                                    wallVerticyInteger = string.atoi(wallVerticy)
                                    print polygonLength
                                    print wallVerticyInteger
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
                                    print ('(%s, %s), (%s, %s)') % (x1, y1, x2, y2)
                                    print eWallWidth
    
                                # Calculate wall area
                                eWallHeightNumber = round(string.atof(eWallHeight),2) 
                                eWallWidthNumber = round(string.atof(eWallWidth),2) 
                                eWallArea = round(eWallHeightNumber*eWallWidthNumber,2)
                                totalEWallArea = totalEWallArea + eWallArea
                                print '--------------------------------'
                                print 'EWALL AREA: %s' % eWallArea
                                print '--------------------------------'
                                
                                wallLine = 'WALL, %s, %s, %s, %s\n' % (childEWall, eWallHeightNumber, eWallWidthNumber, eWallArea)
                                echoLine = 'echo %s >> %s' % (wallLine[:-1], reportFile)
                                os.system(echoLine)
    
                                # Calculate window area    
                                eWallWindows = eWalls[childEWall].returnWindows(windows)
                                for window in eWallWindows:
                                    windowHeight = windows[window].height
                                    windowWidth = windows[window].width
    
                                    print '--------------------------------'
                                    print 'WINDOW: %s' % window
                                    print ' HEIGHT: %s' % windowHeight
                                    print ' WIDTH: %s' % windowWidth
                                    print ' DEFAULT HEIGHT: %s' % defaultWindowHeight
                                    print ' DEFAULT WIDTH: %s' % defaultWindowWidth
                                    print '--------------------------------'
    
                                    ### Window WIDTH ###
                                    # if windows width explicitly defined
                                    if windowWidth <> '':
                                        windowWidth = windowWidth
                                    # if windows width defined as wall width
                                    elif windowWidth == '{#P("WIDTH")}':
                                        windowWidth = eWallWidth
                                    # if windows width defined as wall width
                                    elif defaultWindowWidth == '{#P("WIDTH")}':
                                        windowWidth = eWallWidth
                                    elif defaultWindowWidth <> '':
                                        windowWidth = defaultWindowWidth
                                    else:
                                        pass
                                        print 'could not determine window width for %s' % window
                                        
                                    ### Window HEIGHT ###                                    
                                    # if windows height explicitly defined
                                    if windowHeight <> '':
                                        windowHeight = windowHeight
                                    elif defaultWindowHeight <> '':
                                        windowHeight = defaultWindowHeight
                                    else:
                                        x=x
                                        print 'could not determine window height for %s' % window
                                    
                                    if windowWidth <> '' and windowHeight <> '':
                                        windowHeightNumber = round(string.atof(windowHeight),2)
                                        windowWidthNumber = round(string.atof(windowWidth),2)
                                        windowArea = round(windowWidthNumber * windowHeightNumber,2)
                                        totalWindowArea = totalWindowArea + windowArea
                                        print '--------------------------------'
                                        print 'WINDOW AREA: %s' % eWallArea
                                        print '--------------------------------'
                                        windowLine = 'WINDOW, %s, %s, %s, %s\n' % (window, windowHeightNumber, windowWidthNumber, windowArea)
                                        echoLine = 'echo %s >> %s' % (windowLine[:-1], reportFile)                                    
                                        os.system(echoLine)
                                    else:
                                        windowLine = 'WINDOW ERROR, %s, %s, %s\n' % (window, windowHeight, windowWidth)
                                        echoLine = 'echo %s >> %s' % (windowLine[:-1], reportFile)                                    
                                        os.system(echoLine)
    
    
    
    
    
    
                            else:
                                wallLine = 'ROOF OR FLOOR, %s\n' % (childEWall)
                                echoLine = 'echo %s >> %s' % (wallLine[:-1], reportFile)
                                os.system(echoLine)
                                
                                #frep.write(wallLine)
                                print 'writing %s' % wallLine
    
    
                                print '%s is floor or roof - excluding' % (childEWall)
                    print 'Total EWall Area: %s' % totalEWallArea
                    print 'Total Window Area: %s' % totalWindowArea
                    #frep.close
                            
                        
                # Advanced create roofs
                if i2 == 'acr':
                    advancedCreateRoofs()


                # Advanced create floors
                if i2 == 'acf':
                    advancedCreateFloors()


 

                # automatically create exterior and interior wall
                if i2 == 'acei':
                    createInteriorAndExteriorWalls()

                if i2 == 'dsw':
                    activeElements = returnActiveElements(spaces)
                    for space in activeElements:
                       print 'checking ', space
                       for eWall in spaces[space].returnEWalls(eWalls):
                           print '   checking', eWall
                           for window in eWalls[eWall].returnWindows(eWalls):
                               del windows[window]


                    windows = {}
                    print 'Deleted all windows'
                            
                # delete exterior walls
                if i2 == 'dae':
                    eWalls = {}
                    print 'Deleted exterior walls'
    
                if i2 == 'dau':
                    uWalls = {}
                    print 'Deleted underground walls'
    

                if i2 == 'dai':
                    iWalls = {}
                    print 'Deleted all Interior Walls'

                if i2 == 'dsr':
                    activeElements = returnActiveElements(spaces)
                    for space in activeElements:
                       print 'checking ', space
                       for eWall in spaces[space].returnEWalls(eWalls):
                           print '   checking', eWall
                           if eWall.find('ROOF') > -1:
                               print '      found', eWall
                               del eWalls[eWall]
                               print '      deleted %s' % eWall

                if i2 == 'dsh':
                    activeElements = returnActiveElements(spaces)
                    for space in activeElements:
                       print 'checking ', space
                       for eWall in spaces[space].returnEWalls(eWalls):
                           print '   checking', eWall
                           if eWall.find('HANG') > -1:
                               print '      found', eWall
                               del eWalls[eWall]
                               print '      deleted %s' % eWall

                    
                    
                

                                
                                 
                                
                ## create windows on all selected spaces
                if i2[:2] == 'cw':
                    if i2[2:4] == 'xp':
                        excludePlenum = 1
                    else:
                        excludePlenum = 0
                    activeElements = returnActiveElements(spaces)
                    addedWindows = []
                    for space in activeElements:
                        print '----------------'
                        print '%s (%s)' % (space, spaces[space].countVertices())
                        print '----------------'
                        childEWalls = spaces[space].returnEWalls(eWalls)
                        for childEWall in childEWalls:
                            if eWalls[childEWall].location <> 'TOP' and eWalls[childEWall].location <> 'BOTTOM':
                                if excludePlenum == 0 or spaces[space].zoneType <> 'PLENUM':
                                    print excludePlenum
                                    print spaces[space].zoneType
                                    print 'adding window to %s' % childEWall
                                    window = '"%s-W1"' % (eWalls[childEWall].name[1:-1])
                                    attributes = ''
                                    windows[window]=Window(name=window, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name, wall=verticeseWalls[childEWall].name)
                                    addedWindows.append(windows[window].name)
                                else:
                                    print 'skipping due to plenum restrictions'
                            else:
                                print 'skipping window creation for %s' % childEWall

                # removes plenum and associated objects, work in progress, will eventually move roof
                if i2 == 'dsp':
                    activeSpaces = returnActiveElements(spaces)
                    for space in activeSpaces:
                        if spaces[space].zoneType == 'PLENUM':
                            print '\n -- deleteing plenum %s' % space
                            plenumHeight = spaces[space].trueHeight()
                            plenumP = space.find('-') - 1
                            if (plenumP < 1) or (space[plenumP] <> "P"):
                                print '   ERROR: plenum %s does not contain a "P" in the right spot' % space
                                time.sleep(5)
                            else:
                                spaceBelow = space[:plenumP] + space[plenumP+1:]
                                if not spaceBelow in spaces:
                                    print '   ERROR: no space below found'
                                    time.sleep(5)
                                else:
                                    spaceBelowHeight = spaces[spaceBelow].trueHeight()
                                    newSpaceBelowHeight = spaceBelowHeight + plenumHeight
                                    spaces[space].delete(eWalls, uWalls, iWalls, windows)
                                    spaces[spaceBelow].height = newSpaceBelowHeight
                                    print '   height of space below %s modified to %s' % (spaceBelow, newSpaceBelowHeight)
                                    print '   SUCCESS'


                                            # preserve roof at later date

                                            #spaceEWalls = spaces[space].returnEWalls(eWalls)
                                            #for spaceWall in spaceWalls:
                                            #    roofs = []
                                            #    if eWalls[spaceWall].location = 'TOP':
                                            #        print 'preserving roof'
                                            #        roofs.append[ 
                                            #                     eWalls[spaceWall].construction,
                                            #                     eWalls[spaceWall].shape,
                                            #                     eWalls[spaceWall].polygon,
                                            #                     eWalls[spaceWall].x,
                                            #                     eWalls[spaceWall].y,
                                            #                     eWalls[spaceWall].z,
                                            #                     eWalls[spaceWall].tilt,
                                            #                     eWalls[spaceWall].width,
                                            #                     eWalls[spaceWall].height,
                                            #                     eWalls[spaceWall].azimuth,]
                    
                
      
                if i2 == 'cz':
                    createZones()
                     

                if i2 == 'chic':
                    createHorizontalInteriorWalls()
                         
                if i2 == 'siw':
                    splitInteriorWalls()

                if i2 == 'vs':
                    verifySpaces()
                         
                        
                # interior wall management 
                if i2 == 'aiwm':
                    
                    activeElements = returnActiveElements(spaces)
                    i3 = 'c'

                    xb = '-'
                    yb = '-'
                    aDoe = '-'
                    lTol = '-'
                    aTol = '-'
                    xMin = '-'
                    xMax = '-'
                    yMin = '-'
                    yMax = '-'
                    hMin = '-'
                    hMax = '-'
                    wMin = '-'
                    wMax = '-'
                    #tMin = '90'
                    #tMax = '90'
                    regex = '-'
                    horiz = 'n'
                    vert = 'y'
                    tilted = 'n'
                    plenum = 'y'
                    poly = 'n'
                    custAzimuth = 'n'                        
                    matchSpaces = '-'

                    while i3 <> 'q':


                        if i3 == 'c':
                            print 'Changing inputs'
                    
                            
                            # get comparison coordinates
                            xMinTemp = raw_input('xMin [%s]' % xMin)
                            xMaxTemp = raw_input('xMax [%s]' % xMax)
                            yMinTemp = raw_input('yMin [%s]' % yMin)
                            yMaxTemp = raw_input('yMax [%s]' % yMax)
                            hMinTemp = raw_input('hMin [%s]' % hMin)
                            hMaxTemp = raw_input('hMax [%s]' % hMax)
                            wMinTemp = raw_input('wMin [%s]' % wMin)
                            wMaxTemp = raw_input('wMax [%s]' % wMax)
                            #tMinTemp = raw_input('tMin [%s]' % tMin)
                            #tMaxTemp = raw_input('tMax [%s]' % tMax)
                            regexTemp = raw_input('regex [%s]' % regex)
                            
                            horizTemp = raw_input('horiz [%s]' % horiz)
                            vertTemp = raw_input('vert [%s]' % vert)
                            tiltedTemp = raw_input('tilted [%s]' % tilted)
                            plenumTemp = raw_input('plenum [%s]' % plenum)
                            polyTemp = raw_input('poly [%s]' % poly)
                            custAzimuthTemp = raw_input('Custom Azimuth [%s]' % custAzimuth)
                            matchSpacesTemp = raw_input('match spaces [%s]' % matchSpaces)
                            
                            
                            xMin = fixInput(xMinTemp, xMin)
                            xMax = fixInput(xMaxTemp, xMax)
                            yMin = fixInput(yMinTemp, yMin)
                            yMax = fixInput(yMaxTemp, yMax)
                            hMin = fixInput(hMinTemp, hMin)
                            hMax = fixInput(hMaxTemp, hMax)
                            wMin = fixInput(wMinTemp, wMin)
                            wMax = fixInput(wMaxTemp, wMax)
                            #tMin = fixInput(tMinTemp, tMin)
                            #tMax = fixInput(tMaxTemp, tMax)
                            if regexTemp != '':
                                regex = regexTemp
                            if matchSpacesTemp != '':
                                matchSpaces = matchSpacesTemp
                            if not aDoe == '-':
                                a = swapAngleType(aDoe)
                            if plenumTemp != '':
                                plenum = plenumTemp
                            if horizTemp != '':
                                horiz = horizTemp
                            if vertTemp != '':
                                vert = vertTemp
                            if tiltedTemp != '':
                                tilted = tiltedTemp
                            if polyTemp != '':
                                poly = polyTemp
                            if custAzimuthTemp != '':
                                custAzimuth = custAzimuthTemp
        
        
                            # determine if wall falls in line with comparison coordinates
                            goodIWalls = []
                            addedIWalls = []
                            for space in activeElements:
                                #childIWalls = spaces[space].returnAllIWalls(iWalls)
                                childIWalls = spaces[space].returnAllIWalls(iWalls)
                                
                                for childIWall in childIWalls:
                                    otherSpace = iWalls[childIWall].nextTo
                                    verbose = 1
                                    good = 1
                                    
                                    if childIWall in addedIWalls:
                                        print 'Skipping %s - Is already added from another space' % childIWall
                                        good = 0
                                        #time.sleep(.2)
                                    
                                    if (spaces[space].zoneType == 'PLENUM' or spaces[otherSpace].zoneType) and plenum == 'n':
                                        print 'Skipping %s - Is adjacent to plenum' % childIWall
                                        good = 0

                                    iWallTilt = iWalls[childIWall].returnTilt()
                                    if (iWallTilt == 0 or iWallTilt == 180) and horiz == 'n':
                                        print 'Skipping %s - Is a floor or roof' % childIWall
                                        good = 0
                                    if (iWallTilt == 90) and vert == 'n':
                                        print 'Skipping %s - Is a vertical wall' % childIWall
                                        good = 0
                                    if (iWallTilt != 90 and iWallTilt != 180 and iWallTilt != 0 ) and tilted == 'n':
                                        print 'Skipping %s - Is tilted' % childIWall
                                        good = 0


                                    if iWalls[childIWall].polygon != '' and poly == 'n':
                                        print 'Skipping %s - Is a polygon' % childIWall
                                        good = 0
                                    if iWalls[childIWall].azimuth != '' and custAzimuth == 'n':
                                        print 'Skipping %s - Has custom azimuth' % childIWall
                                        good = 0

                                    if good:
                                                   
                                        #print 'Inspecting %s' % childIWall
                                        debug = 1
                                        
                                        good = iWalls[childIWall].testWall(xMin=xMin, xMax=xMax, yMin=yMin, yMax=yMax, hMin=hMin, hMax=hMax, wMin=wMin, wMax=wMax, regex=regex, matchSpaces=matchSpaces, verbose=verbose)                                
                                        
                                        if good:
                                            try:
                                                coords = iWalls[childIWall].returnCoords()
                                            except:
                                                coords = [None , None , None , None]

                                            try:
                                                width = iWalls[childIWall].returnWidth()
                                            except:
                                                width = None

                                            try:
                                                height = iWalls[childIWall].returnHeight()
                                            except:
                                                height = None

                                            
                                            goodIWalls.append([childIWall, iWalls[childIWall].returnTotalZ(), width, height, [coords[0], coords[2]], [coords[1], coords[3]]])
                                            addedIWalls.append(childIWall)
        
                            if not goodIWalls:
                                print 'Did not find any matching walls'
                            else:
                                print 'Found %s matching walls\n\n' % len(goodIWalls)


                        if i3 == 'pw':

                            if not goodIWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                print 'Found %s matching walls\n' % len(goodIWalls)
                            for goodIWall in goodIWalls:
                                print goodIWall[0]
                                print '    x: %s' % goodIWall[1]
                                print '    z: %s' % goodIWall[2]
                                print '    w: %s' % goodIWall[3]
                                print '    h: %s' % goodIWall[4]
                                print 'space: %s' % iWalls[goodIWall[0]].space
                                print 'next2: %s' % iWalls[goodIWall[0]].nextTo
                                print

                        if i3 =='wf':
                            print 'writing file'
                            writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
                            j = 0
                            countOnly = 1

                        if i3 == 'const':
                            print 'Choose construction type:\n'
                            constructions = []
                            c = 0
                            for line in beginingSection:
                                #print line
                                if  '" = CONSTRUCTION' in line:
                                    c += 1
                                    construction = re.findall('".*"', line)[0]
                                    constructions.append(construction)
                                    print c, construction
                            i4 = raw_input(' > ')
                            if 1==1:
                            #try:
                                n = int(i4)
                                print n
                                chosenConstruction = constructions[n-1]
                                print chosenConstruction
                                for goodIWall in goodIWalls:
                                    print goodIWall
                                    #print type(goodEWall)
                                    #print type(chosenConstruction)
                                    #print type(eWalls[goodEWall].construction)
                                    iWalls[goodIWall[0]].construction = chosenConstruction
                                    
                            #except:
                            #    print "\nwhoops... I don't understand\n"
 

                        print 'Top Menu'
                        print '|'
                        print '+--Working with Spaces'
                        print '  |'
                        print '  +--Advanced Interior Wall Management'
                        print 
                        print '      c:      change iwall selection'
                        print '      pw:     print walls'
                        print '      const:  change construction'
                        print '      wf:     write file'
                        print '      q:      exit out of awm'
                        i3 = raw_input('      >')
                        print '\n'                         
 

 

                # exterior wall management 
                if i2[:3] == 'awm':
                    
                    activeElements = returnActiveElements(spaces)

                    
                    i2Args = i2.split()
                    
                    i3 = 'c'


                    try:
                        xb = float(i2Args[1])
                    except:
                        xb = '-'

                    try:
                        yb = float(i2Args[2])
                    except:
                        yb = '-'

                    try:
                        aDoe = float(i2Args[3])
                    except:
                        aDoe = '-'

                    try:
                        lTol = float(i2Args[4])
                    except:
                        lTol = '-'

                    try:
                        aTol = float(i2Args[5])
                    except:
                        aTol = '-'


                    xMin = '-'
                    xMax = '-'
                    yMin = '-'
                    yMax = '-'
                    hMin = '-'
                    hMax = '-'
                    wMin = '-'
                    wMax = '-'
                    tMin = '90'
                    tMax = '90'
                    regex = '-'
                    wallType = 'e'
                    horiz = 'n'
                    plenum = 'n'
                    poly = 'n'
                    custAzimuth = 'n'

                    scale = 9

                    while i3 <> 'q':


                        if i3 == 'c':
                            print 'Changing inputs'
                    
                            
                            # get comparison coordinates
                            xMinTemp = raw_input('xMin [%s]' % xMin)
                            xMaxTemp = raw_input('xMax [%s]' % xMax)
                            yMinTemp = raw_input('yMin [%s]' % yMin)
                            yMaxTemp = raw_input('yMax [%s]' % yMax)
                            hMinTemp = raw_input('hMin [%s]' % hMin)
                            hMaxTemp = raw_input('hMax [%s]' % hMax)
                            wMinTemp = raw_input('wMin [%s]' % wMin)
                            wMaxTemp = raw_input('wMax [%s]' % wMax)
                            tMinTemp = raw_input('tMin [%s]' % tMin)
                            tMaxTemp = raw_input('tMax [%s]' % tMax)
                            regexTemp = raw_input('regex [%s]' % regex)
                            wallTypeTemp = raw_input('wallType [%s]' % wallType)
                            horizTemp = raw_input('horiz [%s]' % horiz)
                            plenumTemp = raw_input('plenum [%s]' % plenum)
                            polyTemp = raw_input('poly [%s]' % poly)
                            custAzimuthTemp = raw_input('Custom Azimuth [%s]' % custAzimuth)
                            print 'projected walls (for imput)'
                            xbTemp = raw_input('  x [%s]' % xb)
                            ybTemp = raw_input('  y [%s]' % yb)
                            aDoeTemp = raw_input('  a [%s] (doe)' % aDoe)
                            lTolTemp = raw_input('  line tolerance [%s]' % lTol)
                            aTolTemp = raw_input('  angle tolerance [%s]' % aTol)
                              
                            
                            xb = fixInput(xbTemp, xb)
                            yb = fixInput(ybTemp, yb)
                            aDoe = fixInput(aDoeTemp, aDoe)
                            lTol = fixInput(lTolTemp, lTol)
                            aTol = fixInput(aTolTemp, aTol)
                            xMin = fixInput(xMinTemp, xMin)
                            xMax = fixInput(xMaxTemp, xMax)
                            yMin = fixInput(yMinTemp, yMin)
                            yMax = fixInput(yMaxTemp, yMax)
                            hMin = fixInput(hMinTemp, hMin)
                            hMax = fixInput(hMaxTemp, hMax)
                            wMin = fixInput(wMinTemp, wMin)
                            wMax = fixInput(wMaxTemp, wMax)
                            tMin = fixInput(tMinTemp, tMin)
                            tMax = fixInput(tMaxTemp, tMax)
                            if regexTemp != '':
                                regex = regexTemp
                            if not aDoe == '-':
                                a = swapAngleType(aDoe)
                            if plenumTemp != '':
                                plenum = plenumTemp
                            if wallTypeTemp != '':
                                wallType = wallTypeTemp
                            if horizTemp != '':
                                horiz = horizTemp
                            if polyTemp != '':
                                poly = polyTemp
                            if custAzimuthTemp != '':
                                custAzimuth = custAzimuthTemp
        
        
                            # determine if wall falls in line with comparison coordinates
                            goodWalls = []
                            for space in activeElements:
                                if wallType == 'e':
                                    childWalls = spaces[space].returnEWalls(eWalls)
                                if wallType == 'u':
                                    childWalls = spaces[space].returnUWalls(uWalls)
                                
                                for childWall in childWalls:
                                    good = 1
                                    
                                    if spaces[space].zoneType == 'PLENUM' and plenum == 'n':
                                        print 'Skipping %s - Is plenum' % childWall
                                        good = 0
                                    elif wallType == 'e':
                                        if (eWalls[childWall].location == 'TOP' or eWalls[childWall].location == 'BOTTOM') and horiz == 'n':
                                            print 'Skipping %s - Is a floor or roof' % childWall
                                            good = 0
                                        elif eWalls[childWall].polygon != '' and poly == 'n':
                                            print 'Skipping %s - Is a polygon' % childWall
                                            good = 0
                                        elif eWalls[childWall].azimuth != '' and custAzimuth == 'n':
                                            print 'Skipping %s - Has custom azimuth' % childWall
                                            good = 0
                                    elif wallType == 'u':
                                        if (uWalls[childWall].location == 'TOP' or uWalls[childWall].location == 'BOTTOM') and horiz == 'n':
                                            print 'Skipping %s - Is a floor or roof' % childWall
                                            good = 0
                                        elif uWalls[childWall].polygon != '' and poly == 'n':
                                            print 'Skipping %s - Is a polygon' % childWall
                                            good = 0
                                        elif uWalls[childWall].azimuth != '' and custAzimuth == 'n':
                                            print 'Skipping %s - Has custom azimuth' % childWall
                                            good = 0

                                    if good:
                                                   
                                        #print 'Inspecting %s' % childWall
                                        #debug = 1
                                        
                                        if wallType == 'e':
                                            good = eWalls[childWall].testWall(x1=xb, y1=yb, aDoe=aDoe, lTol=lTol, aTol=aTol, xMin=xMin, xMax=xMax, yMin=yMin, yMax=yMax, hMin=hMin, hMax=hMax, wMin=wMin, wMax=wMax, tMin=tMin, tMax=tMax, regex=regex, verbose=1)                                
                                        if wallType == 'u':
                                            good = uWalls[childWall].testWall(x1=xb, y1=yb, aDoe=aDoe, lTol=lTol, aTol=aTol, xMin=xMin, xMax=xMax, yMin=yMin, yMax=yMax, hMin=hMin, hMax=hMax, wMin=wMin, wMax=wMax, tMin=tMin, tMax=tMax, regex=regex, verbose=1)                                
                                        
                                        if good:
                                            try:
                                                if wallType == 'e':
                                                    coords = eWalls[childWall].returnCoords()
                                                if wallType == 'u':
                                                    coords = uWalls[childWall].returnCoords()
                                            except:
                                                coords = [None , None , None , None]
                                            
                                            if wallType == 'e':
                                                goodWalls.append([childWall, eWalls[childWall].returnTotalZ(), eWalls[childWall].returnWidth(), eWalls[childWall].returnHeight(), [coords[0], coords[2]], [coords[1], coords[3]]])
                                            elif wallType == 'u':
                                                goodWalls.append([childWall, uWalls[childWall].returnTotalZ(), uWalls[childWall].returnWidth(), uWalls[childWall].returnHeight(), [coords[0], coords[2]], [coords[1], coords[3]]])
                                            #print goodWalls[-1]
                                            #time.sleep(.5)
                            
        
                            if not goodWalls:
                                print 'Did not find any matching walls'
                            else:
                                print 'Found %s matching walls\n\n' % len(goodWalls)


                        if i3 == 'dwin':
                            c = 0
                            for goodEWall in goodWalls:
                                goodEWallWindows = eWalls[goodEWall[0]].returnWindows(windows)
                                for goodEWallWindow in goodEWallWindows:
                                    c+=1
                                    del windows[goodEWallWindow]
                            print 'deleted %s windows for selected walls\n' % c


                        if i3 == 'dw':
                            for goodEWall in goodWalls:
                                del eWalls[goodEWall[0]]
                                
                            print 'deleted  selected walls\n'

                            
                        if i3 == 'const':
                            print 'Choose construction type:\n'
                            constructions = []
                            c = 0
                            for line in beginingSection:
                                #print line
                                if  '" = CONSTRUCTION' in line:
                                    c += 1
                                    construction = re.findall('".*"', line)[0]
                                    constructions.append(construction)
                                    print c, construction
                            i4 = raw_input(' > ')
                            if 1==1:
                            #try:
                                n = int(i4)
                                print n
                                chosenConstruction = constructions[n-1]
                                print chosenConstruction
                                for goodEWall in goodWalls:
                                    print goodEWall
                                    #print type(goodEWall)
                                    #print type(chosenConstruction)
                                    #print type(eWalls[goodEWall].construction)
                                    eWalls[goodEWall[0]].construction = chosenConstruction
                            #except:
                            #    print "\nwhoops... I don't understand\n"


                        if i3 == 'pw':

                            if not goodWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                print 'Found %s matching walls\n' % len(goodWalls)
                            for goodEWall in goodWalls:
                                print goodEWall[0]
                                print '   x: %s' % goodEWall[1]
                                print '   z: %s' % goodEWall[2]
                                print '   w: %s' % goodEWall[3]
                                print '   h: %s' % goodEWall[4]

                        if i3 == 'ctu':
                            if wallType != 'e':
                                print 'this operation can be applied only to ewalls'
                            else:
                                for goodWall in goodWalls:
                                    name = goodWall[0]
                                    spaceName = eWalls[name].space
                                    
                                    #wallSplit = name.split('-')
                                    #print spaces.keys()
                                    newWallName = spaces[spaceName].findNextUWall(uWalls)

                                    print 'moving ewall %s to uwall %s' % (name, newWallName)
                                    
                                    uWalls[newWallName]=UWall(name=newWallName, floor=eWalls[name].floor, space=eWalls[name].space)
                                    
                                    location = eWalls[name].location

                                    uWalls[newWallName].location  = location
                                    uWalls[newWallName].shape  = eWalls[name].shape
                                    uWalls[newWallName].polygon  = eWalls[name].polygon
                                    uWalls[newWallName].x  = eWalls[name].x
                                    uWalls[newWallName].y  = eWalls[name].y
                                    uWalls[newWallName].z  = eWalls[name].z
                                    uWalls[newWallName].tilt  = eWalls[name].tilt
                                    uWalls[newWallName].width  = eWalls[name].width
                                    uWalls[newWallName].height  = eWalls[name].height
                                    uWalls[newWallName].azimuth  = eWalls[name].azimuth
                                    if location == 'BOTTOM':
                                        uWalls[newWallName].construction = '"SUBGRADE SLAB CONSTRUCTION"'
                                    if location == 'TOP':
                                        uWalls[newWallName].construction = '"UNDERGROUND ROOF CONSTRUCTION"'
                                    else:
                                        uWalls[newWallName].construction = '"UNDERGROUND WALL CONSTRUCTION"'

                                    del eWalls[name]
                                    
    
                        if i3 == 'cte':
                            if wallType != 'u':
                                print 'this operation can be applied only to uwalls'
                            else:
                                for goodWall in goodWalls:
                                    name = goodWall[0]
                                    wallSplit = name.split('-')
                                    spaceName = uWalls[name].space
                                    newWallName = spaces[spaceName].findNextEWall(eWalls)
                                    print 'moving uwall %s to ewall %s' % (name, newWallName)
                                    eWalls[newWallName]=EWall(name=newWallName, floor=uWalls[name].floor, space=uWalls[name].space)
                                    
                                    location = uWalls[name].location
    
                                    eWalls[newWallName].location  = location
                                    eWalls[newWallName].shape  = uWalls[name].shape
                                    eWalls[newWallName].polygon  = uWalls[name].polygon
                                    eWalls[newWallName].x  = uWalls[name].x
                                    eWalls[newWallName].y  = uWalls[name].y
                                    eWalls[newWallName].z  = uWalls[name].z
                                    eWalls[newWallName].tilt  = uWalls[name].tilt
                                    eWalls[newWallName].width  = uWalls[name].width
                                    eWalls[newWallName].height  = uWalls[name].height
                                    eWalls[newWallName].azimuth  = uWalls[name].azimuth
                                    if location == 'BOTTOM':
                                        eWalls[newWallName].construction = '"EXTERIOR FLOOR CONSTRUCTION"'
                                    elif location == 'TOP':
                                        eWalls[newWallName].construction = '"EXTERIOR ROOF CONSTRUCTION"'
                                    else:
                                        eWalls[newWallName].construction = '"EXTERIOR WALL CONSTRUCTION"'

                                    del uWalls[name]
                                
                        

                        if i3 =='wf':
                            print 'writing file'
                            writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
                            j = 0
                            countOnly = 1

                       
                        if i3 == 'sbh':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                newGoodWalls = []
                                for goodEWall in goodWalls:
                                    eWallName = goodEWall[0]
                                    print 'Inspecting %s' % eWallName
                                    eWallWidth = eWalls[eWallName].returnWidth()
                                    eWallWindows = eWalls[eWallName].returnWindows(windows)
                                    if not eWallWindows:
                                        print 'No Windows on %s' % eWallName
                                    else:
                                        winMin = float(windows[eWallWindows[0]].x)
                                        winMax = float(windows[eWallWindows[0]].x) + float(windows[eWallWindows[0]].width)
                                        for eWallWindow in eWallWindows[1:]:
                                            winMin = min(winMin, float(windows[eWallWindow].x))
                                            winMax = max(winMax, float(windows[eWallWindow].x) + float(windows[eWallWindow].width))
                                        if winMin < 0 or winMax > eWallWidth:
                                            newGoodWalls.append(goodEWall)
                                            print '  %s has bad windows' % eWallName
                                            print '  winMin    : %s' % winMin
                                            print '  winMax    : %s' % winMax
                                            print '  eWallWidth: %s' % eWallWidth

                                print 'Found %s walls' % len(newGoodWalls)
                                if len(newGoodWalls):
                                    goodWalls = newGoodWalls
                                else:
                                    print 'Keeping original %s selected walls' % len(goodWalls)

                                
                        if i3 == 'sbv':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                newGoodWalls = []
                                for goodEWall in goodWalls:
                                    eWallName = goodEWall[0]
                                    print 'Inspecting %s' % eWallName
                                    eWallHeight = eWalls[eWallName].returnHeight()
                                    eWallWindows = eWalls[eWallName].returnWindows(windows)
                                    if not eWallWindows:
                                        print 'No Windows on %s' % eWallName
                                    else:
                                        winMin = float(windows[eWallWindows[0]].y)
                                        winMax = float(windows[eWallWindows[0]].y) + float(windows[eWallWindows[0]].height)
                                        for eWallWindow in eWallWindows[1:]:
                                            winMin = min(winMin, float(windows[eWallWindow].y))
                                            winMax = max(winMax, float(windows[eWallWindow].y) + float(windows[eWallWindow].height))
                                        if winMin < 0 or winMax > eWallHeight:
                                            newGoodWalls.append(goodEWall)
                                            print '  %s has bad windows' % eWallName
                                            print '  winMin     : %s' % winMin
                                            print '  winMax     : %s' % winMax
                                            print '  eWallHeight : %s' % eWallHeight

                                print 'Found %s walls' % len(newGoodWalls)
                                if len(newGoodWalls):
                                    goodWalls = newGoodWalls
                                else:
                                    print 'Keeping original %s selected walls' % len(goodWalls)


                        if i3 == 'pwin':
                            c = 0
                            totalArea = 0

                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                print 'Found %s matching walls\n' % len(goodWalls)
                            for goodEWall in goodWalls:
                                print goodEWall[0]
                                eWallWindows = eWalls[goodEWall[0]].returnWindows(windows)
                                if not eWallWindows:
                                    print '   No windows on wall'
                                else:
                                    for window in eWallWindows:
                                        print '   %s' % windows[window].name
                                        print '      x: %s' % windows[window].x
                                        print '      y: %s' % windows[window].y
                                        print '      w: %s' % windows[window].width
                                        print '      h: %s' % windows[window].height
                                        c +=1
                                        totalArea += float(windows[window].width)*float(windows[window].height)
                            print
                            print 'count: %s' % c
                            print 'area : %s' % totalArea

                                                                            
                        if i3 == 'cbn':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                ww = float(raw_input('width   '))
                                wh = float(raw_input('height  '))
                                y = float(raw_input('y       '))
                                n = int(raw_input('number  '))
                                for goodEWall in goodWalls:
                                    eWallName = goodEWall[0]
                                    eWallWindows = eWalls[eWallName].returnWindows(windows)
                                    if eWallWindows:
                                        print 'ERROR: skipping %s due to existing windows'
                                        time.sleep(.5)
                                    else:
                                        ew = eWalls[eWallName].returnWidth()
                                        if (ww * float(n)) > ew:
                                            print 'ERROR: %s windows will not fit on %s' % (n, eWallName)
                                            time.sleep(.5)
                                        else:
                                            s = (ew - (ww*float(n)))/float(n)
                                            xb = s/2.
                                            for c in range(n):
                                                x = xb + float(c)*(ww + s)
                                                windowName = eWallName[:-1] + '-W%s"' % (c + 1)
                                                print 'Creating window %s' % windowName
                                                #print xb, x, c, ww, s, ew
                                                space = eWalls[eWallName].space
                                                floor = spaces[space].floor
                                                windows[windowName]=Window(name=windowName, attributes=attributes, floor=floor, space=space, wall=eWallName)
                                                windows[windowName].x = round(x,2)
                                                windows[windowName].y = round(y,2)
                                                windows[windowName].width = round(ww,2)
                                                windows[windowName].height = round(wh,2)

                                        
                        if i3 == 'crh':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                for goodEWall in goodWalls:
                                    eWallName = goodEWall[0]
                                    eWallWidth = eWalls[eWallName].returnWidth()
                                    eWallWindows = eWalls[eWallName].returnWindows(windows)
                                    if not eWallWindows:
                                        print 'No Windows on %s' % eWallName
                                    else:
                                        winMin = float(windows[eWallWindows[0]].x)
                                        winMax = float(windows[eWallWindows[0]].x) + float(windows[eWallWindows[0]].width)
                                        for eWallWindow in eWallWindows[1:]:
                                            winMin = min(winMin, float(windows[eWallWindow].x))
                                            winMax = max(winMax, float(windows[eWallWindow].x) + float(windows[eWallWindow].width))
                                        winCenter = (winMin + winMax) / 2.
                                        eWallCenter = (eWallWidth) / 2.
                                        shift = round(eWallCenter - winCenter,2)
                                        for eWallWindow in eWallWindows:
                                            windows[eWallWindow].x = round(float(windows[eWallWindow].x) + shift,2)
                                            print 'Moved %s by %s' % (eWallName, shift)

                                    
                        if i3 == 'isvg':     #import windows from svg file
                            if aDoe == '-':
                                print 'no angle defined, cannot get projection for import'
                            elif not goodWalls:
                                print 'no good ewalls'
                            else:
                                # get minimum ewall
                                minEWall = None
                                for goodEWall in goodWalls:
                                    if minEWall == None:
                                        minEWall = goodEWall
                                    else:
                                        if a <= 45 or a >= 315:
                                            if goodEWall[4][0] < minEWall[4][0]:
                                                minEWall = goodEWall
                    
                                        elif a <= 135:
                                            if goodEWall[4][1] < minEWall[4][1]:
                                                minEWall = goodEWall
                                        
                                        elif a <= 225:
                                            if goodEWall[4][0] > minEWall[4][0]:
                                                minEWall = goodEWall
                                        else:
                                            if goodEWall[4][1] > minEWall[4][1]:
                                                minEWall = goodEWall
                                
                                print '\n\n'
                                
            
                            
                                # prompt for origin
                                print 'Which is the origin?'
                                print '1) min : %s, %s (default)' % (round(minEWall[4][0],2), round(minEWall[4][1],2))
                                print '2) base: %s, %s' % (round(xb,2), round(yb,2))
                                print '3) manual input'
                                
                                originSelection = raw_input()
                                if originSelection == '2':
                                    o = xb, yb
                                elif originSelection == '3':
                                    originGood = 0
                                    while not originGood:
                                        print 'Enter your own origin "x,y":'
                                        originInput = raw_input()
                                        r = re.compile('[, ]')
                                        o = r.split(originInput)
                                        d = dist(xb, yb, a, o[0], o[1])
                                        print '   %s, %s is %s from %s, %s %s\n' % (o[0], o[1], d, xb, yb, a)
                                        if  d < lineTolerance:
                                            originGood
                                        else:
                                            print '   try again...\n'
                                else:
                                    o = minEWall[4]


                                # prompt for glass type
                                #print 'Glass Type?'
                                #print '  [Default]'
                                #print '  >'
                                
                                #glassType = raw_input()                                
                                
                                #get projected distance from origin to each wall
                                goodWallsProjected = []
                                print 'o:', o
                                for goodEWall in goodWalls:
                                    
                                    x = findProjectedDistance(a, o[0], o[1], goodEWall[4][0], goodEWall[4][1])
                                    aCartBase = swapAngleType(aDoe)
                                    aCartWall = getAngleCart([o[0],o[1]],[goodEWall[4][0], goodEWall[4][1]])
                                    aDiff = abs(reduceAngle(aCartBase)-reduceAngle(aCartWall))
                                    debug(goodEWall)
                                    debug('  aDoe  Base:   %s' % aDoe)
                                    debug('  aCart Base:   %s' % aCartBase)
                                    debug('  aCart Wall:   %s' % aCartWall)
                                    debug('  a Difference: %s' % aDiff)
                                    if aDiff < 90:
                                        debug('  x Projected:  %s' % x)
                                    else:
                                        x = -x
                                        debug('  x Projected:  %s  (corrected for opposite direction)' % x)
                                    
                                    goodWallsProjected.append([goodEWall[0], x, goodEWall[1], goodEWall[2], goodEWall[3], goodEWall[4], goodEWall[5]])
                                

                                debug( '\n\n')
                                
                                svgFiles = []
                                for file in os.listdir('.'):
                                    if file.find('.svg') > -1:
                                        svgFiles.append(file)
                                
                                if not svgFiles:
                                    print 'no svg files'
                                else:
                                    c = 0
                                    
                                    for svgFile in svgFiles:
                                        c += 1
                                        print c, svgFile
                                    print 
                                    print 'which svg file'
                                    i2 = raw_input('')
                                    
                                    abort = 0
                                    try:
                                        chosenSvg = svgFiles[int(i2)-1]
                                    except:
                                        print "oops, I don't understand"
                                        abort = 1
                                    
                                    #print 
                                    #print 'frame reduction % [0]'
                                    #reduction = 0
                                    #i2 = raw_input('')
                                    #if i2:
                                    #    try:
                                    #        reduction = float(i2)
                                    #    except:
                                    #        print "oops, I don't understand"
                                    #        abort = 1

                                    if not abort:
    
                                        print 'importing svg file %s' % chosenSvg

                                        
                                        windowsfromSvg,colors = getSvgRectangles(chosenSvg)


                                        
                                        #######################################
                                        # Apply glass types to colors

                                        colorMap = {}
                                        markMap = {}
                                        glassTypeString = ''
                                        cgt = 1
                                        modelGlassTypes = []
                                        gtChoices = []

                                        # grab glass types ("modelGlassTypes") from input file
                                        for line in beginingSection:
                                            if line.find('GLASS-TYPE') > -1:
                                                gt = line.split('=')[0]
                                                glassTypeString += '%s - %s\n' % (cgt,gt)
                                                modelGlassTypes.append(gt)
                                                cgt+=1
                                        
                                        # distill color set to unique values
                                        colorsInSvg = list(set(colors))
                                        
                                        useWindowFile = 'n'
                                        if os.path.exists('windows.dat'):
                                            useWindowFile = raw_input('use window dat file? [y]')
                                        if useWindowFile.lower() != 'n':
                                            f = open('windows.dat')
                                            lines = f.readlines()
                                            f.close()
                                            for line in lines:
                                                cols = line.split('|')
                                                colorMap[cols[0].lower()] = cols[1].replace('\n', '')
                                                if not cols[1] in gt:
                                                    print 'Warning, glass type %s in windows.dat not in input file' % cols[1]
                                                if len(cols) > 2:
                                                    markMap[cols[0].lower()] = "_" + cols[2].replace('\n', '')

                                        
                                        else:
                                           # Associate names to colors and assign glass type to color
                                            for colorInSvg in colorsInSvg:
                                                colorInSvgName = '[None]'
                                                
                                                R = int(colorInSvg[:2],16)/(255.)
                                                G = int(colorInSvg[2:4],16)/(255.)
                                                B = int(colorInSvg[4:],16)/(255.)
                                                
                                                r,g,b = 0,0,0
                                                if R > .4:r=1
                                                if G > .4:g=1
                                                if B > .4:b=1
                                                
                                                rgb = [r,g,b]
                                                
                                                colorNames = [
                                                   [[0,0,0],'black'],
                                                   [[1,1,1],'white'],
                                                   [[1,0,0],'red'],
                                                   [[0,1,0],'green'],
                                                   [[0,0,1],'blue'],
                                                   [[1,1,0],'yellow'],
                                                   [[1,0,1],'magenta'],
                                                   [[0,1,1],'cyan'],
                                                   [[1,0,0],'red'],
                                                   ]
                                                
                                                    
                                            
                                                # grab color name for this color in svg file
                                                for colorName in colorNames:
                                                    if colorName[0] == rgb: colorInSvgName = colorName[1]
                                                
                                                # print glass type choices
                                                print '\nwhich glass type is the %s (%s) glass [1-%s]\n%s' % (colorInSvgName, colorInSvg, cgt-1, glassTypeString)
                                            
                                                # allow user to select a choice
                                                gtChoice = raw_input()
                                                
    
                                                # if blank, assign empty string to color dictionary
                                                if not gtChoice:
                                                    colorMap[colorInSvg] = ''
                                                # else assign color based on lookup of model glass types'
                                                else:
                                                    try:
                                                        colorMap[colorInSvg] = modelGlassTypes[int(gtChoice)-1]
                                                    except:
                                                        print '\nerror assigning glasss type %s to %s\n   Using default' % (gtChoice, colorInSvg)
                                                        time.sleep(2)
    
                                                # ask for identifying marking
                                                print '\ndo you want to assign any identifying marking to %s (%s)windows [blank if no]\n' % (colorInSvgName, colorInSvg)
                                            
                                                # allow user to select a choice
                                                marking = raw_input()
                                                
                                                if marking:
                                                    marking = '_%s' % marking
    
                                                markMap[colorInSvg] = marking

                                            
                                                
                                        # print properly assigned glass type choices
                                        print '\nsuccessfully applied the following glass tpyes'
                                        for colorInSvg in colorMap:
                                            print '%s: %s' % (colorInSvg, colorMap[colorInSvg])
                                        
                                        if markMap:
                                            print '\nsuccessfully applied the following marking map'
                                            for colorInSvg in colorMap:
                                                print '%s: %s' % (colorInSvg, markMap[colorInSvg])
                                        
                                        time.sleep(1)
                                        
                                        print 'making windows...'


    
                                        homed = 0
                                        homeless = 0
                                        svgNumber = 1 
                                        for windowfromSvg in windowsfromSvg:
                                            
                                            
                                            foundHome = 0 
                                            wname = windowfromSvg[0]
                                            wx1 = windowfromSvg[1]
                                            wy1 = windowfromSvg[2]
                                            wx2 = windowfromSvg[3]
                                            wy2 = windowfromSvg[4]
                                            ww = windowfromSvg[5]
                                            wh = windowfromSvg[6]
                                            wxc = windowfromSvg[7]
                                            wyc = windowfromSvg[8]
                                            id = windowfromSvg[10]
                                            wa = ww*wh
                                            usedArea = 0
                                            numWindows = 0

                                            wColor = windowfromSvg[9]
                                            
                                            attributes = ''
                                            try:
                                                wGlassType = colorMap[wColor]
                                                if wGlassType:
                                                    attributes = [['GLASS-TYPE', '%s' % wGlassType]]
                                            except:
                                                pass

                                            wMarking = markMap[wColor]
                                                
        

                                            debug('\n###################################################\n')
                                            debug('SVG Window Name, id: %s,%s' % (wname,id))
                                            debug('  wx1/wy1: (%s,%s)' % (round(wx1,2), round(wy1,2)))
                                            debug('  wx2/wy2: (%s,%s)' % (round(wx2,2), round(wy2,2)))
                                            debug('  ww/wwh: (%s,%s)' % (round(ww,2), round(wh,2)))
                                            

                                            
                                            frameNumber = 1
                                            for goodEWallProjected in goodWallsProjected:
                                                
                                            
    
                                                ename =goodEWallProjected[0]
                                                ex1 =goodEWallProjected[1]
                                                ey1 =goodEWallProjected[2]
                                                ew =goodEWallProjected[3]
                                                eh =goodEWallProjected[4]
                                                ex2 = ex1 + ew
                                                ey2 = ey1 + eh
                                                
                                                debug('  ~~~~~~~~~~~~~~~~~~~~~~~')
                                                debug('  Testing wall %s' % ename)
                                                debug('    ex1, ey1: (%s,%s)' % (ex1,ey1))
                                                debug('    ex2, ey2: (%s,%s)' % (ex2,ey2))
                                                debug('    ew, eh: (%s,%s)' % (ew,eh))
                                                
                                                
                                               
                                                try:
    
                                                    if (wx1 < ex2) and (wx2 > ex1) and (wy1 < ey2) and (wy2 > ey1):
                                                        minH = 0.5
                                                        minW = 0.5
                                                        x = max(0, wx1-ex1)
                                                        y = max(0, wy1-ey1)
                                                        w = min(wx2,ex2)-max(ex1,wx1)  
                                                        h = min(wy2,ey2)-max(ey1,wy1)
                                                        if h > minH and w > minW:
                                                            space = eWalls[ename].space
                                                            floor = spaces[space].floor
                                                            #windowNumber += 1
                                                            windowName = ename[:-1] + '-W_%s_%s%s"' % (svgNumber, frameNumber, wMarking)
                                                            frameNumber += 1
            
                                                            
                                                            windows[windowName]=Window(name=windowName, attributes=attributes, floor=floor, space=space, wall=ename)
                                                            windows[windowName].x = x
                                                            windows[windowName].y = y
                                                            windows[windowName].width = w
                                                            windows[windowName].height = h
    
                                                            usedArea += w * h
                                                            numWindows += 1
                                                            debug('  ###################')

                                                            debug('  New Windows Created: %s' % windowName)
                                                            debug('    x/y: (%s,%s)' % (round(x,2), round(y,2)))
                                                            debug('    w/h: (%s,%s)' % (round(w,2), round(h,2)))
                                                            debug('    area: (%s)' % (round(w*h,2)))
                                                            
                                                        
                                                except:
                                                    debug('  Problem comparing Wall/Window data')
                                                    debug('    x/y: (%s,%s)' % (round(x,2), round(y,2)))
                                                    debug('    w/h: (%s,%s)' % (round(w,2), round(h,2)))
                                                    debug('    area: (%s)' % (round(w*h,2)))

                                            debug('\n   Total used area: (%s%%)' % round(usedArea/wa))

                                            svgNumber += 1
                                            #windowsHeaderText += '   area: (%s/%s)\n' % (round(usedArea,2), round(wa,2))
                                             
                                            #debug(windowsHeaderText)
                                            #debug(windowsEachText)

                        
                        if i3 == 'nudge':  # move windows so they fit walls better
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                tol = raw_input('tolerance [2]   ')
                                try:
                                    tol = float(tol)
                                except:
                                    tol = 2
                                
                                problemWindows = [] 
                                nudgedWindows = [] 
                                for goodEWall in goodWalls:
                                    goodEWallName = goodEWall[0]
                                    print '\ninspecting %s' % goodEWallName
                                    w = eWalls[goodEWallName].returnWidth()
                                    h = eWalls[goodEWallName].returnHeight()
                                    eWallWindows = eWalls[goodEWallName].returnWindows(windows)
                                    print '   ewall width     %s ' % w
                                    print '   ewall height   %s ' % h
 
                                    if not eWallWindows:
                                        print '   no windows'
                                    for eWallWindow in eWallWindows:
                                        print '\n   inspecting %s' % eWallWindow
                                        ww = windows[eWallWindow].width
                                        wh = windows[eWallWindow].height
                                        wx = windows[eWallWindow].x
                                        wy = windows[eWallWindow].y
                                        p = ''
                                        
                                        if not w:
                                            print '   skipping nudge x due to default wall width'
                                        else:

                                            if not wx or not ww:
                                                print '\n      skipping nudge x due to default value in windows width or x'
                                            else:
                                                print '      window x       %s ' % wx
                                                print '      window width   %s ' % ww
                                                wx = float(wx)
                                                ww = float(ww)
                                                if ww > w:
                                                    p = '         window width greater than wall width'
                                                    print p 
                                                    problemWindows.append([eWallWindow, p.strip()])
                                                elif wx < 0:
                                                    if wx > -(tol):
                                                        print '         nudging x to the right'
                                                        windows[eWallWindow].x = .1
                                                        nudgedWindows.append(eWallWindow)
                                                    else:
                                                        p = '         out of tolerance'
                                                        print p 
                                                        problemWindows.append([eWallWindow, p.strip()])
                                                        
                                                elif ((wx + ww) > w):
                                                    if ((wx + ww - tol) < w):
                                                        print '         nudging x to the left'
                                                        windows[eWallWindow].x = w - ww-.1
                                                        nudgedWindows.append(eWallWindow)
                                                    else:
                                                        p = '         out of tolerance'
                                                        print p 
                                                        problemWindows.append([eWallWindow, p.strip()])
                                                else:
                                                    print '         no nudge of x necessary'


                                        if not wh or not wy:
                                            print '\n      skipping due to default value in window height or y'
                                        else:
                                            print '      window y       %s ' % wy
                                            print '      window height  %s ' % wh
                                            wy = float(wy)
                                            wh = float(wh)
                                            if wh > h:
                                                p = '         window height greater than wall height'
                                                print p 
                                                problemWindows.append([eWallWindow, p.strip()])

                                            elif wy < 0:
                                                if wy > -(tol):
                                                    print '         nudging y up'
                                                    windows[eWallWindow].y = .1
                                                    nudgedWindows.append(eWallWindow)
                                                else:
                                                    p = '         out of tolerance'
                                                    print p 
                                                    problemWindows.append([eWallWindow, p.strip()])

                                            elif ((wy + wh) > h):
                                                if ((wy + wh - tol) < h):
                                                    print '         nudging y down'
                                                    windows[eWallWindow].y = h - wh -.1
                                                    nudgedWindows.append(eWallWindow)
                                                else:
                                                    p = '         out of tolerance'
                                                    print p 
                                                    problemWindows.append([eWallWindow, p.strip()])
                                            else:
                                                print '         no nudge of y necessary'


                                print '\nNudeged Windows:'
                                for nudgedWindow in nudgedWindows:
                                    print '   ' + nudgedWindow

                                print '\nProblem Windows:'
                                for problemWindow in problemWindows:
                                    print '   ' + problemWindow[0], problemWindow[1]


                        if i3 == 'ipdf':  #inport windows from pdf
                            if aDoe == '-':
                                print 'no angle defined, cannot get projection for import'
                            elif not goodWalls:
                                print 'no good ewalls'
                            else:
                                # get minimum ewall
                                minEWall = None
                                for goodEWall in goodWalls:
                                    if minEWall == None:
                                        minEWall = goodEWall
                                    else:
                                        if a <= 45 or a >= 315:
                                            if goodEWall[4][0] < minEWall[4][0]:
                                                minEWall = goodEWall
                    
                                        elif a <= 135:
                                            if goodEWall[4][1] < minEWall[4][1]:
                                                minEWall = goodEWall
                                        
                                        elif a <= 225:
                                            if goodEWall[4][0] > minEWall[4][0]:
                                                minEWall = goodEWall
                                        else:
                                            if goodEWall[4][1] > minEWall[4][1]:
                                                minEWall = goodEWall
                                
                                print '\n\n'
                                
            
                            
                                # prompt for origin
                                print 'Which is the origin?'
                                print '1) min : %s, %s (default)' % (round(minEWall[4][0],2), round(minEWall[4][1],2))
                                print '2) base: %s, %s' % (round(xb,2), round(yb,2))
                                print '3) manual input'
                                
                                originSelection = raw_input()
                                if originSelection == '2':
                                    o = xb, yb
                                elif originSelection == '3':
                                    originGood = 0
                                    while not originGood:
                                        print 'Enter your own origin "x,y":'
                                        originInput = raw_input()
                                        r = re.compile('[, ]')
                                        o = r.split(originInput)
                                        d = dist(xb, yb, a, o[0], o[1])
                                        print '   %s, %s is %s from %s, %s %s\n' % (o[0], o[1], d, xb, yb, a)
                                        if  d < lineTolerance:
                                            originGood
                                        else:
                                            print '   try again...\n'
                                else:
                                    o = minEWall[4]
                                
                                #get projected distance from origin to each wall
                                goodWallsProjected = []
                                for goodEWall in goodWalls:
                                    x = findProjectedDistance(a, o[0], o[1], goodEWall[4][0], goodEWall[4][1])
                                    #x = ((o[0]-goodEWall[4][0])**2 + (o[1]-goodEWall[4][1])**2)**.5
                                    #print x
                                    goodWallsProjected.append([goodEWall[0], x, goodEWall[1], goodEWall[2], goodEWall[3], goodEWall[4], goodEWall[5]])
                                

                            for goodEWallProjected in goodWallsProjected:
                                print goodEWallProjected
                        
                            scaleTemp = raw_input('scale [%s]' % scale)
                            abort = 0
                            if scaleTemp <> '':
                                scale = float(scaleTemp)
                                
                            fdfFiles = []
                            for file in os.listdir('.'):
                                if file.find('.fdf') > -1:
                                    fdfFiles.append(file)
                            
                            if not fdfFiles:
                                print 'no fdf files'
                            else:
                                c = 0
                                for fdfFile in fdfFiles:
                                    c += 1
                                    print c, fdfFile
                                print 
                                print 'which fdf file'
                                i2 = raw_input('')
                                
                                try:
                                    chosenFdf = fdfFiles[int(i2)-1]
                                except:
                                    print "oops, I don't understand"
                                    abort = 1
                                if not abort:

                                    print 'importing fdf file %s' % chosenFdf

                                    f = open(chosenFdf, 'r')
                                    file = f.read()
                                    lines = file.split("endobj")
                                    
                                    foundOrigin = 0
                                    for line in lines:
                                        if re.search('Subj\(origin\)', line):
                                            rotate = re.findall('Rotate \d{1,3}', line)[0]
                                            print rotate
                                            if rotate == 'Rotate 270':
                                                print line
                                                rect = re.findall('Rect\[[\d\. ]*\]',line)[0]
                                                points = rect[5:-1].split()
                                                o = float(points[3]), float(points[0])
                                                foundOrigin = 1
                                    if not foundOrigin:
                                        print 'ooops, could not locate origin (use "origin" as subject)'
                                    else:
                                        print 'origin (%s, %s)' % o
                                        windowsfromFdf = []
                                        for line in lines:
                                            if not re.search('Subj\(origin\)', line) and re.search('Rect\[[\d\. ]*\]', line):
                                                nameList = re.findall('Subj\(\w*\)', line)
                                                if not nameList:
                                                    name = '[no name]'
                                                else:
                                                    name = nameList[0][5:-1]
                                                    
                                                print
                                                if line.find('origin') > -1:
                                                    print 'origin'
                                                rotate = re.findall('Rotate \d{1,3}', line)[0]
                                                rect = re.findall('Rect\[[\d\. ]*\]',line)[0]
                                                points = rect[5:-1].split()
                                                print points
                                                tc = returnTrueCoords(o, points, rotate)
                                                print tc
                                                x1 = tc[0][0]
                                                y1 = tc[0][1]
                                                x2 = tc[1][0]
                                                y2 = tc[1][1]
                                                w = x2 - x1
                                                h = y2 - y1
                                                xc = (w/2) + x1
                                                yc = (h/2) + y1
                                                print '  x1 : %s' % round(x1,2)
                                                print '  y1 : %s' % round(y1,2)
                                                print '  x2 : %s' % round(x2,2)
                                                print '  y2 : %s' % round(y2,2)
                                                print '  w : %s' % round(w,2)
                                                print '  h : %s' % round(h,2)
                                                print '  cx: %s' % round(xc,2)
                                                print '  cy: %s' % round(yc,2)                                        
                                                windowsfromFdf.append([name, x1, y1, x2, y2, w, h, xc, yc])
    
                                        homed = 0
                                        homeless = 0
                                        
                                        for windowFromFdf in windowsfromFdf:
                                            foundHome = 0 
                                            wname = windowFromFdf[0]
                                            wx1 = windowFromFdf[1]
                                            wy1 = windowFromFdf[2]
                                            wx2 = windowFromFdf[3]
                                            wy2 = windowFromFdf[4]
                                            ww = windowFromFdf[5]
                                            wh = windowFromFdf[6]
                                            wxc = windowFromFdf[7]
                                            wyc = windowFromFdf[8]
                                            
                                            for goodEWallProjected in goodWallsProjected:
    
                                                ename =goodEWallProjected[0]
                                                ex =goodEWallProjected[1]
                                                ey =goodEWallProjected[2]
                                                ew =goodEWallProjected[3]
                                                eh =goodEWallProjected[4]
    
                                                if (wxc >= ex) and (wxc <= (ex + ew)) and (wyc >= ey) and (wyc <= (ey + eh)):
                                                    foundHome = 1
                                                    print '\nfound home for %s \n   x1/y1: (%s,%s)\n   xc/yc: (%s,%s)\n   w/h:  (%s by %s)\n   ewall: %s' % (wname, round(wx1,2),round(wy1,2), round(wxc,2),round(wyc,2),round(ww,2),round(wh,2), ename)
                                                    x = wx1-ex
                                                    y = wy1-ey
                                                    w = ww
                                                    h = wh
    
                                                    space = eWalls[ename].space
                                                    floor = spaces[space].floor
                                                    windowNumber += 1
                                                    windowName = ename[:-1] + '-W%s"' % windowNumber
                                                    attributes = ''
    
                                                    #print windowName
                                                    
                                                    #print attributes
                                                    #print floor
                                                    #print space
                                                    #print ename
    
                                                    #windows[window]=Window(window, attributes, spaces[space].floor, spaces[space].name, eWalls[childEWall].name)
                                                    
                                                    #windows['test']=Window('test', '', 'floor1', 'space1', 'wall1')
    
                                                    windows[windowName]=Window(name=windowName, attributes=attributes, floor=floor, space=space, wall=verticesename)
                                                    windows[windowName].x = x
                                                    windows[windowName].y = y
                                                    windows[windowName].width = w
                                                    windows[windowName].height = h
    
                                            if foundHome:
                                                homed += 1
                                            else:
                                                print wx1, wy1, wxc, wyc, ww, wh
                                                print '\ncould not find home for %s \n   x1/y1: (%s,%s)\n   xc/yc: (%s,%s)\n   w/h:  (%s by %s)' % (wname, round(wx1,2),round(wy1,2), round(wxc,2),round(wyc,2),round(ww,2),round(wh,2))
    
                                                homeless +=1
                                        print 'homed:    %s' % homed
                                        print 'homeless: %s' % homeless

                        
                        if i3 == 'split':

                            if not goodWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                
              
                                minX = eWalls[goodWalls[0][0]].returnTotalZ()
                                maxX = minX + eWalls[goodWalls[0][0]].returnHeight()
                                print 'initiallizing minX to %s' % minX
                                print 'initiallizing maxX to %s' % maxX

                                for goodEWall in goodWalls[1:]:
                                    eWallName = goodEWall[0]
                                    wallBottom = eWalls[eWallName].returnTotalZ()
                                    wallTop = eWalls[eWallName].returnHeight() + wallBottom
                                    print '\nInspecting wall %s' % eWallName
                                    print '   minX %s' % (minX)
                                    print '   maxX %s' % (maxX)
                                    print '   wall top %s' % (wallTop)
                                    print '   wall bottom %s' % (wallBottom)
                                    
                                    print 
                                    if wallBottom < minX:
                                        minX = wallBottom
                                        print '      resetting bottom to %s' % wallBottom
                                    if wallTop > maxX:
                                        maxX = wallTop
                                        print '      resetting top to %s' % wallTop
                                
                                print '\n'  
                                print minX
                                print maxX
                                print '\nwhere to split [0]'
                                
                                grade = raw_input()
                                
                                try:
                                    grade = float(grade)
                                except:
                                    grade = 0
                                    
                                for goodEWall in goodWalls:
                                    eWallName = goodEWall[0]
                                    print '\nInpecting %s' % eWallName
                                    eWallHeight = eWalls[eWallName].returnHeight()
                                    eWallBottom = eWalls[eWallName].returnTotalZ()
                                    eWallTop = eWallBottom + eWallHeight
                                    
                                    
                                    if eWallBottom >= grade:
                                        print '   above grade'
                                    elif eWallTop <= grade:
                                        print '   below grade, converting to Underground wall'
                                    else:
                                        print '\n   partial exposure.  splitting wall'
                                        space = eWalls[eWallName].space
                                        floor = eWalls[eWallName].floor
                                        location = eWalls[eWallName].location
                                        
                                        # new ewall
                                        newEWallHeight = eWallTop - grade
                                        newEWallZ = grade - eWallBottom
                                        eWalls[eWallName].z = newEWallZ
                                        eWalls[eWallName].height = newEWallHeight

                                        print '\n      modified %s'%  eWallName
                                        print '         z %s' % newEWallZ
                                        print '         height %s' % newEWallHeight
                                        print '         location %s' % location
                                        
                                        # get name for uwall
                                        nameSplit = eWallName.split('-')
                                        uWallName = nameSplit[0] + '-' + nameSplit[1] + '-' + nameSplit[2].replace('E','U')
                                        
                                        uWallZ = 0
                                        uWallHeight = (grade - eWallBottom)

                                        attributes = ''
                                        uWalls[uWallName]=UWall(name=uWallName, attributes=attributes, floor=floor, space=space)
                                        uWalls[uWallName].z = uWallZ
                                        uWalls[uWallName].height = uWallHeight
                                        uWalls[uWallName].location = location
                                        print '\n      created %s' % uWallName
                                        print '         z %s' % uWallZ
                                        print '         height %s' % uWallHeight
                                        print '         location %s' % location
                                        
                        if i3 == 'rotate':

                            if not goodWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                r = float(raw_input('angle:'))
                                for goodEWall in goodWalls:
                                    rotateOut = eWalls[goodEWall[0]].rotateWall(r)
                                    if rotateOut[0]:
                                        eWalls[goodEWall[0]].x = rotateOut[0]
                                    if rotateOut[1]:
                                        eWalls[goodEWall[0]].y = rotateOut[1]
                                    if rotateOut[2]:
                                        eWalls[goodEWall[0]].azimuth = rotateOut[2]
                            
                        if i3 == 'mvw':

                            if not goodWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                x = raw_input('x:')
                                y = raw_input('y:')
                                for goodEWall in goodWalls:
                                    for window in eWalls[goodEWall[0]].returnWindows(windows):
                                        print 'moving window %s' % window
                                        if x:
                                            windows[window].moveWindow(x=x)
                                        if y:
                                            windows[window].moveWindow(y=y)


                        if i3 == 'mve':

                            if not goodWalls:
                                print 'Did not find any matching walls\n'
                            else:
                                x = float(raw_input('x:'))
                                y = float(raw_input('y:'))
                                for goodEWall in goodWalls:
                                    moveOut = eWalls[goodEWall[0]].moveWall(x,y)
                                    #if moveOut[0]:
                                    #    UNDERGROUND-WALL  "SUBGRADE SLAB CONSTRUCTION"
                                    #if moveOut[1]:
                                    #    eWalls[goodEWall[0]].y = moveOut[1]

                        if i3 == 'ssw':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                responses = ['','1','2','3']
                                i4 = 'start'
                                while i4 not in responses:
                                
                                    print 'Adjust by:\n  1) percent (constant border)\n  2) percent (proprotional border)\n  3) inches\n[1]\n\n'
                                    i4 = raw_input()
                                
                                if i4 == '3':
                                    adjustBy = 'inches'
                                    question = 'Adjust by how many inches (negative is smaller)? '
                                else:
                                    adjustBy = 'percent'
                                    question = 'Adjust by what percent? (negative is smaller) '
                                    if i4 == '1':
                                        border = 'constant'
                                    else:
                                        border = 'proportional'

                                skip = 0
                                adjust = raw_input(question)
                                try:
                                    adjust = float(adjust)
                                except:
                                    skip = 1
                                    "hmmm. i don't get it..."

                                if not skip:
                                    for goodEWall in goodWalls:
                                        goodEWallName = goodEWall[0]
                                        eWallWindows = eWalls[goodEWallName].returnWindows(windows)
    
                                        for eWallWindow in eWallWindows:

                                            print eWallWindow
                                            
                                            curWidth = float(windows[eWallWindow].width)
                                            curHeight = float(windows[eWallWindow].height)
                                            try:
                                                curX = float(windows[eWallWindow].x)
                                            except:
                                                curX = 0
                                            try:
                                                curY = float(windows[eWallWindow].y)
                                            except:
                                                curY = 0
                                             
                                            
                                            if adjustBy == 'percent':
                                                
                                                if border == 'constant':
                                                    a = 1./curWidth/curHeight
                                                    b = -(1/curWidth + 1/curHeight)
                                                    c = -adjust/100.
                                                    
                                                    wc = -(-b - (b**2.-4.*a*c)**0.5)/(2.*a)
                                                    hc = wc
                                                    print 'constant'
                                                
                                                else:
                                                    a = 1./(curHeight**2)
                                                    b = (2./curHeight)
                                                    c = -adjust/100.
                                                    
                                                    hc = (-b + (b**2-(4.*a*c))**0.5)/(2.*a)
                                                    wc = hc*curWidth/curHeight
                                                    
                                                
                                                #r2 = (-b - (b**2-4*a*c))/2*a
                                                
                                                
                                                newWidth = (curWidth + (wc))
                                                newHeight = (curHeight + (hc))
                                                newX = str(curX +  (curWidth-newWidth)/2.)
                                                newY = str(curY +   (curHeight-newHeight)/2.)
                                                oldArea = curWidth * curHeight
                                                newArea = newWidth * newHeight
                                                scaleChange = newArea/oldArea
                                                newWidth = str(newWidth)
                                                newHeight = str(newHeight)
                                                
                                                
                                                
                                                #newWidth = (curWidth * (1+adjust/200.))
                                                #newHeight = (curHeight * (1+adjust/200.))
                                                #newX = str(curX +  (curWidth-newWidth)/2.)
                                                #newY = str(curY +   (curHeight-newHeight)/2.)
                                                #oldArea = curWidth * curHeight
                                                #newArea = newWidth * newHeight
                                                #scaleChange = newArea/oldArea
                                                #newWidth = str(newWidth)
                                                #newHeight = str(newHeight)
                                                

                                            else:
                                                a = 0
                                                b = 0
                                                c = 0
                                                newWidth = (curWidth - adjust/12.)
                                                newHeight = (curHeight - adjust/12.)
                                                oldArea = curWidth * curHeight
                                                newArea = newWidth * newHeight
                                                newWidth = str(newWidth)
                                                newHeight = str(newHeight)
                                                scaleChange = newArea/oldArea
                                                
                                                newX = str(curX + adjust/24.)
                                                newY = str(curY + adjust/24.)

                                            windows[eWallWindow].width = newWidth
                                            windows[eWallWindow].height = newHeight
                                            windows[eWallWindow].x = newX
                                            windows[eWallWindow].y = newY
                                            
                                            print
                                            print eWallWindow
                                            print '  width changed from %s to %s' % (curWidth, newWidth)
                                            print '  height changed from %s to %s' % (curHeight, newHeight)
                                            print '  x changed from %s to %s' % (curX, newX)
                                            print '  y changed from %s to %s' % (curY, newY)
                                            print '  area changed from %s to %s (%s)' % (oldArea, newArea, scaleChange)
                                            #print '  a,b,c: %s, %s, %s)' % (a, b, c)
                                            #print '  ', hr, wr

                                            if (windows[eWallWindow].width < 0) or (windows[eWallWindow].height < 0):
                                                del windows[eWallWindow]
                                                print 'deleted %s' % eWallWindow
                                    
                        if i3 == 'csw':
                            if not goodWalls:
                                print 'No current walls\n'
                            else:
                                windowHeightScalar = raw_input('What percentage of the height (or global parameter): ')
                                for goodEWall in goodWalls:
                                    goodEWallName = goodEWall[0]
                                    space = eWalls[goodEWallName].space
                                    floor = spaces[space].floor
                                    windowName = '"%s-W1"' % goodEWallName[1:-1]
                                    windows[windowName]=Window(name=windowName, attributes=[], floor=floor, space=space, wall=goodEWallName)
                                    if is_number(windowHeightScalar):
                                        windows[windowName].height = '{#P("HEIGHT")*%s}' % windowHeightScalar
                                    else:
                                        windows[windowName].height = '{#P("HEIGHT")*PARAMETER("%s")}' % windowHeightScalar
                                    windows[windowName].width = '{#P("WIDTH")}'
                                    
                                


                        print 'Top Menu'
                        print '|'
                        print '+--Working with Spaces'
                        print '  |'
                        print '  +--Advanced Wall Management'
                        print 
                        print '      c:      change ewall selection'
                        print '      cbn:    create by nuumber'
                        print '      cte:    change uwalls to ewalls'
                        print '      ctu:    change ewalls to uwalls'
                        print '      csw:    create span windows'
                        print '      mve:    move ewalls'
                        print '      mve:    move ewalls'
                        print '      mvw:    move windows'
                        print '      ssw:    shrink selected windows'
                        print '      nudge:  correct close windows'
                        print '      crh:    center windows horizontally on walls'
                        print '      sbh:    select walls with bad horizontal windows'
                        print '      sbv:    select walls with bad vertical windows'
                        print '      dw:     delete selected walls'
                        print '      dwin:   delete windows for selected walls'
                        print '      pw:     print walls'
                        print '      pwin:   print windows'
                        print '      rotate: rotate ewalls'
                        print '      split:  split ewall into uwall/ewall'
                        print '      ipdf:   import windows from pfd'
                        print '      isvg:   import windows from svg'
                        print '      wf:     write file'
                        print '      q:      exit out of awm'
                        i3 = raw_input('      >')
                        print '\n'



                if i2 == 'dupef':
                    floorIndex = {}
                    c = 0
                    for floor in floors:
                        c += 1
                        floorIndex[c] = floor
                        print c, '-', floor
                        
                
                    print floorIndex
                    c = 0
                    okay = 0
                    print 'which floor?'
                    
                    i3 = raw_input()

                    try:
                        print i3
                        print int(i3)
                        print floors
                        floorChoice = floorIndex[int(i3)]
                        okay = 1
                        print okay
                    except:
                        print 'not a good answer'
                    
                    if okay:
                        floorNumber = int(floorChoice[1:-1])
                        startZ = floors[floorChoice].z
                        floorHeight = floors[floorChoice].floorHeight
                        
                        print "you're on floor %s. what number to go up to?" % floorNumber
                        i3 = int(raw_input())
                        if (i3 <= floorNumber):
                           print 'huh?'
                        else:
                        
                            topFloor = int(i3)
                            currentFloor = floorNumber + 1
                            print topFloor
                            print currentFloor
                            
                            while currentFloor <= topFloor:
                                print currentFloor
                                newFloor = '"%s"' %  (currentFloor)
                                print newFloor
                                
                                floors[newFloor] = copy.copy(floors[floorChoice])
                                floors[newFloor].name = newFloor
                                z = (currentFloor-floorNumber) * floorHeight + startZ
                                floors[newFloor].z = z
                                for space in floors[floorChoice].returnSpaces(spaces):
                                    newSpace = '"%s%s"' % (currentFloor, space[2:-1])
                                    print newSpace
                                    spaces[newSpace] = copy.copy(spaces[space])
                                    spaces[newSpace].name = newSpace
                                    spaces[newSpace].floor = newFloor
                                currentFloor += 1
                    
                
                
                if i2 == 'ass':  # advanced space selection
                    activeElements = returnActiveElements(spaces)
                    i3 = 'c'

                    xMinO = '-'
                    xMaxO = '-'
                    yMinO = '-'
                    yMaxO = '-'
                    xMinI = '-'
                    xMaxI = '-'
                    yMinI = '-'
                    yMaxI = '-'
                    zMin = '-'
                    zMax = '-'
                    zThru = '-'
                    hMin = '-'
                    hMax = '-'
                    regex = '-'
                    isPlenum = '-'
                    isConditioned = '-'
                    isUnconditioned = '-'

                    while i3 <> 'q':
                        
            

                        if i3 == 'a':
                            for space in spaces:
                                print space
                                spaces[space].active = 1
                            printActiveElements(spaces)


                        if i3 =='wf':
                            print 'writing file'
                            writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
                            j = 0
                            countOnly = 1
                        
                        
                        if i3 == 'l':
                            printActiveElements(spaces)

                        if i3 == 'sr':
                            l = raw_input('x1 y1 z1 x2 y2 z2 :')
                            gotIt = 0
                            try: 
                                x1, y1, z1, x2, y2, z2 = l.split()
                                gotIt = 1
                            except:
                                print "I don't understand"
                            
                            if gotIt:
                                for space in spaces:
                                    if spaces[space].active==1:
                                        eWall = '"%s-ROOF"' % space[1:-1]
                                        polygonName = '"%s poly"' % eWall[1:-1]

                                        p = spaces[space].polygon
                                        vs = polygons[p].vertices
                                        roofVs = []
                                        for v in vs:
                                            x,y,z,t,az = translate(x1, y1, z1, x2, y2, z2, v[0], v[1])
                                            #print ' ', x, y, z
                                            roofVs.append([x,y])
                                        polygons[polygonName]=Polygon(name=polygonName, vertices=roofVs)
                                        
                                        attributes = [['CONSTRUCTION', '"EXTERIOR WALL CONSTRUCTION"']]
                                        eWalls[eWall]=EWall(name=eWall, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                                        
                                        eWalls[eWall].x = x1
                                        eWalls[eWall].y = y1
                                        eWalls[eWall].z = float(z1) - spaces[space].trueZ()
                                        eWalls[eWall].azimuth = az
                                        eWalls[eWall].tilt = t
                                        
                                        eWalls[eWall].polygon = polygonName
                                        

                        # Create Sloped roofs
                        # Make roof.svg
                        # define xml attributes up, zmin, zmin for sloped roofs
                        # define xml attributes zmin, zmin for vertical triangle sides
                        # define scale with xml attribute "scale"
                        # See C:\Users\Public\Documents\eQUEST 3-64 Projects\Benchmark_Senior for more detail
                        
                        if i3 == 'sr2':
                            activeSpaceList = []
                            for space in spaces:
                                if spaces[space].active==1:
                                    activeSpaceList.append(space)
                            if len(activeSpaceList) != 1:
                                print ' You must select exactly 1 space'
                            else:
                                space = activeSpaceList[0]

                                orig = 'roofs.svg'
                                new = 'roofs_temp.svg'
                                
                                fo = open(orig, 'r')
                                fn = open(new, 'w')
                                
                                for line in fo.readlines():
                                    if not 'http://www.w3.org/2000/svg' in line:
                                        fn.write(line)
                                    
                                fn.close()
                                
                                import xml.etree.ElementTree as ET
    
                                tree = ET.parse(new)
                                root = tree.getroot()
                                
                                for i in root.findall(".g/rect"):
                                    if i.attrib['id'] == 'scale':
                                        scale = feetToFloat(i.attrib['scale'])
                                        w = float(i.attrib['width'])
                                        h = float(i.attrib['height'])
                                        scaleFactor = scale/(max(w,h))
                                
                                roofs = {}
                                for i in root.findall(".g/path"):
                                    id = i.attrib['id']
                                    print '~~~~~'
                                    print id
                                    print

                                    polygon = inkscapePathToPolygon(i.attrib['d'], scale=scaleFactor)

                                    eWall = '"%s-ROOF-%s"' % (space[1:-1], id)
                                    polygonName = '"%s poly"' % eWall[1:-1]

                                    zmin = float(i.attrib['zmin'])
                                    zmax = float(i.attrib['zmax'])

                                    if len(polygon) > 2: # for sloped polygons
    
                                        up = float(i.attrib['up'])
                                        azimuth = (up + 180)%360

                                            
                                        rPolygon = []     # rotated
                                        rtPolygon = []    # translated
                                        rtsPolygon = []   # shifted (reordered)
                                        rtsePolygon = []  # expanded
                                        r = up
                                    
                                        # rotate polygon
                                        basePoint = []
                                        for p in polygon:
                                            newP = rotate(p[0], p[1], r)
                                            rPolygon.append(newP)
                                            if not basePoint:
                                                basePoint = newP
                                            elif newP[1] < basePoint[1]:
                                                basePoint = newP
                                    
                                    
                                        # translate to the origin
                                        maxPoint = []
                                        for p in rPolygon:
                                            newP = (p[0]-basePoint[0], p[1]-basePoint[1])
                                            rtPolygon.append(newP)
                                            if not maxPoint:
                                                maxPoint = newP
                                            elif newP[1] > maxPoint[1]:
                                                maxPoint = newP

                                    
                                        index = rtPolygon.index((0.0, 0.0))
                                        rtsPolygon = shiftlist(rtPolygon, index)
                                    
                                        tiltRad = math.atan((zmax-zmin)/(maxPoint[1]))
                                        tiltDeg = math.degrees(tiltRad)
                                        factor = 1/math.cos(tiltRad)
                                    
                                        # expand polygon
                                        for p in rtsPolygon:
                                            newP = [p[0], p[1] * factor]
                                            rtsePolygon.append(newP)

    
                                        xOrigin = polygon[index][0]
                                        yOrigin = polygon[index][1]
                                                                    
    
                                        eWall = '"%s-ROOF-%s"' % (space[1:-1], id)
                                        polygonName = '"%s poly"' % eWall[1:-1]
    
                                        polygons[polygonName]=Polygon(name=polygonName, vertices=rtsePolygon)
                                        
                                        attributes = [['CONSTRUCTION', '"EXTERIOR ROOF CONSTRUCTION"']]
                                        eWalls[eWall]=EWall(name=eWall, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                                        
                                        eWalls[eWall].x = xOrigin
                                        eWalls[eWall].y = yOrigin
                                        eWalls[eWall].z = zmin
                                        eWalls[eWall].azimuth = azimuth
                                        eWalls[eWall].tilt = tiltDeg
                                        eWalls[eWall].polygon = polygonName

                                    else: # for verical ewalls

                                        # get angle
                                        print polygon
                                        cAngle = getAngleSafe(polygon[0], polygon[1])
                                        azimuth = swapAngleType(cAngle)
                                        print polygon[0], polygon[1]
                                        print cAngle
                                        print azimuth

                                        xOrigin = polygon[0][0]
                                        yOrigin = polygon[0][1]

                                        x1 = 0
                                        y1 = 0
                                        x2 = pointDistance(polygon[0], polygon[1])
                                        y2 = 0
                                        x3 = x2/2
                                        y3 = (zmax-zmin)

                                        polygons[polygonName]=Polygon(name=polygonName, vertices=[[x1,y1],[x2,y2],[x3,y3]])
                                        
                                        attributes = [['CONSTRUCTION', '"EXTERIOR WALL CONSTRUCTION"']]
                                        eWalls[eWall]=EWall(name=eWall, attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                                        
                                        eWalls[eWall].x = xOrigin
                                        eWalls[eWall].y = yOrigin
                                        eWalls[eWall].z = zmin
                                        eWalls[eWall].azimuth = azimuth
                                        eWalls[eWall].tilt = 90
                                        eWalls[eWall].polygon = polygonName


                                            

                        if i3 == 'piw':
                            tol = 1
                            
                            print 'not yet operable'
                            time.sleep(5)

                            for space in spaces:
                                if spaces[space].active==1:
                                    for iWall in spaces[space].returnIWalls(iWalls):
                                
                                        construction  = self.construction
                                        # fugure out height, width and z
                                        self.height = ''
                                        self.width = ''
                                        self.azimuth = ''
                                        self.nextTo = ''
                                        
                                    
                                    
                                        iWallV = int(iWalls[iWall].location[7:])
                                        thisSpaceVertices = polygons[spaces[space].polygon].vertices
                                        otherSpaceVertices = polygons[spaces[iWalls[iWall].nextTo].polygon].vertices
                                        if iWallV == len(thisSpaceVertices):
                                           vPair = [thisSpaceVertices[-1], thisSpaceVertices[0]]
                                        else:
                                           vPair = [thisSpaceVertices[iWallV-1], thisSpaceVertices[iWallV]]

                                        debug(iWall)
                                        debug('%s, %s'% (vPair[0], vPair[1]))

                                        v = 0
                                        for c in range(0, len(otherSpaceVertices)):
                                            v = c + 1
                                            p1 = otherSpaceVertices[c]
                                            p2 = otherSpaceVertices[(c+1)%len(otherSpaceVertices)]
                                            debug('%s, %s'% (vPair[0], vPair[1]))
                                            d1 = pointDistance(vPair[0], p2)
                                            d2 = pointDistance(vPair[1], p1)
                                            debug('')
                                            debug('%s, %s'% (p1, p2))
                                            debug('%s, %s'% (d1, d2))
                                            if d1 < tol and d2 < tol:
                                                debug('Matching verticy at %s' % v)
                                                matchV = v
                                            
                                        if v:
                                            del iWalls[iWall]
                                            attributes = []
                                            iWalls[iWall]=IWall(name=iWall,attributes=attributes, floor=spaces[space].floor, space=spaces[space].name)
                                            iWalls[iWall].location = 'SPACE-V%s' % v
                                            iWalls[iWall].location = 'SPACE-V%s' % v
                                            

                                            
                                            iWalls[iWall].space, iWalls[iWall].nextTo = iWalls[iWall].nextTo, iWalls[iWall].space
                                        else:
                                            debug('No matching verticy found for iWall %s' % iWall, p=1)
                                        
                                            
                                            
                                        debug('')

                                            
                                            
                                    
                                    
                                


                        if i3 == 'ra':
                            for space in spaces:
                                spaces[space].active = 1
                            
                            for space in spaces:
                                if spaces[space].active==1:
                                    if not spaces[space].testSpace(polygons, floors, xMinO, xMaxO, yMinO, yMaxO, xMinI, xMaxI, yMinI, yMaxI, zMin, zMax, hMin, hMax, regex, isPlenum, isConditioned, isUnconditioned):
                                        spaces[space].active=0
    
                            printActiveElements(spaces)

                        if i3 == 'c':

                            print 'Changing inputs'
                     
                            
                            xMinOTemp = raw_input('xMinO [%s]' % xMinO)
                            xMaxOTemp = raw_input('xMaxO [%s]' % xMaxO)
                            yMinOTemp = raw_input('yMinO [%s]' % yMinO)
                            yMaxOTemp = raw_input('yMaxO [%s]' % yMaxO)
                            xMinITemp = raw_input('xMinI [%s]' % xMinI)
                            xMaxITemp = raw_input('xMaxI [%s]' % xMaxI)
                            yMinITemp = raw_input('yMinI [%s]' % yMinI)
                            yMaxITemp = raw_input('yMaxI [%s]' % yMaxI)
                            zMinTemp = raw_input('zMin [%s]' % zMin)
                            zMaxTemp = raw_input('zMax [%s]' % zMax)
                            zThruTemp = raw_input('zThru [%s]' % zThru)
                            hMinTemp = raw_input('hMin [%s]' % hMin)
                            hMaxTemp = raw_input('hMax [%s]' % hMax)
                            regexTemp = raw_input('regex [%s]' % regex)
                            isPlenumTemp = raw_input('isPlenum [%s]' % isPlenum)
                            isConditionedTemp = raw_input('isConditioned [%s]' % isConditioned)
                            isUnconditionedTemp = raw_input('isUnconditioned [%s]' % isUnconditioned)
                            
                            xMinO = fixInput(xMinOTemp, xMinO)
                            xMaxO = fixInput(xMaxOTemp, xMaxO)
                            yMinO = fixInput(yMinOTemp, yMinO)
                            yMaxO = fixInput(yMaxOTemp, yMaxO)
                            xMinI = fixInput(xMinITemp, xMinI)
                            xMaxI = fixInput(xMaxITemp, xMaxI)
                            yMinI = fixInput(yMinITemp, yMinI)
                            yMaxI = fixInput(yMaxITemp, yMaxI)
                            zMin = fixInput(zMinTemp, zMin)
                            zMax = fixInput(zMaxTemp, zMax)
                            zThru = fixInput(zThruTemp, zThru)
                            hMin = fixInput(hMinTemp, hMin)
                            hMax = fixInput(hMaxTemp, hMax)
                            if regexTemp != '':
                                regex = regexTemp
                            if isPlenumTemp != '':
                                isPlenum = isPlenumTemp.lower()
                            if isConditionedTemp != '':
                                isConditioned = isConditionedTemp.lower()
                            if isUnconditionedTemp != '':
                                isUnconditioned = isUnconditionedTemp.lower()
                            
    
                            for space in spaces:
                                if spaces[space].active==1:
                                    if not spaces[space].testSpace(polygons, floors, xMinO, xMaxO, yMinO, yMaxO, xMinI, xMaxI, yMinI, yMaxI, zMin, zMax, zThru, hMin, hMax, regex, isPlenum, isConditioned, isUnconditioned):
                                        spaces[space].active=0
    
                            printActiveElements(spaces)
                        
                            time.sleep(.5)
                            print '\n still in advanced space selection.  "d" to exit, "c" to make more changes. "l" to list\n'
                            time.sleep(.5)
    
                        print 'Top Menu'
                        print '|'
                        print '+--Working with Spaces'
                        print '  |'
                        print '  +--Advanced Space Selection'
                        print
                        print '      c:      change space selection'
                        print '      a:      all spaces'
                        print '      ra:     reassign active'
                        print '      sr:     sloped roofs'
                        print '      sr2:    sloped roofs 2'
                        print '      piw:    push interior walls to other spaces'
                        print '      l:      list spaces'
                        print '      wf:     write file'
                        print '      q:      exit out of ass'
                        i3 = raw_input('      >')
                        print '\n'



 
                        

                print '\ncTop'
                print '  |'
                print '  +--Working with spaces:'
                print
                print '   -- select --'
                print '   l - list'
                print '   a - all'
                print '   s - select'
                print '   i - inverse'
                print '   f - filter'
                print
                print '   -- report --'
                print '   c - count elements'
                print '   urep - underground report'
                print '   rep - debug report'
                print
                print '   -- duplicate --'
                print '   dupef - duplicate floors (cannot be done after wall creation)'
                print
                print '   -- create --'
                print '   acei - create internal/exterior walls'
                print '   chic - create horiz interior walls'
                print '   acf - create floors'
                print '   acr - create roofs'
                print '   cz - zones'
                print '   cw[xp] - windows [excl. plenum]'
                print
                print '   -- delete --'
                print '   dae - all exterior walls'
                print '   dai - all interior walls'
                print '   dai - all underground walls'
                print '   daw - all windows'
                print '   dsr - selected all roofs'
                print '   dsh - selected all overhangs'
                print '   dsp - selected plenum'
                print
                print '   -- advanced --'
                print '   vs - verify spaces do not intersect'
                print '   awm - advanced wall management'
                print '   aiwm - advanced interior management'
                print '   ass - advanced space selection'
                print '   siw - split interior walls'
                print
                print '   wf - write file'
                print '   q  - quit up to top menu'
                print
                i2 = raw_input('   >')

    
        elif i == 'e':
            while 1==1:
                print 'exterior'
                ui = raw_input("")
                if i[:1] == 'x':
                    break

        elif i == 'sb':
            i4 = raw_input('   default ground level [0] >')

            try:
                ugThreshold = round(float(i4),2)
            except:
                ugThreshold = 0

            #verifySpaces()
            #splitInteriorWalls()
            combineCloseVerticies3()
            splitInteriorWalls()
            createInteriorAndExteriorWalls(ugThreshold=ugThreshold)
            createHorizontalInteriorWalls()
            advancedCreateFloors()
            advancedCreateRoofs()
            createZones()
            #writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
            #print pd2
            #cmd = ["C:\Program Files\eQUEST 3-63\eQUEST.exe", pd2]
            #subprocess.Popen(cmd)
            #errorNumber = 0
            #sys.exit()


        if i =='wf':
            writeFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)

        if i =='wxl':
            writeXlFile(inpFile, beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
                            
        if i =='ixl':
            readXlFile(inpFile)

        
        print ''
        print 'Top Menu:'
        print ''
        print '   f    - import fdf file'
        print '   i    - import existing input file'
        print '   ixl  - import excel file'
        print '   p    - work with polyogns'
        print '   s    - work with spaces'
        print '   sb   - spontaneous building'
        print
        print '   wf  - write file'
        print '   wxl - write excel file'
        print '   q   - quit'
        print ''
        i = raw_input('   >')
        print ''
                                    
    
except:
    if errorNumber != 0:
        print 'Error raised'
        print traceback.print_exc()
        print 'writing file'
        writeFile('backup/'+ inpFile[:-4] + '-' + time.strftime('%y%m%d_%H%M%S')+ '.exc', beginingSection, polygons, polyToElemSection, floors, spaces, eWalls, iWalls, uWalls, windows, doors, elemToSystemSection, systems, zones, endingSection)
    else:
        print 'exiting...'
