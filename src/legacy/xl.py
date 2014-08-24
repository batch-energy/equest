def shoot(sheet, t):
    rc = 0
    for r in t:
        cc = 0
        for c in r:
            sheet.write(rc, cc, c)
            cc += 1
        rc += 1
    



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
      
