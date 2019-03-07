import utils, re

clients = ['dmi', 'tnz']

spaces_json = 'spaces.json'


numeric = ['X', 'Y', 'Z', 'HEIGHT', 'WIDTH', 'SPACE-HEIGHT', 'FLOOR-HEIGHT', 'TILT', 'AZIMUTH']

parents = {
            'SPACE' : 'FLOOR',
            'EXTERIOR-WALL' : 'SPACE',
            'INTERIOR-WALL' : 'SPACE',
            'UNDERGROUND-WALL' : 'SPACE',
            'WINDOW' : 'EXTERIOR-WALL',
            'DOOR' : 'EXTERIOR-WALL',
            'ZONE' : 'SYSTEM' }

parental_groups = [
    ['FLOOR', 'SPACE','EXTERIOR-WALL', 'INTERIOR-WALL', 'UNDERGROUND-WALL', 'WINDOW', 'DOOR'],
    ['ZONE', 'SYSTEM' ]
            ]


kind_list = [

      'INPUT',
      'PARAMETER',

      'RUN-PERIOD',
      'RUN-PERIOD-PD',
      'DESIGN-DAY',
      'HOLIDAYS',
      'SITE-PARAMETERS',
      'BUILD-PARAMETERS',
      'MATERIAL',
      'LAYERS',
      'CONSTRUCTION',

      'WINDOW-LAYER',
      'GLASS-TYPE-CODE',
      'GLASS-TYPE',

      'DAY-SCHEDULE-PD',
      'DAY-SCHEDULE',
      'WEEK-SCHEDULE-PD',
      'WEEK-SCHEDULE',
      'SCHEDULE-PD',
      'SCHEDULE',

      'POLYGON',
      'BASELINE',

      'FLOOR',
      'SPACE',
      'EXTERIOR-WALL',
      'INTERIOR-WALL',
      'UNDERGROUND-WALL',
      'UNDERGROUND-FLOOR',
      'ROOF',
      'DOOR',
      'WINDOW',
      'BUILDING-SHADE',
      'FIXED-SHADE',

      'ELEC-METER',
      'FUEL-METER',
      'STEAM-METER',
      'CHW-METER',

      'MASTER-METERS',

      'CIRCULATION-LOOP',
      'PUMP',
      'BOILER',
      'CHILLER',
      'DW-HEATER',
      'ELEC-GENERATOR',
      'GROUND-LOOP-HX',
      'HEAT-EXCHANGER',
      'HEAT-REJECTION',

      'SYSTEM',
      'ZONE',

      'PARAMETRIC-INPUT',
      'WALL-PARAMETERS',

      'SET-DEFAULT',
      'LIKE',
      'TITLE',
      'LAMP-TYPE',
      'LIGHTING-SYSTEM',
      'LUMINAIRE-TYPE',
      'TROMBE-WALL-NV',

      'LOAD-MANAGEMENT',
      'MATERIALS-COST',
      'PV-MODULE',
      'SUBR-FUNCTIONS',
      'THERMAL-STORAGE',
      'BLOCK-CHARGE',

      'EQUIP-CTRL',
      'COMPONENT-COST',
      'POLLUTANT-COEFFS',
      'CURVE-FIT',
      'RATCHET',
      'UTILITY-RATE',


      'REPORT-BLOCK',
      'HOURLY-REPORT',


      'LOADS-REPORT',
      'PLANT-REPORT',
      'SYSTEMS-REPORT',
      'ECONOMICS-REPORT',
      'ABORT',
      'DIAGNOSTIC',
      'END',
      'COMPUTE',
      'STOP'
      ]





def is_child(object_kind):
    return any([object_kind == value for value in parents.values()])

def is_parent(object_kind):
    return object_kind in parents

def in_same_group(kind1, kind2):
    if kind1 == kind2:
        return True
    for group in parental_groups:
        if all([k in group for k in kind1, kind2]):
            return True
    return False



def pd2(project):
   return utils.outdent(
        '''
        Proj   "%(project)s"
           ProgramVersion = "eQUEST 3.65.7163"
           BDBaseVersion = 25
           ProductCode = "eQUEST"
           WeatherFile = "TMY2\SEATTLWA.bin"
           CreateDate = 1212866696
           ModDate = 1258058376
           LibraryFile = "eQ_Lib.dat"
           InputModule = 1
           UseCameraData = 1
           ClippingRange = ( 703.024, 1952.68 )
           FocalPoint = ( 232.513, 58.7751, 3.52929 )
           Position = ( 1115.21, 632.005, 667.973 )
           ViewUpVector = ( 0, 0, 1 )
           ViewAngle = 19.1564
           InterfaceMode = 1
           AllowWizard = 0
           InputUnitsType = "English"
           OutputUnitsType = "English"
           DetailedModelEdits = 1
           ProjTreeType[1] = 0
           ProjTreeID[1] = 10000
           ProjTreeLabel[1] = "Project:  'Roland_Park'"
           ..

        DiagData   "Detailed UI DiagData"
           PolyWndGridRes = 1
           PolyWndLwrLeftX = 167.1
           PolyWndLwrLeftY = 43.9
           PolyWndWidth = 122.857
           ..

        FacetColor   "By Wall Type"
           FacetType = "Walls"
           ColorOption = "By Wall Type"
           ..

        FacetColor   "By Construction"
           FacetType = "Walls"
           ColorOption = "By Construction"
           ..

        FacetColor   "Uniform"
           FacetType = "Windows"
           ColorOption = "Uniform"
           ..

        FacetColor   "By Glass Type"
           FacetType = "Windows"
           ColorOption = "By Glass Type"
           ..

        Light3D   "Light3D - Default"
           Type = "Default"
           ..

        Light3D   "Light3D - User1"
           Type = "User Defined 1"
           ..

        Light3D   "Light3D - User2"
           Type = "User Defined 2"
           ..

        Light3D   "Light3D - User3"
           Type = "User Defined 3"
           ..

        Light3D   "Light3D - User4"
           Type = "User Defined 4"
           ..

        Light3D   "Light3D - User5"
           Type = "User Defined 5"
           ..


        END_OF_FILE

        ''' % {'project':project}, 8)

def input_seed():
   return utils.outdent(
        '''
        INPUT ..

        "Entire Year" = RUN-PERIOD-PD
           BEGIN-MONTH      = 1
           BEGIN-DAY        = 1
           BEGIN-YEAR       = 2013
           END-MONTH        = 12
           END-DAY          = 31
           END-YEAR         = 2013
           ..

        "Cooling Design Day" = DESIGN-DAY
           TYPE             = COOLING
           DRYBULB-HIGH     = 91
           DRYBULB-RANGE    = 14
           WETBULB-AT-HIGH  = 67
           MONTH            = 7
           NUMBER-OF-DAYS   = 120
           ..

        "Heating Design Day" = DESIGN-DAY
           TYPE             = HEATING
           DRYBULB-HIGH     = 37
           ..

        SITE-PARAMETERS
           ..

        BUILD-PARAMETERS
           ..

        "Standard US Holidays" = HOLIDAYS
           LIBRARY-ENTRY "US"
           ..

        "Ceiling" = LAYERS
           MATERIAL         = ( "AcousTile (HF-E5)" )
           ..
        "Exterior Wall" = LAYERS
           MATERIAL         = ( "Face Brick 3in (BK04)" )
           ..
        "Exterior Roof" = LAYERS
           MATERIAL         = ( "Blt-Up Roof 3/8in (BR01)", "Plywd 1in (PW06)" )
           ..
        "Concrete" = LAYERS
           MATERIAL         = ( "Conc HW 12in (HF-C11)" )
           ..
        "Interior Wall" = LAYERS
           MATERIAL         = ( "Plywd 1in (PW06)" )
           ..

        "EXTERIOR WALL CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           LAYERS           = "Exterior Wall"
           ..
        "EXTERIOR ROOF CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           ROUGHNESS        = 5
           LAYERS           = "Exterior Roof"
           ..
        "EXTERIOR FLOOR CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           LAYERS           = "Concrete"
           ..
        "SUBGRADE SLAB CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           LAYERS           = "Concrete"
           ..
        "UNDERGROUND WALL CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           LAYERS           = "Concrete"
           ..
        "UNDERGROUND ROOF CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           LAYERS           = "Exterior Roof"
           ..
        "INTERIOR WALL CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           ROUGHNESS        = 5
           LAYERS           = "Interior Wall"
           ..
        "INTERIOR CEILING CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           ROUGHNESS        = 5
           LAYERS           = "Ceiling"
           ..
        "INTERIOR SLAB CONSTRUCTION" = CONSTRUCTION
           TYPE             = LAYERS
           ROUGHNESS        = 5
           LAYERS           = "Concrete"
           ..
        "AIR WALL CONSTRUCTION" = CONSTRUCTION
           TYPE             = U-VALUE
           ROUGHNESS        = 5
           U-VALUE          = 10
           ..

        LOADS-REPORT
           ..

        SYSTEMS-REPORT
           ..

        PLANT-REPORT
           ..

        ECONOMICS-REPORT
           ..

        END ..
        COMPUTE ..
        STOP ..
        ''', 8)

