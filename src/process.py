import os
import eo, e_math, time, im, utils

def phase_0(pdf_file):

    print '  Importing from PDF'
    seed_file = [f for f in os.listdir('.') if f.startswith('seed_')][0] 
    return im.create(pdf_file, seed_file)

def phase_2(b):

    floor_data = {
        "1":  [10.0, 10.0, "Y", 4],
        "2":  [20.0, 10.5, "N", 0],
        }
    positions = ['Z', 'H', 'HP', 'PH']
    attrs = utils.make_floor_data(floor_data, positions)

    print '  Rotating Spaces'
    b.rotate_floors(90)

def phase_4(b):

    print '  Combining Close Verteces'
    b.combine_close_vertices_within_floor(tol=0.5)

    print '  Splitting Interior Polygon Sides'
    b.split_interior_walls(tol=0.5)

def phase_6(b):

    print '  Making Walls'
    b.make_walls(short_iwall_names=True)
    print '  Making Roofs'
    b.create_roofs()
    print '  Making Ceilings'
    b.create_ceilings()
    print '  Making Floors'
    b.create_floors()

def phase_8(b):

    print '  Importing Windows'
    for name in b.kinds(['WINDOW', 'DOORS']):
        b.objects[name].delete()
    b.make_windows('e1.svg')
    
def main():

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

    for phase in phases:
        if phase == 0:
            arg = 'Takeoffs.pdf'
        else:
            arg = b
        name = 'phase_%s' % phase
        if name in globals():
            result = globals()[name](arg)
            if result == -1:
                return
        if phase == 0:
            b = eo.Building()
            b.load(utils.input_file_name())

    b.dump()

if __name__ == '__main__':
    main()    

