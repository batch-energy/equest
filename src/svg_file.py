import xml.etree.ElementTree as ET
from e_math import convert_feet
import shlex


class Svg_Page():

    def __init__(self, fn):

        self.scale_rect = None
        self.origins = []
        self.windows = []
        self.projections = []

        self.rects = []
        self.xml_rects = []

        self.xmlns = '{http://www.w3.org/2000/svg}'
        self.__read_xml(fn)
        self.__make_rects()

        if not self.scale_rect:
            print("No Scale")
        else:
            self.__assign_origins

        for origin in self.origins:
            projection_windows = []
            for window in self.windows:
                if origin.svg_rect.contains_center_of(window.svg_rect):
                    projection_windows.append(window)
            self.projections.append(Svg_Projection(origin, projection_windows))

    def __read_xml(self, fn):
        root = ET.parse(fn).getroot()
        for layer in root.findall(self.xmlns + 'g'):
            self.xml_rects += layer.findall(self.xmlns + 'rect')

    def __make_rects(self):

        for xml_rect in self.xml_rects:
            svg_rect = Svg_Rectangle(self, xml_rect)

            if 'scale' in str(svg_rect.title):
                if self.scale_rect:
                    print("Error: Multiple scales")
                else:
                    self.scale_rect = Svg_Scale(svg_rect)
                    self.scale = self.scale_rect.scale
            elif 'origin' in str(svg_rect.title):
                self.origins.append(Svg_Origin(svg_rect))
            else:
                self.windows.append(Svg_Window(svg_rect))

    def __assign_origins(self):
        return

        self.origin = self.origin_rect.x, self.origin_rect.y
        self.origin_scaled = tuple([(point * self.scale) for point in self.origin])

    def colors(self):
        return set([w.color for w in self.windows])

    def color_ids(self):
        return set([w.color_id() for w in self.windows])

    def titles(self):
        return set([w.title for w in self.windows])


class Svg_Projection():

    def __init__(self, origin, windows):

        self.origin = origin
        self.windows = windows
        self.walls = origin.walls
        scale = origin.svg_rect.svg_page.scale

        self.width = origin.svg_rect.width * scale
        self.height = origin.svg_rect.height * scale

        for window in windows:
            window.x = (window.svg_rect.x - origin.svg_rect.x) * scale
            window.y = (window.svg_rect.y - origin.svg_rect.y) * scale
            window.width = window.svg_rect.width * scale
            window.height = window.svg_rect.height * scale


class Svg_Rectangle():

    def __init__(self, svg_page, xml_rect):

        self.svg_page = svg_page
        self.xml_rect = xml_rect
        self.title = xml_rect.find(self.svg_page.xmlns + 'title')

        try:
            self.title = self.title.text
        except AttributeError:
            self.title = ''

        for key in ['width', 'height', 'x', 'y']:
            setattr(self, key, float(xml_rect.attrib[key]))

        self.y = - (self.y + self.height)
        self.id = xml_rect.attrib['id']

        if 'transform' in xml_rect.attrib:
            print('Error: Some elements tranformed, which disrupts parsing (%s / %s)' % (self.title, self.id))

        self.style = {}
        for kv in xml_rect.attrib['style'].split(';'):
            k, v = kv.split(':')
            self.style[k] = v

    def contains_center_of(self, other):
        x_bound = [self.x, self.x + self.width]
        y_bound = [self.y, self.y + self.height]

        return (x_bound[0] < other.center()[0] < x_bound[1] and
            y_bound[0] < other.center()[1] < y_bound[1])

    def center(self):
        return ((2 * self.x + self.width)/2, (2 * self.y + self.height)/2)

    def get(self, key):
        return self.xml_rect.attrib.get(key)

class Svg_Scale():

    def __init__(self, svg_rect):
        self.svg_rect = svg_rect
        scale_rect_label = convert_feet(svg_rect.title.split()[1])
        scale_rect_size = max(svg_rect.width, svg_rect.height)
        self.scale = scale_rect_label/scale_rect_size


class Svg_Origin():

    def __init__(self, svg_rect):

        self.svg_rect = svg_rect

        # Names with spaces need to be encludes with double quotes
        # Multiple walls can be space separated
        self.walls = shlex.split(svg_rect.title)[1:]

class Svg_Window():

    def __init__(self, svg_rect):

        self.svg_rect = svg_rect
        self.color = svg_rect.style['fill']
        self.opacity = svg_rect.style.get('opacity', None)
        self.title = svg_rect.title
        self.id = svg_rect.id

    def center(self):
        return (self.x + self.width/2), (self.y + self.height/2)

    def area(self):
        return self.width*self.height

    def get(self, key):
        return self.svg_rect.get(key)

    def color_id(self):
        return self.color + '-' + str(self.opacity)
if __name__ == '__main__':
    svg = Svg_Page('e1.svg')
    print(svg.colors())

