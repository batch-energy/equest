from eo import Polygon, I_WALL, E_WALL

def make_verticel_walls(b, spaces=None)
    
    if not spaces:
        spaces = b1.kinds('SPACE').values()

    checked = []
    space_pairs = []

    for space in spaces:
        checked.append(space)
        for other_space in set(spaces) - set(checked):
            if (space.poly().distance(other_space.poly())) > 1:
                # Other space is too far away horizontally
                continue
            elif Dec(space.vertical_overlap(other_space)) == 0:
                # Other space is too far away vertically
                continue
            space_pairs.append((space, other_space))
    
    # Identify candidate adjacent wall pairs
    wall_pairs = []
    bad_wall_pairs = []
    for space, other_space in space_pairs:
        for i, line in enumerate(space.lines(), 1):
            if line.distance(other_space.poly()) > 1:
                continue
                # Other space it too far away from this wall
            line_angle = e_math.get_angle(*list(line.coords))
            for j, other_line in enumerate(other_space.lines(), 1):
                other_line_angle = e_math.get_angle(*list(other_line.coords))
                a_difference = e_math.angle_difference(line_angle, other_line_angle)
                if line.distance(other_line) > 1:
                    # Other wall too far away
                    continue
                if abs(a_difference-180) > 5:
                    # Other wall not opposite facing
                    continue
                if line.p1.distance(other_line.p1) < 1 or line.p2.distance(other_line.p2) < 1:
                    # Walls share wrong point
                    continue
                wall_pair = (space.name, i, other_space.name, j)
                if line.p1.distance(other_line.p2) < 1 and line.p2.distance(other_line.p1) < 1:
                    wall_pairs.append(wall_pair)
                    continue
                bad_wall_pairs.append(wall_pair)

    if bad_wall_pairs:
        for pair in bad_wall_pairs:
            print pair
    else:
        pass
    

 
def make_horizontal_internal_walls(b, spaces=None):

    if not spaces:
        spaces = b.kinds('SPACE').values()

    for space in spaces:
        space_poly = self.poly()
        for other_space in spaces:
            if space.vertical_overlap(other_space) < 1:
                continue                
            other_space.poly = other_space.poly()
            intersection = space.polygon().intersection(other_space.polygon())

            if is_instance(intersection, MultiPolygon):
                poly_list = intersection.geoms
            elif is_instance(intersection, Poly):
                poly_list = [intersection]
            else:
                poly_list = []

            for i, poly in enumerate(poly_list):
                name = '"%s-IT+B-%s"' % (space.name.name[1:-1], i)
                i_wall = I_Wall(b, name, 'INTERIOR-WALL' parent=space)

                poly_name = '"%s_poly"' % (name)
                i_wall_polygon = Polygon(b, name, 'POLYGON')
                i_wall_polygon.vertices(page, fdf_polygon)
                i_wall.attr['POLYGON'] = i_wall_polygon
               
                if space.z_global() < other_space.z_global():
                    i_wall.attr['LOCATION'] = 'TOP'
                else:
                    i_wall.attr['LOCATION'] = 'BOTTOM'

                if space.floor == other_space.floor:
                    i_wall.attr['CONSTRUCTION'] = 'ceiling'
                else:
                    i_wall.attr['CONSTRUCTION'] = 'slab'



    