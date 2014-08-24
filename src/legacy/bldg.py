


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
