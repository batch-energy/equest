import os

def get_client():
    if 'seed_tnz.inp' in os.listdir('.'):
        return 'TNZ'
    elif 'seed_dmi.inp' in os.listdir('.'):
        return 'DMI'
    else:
        return None

def get_client_construction():

    client = get_client()
    construction = {}

    if client == 'DMI':

        construction['air'] = '"AIR WALL CONSTRUCTION"'
        construction['interior'] = '"INTERIOR WALL CONSTRUCTION"'
        construction['exterior'] = '"EXTERIOR WALL CONSTRUCTION"'
        construction['underground'] = '"UNDERGROUND WALL CONSTRUCTION"'

        construction['slab'] = '"INTERIOR SLAB CONSTRUCTION"'
        construction['ceiling'] = '"INTERIOR CEILING CONSTRUCTION"'

        construction['roof'] = '"EXTERIOR ROOF CONSTRUCTION"'

        construction['underground_slab'] = '"SUBGRADE SLAB CONSTRUCTION"'
        construction['overhang'] = '"EXTERIOR FLOOR CONSTRUCTION"'

    elif client == 'TNZ':

        construction['air'] = '"AIR WALL"'
        construction['interior'] = '"INT WALL CONST"'
        construction['exterior'] = '"EXT WALL CONST"'
        construction['underground'] = '"SUB WALL CONST"'

        construction['slab'] = '"SLAB CONST"'
        construction['ceiling'] = '"CEILING CONST"'

        construction['underground_slab'] = '"SUB WALL CONST"'
        construction['overhang'] = '"EXT FLOOR CONST"'
        construction['roof'] = '"ROOF CONST"'

    else:
        construction['air'] = '"AIR WALL CONSTRUCTION"'
        construction['interior'] = '"INTERIOR WALL CONSTRUCTION"'
        construction['exterior'] = '"EXTERIOR WALL CONSTRUCTION"'
        construction['underground'] = '"UNDERGROUND WALL CONSTRUCTION"'

        construction['slab'] = '"INTERIOR SLAB CONSTRUCTION"'
        construction['ceiling'] = '"INTERIOR CEILING CONSTRUCTION"'

        construction['roof'] = '"EXTERIOR ROOF CONSTRUCTION"'

        construction['underground_slab'] = '"SUBGRADE SLAB CONSTRUCTION"'
        construction['overhang'] = '"EXTERIOR FLOOR CONSTRUCTION"'


    return construction
