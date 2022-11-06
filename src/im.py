from collections import OrderedDict, Counter, defaultdict
import re
import sys
import os

from e_math import convert_feet, distance, is_close
import eo
import utils
import ref

import PyPDF2

def get_fdf_attribute(attr, line):
    for part in line.split('/'):
        name, _, value = part.partition(' ')
        if name == attr:
            return value.strip().lstrip('(').rstrip(')')


class Pdf_File(object):

    def __init__(self, pdf_path, attrs=None):

        self.pdf_path = pdf_path
        self.annotations = defaultdict(list)
        self.pages = OrderedDict()
        self.errors = []
        self.warnings = []

        self.__provided_attrs = attrs or {}

        self.__define_annotations()
        self.__build()
        self.__verify_specials()

        if self.errors:
            return

    def __define_annotations(self):

        '''Assign annotations from pdf'''

        input = PyPDF2.PdfFileReader(open(self.pdf_path, "rb"))

        for i in range(input.getNumPages()) :
            annots = input.getPage(i).get('/Annots', [])
            if not isinstance(annots, list):
                continue
            for annot in annots:
                self.annotations[i].append(annot.getObject())


    def __build(self):

        '''Build PDF File object from pdf annotations'''

        for page_number, annotations in list(self.annotations.items()):

            for annotation in annotations:

                if not page_number in self.pages:
                    # Make new page if page number is new
                    pdf_page = Pdf_Page()
                    self.pages[page_number] = pdf_page
                else:
                    # Use exsting if page number exists
                    pdf_page = self.pages[page_number]

                if annotation.get('/T', '').lower().startswith('origin'):
                    if pdf_page.origin is None:
                        pdf_page.origin = Pdf_Origin(annotation)
                    else:
                        self.errors.append('Page %s has multiple origins' % page_number)
                elif annotation.get('/T', '').lower().startswith('scale'):
                    if pdf_page.scale is None:
                        pdf_page.scale = Pdf_Scale(annotation)
                    else:
                        self.errors.append('Page %s has multiple scales' % page_number)
                elif annotation.get('/Subtype') == '/Polygon':
                    try:
                        polygon = Pdf_Polygon(annotation)
                        pdf_page.polygons.append(polygon)
                    except:
                        self.errors.append(f'Could not create polygon from annotation {annotation}')



    def __verify_specials(self):

        '''Verify contents of each page'''

        valid_poly_attrs = ['Z', 'H', 'HP', 'PH', 'X', 'Y', 'S']

        for name, page in list(self.pages.items()):

            # check spaces
            floors = defaultdict(list)
            space_names_set = set()
            for polygon in page.polygons:

                if not polygon.name.count('-') == 1:
                    self.errors.append('Space %s has wrong number of hyphens' % (polygon.name))

                if polygon.name in space_names_set:
                    orig_name = polygon.name
                    while polygon.name[-1].isdigit():
                        polygon.name= polygon.name[:-1]
                    i = 2
                    while polygon.name + str(i) in space_names_set:
                        i += 1
                    polygon.name = polygon.name + str(i)
                    self.warnings.append('Space %s renamed to %s' % (orig_name, polygon.name))

                space_names_set.add(polygon.name)
                # This controls the rules for determining the floor name
                if os.environ.get('USE_FIRST_CHARACTER_AS_FLOOR_GROPUING'):
                    # first character
                    floor_name = polygon.name[0]
                elif os.environ.get('USE_PAGE_NAME_AS_FLOOR_GROUPING'):
                    # use page number
                    floor_name = str(name)
                else:
                    # All charactors before the hyphen
                    floor_name = polygon.name.split('-')[0]

                floors[floor_name].append(polygon.name)

                for key in list(polygon.attrs.keys()):
                    if not key in valid_poly_attrs:
                        self.errors.append('Invalid attribute "%s" in %s' % (key, polygon.name))

            if not floors:
                #self.errors.append('Warning, no spaces on page %s' % name)
                continue

            max_polys = 0
            max_floor = None
            for name, polys in floors.items():
                if len(polys) > max_polys:
                    max_polys =len(polys)
                    max_floor = name

            floor_name = max_floor

            for name, poly in floors.items():
                if name != max_floor:
                    self.errors.append('Polygon(s) %s is in floor %s' % (', '.join(poly), max_floor))

            # assign floor name from dominent space
            page.name = floor_name

            if page.origin is None:
                self.errors.append('Page %s has no origin' % (page.name))
                continue

            for key in page.origin.attrs:
                if not key in valid_poly_attrs:
                    self.errors.append('Invalid attribute "%s" in %s' % (key, polygon.name))

            if floor_name in self.__provided_attrs:
                page.origin.attrs = self.__provided_attrs[floor_name]
            elif self.__provided_attrs:
                self.errors.append('Floor %s was not provided attributes' % (floor_name))

            if page.scale is None:
                self.errors.append('Page %s has no scale' % (page.name))

        for name, count in Counter([page.name for page in list(self.pages.values())]).items():
            if name is not None and count > 1:
                self.errors.append('Floor %s is defined multiple items' % name)

    def create(self):

        '''Create the building from pdf'''

        b = eo.Building()

        for name, page in list(self.pages.items()):

            if page.name is None:
                continue

            floor = eo.Floor(b, name=utils.wrap(page.name))
            floor.attr['Z'] = page.origin.attrs['Z']

            if not page.origin.attrs['HP']:
                page.origin.attrs['PH'] = 0

            floor.attr['FLOOR-HEIGHT'] = page.origin.attrs['H']
            floor.attr['SPACE-HEIGHT'] = \
                page.origin.attrs['H'] - page.origin.attrs['PH']
            floor.attr['SHAPE'] = 'NO-SHAPE'

            for fdf_polygon in page.polygons:
                name = '"%s_poly"' % (fdf_polygon.name)
                vertices = self.__set_vertices(page, fdf_polygon)
                polygon = eo.Polygon(b, name=name, vertices=vertices)
                polygon.rotate_in_place(-fdf_polygon.rotation)

                if not polygon.is_ccw():
                    polygon.reverse()
                spaces = \
                    self.__create_space(b, floor, fdf_polygon, polygon, page)

                if 'S' in fdf_polygon.attrs:
                    system_name = utils.wrap(fdf_polygon.attrs['S'] + '_SYS')
                else:
                    system_name = '"Dummy System"'

                self.__create_zones(b, spaces, system_name)

        return b

    def __create_zones(self, b, spaces, system_name):

        '''Creates zones under system'''

        if not system_name in b.objects:
            system = eo.System(b, system_name)
            system.attr['TYPE'] = 'VAVS'
            system.attr['HEAT-SOURCE'] = 'NONE'
            system.attr['CHW-LOOP'] = '"DEFAULT-CHW"'
        else:
            system = b.objects[system_name]


        for space in spaces:
            if space is not None:
                space.make_zone(system)

    def __set_vertices(self, page, fdf_polygon):

        '''Set vertices for the newly created polygon'''

        reversed = page.origin.reversed
        x_mirror = page.origin.x_mirror
        y_mirror = page.origin.y_mirror
        factor = page.scale.factor
        origin_x = page.origin.x
        origin_y = page.origin.y

        vertices = []
        x_offset = page.origin.attrs.get('X', 0)
        y_offset = page.origin.attrs.get('Y', 0)
        for verticy in fdf_polygon.vertices:
            if not reversed:
                x = (factor * float(verticy[0]-origin_x) * x_mirror +
                    x_offset)
                y = (factor * float(verticy[1]-origin_y) * y_mirror +
                    y_offset)
            else:
                x = (factor * float(verticy[1]-origin_x) * x_mirror +
                    x_offset)
                y = (factor * float(verticy[0]-origin_y) * y_mirror +
                    y_offset)
            vertices.append([x,y])

        # The takesoffs may have open or closed polygons definitions
        if distance(vertices[0], vertices[-1]) < 0.5:
            del vertices[-1]

        for i, pt1 in enumerate(vertices, start=1):
            for j, pt2 in enumerate(vertices, start=1):
                if i >= j - 1:
                    continue
                if distance(pt1, pt2) < 0.5:
                    self.errors.append(('Points in polygon %s has vertices'
                        ' %s and %s defined too closely together ' % (
                        fdf_polygon.name, i, j)))


        return vertices

    def __create_space(self, b, floor, fdf_polygon, polygon, page):

        '''Convert polygon to space'''

        if 'Z' in fdf_polygon.attrs:
            space_z = fdf_polygon.attrs['Z']
        else:
            space_z = 0

        if 'H' in fdf_polygon.attrs:
            total_height = fdf_polygon.attrs['H']
        else:
            total_height = floor.attr['FLOOR-HEIGHT']

        if 'HP' in fdf_polygon.attrs:
            has_plenum = fdf_polygon.attrs['HP']
        else:
            has_plenum = page.origin.attrs['HP']

        if has_plenum:
            if 'PH' in fdf_polygon.attrs:
                plenum_height = fdf_polygon.attrs['PH']
            elif 'PH' in page.origin.attrs:
                plenum_height = page.origin.attrs['PH']
        else:
            plenum_height = 0

        space_height = total_height - plenum_height

        if abs(plenum_height) < 0.1:
            has_plenum = False

        plenum_z = space_z + space_height

        name = '"' + fdf_polygon.name + '"'

        if len(name) > 23:
            self.errors.append(
                'Name %s is too long, shorten by %s' %
                (name, len(name) - 23))

        space = eo.Space(b, name, 'SPACE', floor)

        space.attr['ZONE-TYPE'] = 'CONDITIONED'
        space.attr['POLYGON'] = polygon.name
        space.attr['SHAPE'] = 'POLYGON'

        if abs(space_height - floor.attr['SPACE-HEIGHT']) > 0.1:
            space.attr['HEIGHT'] = space_height

        if abs(space_z) > 0.1:
            space.attr['Z'] = space_z

        if fdf_polygon.activity is not None:
            space.attr['C-ACTIVITY-DESC'] = '*%s*' % fdf_polygon.activity

        plenum_space = None

        if has_plenum:
            plenum_name = name[:-1] + '_p"'
            plenum_space = eo.Space(b, plenum_name, 'SPACE', floor)
            plenum_space.attr['ZONE-TYPE'] = 'PLENUM'
            plenum_space.attr['POLYGON'] = polygon.name
            plenum_space.attr['SHAPE'] = 'POLYGON'
            if abs(plenum_height - (floor.attr['FLOOR-HEIGHT'] - floor.attr['SPACE-HEIGHT'])) > 0.1:
                plenum_space.attr['HEIGHT'] = plenum_height
            if abs(plenum_z - floor.attr['SPACE-HEIGHT']) > 0.1:
                plenum_space.attr['Z'] = plenum_z
            plenum_space.attr['C-ACTIVITY-DESC'] = '*Plenum*'

        return [space, plenum_space]

class Pdf_Page(object):

    def __init__(self):
        self.polygons = []
        self.origin = None
        self.scale = None
        self.name = None

    def __repr__(self):
        return f'PDF PAGE {self.name}'

class Pdf_Origin(object):

    def __init__(self, annotation):


        vl = annotation.get('/Vertices')
        self.vertices = [vl[i:i+2] for i in range(0, len(vl), 2)]
        self.name, self.attrs = process_name(annotation.get('/T'))

        # set orientation

        pt1 = [self.vertices[0][0], self.vertices[0][1]]
        pt2 = [self.vertices[1][0], self.vertices[1][1]]
        pt3 = [self.vertices[2][0], self.vertices[2][1]]
        self.x_mirror = 1
        self.y_mirror = 1

        # test if point 1's dy > dx
        if abs(pt2[1]-pt1[1]) > abs(pt2[0]-pt1[0]):
            # y location bound to up
            self.reversed = False
            self.x, self.y = pt2
            if pt3[0] < pt2[0]: self.x_mirror = -1
            if pt1[1] < pt2[1]: self.y_mirror = -1
        else:
            # x location bound to up
            self.reversed = True
            self.y, self.x = pt2
            if pt1[0] < pt2[0]: self.y_mirror = -1
            if pt3[1] < pt2[1]: self.x_mirror = -1


class Pdf_Scale(object):

    def __init__(self, annotation):

        self.name, _, value = annotation.get('/T').partition(' ')
        self.length = convert_feet(value)
        pl = annotation.get('/L')
        self.distance = distance([pl[0], pl[1]], [pl[2], pl[3]])
        self.factor = self.length/self.distance


class Pdf_Polygon(object):

    def __init__(self, annotation):

        self.attrs = {}
        vl = annotation.get('/Vertices')
        self.vertices = [vl[i:i+2] for i in range(0, len(vl), 2)]

        if annotation.get('/Subject', '').lower() != 'polygon':
            self.activity, s_attrs = process_name(annotation.get('/Subj'))
        else:
            self.activity == None

        if annotation.get('/Rotation'):
            self.rotation = int(annotation.get('/Rotation'))
        else:
            self.rotation = 0

        self.name, a_attrs = process_name(annotation.get('/T'))

        self.attrs.update(s_attrs)
        self.attrs.update(a_attrs)

def process_name(s):

    if ' ' in s.split('[')[0].strip():
        raise Exception('Space in name "%s"' % s)

    normalized = re.sub(r'[\[\]\;\(\)\,]', ' ', s)

    name_parts = []
    attrs_parts = []
    for part in normalized.split():
        if ':' in part:
            attrs_parts.append(part)
        else:
            name_parts.append(part)

    name = ' '.join(name_parts)

    attrs = {}

    for pair in attrs_parts:
        key, value = pair.split(':')
        if key == 'HP':
            attrs[key] = value.upper().startswith('Y')
        elif key == 'S':
            attrs[key] = value
        else:
            attrs[key] = convert_feet(value)

    return name, attrs


def from_pdf(pdf_file, seed_file, attrs=None):

    '''Create a building from an pdf file'''

    project_name = os.getcwd().split(os.sep)[-1]

    with open(project_name + '.pd2', 'w') as f:
        f.write(utils.project_pd2_text(project_name))

    b = eo.Building()
    b.load(seed_file)

    pdf = Pdf_File(pdf_file, attrs)

    if not pdf.errors:
        pdf_building = pdf.create()
        b.extend(pdf_building)

    if pdf.warnings:
        print('  WARNINGS')
        for warning in pdf.warnings:
            print('    %s' % warning)

    if pdf.errors:
        print('  ERRORS')
        for error in pdf.errors:
            print ('    %s' % error)
        input()
        return None

    return b

def create(pdf, seed_file, attrs=None):

    '''Helper to dump building from pdf to prescribed input file name'''

    b = from_pdf(pdf, seed_file, attrs)
    if b is None:
        print('  Exiting...')
        return -1
    else:
        b.dump(utils.input_file_name())
        return 0

def main():

    '''Command line version of creating a building from pdf'''


    pdf_file = sys.argv[1]
    if len(sys.argv) == 3:
        client = sys.argv[2]
    else:
        client = 'none'

    from_pdf(pdf_file, client)

if __name__ == '__main__':
    main()
