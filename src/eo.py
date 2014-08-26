from collections import OrderedDict
import re, time, os, ref, textwrap, e_math, math
from shapely.geometry import Polygon as Poly
from shapely.geometry import Point as Pt
from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString
import copy
from pprint import pprint as pp

class Filter(object):
    def __init__(self):
        attrs = {}


class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def str(self, round=2):
        pass


class Building(object):
    def __init__(self):
        self.objects = OrderedDict()
        self.selected = []

    def load(self, fn):
        self.fn = fn
        with open(self.fn, 'r') as f:
            text = f.read()
        self.read(text)

    def read(self, text):
        text = self.clean_file(text)
        self.objectify(self.split_objects(text))

    def kinds(self, kind):
        '''OrderedDict of objects only of kind'''
        kinds = copy.copy(self.objects)
        for k, v in sorted(kinds.items()):
            if v.kind != kind:
                del kinds[k]
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
        for kind in ref.kind_list:
            if not kind in ref.parents.keys():
                for o in self.kinds(kind).values():
                    t += o.write()
            default = self.objects.get('SET-DEFAULT FOR ' + kind)
            if default:
                t += default.write()
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
        new_line, new_lines = '', []
        opens, closes = 0 ,0
    
        for i, line in enumerate(lines):
            new_line += line
            opens += len(re.findall('[\{\(]', line))
            closes += len(re.findall('[\}\)]', line))
            if opens == closes and line[-1] != '=':
                new_lines.append(new_line)
                new_line = ''
    
        return '\n'.join(new_lines)
    
    def objectify(self, object_text_list):
        current_parent = {}
        for object_text in object_text_list:            
            lines = object_text.split('\n')
                        
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


class Object(object):

    def __init__(self, b, name=None, kind=None, parent=None):
        self.b = b
        b.objects[name] = self
        self.is_default = False
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
        if lines:
            if 'SET-DEFAULT FOR' in lines[0]:
                self.is_default = True

            for line in lines[1:]:
                if '=' in line:
                    n, v = re.split("\s*=\s*", line, maxsplit=1)
                else:
                    n, v = line, None
                self.attr[n] = v        

    def write(self):

        t = ''
        if self.is_default or not self.has_name:
            t += self.kind + '\n'        
        else:
            t += self.name + ' = ' + self.kind + '\n'

        for k, v in self.attr.items():
            a = '   '
            if v != None:
                a += k + ' = ' + str(v)
            else:
                a = '   ' + k 
            t += self.splitter(a) + '\n'

        t += '   ..\n'

        for child in self.children:
            t += child.write()

        return t

    def splitter(self, s):
        pad = ' '*9
        if s.count(',') > 1:
            # put items of comma separated list on separate lines
            text = '   ' + (',\n' + pad).join([i.strip() for i in s.split(',')])

        else:
            # otherwise, just make sure it's not more than 75 charaters
            wrapper = textwrap.TextWrapper(width=75, subsequent_indent=pad)
            text = '\n'.join(wrapper.wrap(s))

        return text
            
    def get(self, attr):
        if attr in self.attr:
            value = self.attr[attr]
            if attr in ref.numeric:
                return float(value)
            else:
                return value
        else:
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

        
class Polygon(Object):

    def __init__ (self, b, name=None, kind='POLYGON'):
        self.b = b
        self.vertices = []
        Object.__init__(self, b, name, kind)
        
    def delete_verticy(self, v):
        self.vertices.pop(v+1)
    
    def add_verticy(self, point, verticy):
        self.vertices.insert(verticy+1, point)
        
    def read(self, lines):
        self.vertices = []

        for line in lines[1:]:
            if '=' in line:
                n, v = [s.strip() for s in  line.split('=')]
            else:
                n, v = line, None
            self.attr[n] = v        
            x, y = v[1:-1].split(',')
            self.vertices.append([float(x),float(y)])

    def write(self):
        t = self.name + ' = ' + self.kind + '\n'

        for i, (x, y) in enumerate(self.vertices, start=1):  
            t += '   V%s = ( %s, %s )\n' % (i, x, y)
        t += '   ..\n'
        return t
        
    def area(self):
        p = Poly(self.vertices)
        return p.area

    def delete_sequential_dupes(self, tol=0.1):
        new = []
        count = len(self.vertices)
        for i in range(count):
            if e_math.distance(self.vertices[i], self.vertices[i%count]) > tol:
                new.append(self.vertices[i])
    
    def get_vertices(self, v):
        vertices = self.vertices + [self.vertices[0]]
        return vertices[v-1:v+1]


class Floor(Object):

    def __init__ (self, b, name=None, kind='FLOOR'):

        Object.__init__(self, b, name, kind)

    def x(self):
        return self.get('X')

    def y(self):
        return self.get('Y')

    def z(self):
        return self.get('Z')

    def delete(self):
        for space in self.children:
            space.delete()
        del self


class Space(Object):

    def __init__ (self, b, name=None, kind='SPACE', parent=None):

        Object.__init__(self, b, name, kind, parent)
    
    def z(self):
        if 'Z' in self.attr:
            return self.attr['Z']
        elif self.is_plenum():
            return self.parent.get('SPACE-HEIGHT')
        else:
            return self.get('Z')
    
    def x_global(self):
        return self.parent.x() + self.get('X')

    def y_global(self):
        return self.parent.y() + self.get('Y')

    def z_global(self):
        return self.parent.z() + self.z()

    def height(self):        
        if 'HEIGHT' in self.attr:
            return self.attr['HEIGHT']
        elif self.is_plenum():
            return self.parent.get('FLOOR-HEIGHT') - self.parent.get('SPACE-HEIGHT')
        else:
            return self.parent.get('SPACE-HEIGHT')
 
    def is_plenum(self):
        return self.get('ZONE-TYPE') == 'PLENUM'
        
    def polygon(self):
        return self.b.objects[self.get('POLYGON')]
    
    def count_vertices(self):
        return len(self.vertices())

    def vertices(self):
        return self.polygon().vertices

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
    
    def delete(self):
        for wall in self.e_walls() + self.i_walls() + self.u_walls():
            wall.delete()
        del self

    def overlap(self, other):
        l1 = self.z_global()
        u1 = l1 + self.height()
        l2 = other.z_global()
        u2 = l2 + other.height()
        u = min(u1, u2)
        l = max(l1, l2)
        ol = u - l
        return ol

    def zone(self):
        for zone in self.b.kinds('ZONE').values():
            if zone.get('SPACE') == self.name:
                return zone


class Wall(Object):

    def __init__ (self, b, name, kind, parent):

        Object.__init__(self, b, name, kind, parent)

    def windows(self, windows):
        return [window for window in self.b.objects['WINDOW']
            if window.parent.name == self.name]

    def doors(self, doors):
        return [window for window in self.b.objects['DOOR']
            if window.parent.name == self.name]
    
    
    def z(self):

        if 'Z' in self.attr:
            return self.attr['Z']
        elif self.get('LOCATION') == 'TOP':
            return self.parent.get('Z')
        else:
            return self.get('Z')

    def special_horizontal(self):
        return self.get('LOCATION') in ['TOP', 'BOTTOM']
    
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
        polygon = self.parent.polygon()
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
        angle = e_math.get_angle(*self.get_vertices()[:2])
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
        return self.parent.x() + self.get('X')

    def y(self):
        return self.parent.y() + self.get('Y')

    def z(self):
        return self.parent.z() + self.get('Z')

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

    def __init__ (self, b, name=None, kind=None):

        Object.__init__(self, b, name, kind)


class Zone(Object):

    def __init__ (self, b, name=None, kind='ZONE', parent=None):

        Object.__init__(self, b, name, kind, parent)

    