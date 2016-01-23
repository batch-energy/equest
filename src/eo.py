from collections import OrderedDict, namedtuple
import re, time, os, ref, e_math, math, utils
from shapely.geometry import Polygon as ShapelyPoly
from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString
import copy
from pprint import pprint as pp
from decimal import Decimal as Dec
import decimal
decimal.getcontext().prec = 4

class Filter(object):
    def __init__(self):
        attr = {}


class Building(object):
    def __init__(self):
        self.objects = OrderedDict()
        self.defaults = OrderedDict()
        self.parameters = OrderedDict()
        self.selected = []

    def load(self, fn):
        self.fn = fn
        with open(self.fn, 'r') as f:
            text = f.read()
        self.read(text)

    def read(self, text):
        text = self.clean_file(text)
        objects = self.split_objects(text)
        self.objectify(self.split_objects(text))

    def kinds(self, kind):
        '''OrderedDict of objects only of kind'''
        kinds = OrderedDict()
        for name, obj in self.objects.items():
            if obj.kind == kind:
                kinds[name] = obj
        return kinds

    def dump(self, fn=None, backup=False):

        fn = fn or self.fn

        if backup:
            if not os.path.exists('backup'):
                os.mkdir('backup')
            fn = os.path.join('backup', fn.replace(
                '.inp', time.strftime('_%y%m%d-%H%M%S.inp')))

        if os.path.exists(fn):
            os.remove(fn)

        t = ''
        defaults_written = []
        for kind in ref.kind_list:
            if kind == 'PARAMETER':
                for parameter in self.parameters.values():
                    t += parameter.write()
            for name, default in self.defaults.items():
                if ref.in_same_group(default.kind, kind):
                    if not default in defaults_written:
                        t += default.write()
                        defaults_written.append(default)

            if not kind in ref.parents.keys():
                for o in self.kinds(kind).values():
                    t += o.write()

        self.write(fn, t)

    def write(self, fn, t):
        with open(fn, 'w') as f:
            f.write(t)

    def clean_file(self, text):
        return '\n'.join([l.strip() for l in text.split('\n')
            if l.strip() and not l.strip()[0] == '$'])

    def split_objects(self, text):
        return [self.clean_object(o) for o in text.split('..')]

    def clean_object(self, object):
        lines = [l.strip() for l in object.split('\n') if l.strip()]
        if not lines:
            return ''

        new_lines = []
        new_line, attr_lines =  lines[0],lines[1:]

        for i, line in enumerate(attr_lines):
            if re.search(r' =($| )', line):
                new_lines.append(new_line)
                new_line = line
            else:
                new_line += ' ' + line

        new_lines.append(new_line)
        return '\n'.join(new_lines)

    def objectify(self, object_text_list):
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

            if kind in ref.parents.keys():
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
                o = Window(self, name, kind, parent=parent)
            elif kind == 'ZONE':
                o = Zone(self, name, kind, parent=parent)
            elif kind == 'POLYGON':
                o = Polygon(self, name, kind)
            else:
                o = Object(self, name, kind, parent=parent)
            o.read(lines)

            current_parent[kind] = o

    def select(self, name):
        self.objects[name].selected = True
        if not self.objects[name].selected:
            self.selected.append(name)

    def toggle(self, name):
        if self.objects[name].selected:
            self.selected.remove(name)
            self.objects[name].selected = False
        else:
            self.selected.append(name)
            self.objects[name].selected = True

    def deselect(self, name):
        if self.objects[name].selected:
            self.selected.remove(name)
        self.objects[name].selected = True

    def selected_by_kind(self, kind):
        return [name for name, object in self.kinds(kind).items() if object.selected]

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


    def space_pairs(self, tol=0.0001):
        '''returns a list of spaces pairs which are adjacent to one another'''
        spaces = self.kinds('SPACE').values()
        checked = []
    
        # Identify candidate adjacent space pairs
        horiz_space_pairs, vert_space_pairs = [], []
        for space in spaces:
            checked.append(space)
            for space2 in set(spaces) - set(checked):
                if (space.shapely_poly().distance(space2.shapely_poly())) > tol:
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

        for k, v in self.attr.items():
            a = '   '
            if v != None:
                a += k + ' = ' + str(v)
            else:
                a = '   ' + k
            t += utils.splitter(a, 65) + '\n'

        t += '   ..\n'
        return t


    def delete(self):
        del self


class Parameter(object):
    def __init__(self, b, name=None, kind=None, parent=None):
        self.b = b

    def read(self, lines):
        self.name, self.value = [t.strip() for t in lines[1].split('=')]
        self.b.parameters[self.name] = self

    def load(self, name, value):
        self.name = name
        self.value = value
        self.b.parameters[self.name] = self

    def write(self):
        return 'PARAMETER\n  %s = %s\n  ..\n' % (self.name, self.value)

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
        self.selected = False

        if self.parent:
            self.parent.children.append(self)

        if name==kind:
            self.has_name = False
        else:
            self.has_name = True

    def delete(self):
        if self.parent:
            self.parent.children.pop(self)
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

    def write(self):

        t = ''
        if not self.has_name:
            t += self.kind + '\n'
        else:
            t += self.name + ' = ' + self.kind + '\n'

        for k, v in self.attr.items():
            a = '   '
            if v != None:
                a += k + ' = ' + str(v)
            else:
                a = '   ' + k
            t += utils.splitter(a, 65) + '\n'

        t += '   ..\n'

        for child in self.children:
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
        return [o for o in self.b.kinds(self.kind).values()
            if o.parent==self.parent]

class Polygon(Object):

    def __init__ (self, b, name=None, kind='POLYGON'):
        self.b = b
        self.vertices = []
        self.shapely_poly = None
        Object.__init__(self, b, name, kind)

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
            self.vertices = list(shapely_polygon.exterior.coords)[:-1]
        else:
            self.vertices = vertices
        self.regenerate()

    def delete_verticy(self, v):
        self.vertices.pop(v+1)
        self.regenerate()

    def add_verticy(self, point, verticy):
        self.vertices.insert(verticy+1, point)
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

    def delete_sequential_dupes(self, tol=0.1):
        new = []
        count = len(self.vertices)
        for i in range(count):
            if e_math.distance(self.vertices[i], self.vertices[(i+1)%count]) > tol:
                new.append(self.vertices[i])
        self.vertices = new
        self.regenerate()

    def get_vertices(self, v):
        vertices = self.vertices + [self.vertices[0]]
        return vertices[v-1:v+1]

    def sequential_vertices_list(self):
        return [(self.vertices[i], self.vertices[(i+1)%(len(self.vertices))]) 
            for i in range(len(self.vertices))]

    def is_ccw(self):
        return self.shapely_poly.is_ccw()

    def mirror(self):
        self.vertices = ([[y, x] for x, y in self.vertices])
        self.regenerate()

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

    def z_global(self):
        return self.z()

    def plenum_height(self):
        return self.attr.get('FLOOR-HEIGHT') - self.attr.get('SPACE-HEIGHT')

    def has_plenum(self):
        return (self.plenum_height > 0)

    def delete(self):
        for space in self.children:
            space.delete()
        del self.b.objects[self.name]
        del self


class Space(Object):

    def __init__ (self, b, name=None, kind='SPACE', parent=None):

        Object.__init__(self, b, name, kind, parent)

    @classmethod
    def vertically_ordered(cls, space1, space2):
        if space1.z_global() <= space2.z_global():
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

    def all_i_walls(self): # include ones for which this is the other space
        return [i_wall for i_wall in self.b.objects['INTERIOR-WALL']
            if i_wall.parent.name == self.name or
            i_wall.get('NEXT-TO') == self.name]

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
        pass

    def delete(self):
        for wall in self.e_walls() + self.i_walls() + self.u_walls():
            wall.delete()
        del self

    def vertical_overlap(self, other):
        l1 = self.z_global()
        u1 = l1 + self.height()
        l2 = other.z_global()
        u2 = l2 + other.height()
        u = min(u1, u2)
        l = max(l1, l2)
        return u - l

    def adjacent(self):
        pass

    def zone(self):
        for zone in self.b.kinds('ZONE').values():
            if zone.get('SPACE') == self.name:
                return zone

    def system(self):
        return self.zone().system()


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
            return self.get_vertices()[0][0]
        else:
            return self.get('Y')

    def z(self):
        if 'Z' in self.attr:
            return float(self.attr['Z'])
        elif self.get('LOCATION') == 'TOP':
            return self.parent.get('Z')
        else:
            return self.get('Z')

    def special_horizontal(self):
        return self.get('LOCATION') in ['TOP', 'BOTTOM']

    def x_global(self):
        return self.parent.x_global() + self.x() 

    def y_global(self):
        return self.parent.y_global() + self.y() 

    def z_global(self):
        return self.parent.z_global() + self.z()

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
        if (self.get('POLYGON') or self.special_horizontal()):
            return None
        elif self.get('HEIGHT'):
            return self.get('HEIGHT')
        else:
            return self.parent.height()

    def width(self):
        if (self.get('POLYGON') or self.special_horizontal()):
            return None
        elif self.get('WIDTH'):
            return self.get('WIDTH')
        else:
            e_math.distance(self.get_vertices(self.get_vertices()))

    def get_side_number(self):
        if 'SPACE-' in self.get('LOCATION'):
            return int(re.findall('(?<=SPACE-V)\d+', self.get('LOCATION'))[0])
        else:
            return None

    def get_vertices(self):
        polygon = self.parent.polygon
        side_number = self.get_side_number()
        return polygon.get_vertices(side_number)

    def area(self):
        if self.shape == 'POLYGON':
            return self.b.objects[self.attr['POLYGON']].area()
        elif self.special_horizontal:
            return self.b.objects[self.parent.attr['POLYGON']].area()
        else:
            return self.width() * self.height()

    def zone_type(self):
        return self.parent.zone_type()

    def angle(self, kind='doe'):

        if self.tilt()%180 == 0:
            return None

        v1, v2 = self.get_vertices()[:2]
        angle = e_math.get_angle(*self.get_vertices()[:2], cartesian=False)
        if kind == 'doe':
            angle = e_math.swap_angle(angle)
        return angle

    def zone(self):
        return self.parent.zone()

    def delete(self):
        del self


class E_Wall(Wall):

    def __init__ (self, b, name=None, kind='EXTERIOR-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)


    def windows(self):
        return [window for window in self.b.objects['WINDOW']
            if window.parent.name == self.name]

    def doors(self):
        return [door for door in self.b.objects['DOOR']
            if door.parent.name == self.name]

    def delete(self):
        for item in self.windows() + self.doors():
            item.delete()
        del self


class U_Wall(Wall):

    def __init__ (self, b, name=None, kind='UNDERGROUND-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)


class I_Wall(Wall):

    def __init__ (self, b, name=None, kind='INTERIOR-WALL', parent=None):

        Wall.__init__(self, b, name, kind, parent)


class Wall_Object(Object):

    def __init__ (self, b, name, kind, parent):

        Object.__init__(self, b, name, kind, parent)

    def x(self):
        self.get('X')

    def y(self):
        self.get('Y')

    def x_global(self):
        pass #TODO - make this as needed
        return 

    def y_global(self):
        pass #TODO - make this as needed

    def z_global(self):

        wall_z = self.parent.z_global()
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
        self.object_keys = list(set(b1.objects.keys() + b2.objects.keys()))
        self.object_keys_common = list(set(b1.objects.keys()) & set(b2.objects.keys()))

        self.default_keys = list(set(b1.defaults.keys() + b2.defaults.keys()))
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

        for name, object in overwrite.objects.items():
            if not name in base.objects:
                base.objects[name] = object
            else:
                base.objects[name].attr.update(object.attr)

        for key, default in overwrite.defaults.items():
            if not key in base.defaults:
                base.defaults[key] = default
            else:
                base.defaults[key].attr.update(default.attr)

        return base

if __name__ == '__main__':

    b1 = Building()
    b1.load(os.path.join('compare', 'b1.inp'))

    spaces = b1.kinds('SPACE').values()
    checked = []

    
    # Identify candidate adjacent wall pairs
    wall_pairs = []
    bad_wall_pairs = []
    for space, other_space in b1.space_pairs():
        for i, line in enumerate(space.lines(), 1):
            if line.distance(other_space.shapely_poly()) > 1:
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
        
    print 'discovered %s wall_pairs' % len(wall_pairs)
    print 'discovered %s bad_wall_pairs' % len(bad_wall_pairs)
    print bad_wall_pairs

    print "done"
    #compare = Comparison(b1, b2)
    #b1.dump('compare/test1.inp')
    #b2.dump('compare/test2.inp')
    #b3 = compare.combine(resolve=Comparison.LEFT)
    #b3.dump('compare/test3.inp')



    