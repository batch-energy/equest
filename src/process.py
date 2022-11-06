import os
try:
    pass #os.add_dll_directory(r'"C:\OSGeo4W64\bin')
except AttributeError:
    pass

import os, sys, time
import eo
import e_math
import im
import utils

def phase_0(pdf_file):

    print('  Importing from PDF')

    floor_data = {
        'B': [-11.5, 11.5, 'N', 0],
        '1': [0, 18, 'N', 0],
        '2': [18, 15, 'N', 0],
        '3': [33, 15, 'N', 0],
        '4': [48, 20, 'N', 0]}

    positions = ['Z', 'H', 'HP', 'PH']
    attrs = utils.make_floor_data(floor_data, positions)

    seed_file = [f for f in os.listdir('.') if f.startswith('seed_')][0]
    return im.create(pdf_file, seed_file, attrs)

def phase_2(b):

    print('  Rotating Spaces')
    b.rotate_floors(90)

def phase_4(b):

    print('  Combining Close Verteces')
    b.combine_close_vertices_within_floor(tol=0.5)

    print('  Splitting Interior Polygon Sides')
    b.split_interior_walls(tol=0.5)

def phase_6(b):

    print('  Making Walls')
    b.make_walls(short_iwall_names=True)
    print('  Making Roofs')
    b.create_roofs()
    print('  Making Ceilings')
    b.create_ceilings()
    print('  Making Floors')
    b.create_floors()

    #b.remove_plenum_for_spaces_with_no_exterior_walls()

    for floor in b.objects.get(['"B"'], []):
        for space in floor.spaces():
            for wall in space.e_walls():
                if wall.is_vertical():
                    wall.to_uwall()

def phase_8(b):

    print('  Importing Windows')
    for name in b.kinds(['WINDOW', 'DOOR']):
        b.objects[name].delete()
    b.make_windows('e1.svg')
    b.validate_windows()

    #b.add_daylighting()
    #b.remove_vertical_interior_walls_for_spaces_with_no_windows()


def main():

    phases = set()
    if len(sys.argv) == 1:
        phase_groups = ['0_9']
    else:
        phase_groups = sys.argv[1].split(',')

    for phase_group in phase_groups:
        if phase_group.startswith('_'):
            phases |= set(range(int(phase_group[1:]) + 1))
        elif phase_group.endswith('_'):
            phases |= set(range(int(phase_group[:-1]), 10))
        elif '_' in phase_group:
            start, end = [int(i) for i in phase_group.split('_')]
            phases |= set(range(start, end+1))
        else:
            phases.add(int(phase_group))

    b = None
    for phase in phases:
        if phase == 0:
            result = phase_0('Takeoffs.pdf')
            if result == -1:
                return
            b = eo.Building()
            b.load(utils.input_file_name())
            continue
        if b is None:
            b = eo.Building()
            b.load(utils.input_file_name())
        name = 'phase_%s' % phase
        if name in globals():
            result = globals()[name](b)

    b.dump()

if __name__ == '__main__':
    main()

