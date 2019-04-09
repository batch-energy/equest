import os
import eo, e_math, time, im, utils

def phase_0(pdf_file):

    seed_file = [f for f in os.listdir('.') if f.startswith('seed_')][0] 
    im.create(pdf_file, seed_file)

def phase_1(b):

    b.create_zones()
    b.rotate_space_polygons(270)

def phase_2(b):

    b.combine_close_vertices_within_floor(tol=0.75)

    added = True
    c = 0
    while added:
        c += 1
        added = b.split_interior_walls(tol=0.75)

def phase_3(b):

    b.make_walls(short_iwall_names=True)
    b.create_roofs()
    b.create_ceilings()
    b.create_floors()

def phase_4(b):

    for name in b.kinds('WINDOW'):
        b.objects[name].delete()

    b.make_windows('e_new.svg')
    
    
def main():

    phase_0('Takeoffs.pdf')

    input_file = utils.input_file_name()


    b = eo.Building()
    b.load(input_file)

    phase_1(b)
    phase_2(b)
    phase_3(b)
    phase_4(b)
    b.dump()

if __name__ == '__main__':
    main()    

