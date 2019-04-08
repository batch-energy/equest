import os

def get_client():
    if 'seed_tnz.inp' in os.listdir('.'):
        return 'TNZ'
    elif 'seed_dmi.inp' in os.listdir('.'):
        return 'DMI'
    elif 'seed_smma.inp' in os.listdir('.'):
        return 'SMMA'
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

        construction['door'] = '"EXTERIOR WALL CONSTRUCTION"'

    elif client == 'TNZ':

        construction['air'] = '"AIR WALL"'
        construction['interior'] = '"C I WALL"'
        construction['exterior'] = '"C E WALL"'
        construction['underground'] = '"C S WALL"'

        construction['slab'] = '"C I FLOOR"'
        construction['ceiling'] = '"C I CEIL"'

        construction['underground_slab'] = '"C S FLOOR"'
        construction['overhang'] = '"C E FLOOR"'
        construction['roof'] = '"C E ROOF"'

        construction['door'] = '"C DOOR"'

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

        construction['door'] = '"EXTERIOR WALL CONSTRUCTION"'

    return construction

def get_client_glass():
    if get_client() == 'TNZ':
        return '"F W"'
    else:
        return '"EXTERIOR GLASS"'
