from collections import OrderedDict, namedtuple, defaultdict
import re, time, os, math
from shapely.geometry import Polygon as ShapelyPoly
from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString
from shapely.ops import split as shapely_split, nearest_points
import copy
from string import ascii_lowercase
import operator
from shapely.errors import TopologicalError
from shapely import affinity

from utils import wrap, unwrap
from client import get_client_construction, get_client_glass
import svg_file
import e_math
import utils
import ref
from e_math import is_close, distance, angle, projected_distance, angle_distance, dist

class RegenerateError(Exception):

    def __init__(self, msg):
        self.msg = msg

class Filter(object):

    def __init__(self):
        attr = {}

class TolerantOrderedDict(OrderedDict):

    def __init__(self):
        super(TolerantOrderedDict, self).__init__()

    def __getitem__(self, value):
        try:
            return super(TolerantOrderedDict, self).__getitem__(wrap(value))
        except KeyError:
            return super(TolerantOrderedDict, self).__getitem__(value)
        except KeyError:
            raise


class Building(object):
    def __init__(self):
        self.objects = TolerantOrderedDict()
        self.defaults = OrderedDict()
        self.parameters = OrderedDict()

    def load(self, fn):
        self.fn = fn
        with open(self.fn, 'r') as f:
            text = f.read()
        self.read(text)

    def read(self, text):
        text = self.__clean_file(text)
        self.__objectify(self.__split_objects(text))

    def kinds(self, kind_or_kinds):
        '''OrderedDict of objects only of kind or kinds'''

        if isinstance(kind_or_kinds, list):
            target_kinds = kind_or_kinds
        else:
            target_kinds = [kind_or_kinds]

        kinds = {}

        for name, obj in list(self.objects.items()):
            if obj.kind in target_kinds:
                kinds[name] = obj
        return kinds

    def dump(self, fn=None):

        def order(a_pair, b_pair):
            a = a_pair[0]
            b = b_pair[0]
            if '-' in a and '-' in b:
                for a_part, b_part in zip(a.split('-'), b.split('-')):
                    if a_part == b_part:
                        continue
                    if a_part.isdigit() and b_part.isdigit():
                        a_part = int(a_part)
                        b_part = int(b_part)
                    if a_part > b_part:
                        return 1
                    else:
                        return -1
                return 0
            elif a > b:
                return 1
            elif a < b:
                return -1
            else:
                 return 0

        fn = fn or self.fn

        #if os.path.exists(fn):
        #    os.remove(fn)

        t = ''
        defaults_written = []
        for kind in ref.kind_list:
            if kind == 'PARAMETER':
                for parameter in list(self.parameters.values()):
                    t += parameter.write()
            for name, default in list(self.defaults.items()):
                if ref.in_same_group(default.kind, kind):
                    if not default in defaults_written:
                        t += default.write()
                        defaults_written.append(default)

            if not kind in list(ref.parents.keys()):
                for _, o in sorted(list(self.kinds(kind).items())):
                    t += o.write()

        self.write(fn, t)

    def write(self, fn, t):
        with open(fn, 'w') as f:
            f.write(t)

    def get_objects(self, *names):

        '''Given a list of object names, return the objects, tolerates no quotes'''

        objects = []
        for name in names:
            if name in self.objects:
                objects.append(self.objects[name])
            elif wrap(name) in self.objects:
                objects.append(self.objects[wrap(name)])
            else:
                raise Exception('%s not found' % name)
        return objects

    def force_object(self, s):
        if isinstance(s, str):
            if not s.startswith('"'):
                s = wrap(s)
            return self.objects[s]
        else:
            return s


    def __clean_file(self, text):
        return '\n'.join([l.strip() for l in text.split('\n')
            if l.strip() and not l.strip()[0] == '$'])

    def __split_objects(self, text):
        return [self.__clean_object(o) for o in text.split('..')]

    def __clean_object(self, object):
        lines = [l.strip() for l in object.split('\n') if l.strip()]
        if not lines:
            return ''

        new_lines = []
        new_line, attr_lines = lines[0], lines[1:]

        for i, line in enumerate(attr_lines):
            if not i or re.search(r' =($| )', line):
                new_lines.append(new_line)
                new_line = line
            else:
                new_line += ' ' + line

        new_lines.append(new_line)
        return '\n'.join(new_lines)

    def __objectify(self, object_text_list):
        current_parent = {}
        for object_text in object_text_list:
            lines = object_text.split('\n')

            if 'SET-DEFAULT' in lines[0]:
                kind = lines[0].split()[-1]
                types= [line.split('=')[1].strip()
                    for line in lines
                    if len(line.split('='))>1
                    and line.split('=')[0].strip()=='TYPE']

                d = Default(self, kind, types[0] if types else None)
                d.read(lines)
                continue

            if lines[0].strip() == 'PARAMETER':
                p = Parameter(self)
                p.read(lines)
                continue

            if '=' in lines[0]:
                name, kind = [s.strip() for s in lines[0].split('=')]
            else:
                name, kind = lines[0], lines[0]

            if kind in list(ref.parents.keys()):
                parent = current_parent[ref.parents[kind]]
            else:
                parent = None

            # Load special objects
            if kind == 'FLOOR':
                o = Floor(self, name, kind)
            elif kind == 'SPACE':
                o = Space(self, name, kind, parent=parent)
            elif kind == 'EXTERIOR-WALL':
                o = E_Wall(self, name, kind, parent=parent)
            elif kind == 'INTERIOR-WALL':
                o = I_Wall(self, name, kind, parent=parent)
            elif kind == 'UNDERGROUND-WALL':
                o = U_Wall(self, name, kind, parent=parent)
            elif kind == 'WINDOW':
                o = Window(self, name, kind, parent=parent)
            elif kind == 'DOOR':
                o = Door(self, name, kind, parent=parent)
            elif kind == 'SYSTEM':
                o = System(self, name, kind, parent=parent)
            elif kind == 'ZONE':
                o = Zone(self, name, kind, parent=parent)
            elif kind == 'POLYGON':
                o = Polygon(self, name, kind)
            else:
                o = Object(self, name, kind, parent=parent)
            o.read(lines)

            current_parent[kind] = o

    def get_object_attr(self, object_name):
        if object_name in self.objects:
            return self.objects[object_name].attr
        else:
            return {}

    def get_default_attr(self, key):
        if key in self.defaults:
            return self.defaults[key].attr
        else:
            return {}

    def extend(self, other):
        self.objects.update(other.objects)
        self.defaults.update(other.defaults)
        self.parameters.update(other.parameters)

    def rename(self, object, name):
        old_name = object.name
        self.objects[name] = object
        object.name = name
        del self.objects[old_name]

    def sorted_floors(self):

        '''Floors in ascenting z'''
        return [sf[1] for sf in sorted([(f.z(), f)
            for f in list(self.kinds('FLOOR').values())])]

    def next_name(self, template):
        i = 1
        while True:
            name = template % i
            if name in self.b.objects:
                i += 1
            else:
                return name

    def space_pairs(self, tol=0.1):

        '''Returns a list of spaces pairs which are adjacent to one another'''

        spaces = list(self.kinds('SPACE').values())
        checked_set = set()
        space_set = set(spaces)

        # Identify candidate adjacent space pairs
        horiz_space_pairs, vert_space_pairs = [], []
        for space in spaces:
            checked_set.add(space)
            for space2 in space_set - checked_set:
                if (space.shapely_poly.distance(space2.shapely_poly)) > tol:
                    # Other space is too far away horizontally
                    continue
                vertical_overlap = space.vertical_overlap(space2)
                if vertical_overlap < -tol:
                    # Other space is too far away vertically
                    continue
                if vertical_overlap < tol:
                    vert_space_pairs.append(Space.vertically_ordered(space,
                        space2))
                    continue
                horiz_space_pairs.append((space, space2))
        return horiz_space_pairs, vert_space_pairs

    def space_map(self):
        lookup = defaultdict(list)
        for space1, space2 in self.space_pairs()[0]:
            lookup[space1.name].append(space2.name)
            lookup[space2.name].append(space1.name)
        return lookup

    def make_walls(self, make_ewall_for_bad_space_pairs=True, short_iwall_names=False):

        '''Make interior walls, then exterior walls where there are no interio ones'''

        construction = get_client_construction()
        bad_space_pairs = []

        space_pairs = self.space_pairs()

        # Indentify interior walls
        interior_walls = defaultdict(list)
        for space_1, space_2 in self.space_pairs()[0]:
            z_min, z_max = space_1.overlap_heights(space_2)
            for i, ls1 in enumerate(space_1.polygon.lines, 1):
                points_1 = space_1.point_pair_shapely(i)
                for j, ls2 in enumerate(space_2.polygon.lines, 1):
                    points_2 = space_2.point_pair_shapely(j)
                    if ls1.distance(ls2) > 0.1:
                        continue
                    elif points_1[0].distance(points_2[0]) < 0.1:
                        continue
                    elif points_1[1].distance(points_2[1]) < 0.1:
                        continue
                    elif abs(180 - angle(ls1.coords, ls2.coords)) > 4:
                        continue
                    elif points_1[0].distance(points_2[1]) < 0.1 and points_1[1].distance(points_2[0]) < 0.1:
                        interior_walls[(space_1.name, i)].append((space_2.name, (z_min, z_max)))
                        interior_walls[(space_2.name, j)].append((space_1.name, (z_min, z_max)))
                    else:
                        bad_space_pairs.append([(space_1.name, i), (space_2.name, j)])

        bad_walls = []
        if bad_space_pairs:
            print(('\n  Bad Space Pairs, %s\n' % len(bad_space_pairs)))
            for pair in bad_space_pairs:
                print(('    ' + '  -  '.join(['%s : %s ' % (name, i) for (name, i) in pair])))
                bad_walls +=  pair
            if make_ewall_for_bad_space_pairs is True:
                print('\n  Exterior wall will be made for these, but they are probably not exterior walls\n')
            else:
                print('\n  No walls will be made for these, but they are probably misaligned interior walls\n')


        # Create interior walls
        for (space_name, wall_index), adjacents in list(interior_walls.items()):
            for i, (other_space_name, (lower, upper)) in enumerate(adjacents):
                if space_name < other_space_name:
                    continue
                space = self.objects[space_name]
                other_space = self.objects[other_space_name]
                name = space.name[:-1] + '-I%s' % (wall_index)
                if short_iwall_names:
                    name = name + '_%s"' % i
                else:
                    name = name + '_%s"' % (other_space_name[1:-1].split('-')[1])
                space_min = space.z_global
                space_max = space_min + space.height()
                i = I_Wall(self, name=name, parent=space)
                z = lower - space.z_global
                if not is_close(lower, space_min, 0.1):
                    i.attr['Z'] = z
                if not is_close(upper-lower, space_max-space_min, 0.1):
                    i.attr['HEIGHT'] = upper - lower
                i.attr['NEXT-TO'] = other_space_name
                i.attr['LOCATION'] = 'SPACE-V%s' % (wall_index)
                if space.is_plenum() and other_space.is_plenum():
                    i.attr['CONSTRUCTION'] = construction['air']
                else:
                    i.attr['CONSTRUCTION'] = construction['interior']

        # Create exterior walls
        for space in list(self.kinds('SPACE').values()):
            space_min = space.z_global
            space_max = space_min + space.height()
            for i in range(1, len(space.vertices()) + 1):
                adjacents = interior_walls.get((space.name, i), [])
                pairs = [a[1] for a in adjacents]
                spans = [s for s in e_math.overlap_split([space_min, space_max], pairs)[1]]

                if (space.name, i) in bad_walls and make_ewall_for_bad_space_pairs is False:
                    continue

                for j, (lower, upper) in enumerate(spans, 1):
                    if is_close(lower, upper, 0.1):
                        continue
                    suffix = '' if (len(spans) == 1) else ('_%s' % j)
                    name = space.name[:-1] + '-E%s%s"' % (i, suffix)
                    e = E_Wall(self, name=name, parent=space)
                    z = lower - space.z_global
                    if not is_close(lower, space_min, 0.1):
                        e.attr['Z'] = z
                    if not is_close(upper-lower, space_max-space_min, 0.1):
                        e.attr['HEIGHT'] = upper - lower
                    e.attr['LOCATION'] = 'SPACE-V%s' % (i)
                    e.attr['CONSTRUCTION'] = construction['exterior']

    def remove_walls(self):
        for name in [wall for wall in list(self.kinds('INTERIOR-WALL').keys()) \
                                         + list(self.kinds('EXTERIOR-WALL').keys()) \
                                         + list(self.kinds('UNDERGROUND-WALL').keys()) ]:
            self.objects[name].delete()


    def apply_grade(self, default=0, gradelines=None):
        gradelines = gradelines or []

    def convert_obvious_underground_walls(self):

        '''Convert Ewall to Uwall if it's under a Uwall floor'''

        ewall_midpoints = {ewall:Point(ewall.midpoint())
            for ewall in list(self.kinds('EXTERIOR-WALL').values())
            if ewall.is_regular_wall()}

        underground_floors = [ugw
            for ugw in list(self.kinds('UNDERGROUND-WALL').values())
            if ugw.tilt() == 180]

        candidates = []
        for ugf in underground_floors:
            for ewall, ewall_midpoint in list(ewall_midpoints.items()):
                if ewall.z_global < ugf.z_global:
                    if ewall_midpoint.distance(ugf.parent.polygon.shapely_poly) < 1:
                        candidates.append(ewall)

        for ewall in set(candidates):
            ewall.to_uwall()

    def collapse_floors(self):
        z = 0
        self.__floor_orig_z = {}
        for floor in self.sorted_floors():
            self.__floor_orig_z[floor.name] = floor.z()
            floor.attr['Z'] = z
            z += float(floor.height())


    def expand_floors(self):
        for floor in self.kinds('FLOOR').values():
            floor.attr['Z'] = self.__floor_orig_z[floor.name]

    def make_windows(self, svg_path, tol_d=5, tol_a=5):

        '''Make windows from svg projections'''

        id_ = 0

        Window_Kind = namedtuple('Window_Kind', ['kind', 'title', 'height', 'width', 'y', 'scale', 'frame', 'split', 'material', 'plenum'])

        svg = svg_file.Svg_Page(svg_path)

        # - Sizes and attributes are ALL based off the color
        # - each color for windows should have single one, of the same color with a
        #   title and attributes defeined in the xml directly
        # - attributes are:
        #   _y : y
        #   _h : height
        #   _w : width
        #   _r : reduce to
        #   _f : add frame
        #   _s : split y/[n]
        #   _c : construction (for doors)
        #   _gt : glass type (for windows)
        #   _plenum : include on plenum y/[n]

        color_map = {}
        for window in svg.windows:
            color = window.color_id()

            if window.title:
                if color in color_map:
                    raise Exception('title defined multiple times for color %s' % color)

                # TODO - Handle default more gracefully
                if '#000000' in color or window.get('_c'):
                    kind = 'door'
                    material = window.get('_c') or get_client_construction()['door']
                else:
                    kind = 'window'
                    material = window.get('_gt') or get_client_glass()

                color_map[color] = Window_Kind(
                    kind,
                    window.title,
                    e_math.convert_feet(window.get('_h')) if window.get('_h') else None,
                    e_math.convert_feet(window.get('_w')) if window.get('_w') else None,
                    e_math.convert_feet(window.get('_y')) if window.get('_y') else None,
                    float(window.get('_r')) if window.get('_r') else 1,
                    window.get('_f') and window.get('_f').startswith('y'),
                    window.get('_s') and window.get('_s').startswith('y'),
                    material,
                    (window.get('_plenum') or 'no').startswith('y')
                    )

        for color in sorted(svg.color_ids()):
            if not color in color_map:
                raise Exception('Color %s not defined' % color)

        # These track probems in window takeoffs
        reference_wall_names = defaultdict(list)
        wall_windows = defaultdict(list)
        used_window_colors = set()

        for projection in svg.projections:

            # This loop because it's possible for projection to
            # represent more than one identical wall
            for reference_wall_name in projection.walls:

                try:
                    reference_wall = self.objects[wrap(reference_wall_name)]
                except KeyError as e:
                    print('Wall %s not found (%s)' % (reference_wall_name, \
                        projection.origin.svg_rect.id))
                    raise

                if not isinstance(reference_wall, E_Wall):
                    raise Exception(f'{reference_wall_name} is a {type(reference_wall)} instead of an E_Wall')

                reference_wall_names[reference_wall_name].append(
                    projection.origin.svg_rect.id)

                ref_p1, ref_p2 = reference_wall.get_vertices()

                for wall in reference_wall.planar_walls(tol_d=tol_d, tol_a=tol_a):
                    w_p1, w_p2 = wall.get_vertices()

                    origin_shift = distance(ref_p1, w_p1)

                    if e_math.angle_difference(
                            e_math.get_angle(ref_p1, ref_p2),
                            e_math.get_angle(ref_p1, w_p1)) > 90:
                        origin_shift = -origin_shift

                    wall_x1 = origin_shift
                    wall_y1 = wall.z_global - reference_wall.z_global
                    wall_width = wall.width()
                    wall_height = wall.height()
                    wall_x2 = wall_x1 + wall_width
                    wall_y2 = wall_y1 + wall_height

                    for i, window in enumerate(projection.windows, 1):
                        color_id = window.color_id()
                        used_window_colors.add(color_id)
                        window_data = color_map[color_id]

                        # Plenum walls normally ignored
                        if window_data.plenum == False and wall.parent.is_plenum():
                            continue

                        window_x1 = window.x
                        window_y1 = window.y
                        window_width = window_data.width or window.width
                        window_height = window_data.height or window.height
                        window_x2 = window_x1 + window_width
                        window_y2 = window_y1 + window_height

                        # if windows is set to split, it will be broken across the
                        # different walls and omitted when the wall does not exist.
                        # Otherwise, the windows is applied, in full, on the wall
                        # where its center falls

                        if window_data.split:
                            x1 = max(0, window_x1-wall_x1)
                            y1 = max(0, window_y1-wall_y1)
                            x2 = min(wall_width, window_x2-wall_x1)
                            y2 = min(wall_height, window_y2-wall_y1)
                            w = x2 - x1
                            h = y2 - y1
                            if w < 0.25 or h < 0.25:
                                continue
                        else:
                            window_center = (window_x1 + window_x2)/2, (window_y1 + window_y2)/2,
                            if (wall_x1 < window_center[0] < wall_x2 and
                                wall_y1 < window_center[1] < wall_y2):
                                    x1, y1 = window_x1-wall_x1, window_y1-wall_y1
                                    w, h = window_width, window_height
                            else:
                                continue

                        # Scale windows for frames
                        orig_w, orig_h = w, h
                        w, h = e_math.scale_rectangle(w, h, float(window_data.scale))
                        frame_width = (orig_w-w)/2.
                        x1 = x1 + frame_width
                        y1 = window_data.y or y1 + frame_width

                        id_ += 1

                        if window_data.kind == 'door':
                            template = '-D_%s_{number}' % window_data.title
                            name = wall.find_next_child_name(template)
                            door = Door(self, name=name, parent=wall)
                            door.attr['X'] = x1
                            door.attr['Y'] = y1
                            door.attr['WIDTH'] = w
                            door.attr['HEIGHT'] = h
                            door.attr['CONSTRUCTION'] = window_data.material
                        else:
                            name = utils.suffix(wall.name, '-W_%s_%s' % (id_, window_data.title))
                            win = Window(self, name=name, parent=wall)
                            win.attr['X'] = x1
                            win.attr['Y'] = y1
                            win.attr['WIDTH'] = w
                            win.attr['HEIGHT'] = h
                            win.attr['GLASS-TYPE'] = window_data.material
                            if window_data.frame:
                                win.attr['FRAME-WIDTH'] = frame_width


                        if False:
                            print()
                            print(('NAME      ', name))
                            print(('REFERENCE ', reference_wall_name))
                            print(('PROJECTION', projection.origin.svg_rect.id))
                            print()


        for reference_wall_name, svg_rects in reference_wall_names.items():
            if len(svg_rects) > 1:
                print('  Error for %s' % reference_wall_name)
                print('    has multiple rectangles: %s' % ', '.join(svg_rects))

        if svg.errors:
            print('\n  Error on svg parsing')
            for error in svg.errors:
                print(f'    {error}')
            print('')

        if True:
            # Print wond attrs when creating windows
            for color_id in sorted(used_window_colors):
                win = color_map[color_id]
                if win.kind == 'door':
                    continue
                print ('\n  %s : %s (%s)' % (win.title, unwrap(win.material), color_id))
                for attr, value in sorted(win._asdict().items()):
                    if attr == 'kind' and value=='door':
                        continue
                    if attr in ['kind', 'material', 'title']:
                        continue
                    if attr in ['height', 'width'] and value is None:
                        continue
                    print('    %s %s' % (attr, value))
            print('')

    def validate_windows(self):

        off_wall = dict()
        bad_pairs = defaultdict(set)
        for wall in self.kinds('EXTERIOR-WALL').values():
            for window in wall.windows():
                for other_window in wall.windows():
                    if window is other_window:
                        continue
                    pair = tuple(sorted([window.name, other_window.name]))
                    if pair in bad_pairs[wall.name]:
                        continue
                    elif window.within(other_window):
                        bad_pairs[wall.name].add(pair)
                    elif other_window.within(window):
                        bad_pairs[wall.name].add(pair)

                # TODO: need to adjust for polygon wall defintion with window
                frame_width = window.frame_width()
                if isinstance(frame_width, str):
                    frame_width = 0

                off_by = {
                    0 - (window.x() - frame_width) :'left',
                    window.x() + window.width() + frame_width - wall.width() : 'right',
                    0 - (window.y() - frame_width) : 'bottom',
                    window.y() + window.height() + frame_width - wall.height() : 'top'
                }
                max_off = max(off_by.keys())
                if max_off > 0:
                    off_wall[window.name] = (max_off, off_by[max_off])

        if any([prs for prs in bad_pairs.values()]):
            print('  Some windows overlap')
            for wall, window_names in sorted(bad_pairs.items()):
                if window_names:
                    print('    %s' % wall)
                    for name1, name2 in window_names:
                        print('      %s / %s' % (name1, name2))
            print('')
        else:
            print('  No Overlapping windows\n')

        if off_wall:
            print('  Some windows are off the walls (%s)' % len(off_wall))
            for wall_name, (off_by, direction) in sorted(off_wall.items()):
                print(f'    {wall_name} ({round(off_by, 2)} - {direction})')
            print('')
        else:
            print('  No windows are off walls\n')

    def rotate_floors(self, degrees, floors=None):

        '''Rotate all spaces or spaces on floors'''

        if floors is None:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())]
        else:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())
                if space.parent.name in floors]

        for polygon in set(polygons):
            polygon.rotate(degrees)

    def flip_horizontal(self, floors=None):

        '''Rotate all spaces or spaces on floors'''

        if floors is None:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())]
        else:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())
                if space.parent.name in floors]

        for polygon in set(polygons):
            polygon.flip_horizontal()

    def move_floors(self, x, y, floors=None):

        '''Rotate all spaces or spaces on floors'''

        if floors is None:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())]
        else:
            polygons = [space.polygon for space in list(self.kinds('SPACE').values())
                if space.parent.name in floors]

        for polygon in set(polygons):
            polygon.move(x, y)

    def combine_close_vertices(self, spaces=None, tol=0.5):

        '''Combines polygon vertices for provided spaces'''

        def mean(values):
            return float(sum(values)) / len(values)

        # must add spaces by sorted floors to assign group membership
        points = OrderedDict()
        for floor in self.sorted_floors():
            for space in floor.children:
                if spaces is not None and not space in spaces:
                    continue
                for i, point in enumerate(space.polygon.points):
                    points[(space, i)] = point

        # Create groups of points
        groups = []
        for key, point in list(points.items()):
            space, verticy = key
            flag = False
            for group in groups:
                for other_key, other_point in group:
                    other_space, other_verticy = other_key
                    if other_point.distance(point) < tol:
                        if space.polygon is other_space.polygon or \
                                space.vertical_overlap(other_space) > 1:
                            flag = True
                            group.append((key, point))
                            break
                if flag:
                    # inner loop was broken
                    break
            else:
                # inner loop not broken, make new group
                groups.append([(key, point)])

        # Create map for lookup of new vertices
        lookup = {}
        for group in groups:
            if len(group) > 1:
                x, y = [mean(n) for n in zip(*[(p.x, p.y) for _, p in group])]
                for (space, i), point in group:
                    lookup[(space, i)] = (x, y)

        # Assign new points if defined, or existing if not
        polygons = []
        for space in list(self.kinds('SPACE').values()):

            # do not adjust the same polygons more than once
            if space.polygon in polygons:
                continue
            else:
                polygons.append(space.polygon)

            space.polygon.set_vertices(
                [lookup.get((space, i), point)
                for i, point in enumerate(space.polygon.vertices)])
            space.polygon.delete_sequential_dupes()

    def combine_close_vertices_within_floor(self, tol=0.5):

        '''Combines space polygon vertices within a floor if they are close'''

        # this is faster because the loop is tighter, (per floor), reducing
        # comparisons substantially

        def mean(values):
            return float(sum(values)) / len(values)

        # Floors are done individually
        for floor in list(self.kinds('FLOOR').values()):
            polygons = set([space.polygon for space in floor.children])
            points = {
                (polygon, i):point for polygon in polygons
                    for i, point in enumerate(polygon.points)}

            # Create groups of points
            groups = []
            for key, point in list(points.items()):
                flag = False
                for group in groups:
                    for other_key, other_point in group:
                        if other_point.distance(point) < tol:
                            flag = True
                            group.append((key, point))
                            break
                    if flag:
                        break
                else:
                    groups.append([(key, point)])

            # Create map for lookup of new vertices
            lookup = {}
            for group in groups:
                if len(group) > 1:
                    x, y = [mean(n) for n in zip(*[(p.x, p.y) for _, p in group])]
                    for (polygon, i), point in group:
                        lookup[(polygon, i)] = (x, y)

            # Assign new points if defined, or existing if not
            for polygon in polygons:
                polygon.set_vertices(
                    [lookup.get((polygon, i), point)
                    for i, point in enumerate(polygon.vertices)])
                polygon.delete_sequential_dupes()

    def combine_close_vertices_to_space(self, space, floors, tol=0.5):

        '''Aligns polygons on floors to specific space'''

        floor_polygons = set([s.polygon
            for f in floors for s in f.children if s is not space])

        for floor_polygon in floor_polygons:

            if floor_polygon.shapely_poly.distance(space.shapely_poly) > tol:
                continue

            for i, floor_point in enumerate(floor_polygon.points):
                for space_point in space.points():
                    if floor_point.distance(space_point) < tol:
                         floor_polygon.set_verticy(space_point, i)

    def split_interior_walls_spanned(self, tol=1, space_pairs=None):

        '''
        Splits space where it intersects with adjacent space across multiple floors

        space pairs can be provided, if known. for each pair, the first contains the
        lines, and the second contains the points which are along that line

        '''

        if not space_pairs:
            _, pairs = self.space_pairs()
        else:
            pairs = space_pairs

        for space, other_space in pairs:
            print((space, other_space))
            for i, line in enumerate(space.polygon.lines):
                for j, point in enumerate(other_space.polygon.points):

                    # Line and point are distant
                    if point.distance(line) > tol:
                        continue

                    # Point is on line endpoint
                    if any([(p.distance(point) < tol) for p in [line.p1, line.p2]]):
                        continue

                    p = line.interpolate(line.project(point))

                    space.polygon.add_verticy(p, i) # plus because we're looping through the lines
                    other_space.polygon.set_verticy(p, j)

                    #space.polygon.delete_sequential_dupes()
                    other_space.polygon.delete_sequential_dupes()

    def split_interior_walls_prescribed_(self, spaces, tol=1):

        '''Splits space where it intersects with adjacent space'''

        for space in spaces:
            ssp = space.shapely_poly

            add_points = []
            print((space.name))

            for other_space in spaces:
                if space is other_space:
                    continue
                if space.vertical_overlap(other_space) < 0:
                    continue
                ossp = space.shapely_poly
                if ssp.distance(ossp) > 1:
                    continue

                print(('  ', other_space.name))
                for ls1 in space.polygon.lines:
                    for ls2 in other_space.polygon.lines:
                        if ls1.distance(ls2) > 1:
                            continue
                        if abs(180 - angle(ls1.coords, ls2.coords)) > 5:
                            continue
                        spt1, spt2 = [Point(p) for p in ls1.coords]
                        ospt1, ospt2 = [Point(p) for p in ls2.coords]


                        if spt1.distance(ospt1) < 1:
                            continue
                        if spt2.distance(ospt2) < 1:
                            continue

                        print(('        s1', spt1))
                        print(('        s2', spt2))
                        print(('        o1', ospt1))
                        print(('        o2', ospt2))

                        print(('     ', ls1, ls2))

                        if spt2.distance(ospt1) > 1 and ospt1.distance(ls1) < 1:
                            print(('         ADDED 1 ', list(ospt1.coords)))
                            add_points.append(ospt1)

                        if spt1.distance(ospt2) > 1 and ospt2.distance(ls1) < 1:
                            print(('         ADDED 2 ', list(ospt2.coords)))
                            add_points.append(ospt2)


    def split_interior_walls_prescribed(self, spaces=None, tol=1):

        '''Splits space where it intersects with adjacent space'''

        def sorter(point):
            return point.distance(base_point)

        if spaces is None:
            spaces = list(self.kinds('SPACE').values())
        else:
            spaces = [self.force_object(s) for s in spaces]

        added_total = True

        while added_total:

            added_total = 0

            for space in spaces:
                #print space.name
                poly = space.shapely_poly

                add_points = defaultdict(list)

                for other_space in spaces:
                    other_poly = other_space.shapely_poly
                    if space is other_space:
                        continue
                    if space.vertical_overlap(other_space) < 0.1:
                        continue
                    if poly.distance(other_poly) > 1:
                        continue

                    for i, line in enumerate(space.polygon.lines, 0):
                        point_1, point_2 = [Point(p) for p in line.coords]
                        for point in other_space.polygon.points:
                            if line.distance(point) > 1:
                                continue
                            if point.distance(point_1) < 1:
                                continue
                            if point.distance(point_2) < 1:
                                continue
                            add_points[i].append(point)

                            added_total += 1

                for point_loc, added_points in sorted(list(add_points.items()), reverse=True):
                    base_point = space.polygon.points[point_loc]
                    added_points.sort(key=sorter, reverse=True)
                    prev_point = None
                    for point in added_points:
                        if prev_point is not None and prev_point.distance(point) < 0.1:
                            continue
                        pt = point.coords[0]
                        space.polygon.add_verticy(pt, point_loc)
                        prev_point = point

            print('  Added', added_total)

    def adjust_spaces_to_align(self, basespace, move_spaces):

        basespace = self.force_object(basespace)
        move_spaces = [self.force_object(s) for s in move_spaces]

        moved_points = []
        moved_floors = set()
        for point in basespace.polygon.points:
            #print '\n', point.coords[0]
            for space in move_spaces:
                #print '  ', space.name
                moved_floors.add(space.parent.name)
                for i, move_point in enumerate(space.polygon.points):
                    #print '   ', move_point
                    if point.distance(move_point) < 1:
                        #print '     Close', move_point, point
                        moved_points.append((move_point, point))
                        #print space.polygon.vertices
                        space.polygon.set_verticy(point.coords[0], i)
                        #print space.polygon.vertices

        for floor_name in moved_floors:
            for space in list(self.kinds('SPACE').values()):
                if space.parent.name != floor_name:
                    continue
                for i, point in enumerate(space.polygon.points):
                    for moved_point, base_point in moved_points:
                        if point.distance(moved_point) < 0.1:
                            space.polygon.set_verticy( base_point.coords[0], i)

    def magic_align_by_base(self, base_space_names):
        if isinstance(base_space_names, str):
            base_space_names = [base_space_names]
        lookup = self.space_map()
        for base_space_name in base_space_names:
            other_spaces = [self.objects[n] for n in lookup[base_space_name]]
            other_spaces.sort(key=operator.attrgetter('z_global'), reverse=True)
            names = [other.name for other in other_spaces]
            self.magic_align_by_name(base_space_name, *names)
            for space in [self.objects[base_space_name]] + other_spaces:
                space.polygon.delete_sequential_dupes()

    def magic_align_by_name(self, *space_names):
        self.magic_align(self.get_objects(*space_names))

    def magic_align(self, spaces):
        self.split_interior_walls_prescribed(spaces)
        self.adjust_spaces_to_align(spaces[0], spaces[1:])

    def align_all_to_this(self, points):

        '''Forces all spaces along provided points to share wall vertices'''

        def loc(obj):
            if isinstance(obj, Point):
                return obj.coords[0]
            elif isinstance(obj, LineString):
                return list(obj.coords)

        def segs(ls):
            return zip(ls.coords[:-1], ls.coords[1:])

        # Make linestring from points provided
        ls = LineString(points)
        ls_pts = [Point(p) for p in ls.coords]

        # Find all spaces near that linestring
        spaces = [s for s in self.kinds('SPACE').values()
            if s.shapely_poly.distance(ls) < 1]

        # Move all close points to provided linestring.
        # Shared points will remain aligned since they are treated equally
        points = set()
        for space in spaces:
            poly_points = []
            poly = space.polygon
            for verticy in poly.vertices:
                point = Point(verticy)
                if point.distance(ls) < 1:
                    for pt in ls_pts:
                        if point.distance(pt) < 1:
                            poly_points.append(loc(pt))
                            points.add(loc(pt))
                            break
                    else:
                        new_point = list(nearest_points(ls, point)[0].coords)[0]
                        poly_points.append(new_point)
                        points.add(new_point)
                else:
                    poly_points.append(list(point.coords)[0])
            poly.set_vertices(poly_points)

        # Make a map of all of the points that need to be consolidated
        # because they are close to one another
        point_locs = set()
        update_map = {}
        for i, (near_loc, far_loc) in enumerate(segs(ls)):
            ls_points = []
            near_point, far_point = Point(near_loc), Point(far_loc)
            for point_loc in points:
                point = Point(point_loc)
                if point.distance(near_point) > 0.001 and \
                        point.distance(far_point) > 0.001 and \
                        point.distance(LineString([near_loc, far_loc])) < 0.001:
                    ls_points.append((point.distance(near_point), point_loc))
            current = None
            for dist, point_loc in sorted(ls_points):
                if current is None:
                    point_locs.add(point_loc)
                    current = point_loc
                elif Point(current).distance(Point(point_loc)) < 1:
                    update_map[point_loc] = current
                else:
                    point_locs.add(point_loc)
                    current = point_loc

        # Consolidate the space points and save to space polygon
        for space in spaces:
            poly_points = []
            poly = space.polygon
            for verticy in poly.vertices:
                if verticy in update_map:
                    if update_map[verticy] not in poly_points:
                        poly_points.append(update_map[verticy])
                else:
                    poly_points.append(verticy)
            poly.set_vertices(poly_points)

        # Add a point for each point between any existing polygon points
        def add(pt):
            if pt not in new_points:
                new_points.append(pt)
        for space in spaces:
            new_points = []
            for i, line in enumerate(space.lines(), start=1):
                queue = []
                near_loc = list(line.coords)[0]
                add(near_loc)
                for point_loc in point_locs:
                    point = Point(point_loc)
                    if line.distance(point) < 0.0001:
                        queue.append((Point(near_loc).distance(point), point_loc))
                for _, pt in sorted(queue):
                    add(pt)

            space.polygon.set_vertices(new_points)

    def split_interior_walls(self, tol=1):

        '''Splits space where it intersects with adjacent space'''

        for floor in self.kinds('FLOOR').values():

            added = True
            while added:
                added = 0

                polygons = set([space.polygon for space in floor.children])

                points = {
                    (polygon, i):point for polygon in polygons
                        for i, point in reversed(list(enumerate(polygon.points)))}

                lines = {
                    (polygon, i):line for polygon in polygons
                        for i, line in reversed(list(enumerate(polygon.lines)))}

                lookup_move = {}
                lookup_add = {}

                # finds at most one point near line
                for (line_poly, i), line in lines.items():
                    for (point_poly, j), point in points.items():
                        if (point_poly, j) in lookup_move or line_poly is point_poly:
                            continue
                        if any([(p.distance(point) < tol) for p in [line.p1, line.p2]]):
                            continue
                        if point.distance(line) < tol:
                            p = line.interpolate(line.project(point))
                            lookup_move[(point_poly, j)] = (p.x, p.y)
                            lookup_add[(line_poly, i)] = (p.x, p.y)

                # move close points
                for polygon in polygons:
                    polygon.set_vertices(
                        [lookup_move.get((polygon, i), point)
                        for i, point in enumerate(polygon.vertices)])

                # add new points along lines
                for (poly, i), point in lookup_add.items():
                    poly.add_verticy(point, i)
                    added += 1

                print(('    ...added %s' % added))


    def create_roofs(self, tol=1, use_space_poly_tol=0.99, ratio_tol=0.05):

        '''
        Creates roofs in model

            tol: vertical tolerance for overlapping spaces
            use_space_poly_tol: when close enough, just use the space poly
            ratio_tol: skip when area is very small compared to perimeter

        '''

        for space in list(self.kinds('SPACE').values()):
            running_roof_polygon = copy.copy(space.shapely_poly)
            for other_space in list(self.kinds('SPACE').values()):
                if abs(space.z_global + space.height() - other_space.z_global) < tol:
                    try:
                        running_roof_polygon = running_roof_polygon.difference(other_space.shapely_poly)
                    except TopologicalError as e:
                        msg = 'Shapely failure making roof for %s\n' % space.name + \
                              'This line fails when a space has very narrow ' + \
                              ' corridors connecting larger pieces. ' + \
                              '"Combine close vertices collapes the corridor\n\n'
                        print(msg)
                        raise e
            if running_roof_polygon.area / space.shapely_poly.area > use_space_poly_tol:
                roof_polygon_name_list = [space.polygon.name]
            else:
                roof_polygon_name_list = []

                if isinstance(running_roof_polygon, MultiPolygon):
                    roof_shapely_polygon_list = [p for p in running_roof_polygon.geoms]
                elif isinstance(running_roof_polygon, ShapelyPoly):
                    roof_shapely_polygon_list = [running_roof_polygon]
                else:
                    continue

                deleted_count = 0
                for i, shapely_polgyon in enumerate(roof_shapely_polygon_list, 1):
                    name = utils.suffix(space.name, '-Roof_%s poly' % (i-deleted_count))
                    polygon = Polygon(self, name=name)
                    polygon.set_vertices(list(shapely_polgyon.exterior.coords))
                    try:
                        polygon.delete_sequential_dupes()
                    except RegenerateError:
                        polygon.delete()
                        deleted_count += 1
                        continue
                    if polygon.area()/polygon.perimeter() < ratio_tol:
                        polygon.delete()
                        deleted_count += 1
                        continue
                    if not polygon.is_ccw():
                        polygon.reverse()
                    roof_polygon_name_list.append(name)

            for i, polygon_name in enumerate(roof_polygon_name_list, 1):
                if (space.z_global + space.height()) >= 0:
                    Wall = E_Wall
                    construction = get_client_construction()['roof']
                else:
                    Wall = U_Wall
                    construction = get_client_construction()['underground_slab']
                wall = Wall(self, name=utils.suffix(space.name, '-Roof_%s' % i), parent=space)
                wall.attr['CONSTRUCTION'] = get_client_construction()['roof']
                wall.attr['LOCATION'] = 'TOP'
                if polygon_name != space.polygon.name:
                    wall.attr['POLYGON'] = polygon_name

    def create_floors(self, tol=1, use_space_poly_tol=0.99, ratio_tol=0.10, z=0, spaces=None):

        '''
        Creates floors and overhangs in model

            tol: vertical tolerance for overlapping spaces
            use_space_poly_tol: when close enough, just use the space poly
            ratio_tol: skip when area is very small compared to perimeter
        '''

        for space in spaces or list(self.kinds('SPACE').values()):
            running_floor_polygon = copy.copy(space.shapely_poly)
            for other_space in list(self.kinds('SPACE').values()):
                if abs(space.z_global - (other_space.z_global + other_space.height())) < tol:
                    try:
                        running_floor_polygon = running_floor_polygon.difference(other_space.shapely_poly)
                    except TopologicalError as e:
                        msg = 'Shapely failure making floor for %s\n' % space.name + \
                              'This line fails when a space has very narrow ' + \
                              ' corridors connecting larger pieces. ' + \
                              '"Combine close vertices collapes the corridor\n\n'
                        print(msg)
                        raise e

            if running_floor_polygon.area / space.shapely_poly.area > use_space_poly_tol:
                floor_polygon_name_list = [space.polygon.name]
            else:
                floor_polygon_name_list = []

                if isinstance(running_floor_polygon, MultiPolygon):
                    floor_shapely_polygon_list = [p for p in running_floor_polygon.geoms]
                elif isinstance(running_floor_polygon, ShapelyPoly):
                    floor_shapely_polygon_list = [running_floor_polygon]
                else:
                    continue

                deleted_count = 0
                for i, shapely_polygon in enumerate(floor_shapely_polygon_list, 1):
                    name = utils.suffix(space.name, 'FLOOR_%s poly' % (i-deleted_count))
                    polygon = Polygon(self, name=name)
                    polygon.set_vertices(list(shapely_polygon.exterior.coords))
                    polygon.mirror_and_reverse()
                    try:
                        polygon.delete_sequential_dupes()
                    except RegenerateError:
                        polygon.delete()
                        deleted_count += 1
                        continue
                    if polygon.area()/polygon.perimeter() < ratio_tol:
                        polygon.delete()
                        deleted_count += 1
                        continue
                    if not polygon.is_ccw():
                        polygon.reverse()
                    floor_polygon_name_list.append(name)

            for i, polygon_name in enumerate(floor_polygon_name_list, 1):
                if (space.z_global) <= z + 1:
                    Wall = U_Wall
                    construction = get_client_construction()['underground_slab']
                else:
                    Wall = E_Wall
                    construction = get_client_construction()['overhang']
                wall = Wall(self, name=utils.suffix(space.name, '-Floor_%s' % i), parent=space)
                wall.attr['CONSTRUCTION'] = construction
                wall.attr['LOCATION'] = 'BOTTOM'
                if polygon_name != space.polygon.name:
                    wall.attr['POLYGON'] = polygon_name

    def create_ceilings(self, tol=1, use_space_poly_tol=0.99, ratio_tol=0.05):

        '''
        Creates horizontal interior walls

            tol: vertical tolerance for overlapping spaces
            use_space_poly_tol: when close enough, just use the space poly
            ratio_tol: skip when area is very small compared to perimeter
        '''
        count = 0
        for space in list(self.kinds('SPACE').values()):
            ceiling_polygons = copy.copy(space.shapely_poly)
            for i, other_space in enumerate(self.kinds('SPACE').values()):
                if abs(space.z_global + space.height() - other_space.z_global) < tol:
                    try:
                        ceiling_polygon = space.shapely_poly.intersection(other_space.shapely_poly)
                    except TopologicalError as e:
                        msg = 'Shapely failure making ceiling for %s\n' % space.name + \
                              'This line fails when a space has very narrow ' + \
                              ' corridors connecting larger pieces. ' + \
                              '"Combine close vertices collapes the corridor\n\n'
                        print(msg)
                        raise e

                    if isinstance(ceiling_polygon, MultiPolygon):
                        ceiling_shapely_polygon_list = [p for p in ceiling_polygon.geoms]
                    elif isinstance(ceiling_polygon, ShapelyPoly):
                        ceiling_shapely_polygon_list = [ceiling_polygon]
                    else:
                        continue

                    if other_space.is_plenum():
                        construction = get_client_construction()['ceiling']
                    else:
                        construction = get_client_construction()['slab']

                    ceiling_polygon_name_list = []
                    for j, ceiling_shapely_polygon in enumerate(ceiling_shapely_polygon_list):
                        count += 1
                        if (ceiling_shapely_polygon.area / space.shapely_poly.area) > use_space_poly_tol:
                            ceiling_polygon_name = space.polygon.name
                        else:
                            ceiling_polygon_name = utils.suffix(space.name, '-C%s poly' % (count))
                            polygon = Polygon(self, name=ceiling_polygon_name)
                            polygon.set_vertices(list(ceiling_shapely_polygon.exterior.coords))
                            try:
                                polygon.delete_sequential_dupes()
                            except RegenerateError:
                                polygon.delete()
                                continue
                            if polygon.area()/polygon.perimeter() < ratio_tol:
                                polygon.delete()
                                continue
                            if not polygon.is_ccw():
                                polygon.reverse()
                        ceiling_name = utils.suffix(space.name, '-C%s' % (count))
                        ceiling = I_Wall(self, name=ceiling_name, parent=space)
                        ceiling.attr['LOCATION'] = 'TOP'
                        ceiling.attr['NEXT-TO'] = other_space.name
                        ceiling.attr['POLYGON'] = ceiling_polygon_name
                        ceiling.attr['CONSTRUCTION'] = construction

    def create_zones(self):

        '''Creates zones under fake system'''

        system = System(self, '"Dummy System"')
        system.attr['TYPE'] = 'VAVS'
        system.attr['HEAT-SOURCE'] = 'NONE'
        system.attr['CHW-LOOP'] = '"DEFAULT-CHW"'

        for space in list(self.kinds('SPACE').values()):
            space.make_zone()

    def remove_vertical_interior_walls_for_spaces_with_no_windows(self):

        '''
        Remove interior walls where the plenum and associate zones for spaces
        with no exterior walls
        '''

        delete_i_walls = []
        for name, i_wall in list(self.kinds('INTERIOR-WALL').items()):

            if not i_wall.is_vertical():
                continue

            parent, next_to = i_wall.parents()

            windows = []
            for space in i_wall.parents():
                for e_wall in space.e_walls():
                    windows += e_wall.windows()

            if not windows:
                delete_i_walls.append(name)

        for name in delete_i_walls:
            self.objects[name].delete()

    def remove_vertical_interior_walls(self):

        '''Remove vertical interior walls'''

        delete_i_walls = []
        for name, i_wall in list(self.kinds('INTERIOR-WALL').items()):
            if i_wall.is_vertical():
                delete_i_walls.append(name)

        for name in delete_i_walls:
            self.objects[name].delete()

    def remove_plenum_for_spaces_with_no_exterior_walls(self, candidates=None):

        '''
        Remove plenum and associate zones for spaces with no
        exterior walls, then delete walls, roofs and floors
        recreate walls and recreate them. Walls must be created
        first, but they are removed and recreated in this process.
        '''

        if candidates is None:
            candidates = list(self.kinds('SPACE').values())

        # Mark deletes, adjust sibling space height
        delete_space_names = []
        delete_zone_names = []
        for space in candidates:
            if space.is_plenum() and len(space.e_walls()) == 0:
                delete_space_names.append(space.name)
                delete_zone_names.append(space.zone().name)
                adjust_space = self.objects[space.name.replace('_p', '')]
                adjust_space.attr['HEIGHT'] = adjust_space.height() + space.height()

        # Delete spcaes and zones
        for name in delete_space_names:
            self.objects[name].delete()
        for name in delete_zone_names:
            self.objects[name].delete()

        # Delete all walls and start over
        delete_names = []
        for kind in 'EXTERIOR-WALL', 'INTERIOR-WALL', 'UNDERGROUND-WALL':
            for name in self.kinds(kind):
                delete_names.append(name)
        for name in delete_names:
            self.objects[name].delete()

        # Recreate Walls
        self.make_walls()
        self.create_roofs()
        self.create_floors()
        self.create_ceilings()

    def nudge_windows(self, buffer=0, trim=False, leave_if_unfit=True):

        for window in list(self.kinds('WINDOW').values()):
            try:
                win_x = window.attr['X']
                win_y = window.attr['Y']
                win_w = window.attr['WIDTH']
                win_h = window.attr['HEIGHT']
            except IndexError:
                continue

            wall = window.parent

            wall_x = float(wall.x())
            wall_y = float(wall.y())
            wall_w = float(wall.width())
            wall_h = float(wall.height())

            if win_h + 2 * buffer > wall_h and leave_if_unfit:
                continue

            # TODO - consider undoing this
            if win_w + 2 * buffer > wall_w:
                print(('Cannot fit window %s' % window.name))
                window.attr['X'] = round(buffer, 2)
                if trim:
                    window.attr['WIDTH'] = wall_w - 2 * buffer
            elif win_w / wall_w > 0.9:
                window.attr['X'] = (wall_w - win_w) / 2
            elif win_x < 0:
                window.attr['X'] = round(buffer, 2)
            elif win_x + win_w + buffer > wall_w:
                window.attr['X'] = round(wall_w - win_w - buffer, 2)

            if win_h + 2 * buffer > wall_h:
                print(('Cannot fit window %s' % window.name))
                window.attr['Y'] = round(buffer, 2)
                if trim:
                    window.attr['HEIGHT'] = wall_h - 2 * buffer

            elif win_y < 0:
                window.attr['Y'] = round(buffer, 2)
            elif win_y + win_h + buffer > wall_h:
                window.attr['Y'] = round(wall_h - win_h - buffer, 2)

    def center_windows(self):
        for window in self.kinds('WINDOW').values():
            wall = window.parent

            factor = window.width() * window.height() / \
                     wall.width() * wall.height()
            if factor > 0.5 and len(wall.windows()) == 1:
                print('Centering %s' % window.name)
                window.attr['X'] = (wall.width() - window.width()) / 2
                window.attr['Y'] =(wall.height() - window.height()) / 2

    def add_daylighting(self, depth=10, spaces=None):

        print(spaces)

        if spaces is None:
            spaces = self.kinds('SPACE').values()

        for space in spaces:
            windows = defaultdict(int)

            if space.is_plenum():
                continue

            for e_wall in space.e_walls():
                if e_wall.tilt() != 90:
                    continue
                for window in e_wall.windows():
                    windows[e_wall] += window.area()

            if not windows:
                continue

            _, wall = sorted([(v, k) for k, v in list(windows.items())])[-1]
            p1, p2 = wall.get_vertices()
            mx, my = e_math.midpoint(p1, p2)
            angle = e_math.get_angle(p1, p2, True)
            offset_radians = math.radians((e_math.get_angle(p1, p2, True) + 90) % 360)
            y = depth * math.sin(offset_radians) + my
            x = depth * math.cos(offset_radians) + mx
            space.attr['DAYLIGHTING'] = 'YES'
            space.attr['LIGHT-REF-POINT1'] = ( x, y)
            space.attr['VIEW-AZIMUTH'] = e_math.swap_angle(angle)


class Default(object):

    def __init__(self, b, kind, type=None):
        self.b = b
        self.key = ((kind, type))
        b.defaults[self.key] = self
        self.attr = OrderedDict()

    @property
    def kind(self):
        return self.key[0]

    @property
    def type(self):
        return self.key[1]

    def read(self, lines):

        for line in lines[1:]:
            if '=' in line:
                n, v = re.split("\s*=\s*", line, maxsplit=1)
            else:
                n, v = line, None
            self.attr[n] = v

    def write(self):

        t = 'SET-DEFAULT FOR %s\n' % self.kind

        for k, v in list(self.attr.items()):
            a = '   '
            if v != None:
                a += k + ' = ' + str(v)
            else:
                a = '   ' + k
            t += utils.splitter(a, 65) + '\n'

        t += '   ..\n'
        return t

    def delete(self):
        del self.b.defaults[self.key]
        del self


class Parameter(object):
    def __init__(self, b, name=None, kind=None, parent=None):
        self.b = b
        self.name = name
        self.b.parameters[name] = self

    def read(self, lines):
        self.name, self.value = [t.strip() for t in lines[1].split('=')]
        self.b.parameters[self.name] = self

    def load(self, name, value):
        self.name = name
        self.value = value
        self.b.parameters[self.name] = self

    def write(self):
        return 'PARAMETER\n  %s = %s\n  ..\n' % (self.name, self.value)

    def delete(self):
        del self.b.parameters[self.name]
        del self


class Object(object):

    def __init__(self, b, name=None, kind=None, parent=None):
        self.b = b
        b.objects[name] = self
        if kind != 'POLYGON':
            self.attr = OrderedDict()
        self.kind = kind
        self.name = name
        self.parent=parent
        self.children = []

        if self.parent:
            self.parent.children.append(self)

        if name==kind:
            self.has_name = False
        else:
            self.has_name = True

    def delete(self):
        for child in self.children:
            child.delete()
        if self.parent:
            self.parent.children.remove(self)
        del self.b.objects[self.name]
        del self

    def read(self, lines):

        for line in lines[1:]:
            if '=' in line:
                n, v = re.split("\s*=\s*", line, maxsplit=1)
            else:
                n, v = line, None
            self.attr[n] = v

    def adopt(self, child):
        '''move from one parent to another'''
        child.parent.children.remove(child)
        child.parent = self
        self.children.append(child)

    def inherit(self, other):
        for name, value in list(other.attr.items()):
            self.attr[name] = value

    def write(self):

        t = ''
        if not self.has_name:
            t += self.kind + '\n'
        else:
            t += self.name + ' = ' + self.kind + '\n'

        for k, v in list(self.attr.items()):
            a = '   '
            if v != None:
                a += k + ' = ' + str(v)
            else:
                a = '   ' + k
            t += utils.splitter(a, 65) + '\n'

        t += '   ..\n'

        for child in sorted(self.children, key=operator.attrgetter('name')):
            t += child.write()

        return t

    def get(self, attr):

        # if defined explicitly
        if attr in self.attr:
            value = self.attr[attr]
            if attr in ref.numeric:
                return float(value)
            else:
                return value

        # if defined in defaults
        type = self.attr['type'] if 'type' in self.attr else None
        kind_type = (self.kind, type)
        if kind_type in self.b.defaults:
            if attr in self.b.defaults[kind_type].attr:
                return self.b.defaults[kind_type].attr[attr]

        # if implict default
        if attr in ref.numeric:
            return 0
        else:
            return None

    def set(self, name, value):
        self.attr[name] = value

    def filter(self, attr, min=None, max=None, l=None, like=None):
        if l and self.attr[attr] in l:
            return True
        elif like and like in self.attr[attr]:
            return True
        elif min != None and float(self.attr[attr]) < min:
            return False
        elif max != None and float(self.attr[attr]) > max:
            return False
        else:
            return True

    def siblings(self):
        return [o for o in list(self.b.kinds(self.kind).values())
            if o.parent==self.parent]




class Polygon(Object):

    def __init__ (self, b, name=None, kind='POLYGON', vertices=None):
        self.b = b
        self.vertices = vertices or []
        if vertices:
            self.regenerate()
        else:
            self.shapely_poly = None
        Object.__init__(self, b, name, kind)
        if self.vertices:
            self.regenerate()

    @property
    def attr(self):
        '''attr not stored for Polygons. Data stored in self.vertices
        instead.  Attrs are are created on the fly as needed'''

        attr = OrderedDict()
        for i, (x, y) in enumerate(self.vertices, start=1):
            attr['V%s' % i] = '( %s, %s )' % (x, y)
        return attr

    def regenerate(self):
        self.shapely_poly = ShapelyPoly(self.vertices)

        self.lines = []
        for ps in self.sequential_vertices_list():
            line = LineString(ps)
            line.p1, line.p2 = [Point(p) for p in ps]
            self.lines.append(line)
        self.points = [Point(p) for p in self.vertices]

    def set_vertices(self, vertices):
        if isinstance(vertices, ShapelyPoly):
            self.vertices = list(vertices.exterior.coords)[:-1]
        else:
            self.vertices = vertices
        self.regenerate()

    def shift(self, count):
        if count < 0:
            for _ in range(-count):
                self.set_vertices(self.vertices[1:] + self.vertices[:1])
        else:
            for _ in range(count):
                self.set_vertices(self.vertices[-1:] + self.vertices[:-1])

    def rotate(self, degrees):
        self.set_vertices(
            [e_math.rotate(p[0], p[1], degrees) for p in self.vertices])
        self.regenerate()

    def rotate_in_place(self, degrees):
        self.set_vertices(affinity.rotate(self.shapely_poly, degrees))

    def flip_horizontal(self):
        self.set_vertices([(-p[0], p[1]) for p in self.vertices])
        self.reverse()

    def delete_verticy(self, v):
        self.vertices.pop(v-1)
        self.regenerate()

    def add_verticy(self, point, verticy):
        if isinstance(point, Point):
            point = point.x, point.y
        self.vertices.insert(verticy+1, point)
        self.regenerate()

    def set_verticy(self, point, verticy):
        if isinstance(point, Point):
            point = point.x, point.y
        self.vertices[verticy] = point
        self.regenerate()

    def read(self, lines):
        self.vertices = []

        for line in lines[1:]:
            if '=' in line:
                n, v = [s.strip() for s in  line.split('=')]
            else:
                n, v = line, None
            x, y = v[1:-1].split(',')
            self.vertices.append([float(x),float(y)])
        self.regenerate()

    def area(self):
        return self.shapely_poly.area

    def perimeter(self):
        return self.shapely_poly.length

    def delete_sequential_dupes(self, tol=0.1):

        # Remove sequential dupes
        temp = []
        for pair in self.sequential_vertices_list():
            if e_math.distance(*pair) > tol:
                temp.append(pair[0])

        # Remove branched dupes
        skips = []
        if len(temp) > 4:
            for i in range(len(temp)):
                pair = self.vertices[i], self.vertices[(i+2)%(len(self.vertices))]
                if e_math.distance(*pair) < tol:
                    skips.append(i+1)
                    skips.append(i+2)

            final = []
            for i in range(len(temp)):
                if i not in skips:
                    final.append(temp[i])
        else:
            final = temp

        if len(final) < 3:
            raise RegenerateError('Cannot Regenerate Polygon')

        self.set_vertices(final)

    def get_vertices(self, v):
        vertices = self.vertices + [self.vertices[0]]
        return vertices[v-1:v+1]

    def sequential_vertices_list(self):
        return [(self.vertices[i], self.vertices[(i+1)%(len(self.vertices))])
            for i in range(len(self.vertices))]

    def gapped_vertices_list(self):
        return [(self.vertices[i], self.vertices[(i+2)%(len(self.vertices) + 1)])
            for i in range(len(self.vertices))]

    def is_ccw(self):
        return self.shapely_poly.exterior.is_ccw

    def mirror(self):
        self.set_vertices([[y, x] for x, y in self.vertices])

    def reverse(self):
        self.set_vertices(list(reversed(self.vertices)))

    def mirror_and_reverse(self):
        self.set_vertices([[y, x] for x, y in reversed(self.vertices)])

    def move(self, x, y):
        self.set_vertices([[x + px, y + py] for px, py in self.vertices])

class Floor(Object):

    def __init__ (self, b, name=None, kind='FLOOR'):

        Object.__init__(self, b, name, kind)

    def x(self):
        return self.get('X')

    def y(self):
        return self.get('Y')

    def z(self):
        return self.get('Z')

    def x_global(self):
        return self.x()

    def y_global(self):
        return self.x()

    @property
    def z_global(self):
        return self.z()

    def plenum_height(self):
        return self.attr.get('FLOOR-HEIGHT') - self.attr.get('SPACE-HEIGHT')

    def height(self):
        return self.attr.get('FLOOR-HEIGHT')

    def has_plenum(self):
        return (self.plenum_height > 0)

    def spaces(self):
        return [space for space in list(self.b.kinds('SPACE').values())
            if space.parent==self]

    def duplicate(self, name, z):

        '''Duplicates Floor and all child elements, with new z and name'''

        old_replace = '"' + unwrap(self.name) + '-'
        new_replace = '"' + unwrap(name) + '-'
        new_floor = Floor(self.b, name=name, kind='FLOOR')
        new_floor.inherit(self)
        new_floor.attr['Z'] = z
        for space in self.children:
            new_space_name = space.name.replace(old_replace, new_replace)
            new_space = Space(self.b, new_space_name, 'SPACE', parent=new_floor)
            new_space.inherit(space)
            new_space.make_zone()
            for wall in space.children:
                new_wall_name = wall.name.replace(old_replace, new_replace)
                if wall.kind == 'EXTERIOR-WALL':
                    new_wall = E_Wall(self.b, new_wall_name, 'EXTERIOR-WALL', parent=new_space)
                elif wall.kind == 'INTERIOR-WALL':
                    new_wall = I_Wall(self.b, new_wall_name, 'INTERIOR-WALL', parent=new_space)
                elif wall.kind == 'UNDERGROUND-WALL':
                    new_wall = U_Wall(self.b, new_wall_name, 'UNDERGROUND-WALL', parent=new_space)
                new_wall.inherit(wall)
                if 'NEXT-TO' in new_wall.attr:
                     new_wall.attr['NEXT-TO'] = new_wall.attr['NEXT-TO'].replace(old_replace, new_replace)
                for wall_element in wall.children:
                    new_wall_element_name = wall_element.name.replace(old_replace, new_replace)
                    if wall_element.kind == 'WINDOW':
                        new_wall_element = Window(self.b, new_wall_element_name, 'WINDOW', parent=new_wall)
                    elif wall_element.kind == 'DOOR':
                        new_wall_element = Door(self.b, new_wall_element_name, 'DOOR', parent=new_wall)
                    new_wall_element.inherit(wall_element)

        return new_floor

class Space(Object):

    def __init__ (self, b, name=None, kind='SPACE', parent=None):

        Object.__init__(self, b, name, kind, parent)

    @classmethod
    def vertically_ordered(cls, space1, space2):
        if space1.z_global <= space2.z_global:
            return space1, space2
        else:
            return space2, space1

    def x(self):
        return self.get('X')

    def y(self):
        return self.get('Y')

    def z(self):
        if 'Z' in self.attr:
            return float(self.attr['Z'])
        elif self.is_plenum():
            return self.parent.get('SPACE-HEIGHT')
        else:
            return self.get('Z')

    def x_global(self):
        return self.parent.x() + self.x()

    def y_global(self):
        return self.parent.y() + self.y()

    @property
    def z_global(self):
        return self.parent.z() + self.z()

    def height(self):
        if 'HEIGHT' in self.attr:
            return float(self.attr['HEIGHT'])
        elif self.is_plenum():
            return self.parent.get('FLOOR-HEIGHT') - self.parent.get('SPACE-HEIGHT')
        else:
            return self.parent.get('SPACE-HEIGHT')

    def is_plenum(self):
        return self.get('ZONE-TYPE') == 'PLENUM'

    @property
    def polygon(self):
        return self.b.objects[self.attr['POLYGON']]

    @property
    def shapely_poly(self):
        return self.polygon.shapely_poly

    def lines(self):
        return self.polygon.lines

    def points(self):
        return self.polygon.points

    def count_vertices(self):
        return len(self.vertices())

    def vertices(self):
        return self.polygon.vertices

    def point_pair_shapely(self, verticy):
        return (self.polygon.points[verticy-1],
                self.polygon.points[verticy%self.count_vertices()])

    def all_i_walls(self): # include ones for which this is the other space
        return self.i_walls() + self.i_walls_via_next_to()

    def i_walls_via_next_to(self):
        return [i_wall for i_wall in list(self.b.kinds('INTERIOR-WALL').values())
            if i_wall.next_to().name == self.name]

    def i_walls(self):
        return [wall for wall in self.children if wall.kind == 'INTERIOR-WALL']

    def e_walls(self):
        return [wall for wall in self.children if wall.kind == 'EXTERIOR-WALL']

    def u_walls(self):
        return [wall for wall in self.children if wall.kind == 'UNDERGROUND-WALL']

    def find_next_wall_name(self, kind="E"):
        space_name = self.name[1:-1]
        c = 1
        k = '"%s-%s%s"' % (space_name, kind, c)
        while k in self.b.objects:
            c = c + 1
            k = '"%s-%s%s"' % (space_name, kind, c)

        return k

    def extents(self):
        return self.z_global, self.z_global + self.height()

    def vertical_overlap(self, other):
        z_min, z_max = self.overlap_heights(other)
        return z_max - z_min

    def overlap_heights(self, other):
        l1 = self.z_global
        u1 = l1 + self.height()
        l2 = other.z_global
        u2 = l2 + other.height()
        z_max = min(u1, u2)
        z_min = max(l1, l2)
        return z_min, z_max

    def adjacent(self):
        pass

    def zone(self):
        for zone in list(self.b.kinds('ZONE').values()):
            if zone.get('SPACE') == self.name:
                return zone

    def system(self):
        return self.zone().system()

    def name_parts(self):
        parts = unwrap(self.name).split('-')
        assert len(parts) == 2
        return parts

    def make_zone(self, system=None):

        if system == None:
            system = self.b.objects['"Dummy System"']

        name = utils.suffix(self.name, ' ZONE')
        zone = Zone(self.b, name=name, parent=system)
        zone.attr['TYPE'] = self.get('ZONE-TYPE') or 'CONDITIONED'
        zone.attr['SPACE'] = self.name

    def has_windows(self):
        return any([e.has_windows() for e in self.e_walls()])

    def combine_vertical(self, other):

        deletes = [other.name, other.zone().name]

        # see if the other
        for i_wall in self.i_walls():
            if i_wall.next_to().name == other.name:
                deletes.append(i_wall.name)

        for wall in other.e_walls() + other.u_walls() + other.i_walls():

            if wall.attr.get('NEXT-TO') == self.name:
                deletes.append(wall.name)
                continue

            z = wall.z_global - self.z_global
            if wall.is_vertical():
                x = wall.x()
                y = wall.y()
                height = wall.height()
                width = wall.width()
                angle = wall.angle()
            else:
                polygon_name = wall.polygon().name

            self.adopt(wall)

            wall.attr['Z'] = z
            if wall.is_vertical():
                wall.attr['X'] = x
                wall.attr['Y'] = y
                wall.attr['HEIGHT'] = height
                wall.attr['WIDTH'] = width
                wall.attr['AZIMUTH'] = angle
                wall.attr.pop('LOCATION')
            else:
                wall.attr['POLYGON'] = polygon_name

        for name in deletes:
            print(('deleting ' + name))
            self.b.objects[name].delete()


class Wall(Object):

    def __init__ (self, b, name, kind, parent):

        Object.__init__(self, b, name, kind, parent)

    def windows(self, windows):
        return [window for window in self.b.objects['WINDOW']
            if window.parent.name == self.name]

    def doors(self, doors):
        return [door for door in self.b.objects['DOOR']
            if door.parent.name == self.name]

    def x(self):
        if 'X' in self.attr:
            return float(self.attr['X'])
        elif self.get_side_number():
            return self.get_vertices()[0][0]
        else:
            return self.get('X')

    def y(self):
        if 'Y' in self.attr:
            return float(self.attr['Y'])
        elif self.get_side_number():
            return self.get_vertices()[0][1]
        else:
            return self.get('Y')

    def z(self):
        if 'Z' in self.attr:
            return float(self.attr['Z'])
        elif self.get('LOCATION') == 'TOP':
            return self.parent.height()
        else:
            return self.get('Z')

    def special_horizontal(self):
        return self.get('LOCATION') in ['TOP', 'BOTTOM']

    def is_vertical(self):
        return self.tilt() == 90

    def x_global(self):
        return self.parent.x_global() + self.x()

    def y_global(self):
        return self.parent.y_global() + self.y()

    @property
    def z_global(self):
        return self.parent.z_global + self.z()

    def tilt(self):
        if self.get('TILT'):
            tilt = self.get('TILT')
        elif self.get('LOCATION') == 'TOP':
            tilt = 0
        elif self.get('LOCATION') == 'BOTTOM':
            tilt = 180
        else:
            tilt = 90
        return tilt

    def height(self):
        if self.get('POLYGON'):
            polygon = self.b.objects[self.get('POLYGON')]
            return max([y for x, y in polygon.vertices])
        elif self.special_horizontal():
            return None
        elif self.get('HEIGHT'):
            return self.get('HEIGHT')
        else:
            return self.parent.height()

    def width(self):
        if self.get('POLYGON'):
            polygon = self.b.objects[self.get('POLYGON')]
            return max([x for x, y in polygon.vertices])
        elif self.special_horizontal():
            return None
        elif self.get('WIDTH'):
            return self.get('WIDTH')
        else:
            return e_math.distance(*self.get_vertices())

    @property
    def shape(self):
        return self.get('SHAPE')

    def get_side_number(self):
        if 'LOCATION' in self.attr and 'SPACE-' in self.get('LOCATION'):
            return int(re.findall('(?<=SPACE-V)\d+', self.get('LOCATION'))[0])
        else:
            return None

    def is_regular_wall(self):
        return bool(self.get_side_number())

    def get_vertices(self):
        polygon = self.parent.polygon
        side_number = self.get_side_number()
        if side_number is not None:
            return polygon.get_vertices(side_number)
        else:
            x1, y1 = self.x(), self.y()
            angle = e_math.swap_angle(self.attr['AZIMUTH'])
            x2 = math.cos(math.radians(angle)) + x1
            y2 = math.sin(math.radians(angle)) + y1
            return [(x1, y1), (x2, y2)]

    def line(self):
        return self.parent.polygon.lines[self.get_side_number()-1]

    def area(self):
        if 'POLYGON' in self.attr:
            return self.b.objects[self.attr['POLYGON']].area()
        elif self.special_horizontal:
            return self.b.objects[self.parent.attr['POLYGON']].area()
        else:
            return self.width() * self.height()

    def zone_type(self):
        return self.parent.zone_type()

    def angle(self, cartesian=False):

        if self.tilt()%180 == 0:
            return None

        return e_math.get_angle(*self.get_vertices()[:2], cartesian=cartesian)

    def zone(self):
        return self.parent.zone()

    def near(self, point, tol):
        return e_math.line_distance(point, *self.get_vertices()) < tol

    def midpoint(self):
        p1, p2 = self.get_vertices()
        return ((p1[0] + p2[0]) / 2, ((p1[1] +p2[1]) / 2))

    def polygon(self):
        # This may not always return expected values for BOTTOM walls
        if 'POLYGON' in self.attr:
            return self.b.objects[self.attr['POLYGON']]
        elif self.special_horizontal:
            return self.b.objects[self.parent.attr['POLYGON']]

    def name_parts(self):
        parts = unwrap(self.name).split('-')
        assert len(parts) == 3
        return parts

    def planar_walls(self, tol_d, tol_a):

        '''All walls in same plane, given distance and angle tolerances'''

        def x_y_angle(wall):
            return list(wall.midpoint()) + [wall.angle(True)]

        walls = []

        x_base, y_base, angle_base = x_y_angle(self)

        for wall in list(self.b.kinds(self.kind).values()):
            if abs(self.tilt() - wall.tilt()) > 1:
                continue
            x_target, y_target, angle_target = x_y_angle(wall)
            diff_d = dist(x_base, y_base, angle_base, x_target, y_target)
            diff_a = angle_distance(angle_base, angle_target)
            if abs(diff_d) < tol_d and abs(diff_a) < tol_a:
                walls.append(wall)

        return walls


class E_Wall(Wall):

    def __init__ (self, b, name=None, kind='EXTERIOR-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)

    def clone(self, name):
        other = E_Wall(self.b, name, parent=self.parent)
        other.inherit(self)

    def create_window(self, name, x=0, y=0, height=None, width=None):
        height = height or self.height()
        width = width or self.width()
        window = Window(self.b, name, parent=self)
        for attr, value in [('X', x), ('Y', y), ('HEIGHT', height), ('WIDTH', width)]:
            window.attr[attr] = value
        return window

    def windows(self):
        return [window for window in self.b.objects['WINDOW']
            if window.parent.name == self.name]

    def doors(self):
        return [door for door in self.b.objects['DOOR']
            if door.parent.name == self.name]

    def to_uwall(self, split=None):

        def get_new_uwall_name():
            name_parts = self.name_parts()
            while 1:
                name_parts[2] = 'U' + name_parts[2][1:]
                for suffix in (' ' + ascii_lowercase):
                    name_parts[2] += suffix.strip()
                    name = '"%s"' % '-'.join(name_parts)
                    if not name in self.b.objects:
                        return name

        uwall = U_Wall(self.b, name=get_new_uwall_name(), parent=self.parent)
        for name, value in list(self.attr.items()):
            uwall.attr[name] = value

        # custom map construction chanage
        uwall.attr['CONSTRUCTION'] = get_client_construction()['underground']

        if split:
            self.attr['HEIGHT'] = self.height() - split
            uwall.attr['HEIGHT'] = split
            self.attr['Z'] = split
        else:
            self.delete()

    def to_uslab(self, delete=True):

        '''Like to_uwall, but for overhang|roof >> slab conversion'''

        uwall = U_Wall(self.b, name=self.name[:-1] + '_1"', parent=self.parent)
        for name, value in list(self.attr.items()):
            uwall.attr[name] = value
        uwall.attr['CONSTRUCTION'] = get_client_construction()['underground_slab']

        if delete:
            self.delete()

    def find_next_child_name(self, template):
        i = 1
        while True:
            name = wrap(unwrap(self.name) + template.format(number=i))
            if name in self.b.objects:
                i += 1
            else:
                return name

    def windows(self):
        return [c for c in self.children if c.kind=='WINDOW']

    def has_windows(self):
        return bool(self.windows())

    def chain(self, count):

        floor_ewalls = [ew for ew in list(self.b.kinds('EXTERIOR-WALL').values())
            if ew.parent.parent.name == self.parent.parent.name and ew.is_regular_wall()]

        chain = [self]
        i = 1

        for ewall in floor_ewalls:
            if ewall in chain:
                continue
            if ewall.get_vertices()[0] == chain[-1].get_vertices()[0]:
                i += 1
                chain.append(ewall)
        if i >= count:
            return chain

        flag = True
        while flag:
            if i >= count:
                break
            current = chain[-1]
            for ewall in floor_ewalls:
                if ewall in chain:
                    continue
                if distance(ewall.get_vertices()[0], current.get_vertices()[1]) < 0.1:
                    chain.append(ewall)
                    i += 1
        return chain


class U_Wall(Wall):

    def __init__ (self, b, name=None, kind='UNDERGROUND-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)

    def to_ewall(self, split=None):

        def get_new_ewall_name():
            name_parts = self.name_parts()
            while 1:
                name_parts[2] = 'E' + name_parts[2][1:]
                for suffix in ' ' + ascii_lowercase:
                    name_parts[2] += suffix.strip()
                    name = '"%s"' % '-'.join(name_parts)
                    if not name in self.b.objects:
                        return name

        ewall = E_Wall(self.b, name=get_new_ewall_name(), parent=self.parent)
        for name, value in list(self.attr.items()):
            ewall.attr[name] = value

        # custom map construction chanage
        ewall.attr['CONSTRUCTION'] = get_client_construction()['exterior']

        if split:
            ewall.attr['HEIGHT'] = self.height() - split
            self.attr['HEIGHT'] = split
            ewall.attr['Z'] = split
        else:
            self.delete()

    #TODO - combine
    def chain(self, count):

        floor_uwalls = [uw for uw in self.b.kinds('UNDERGROUND-WALL').values()
            if uw.parent.parent.name == self.parent.parent.name and uw.is_regular_wall()]

        chain = [self]
        i = 1

        for uwall in floor_uwalls:
            if uwall in chain:
                continue
            if uwall.get_vertices()[0] == chain[-1].get_vertices()[0]:
                i += 1
                chain.append(uwall)
        if i >= count:
            return chain

        flag = True
        while flag:
            if i >= count:
                break
            current = chain[-1]
            for uwall in floor_uwalls:
                if uwall in chain:
                    continue
                if distance(uwall.get_vertices()[0], current.get_vertices()[1]) < 0.1:
                    chain.append(uwall)
                    i += 1
        return chain


class I_Wall(Wall):

    def __init__(self, b, name=None, kind='INTERIOR-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)

    def next_to(self):
        return self.b.kinds('SPACE')[self.get('NEXT-TO')]

    def parents(self):
        return [self.parent, self.next_to()]


class Wall_Object(Object):

    def __init__ (self, b, name, kind, parent):

        Object.__init__(self, b, name, kind, parent)

    def x(self):
        return self.get('X')

    def y(self):
        return self.get('Y')

    def width(self):
        return self.get('WIDTH')

    def height(self):
        return self.get('HEIGHT')

    def x2(self):
        return self.x() + self.width()

    def y2(self):
        return self.y() + self.height()

    def center(self):
        return((self.x() + self.width()/2, self.y() + self.height()/2))

    def within(self, other):
        x, y = self.center()
        return other.x() < x < other.x2() and other.y() < y < other.y2()

    def x_global(self):
        pass #TODO - make this as needed
        return

    def y_global(self):
        pass #TODO - make this as needed

    @property
    def z_global(self):

        wall_z = self.parent.z_global
        object_z = self.y() * math.sin(math.radians(self.parent.tilt))
        return wall_z + object_z

    def area(self):
        return self.width() * self.height()

    def tilt(self):
        return self.parent.tilt()

    def angle(self):
        return self.parent.angle()

    def move(self, x=0, y=0):
        self.attr['X'] = self.get('X') + x
        self.attr['Y'] = self.get('Y') + y

    def zone(self):
        return self.parent.zone()


class Window(Wall_Object):

    def __init__ (self, b, name=None, kind='WINDOW', parent=None):

        Wall_Object.__init__(self, b, name, kind, parent)

    def reduce(self, factor):

        # scale window to percent vision
        x, y, w, h = e_math.scale_move_rectangle(
            self.attr['X'],
            self.attr['Y'],
            self.attr['WIDTH'],
            self.attr['HEIGHT'],
            factor)

        for attr, value in [('X', x), ('Y', y), ('WIDTH', w), ('HEIGHT', h)]:
            self.attr[attr] = value

    def area(self):
        return round(float(self.attr['WIDTH']) * float(self.attr['HEIGHT']), 2)

    def frame_width(self):
        return self.get('FRAME-WIDTH')


class Door(Wall_Object):

    def __init__ (self, b, name=None, kind='DOOR', parent=None):

        Wall_Object.__init__(self, b, name, kind, parent)


class System(Object):

    def __init__ (self, b, name=None, kind='SYSTEM', parent=None):

        Object.__init__(self, b, name, kind)


class Zone(Object):

    def __init__ (self, b, name=None, kind='ZONE', parent=None):

        Object.__init__(self, b, name, kind, parent)

    def space(self):
        return self.attr('SPACE')

    def system(self):
        return self.parent

class Comparison():

    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, b1, b2):

        self.b1 = b1
        self.b2 = b2
        self.object_keys = list(set(list(b1.objects.keys()) + list(b2.objects.keys())))
        self.object_keys_common = list(set(b1.objects.keys()) & set(b2.objects.keys()))

        self.default_keys = list(set(list(b1.defaults.keys()) + list(b2.defaults.keys())))
        self.default_keys_common = list(set(b1.defaults.keys()) & set(b2.defaults.keys()))

        self.messages = []

    def conflicts(self):

        conflicts =[]

        for object_key in self.object_keys_common:
            b1_attrs = self.b1.get_object_attr(object_key)
            b2_attrs = self.b2.get_object_attr(object_key)
            for attr_key in list(set(b1_attrs.keys()) & set(b2_attrs.keys())):
                if b1_attrs[attr_key] != b2_attrs[attr_key]:
                    conflicts.append((object_key, attr_key))

        for default_key in self.default_keys_common:
            b1_attrs = self.b1.get_default_attr(default_key)
            b2_attrs = self.b2.get_default_attr(default_key)
            for attr_key in list(set(b1_attrs.keys()) & set(b2_attrs.keys())):
                if b1_attrs[attr_key] != b2_attrs[attr_key]:
                    conflicts.append((default_key, attr_key))

        return conflicts

    def combine(self, resolve=None):

        messages = []
        if self.conflicts() and not resolve:
            return None

        if resolve == Comparison.RIGHT:
            base = copy.deepcopy(self.b1)
            overwrite = self.b2
        else:
            base = copy.deepcopy(self.b2)
            overwrite = self.b1

        for name, object in list(overwrite.objects.items()):
            if not name in base.objects:
                base.objects[name] = object
            else:
                base.objects[name].attr.update(object.attr)

        for key, default in list(overwrite.defaults.items()):
            if not key in base.defaults:
                base.defaults[key] = default
            else:
                base.defaults[key].attr.update(default.attr)

        return base

def split_roof(roof, points, combine_tolerance=0.5):


    '''
    Splits a roof along a line made up of points. Points are aligned
    to a point in the polygon if they are within the tolerance. No action
    is taken if the line does not fully instersect the roof. New
    roofs are created and the old roof is deleted.
    '''

    # Get next unique name for roof and polyogn
    def get_new_names():
        i = 1
        while True:
            wall_name = utils.suffix(space.name, '-Roof_%s' % i)
            poly_name = utils.suffix(space.name, '-Roof_%s_poly' % i)
            if wall_name not in b.objects and poly_name not in b.objects:
                break
            i += 1

        return wall_name, poly_name

    # Define objects
    b = roof.b
    space = roof.parent
    shapely_poly = roof.polygon().shapely_poly

    # Combine points with known polygon point if within tolerance
    adjusted_points = []
    for point in points:
        for point_poly in shapely_poly.exterior.coords:
            dist = Point(point_poly).distance(Point(point))
            if dist < combine_tolerance:
                adjusted_points.append(point_poly)
                break
        else:
            adjusted_points.append(point)

    # Split polygon
    split = shapely_split(shapely_poly, LineString(adjusted_points))
    if len(split) == 1:
        print(('No split occured for %s' % roof.name))
        return

    print(('Split %s into %s' % (roof.name, len(split))))

    # Create new objects
    for polygon_new in split:
        wall_name, poly_name = get_new_names()

        # Make new polygon
        polygon = Polygon(b, name=poly_name)
        polygon.set_vertices(list(polygon_new.exterior.coords))
        polygon.delete_sequential_dupes()
        if not polygon.is_ccw():
            polygon.reverse()

        # Make new roof
        wall = E_Wall(b, name=wall_name, parent=roof.parent)
        wall.inherit(roof)
        wall.attr['POLYGON'] = poly_name

    # Delete old
    roof.delete()

def sloped_roof(roof, base_point, other_point):

    '''
    Convert existing roofs to sloped roofs. Use a base point
    and reference point to define the plane, and the existing
    roof will be converted. It's helpful to first split the roofs
    using the split roof function above, then use the split line
    endpoints and the polygon centroid, alond with the shapely
    counter clockwise function to determine all of the roofs on
    either side of the split.

    See Gardner Elementary for an example
    '''

    def angle(p1, p2):
        x1 = float(p1[0])
        y1 = float(p1[1])
        x2 = float(p2[0])
        y2 = float(p2[1])

        if abs(x2-x1) > abs(y2-y1):
            baseAngle = math.degrees(math.atan(abs((y2-y1)/(x2-x1))))
        else:
            baseAngle = 90 - math.degrees(math.atan(abs((x2-x1)/(y2-y1))))

        if (x2 > x1):
            if (y2 > y1):
                a = baseAngle
            else:
                a = 360 - baseAngle
        else:
            if (y2 > y1):
                a = 180 - baseAngle
            else:
                a = 180 + baseAngle
        return(a)

    def translate(x1, y1, z1, x2, y2, z2, x, y): # translates x,y coordinate system to new vector (for roofs)

        x1 = float(x1)
        y1 = float(y1)
        z1 = float(z1)
        x2 = float(x2)
        y2 = float(y2)
        z2 = float(z2)
        x = float(x)
        y = float(y)

        va = angle((x1, y1), (x2, y2))               # vector angle
        pa = angle((x1, y1), (x, y))           # point angle
        da = 90 - (va - pa)                      # translated angle

        pd = e_math.distance([x1, y1], [x, y])     # point distance
        vd = e_math.distance([x1, y1], [x2, y2])   # vector distance

        za = math.degrees(math.atan((z2-z1)/vd)) # translated angle

        xt = math.cos(math.radians(da)) * pd
        yt = math.sin(math.radians(da)) * pd / math.cos(math.radians(za))
        zt = z1 + (yt/vd) * (z2 - z1)
        t = math.degrees(math.atan((z2-z1)/vd))
        a = angle((x1,y1),(x2,y2)) - 90

        return xt, yt, zt, t, (180-a)%360

    polygon = roof.polygon()

    x1, y1, z1 = base_point
    x2, y2, z2 = other_point

    new_vertices = []
    for v in polygon.vertices:
        x,y,z,t,az = translate(x1, y1, z1, x2, y2, z2, v[0], v[1])
        new_vertices.append([x,y])

    name = utils.rewrap(roof.name, '_poly')
    new_polygon=Polygon(roof.b, name=name, vertices=new_vertices)

    roof.attr['X'] = x1
    roof.attr['Y'] = y1
    roof.attr['Z'] = float(z1) - roof.parent.z_global
    roof.attr['AZIMUTH'] = az
    roof.attr['TILT'] = t
    roof.attr['POLYGON'] = new_polygon.name

def sloped_wall(wall, base_point, other_point):
    pass

def merge(base, other):

    for name, object in list(other.objects.items()):
        if not name in base.objects:
            base.objects[name] = object

    for key, default in list(other.defaults.items()):
        if not key in base.defaults:
            base.defaults[key] = default

def identify_candidate_adjacent_walls():

    # Identify candidate adjacent wall pairs
    wall_pairs = []
    bad_wall_pairs = []
    for space, other_space in b1.space_pairs():
        for i, line in enumerate(space.lines(), 1):
            if line.distance(other_space.shapely_poly) > 1:
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

    print(('discovered %s wall_pairs' % len(wall_pairs)))
    print(('discovered %s bad_wall_pairs' % len(bad_wall_pairs)))
    print(bad_wall_pairs)

if __name__ == '__main__':

    b1 = Building()
    b1.load(os.path.join('compare', 'b1.inp'))

    for object in b1.objects:
        print(object)
        for attr in object.attrs:
            print(attr)

    b2 = Building()
    b1.load(os.path.join('compare', 'b1.inp'))




    print("done")
    compare = Comparison(b1, b2)
    print(compare)
    #b1.dump('compare/test1.inp')
    #b2.dump('compare/test2.inp')
    #b3 = compare.combine(resolve=Comparison.LEFT)
    #b3.dump('compare/test3.inp')



