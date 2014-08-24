def orig_fdf():
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
