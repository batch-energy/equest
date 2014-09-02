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


kind_list = [

      'INPUT',
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

      'SYSTEM',
      'ZONE',

      'PARAMETER',
      'PARAMETRIC-INPUT',
      'WALL-PARAMETERS',

      'SET-DEFAULT',
      'LIKE',
      'TITLE',
      'LAMP-TYPE',
      'LIGHTING-SYSTEM',
      'LUMINAIRE-TYPE',
      'TROMBE-WALL-NV',

      'PUMP',
      'BOILER',
      'CHILLER',
      'CIRCULATION-LOOP',
      'DW-HEATER',
      'ELEC-GENERATOR',
      'GROUND-LOOP-HX',
      'HEAT-EXCHANGER',
      'HEAT-REJECTION',

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
