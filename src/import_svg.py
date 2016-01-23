import eo
import os
from ref import pd2, input_seed
from utils import rewrap, wrap, unwrap
from svg_building import Svg_Building
from shapely.geometry import LineString, Point, MultiLineString, Polygon, MultiPolygon, GeometryCollection
from collections import defaultdict
import e_shapely, e_math
from e_math import get_angle, angle_difference
import client
DELIMETER = '__'

def build(svg_building):
    b = eo.Building()
    b.construction = client.get_client_construction()
    system = eo.System(b, name=wrap('SYSTEM-PLACEHOLDER'))

    for svg_floor in svg_building.svg_floors:
        poly_suffix = '-POLY'
        floor_name = wrap(svg_floor.floor_name)
        floor = eo.Floor(b, name=floor_name)
        floor.attr['SHAPE'] = 'NO-SHAPE'
        floor.attr['Z'] = svg_floor.z
        floor.attr['FLOOR-HEIGHT'] = svg_floor.floor_height
        floor.attr['SPACE-HEIGHT'] = svg_floor.space_height
        
        system.attr['TYPE'] = 'VAVS'
        system.attr['HEAT-SOURCE'] = 'NONE'
        system.attr['CHW-LOOP'] = wrap('DEFAULT-CHW')

        for svg_space in svg_floor.svg_spaces:
            space_name = wrap(unwrap(floor_name) + DELIMETER + svg_space.path.title)
            poly_name = rewrap(space_name, poly_suffix)
            if svg_space.zone_kind == 'PLENUM':
                space_name = rewrap(space_name, '+P')
            zone_name = rewrap(space_name, ' ZONE')

            space = eo.Space(b, name=space_name, parent=floor)
            space.attr['SHAPE'] = 'POLYGON'
            space.attr['POLYGON'] = poly_name
            space.attr['ZONE-TYPE'] = svg_space.zone_kind

            zone = eo.Zone(b, name=zone_name, parent=system)
            zone.attr['TYPE'] = svg_space.zone_kind
            zone.attr['SPACE'] = space_name

        for svg_polygon in svg_floor.svg_polygons:
            poly_name = wrap(unwrap(floor_name) + DELIMETER + svg_polygon.path.title
                + poly_suffix)
            polygon = eo.Polygon(b, name=poly_name)
            polygon.set_vertices(svg_polygon.scaled_points)

    return b

def split_interior_walls(b, horiz_space_pairs):

    '''
    This needs to be run multiple times in case the creation of one point
    subsequently affect the creation of another which was already completed
    '''

    new_points, times = 0, 0
    times = 0
    while times == 0 or new_points > 1:
        times += 1
        new_points = split_walls_loop(b, horiz_space_pairs)

def split_walls_loop(b, horiz_space_pairs, tol=0.0001):

    messages, new_points = [], defaultdict(list)

    # Find intersection of adjacent spaces to assess errors and add points
    for space, space2 in horiz_space_pairs:
        coords = []
        intersect = space.shapely_poly().intersection(space2.shapely_poly())
        shapely_list = e_shapely.decompose(intersect)
        for shape in shapely_list:

            # Adjacent shapes should not overlap
            if isinstance(shape, (Polygon)):
                if shape.area > tol:
                    messages.append('Spaces %s and %s ' % (space.name,
                        space2.name)  + 'are not aligned properly')
                coords += [tuple(c) for c in shape.exterior.coords]
            else:
                coords += [tuple(c) for c in shape.coords]

        # Assign the points to space line, if they are not already in the space
        for s in [space, space2]:
            for coord in coords:
                point = Point(coord)
                if min([point.distance(p) for p in s.points()]) > tol:

                #if not list(coord) in s.vertices():
                    for i, line in enumerate(s.lines()):
                        key = (s, i)

                        # Check for point already added
                        if key in new_points:
                            if any([p.distance(point) < tol for 
                                    p in new_points[key]]):
                                break

                        # Add point if on line
                        if line.distance(point) < tol:
                            new_points[key].append(point)
                            break
                    else:
                        messages.append('Point %s did not find a ' % point + 
                            'home in %s' % space.name)

    # Add the points to the polygon, starting with the furthest
    for (space, index), (points) in sorted(new_points.items(), reverse=True):
        line = space.lines()[index]
        start = Point(line.coords[0])
        points.sort(key=lambda x:start.distance(x), reverse=True)
        for point in points:
            p = list(point.coords)[0]
            if not p in space.vertices():
                space.polygon().add_verticy(p, index)

    return len(new_points)

def add_walls(b, horiz_space_pairs, tol=0.0001):
    wall_pairs = []
    for space, space2 in horiz_space_pairs:
        for i, line in enumerate(space.lines(), 1):
            if line.distance(space2.shapely_poly()) > tol:
                # space2 it too far away from this wall
                continue

            line_angle = get_angle(*list(line.coords))
            for j, line2 in enumerate(space2.lines(), 1):
                line2_angle = get_angle(*list(line2.coords))
                a_difference = angle_difference(line_angle, line2_angle)
                if line.distance(line2) > tol:
                    # Other wall too far away
                    continue

                if abs(a_difference-180) > tol:
                    # Other wall not opposite facing
                    continue

                if (line.p1.distance(line2.p1) < tol or 
                        line.p2.distance(line2.p2) < tol):
                    # Walls share wrong point
                    continue

                wall_pairs.append((space, i, space2, j))

    # Add IWalls - Cannot add EWalls until all IWalls are made
    partial_ewall_candidates = []
    flat_wall_pairs = []
    
    for wall_pair in wall_pairs:
        # keep this flattened list
        flat_wall_pairs += [(space, i), (space2, j)]

        space, i, space2, j = wall_pair
        space_gz, space2_gz = space.z_global(), space2.z_global()
        space_height, space2_height = space.height(), space2.height()

        # Name manipulation
        iwall_suffix = DELIMETER + ('IW-%s-' % i) + unwrap(space2.name.replace(
            DELIMETER + unwrap(space2.name.split(DELIMETER)[0]), ''))
        iwall_name = rewrap(space.name, iwall_suffix)
        iwall = eo.I_Wall(b, name=iwall_name, parent=space)

        iwall.attr['NEXT-TO'] = space2.name
        iwall.attr['LOCATION'] = 'SPACE-V%s' % (i)
        if space.is_plenum() and space2.is_plenum():
            iwall.attr['CONSTRUCTION'] = b.construction['air']
            iwall.attr['INT-WALL-TYPE'] = 'AIR'
        else:
            iwall.attr['CONSTRUCTION'] = b.construction['interior']

        if space_gz != space2_gz or space_height != space2_height:
            # keep this for partial exteior walls
            ewall_candidates.append(wall_pair)
            wall_z = max(space_gz, space2_gz) - space_gz
            wall_height = min(space_gz + space_height,
                space2_gz + space2_height)
            if wall_z != 0:
                iwall.attr['Z'] = wall_z
            if wall_height != space_height:
                iwall.attr['HEIGHT'] = wall_height

    # Add EWalls on walls which have IWalls
    for partial_ewall_candidate in partial_ewall_candidates:
        print wall_pair
                
    # Any remaining wall which does not have an IWall, gets an Ewall
    for space in b.kinds('SPACE').values():
        for i in range(1, len(space.lines())+1):
            if not (space, i) in flat_wall_pairs:
                ewall_name = rewrap(space.name, DELIMETER + 'E%s' % (i))
                ewall = eo.E_Wall(b, name=ewall_name, parent=space)
                ewall.attr['CONSTRUCTION'] = b.construction['exterior']
                ewall.attr['LOCATION'] = 'SPACE-V%s' % (i)

def interior_horizontal_walls(b, vert_space_pairs, tol=0.01, min_area=1):
    
    c = 0
    for lower_space, upper_space in vert_space_pairs:
        intersect = lower_space.polygon().shapely_poly.intersection(
            upper_space.polygon().shapely_poly)
        for intersect in e_shapely.decompose(intersect):
            if not isinstance(intersect, Polygon):
                continue
            if intersect.area < min_area:
                continue
            c += 1
            iwall_name = rewrap(lower_space.name, DELIMETER + 'top-%04d' % c)
            iwall = eo.I_Wall(b, name=iwall_name, parent=lower_space)
            iwall.attr['LOCATION'] = 'TOP'
            iwall.attr['NEXT-TO'] = upper_space.name        
            if not lower_space.is_plenum() and upper_space.is_plenum():
                iwall.attr['CONSTRUCTION'] = b.construction['ceiling']
            else:
                iwall.attr['CONSTRUCTION'] = b.construction['slab']
            if e_math.tol(intersect.area, lower_space.shapely_poly().area, tol):
                # use space polygon if wall exhausts space
                iwall.attr['POLYGON'] = lower_space.get('POLYGON')
            else:
                # make custom polygon
                poly_name = rewrap(iwall_name, DELIMETER + 'POLY')
                polygon = eo.Polygon(b, name=poly_name)
                point_list = e_shapely.shapely_polygon_to_point_list(intersect)
                if not intersect.convex_hull.exterior.is_ccw:
                    point_list.reverse()
                polygon.set_vertices(point_list)
                iwall.attr['POLYGON'] = poly_name

def exterior_walls_top(b, vert_space_pairs, min_area=1):

    def make_roof(b, roof_name, space, poly_name):
        roof = eo.E_Wall(b, name=roof_name, parent=space)
        roof.attr['LOCATION'] = 'TOP'
        roof.attr['CONSTRUCTION'] = b.construction['roof']                
        roof.attr['POLYGON'] = poly_name

    top_polygons = dict()
    for lower_space, upper_space in vert_space_pairs:
        name = lower_space.name
        if not name in top_polygons:
            top_polygons[name] = lower_space.shapely_poly()
        top_polygons[name] = top_polygons[name].difference(upper_space.shapely_poly())     
        
    for name, space in b.kinds('SPACE').items():
        if name in top_polygons:
            for i, shape in enumerate(e_shapely.decompose(top_polygons[name])):
                if not isinstance(shape, (Polygon)):
                    continue
                elif shape.area < min_area:
                    continue
                roof_name = rewrap(name, DELIMETER + 'roof-%s' % i)
                poly_name = rewrap(roof_name, DELIMETER + 'POLY')
                polygon = eo.Polygon(b, name=poly_name)
                point_list = e_shapely.shapely_polygon_to_point_list(shape)
                if not shape.convex_hull.exterior.is_ccw:
                    point_list.reverse()
                polygon.set_vertices(point_list)
                make_roof(b, roof_name, space, poly_name)
        else:
            roof_name = rewrap(name, DELIMETER + 'roof')
            poly_name = space.polygon().name
            make_roof(b, roof_name, space, poly_name)

def exterior_walls_bottom(b, vert_space_pairs, min_area=1):

    def make_floor(b, floor_name, space, shape):

        poly_name = rewrap(floor_name, DELIMETER + 'POLY')
        polygon = eo.Polygon(b, name=poly_name)
        point_list = e_shapely.shapely_polygon_to_point_list(shape)
        if not shape.exterior.is_ccw:
            point_list.reverse()
        point_list = [list(reversed(p)) for p in list(reversed(point_list))]
        polygon.set_vertices(point_list)

        floor = eo.E_Wall(b, name=floor_name, parent=space)
        floor.attr['LOCATION'] = 'BOTTOM'
        floor.attr['CONSTRUCTION'] = b.construction['overhang']                
        floor.attr['POLYGON'] = poly_name

    bottom_polygons = dict()
    for lower_space, upper_space in vert_space_pairs:
        name = upper_space.name
        if not name in bottom_polygons:
            bottom_polygons[name] = upper_space.shapely_poly()
        bottom_polygons[name] = bottom_polygons[name].difference(lower_space.shapely_poly())     
        
    for name, space in b.kinds('SPACE').items():
        if name in bottom_polygons:
            for i, shape in enumerate(e_shapely.decompose(bottom_polygons[name]), 1):
                if not isinstance(shape, (Polygon)):
                    continue
                elif shape.area < min_area:
                    continue
                floor_name = rewrap(name, DELIMETER + 'floor-%s' % i)
                make_floor(b, floor_name, space, shape)
        else:
            floor_name = rewrap(name, DELIMETER + 'floor')
            make_floor(b, floor_name, space, space.shapely_poly())

def check(svg_building):
    svg_building.check()
    for m in svg_building.messages:
        print m
    return len(svg_building.messages)

def write(b):
    project_name = os.getcwd().split(os.sep)[-1]
    with open(project_name + '.pd2', 'wb') as f:
        f.write(pd2(project_name))

    seed = eo.Building()
    seed.read(input_seed())
    b.extend(seed)
    b.dump(project_name + '.inp')


def main():

    fn = 'floorplans.svg'
    svg_building = Svg_Building(fn) 

    if not check(svg_building):
        b = build(svg_building)
        horiz_space_pairs, vert_space_pairs = b.space_pairs()
        split_interior_walls(b, horiz_space_pairs)
        add_walls(b, horiz_space_pairs)
        interior_horizontal_walls(b, vert_space_pairs)
        exterior_walls_top(b, vert_space_pairs)
        exterior_walls_bottom(b, vert_space_pairs)

        write(b)

if __name__ == '__main__':
    main()
