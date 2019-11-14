import os
import eo, e_math, time, im, utils

def phase_0(pdf_file):

    print '  Importing from PDF'
    seed_file = [f for f in os.listdir('.') if f.startswith('seed_')][0] 
    return im.create(pdf_file, seed_file)

def phase_1(b):

    print '  Creating Zones'
    b.create_zones()
    print '  Rotating Spaces'
    b.rotate_floors(90)

def phase_2(b):

    print '  Combining Close Verteces'
    b.combine_close_vertices_within_floor(tol=0.5)

    print '  Splitting Interior Polygon Sides'
    b.split_interior_walls(tol=0.5)

def phase_3(b):

    print '  Making Walls'
    b.make_walls(short_iwall_names=True)
    print '  Making Roofs'
    b.create_roofs()
    print '  Making Ceilings'
    b.create_ceilings()
    print '  Making Floors'
    b.create_floors()

def phase_4(b):

    print '  Importing Windows'
    for name in b.kinds(['WINDOW', 'DOORS']):
        b.objects[name].delete()
    b.make_windows('e1.svg')
    
def main():

    print
    if phase_0('Takeoffs.pdf') is None:
        return

    input_file = utils.input_file_name()


    b = eo.Building()
    b.load(input_file)

    phase_1(b)
    phase_2(b)
    phase_3(b)
    phase_4(b)
    b.dump()

    print

if __name__ == '__main__':
    main()    

