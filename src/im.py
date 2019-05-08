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

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.annotations = defaultdict(list)
        self.pages = OrderedDict()
        self.messages = []

        self.__define_annotations()
        self.__build()
        self.__verify_specials()
        
        if self.messages:
            return

    def __define_annotations(self):

        '''Assign annotations from pdf'''

        input = PyPDF2.PdfFileReader(open(self.pdf_path, "rb"))

        for i in range(input.getNumPages()) :
            for annot in input.getPage(i).get('/Annots', []):
                self.annotations[i].append(annot.getObject())


    def __build(self):

        '''Build PDF File object from pdf annotations'''

        for page_number, annotations in self.annotations.items():

            for annotation in annotations:

                if not page_number in self.pages:
                    # Make new page if page number is new
                    pdf_page = Pdf_Page()
                    self.pages[page_number] = pdf_page
                else: 
                    # Use exsting if page numebr exists
                    pdf_page = self.pages[page_number]

                if annotation.get('/T', '').lower().startswith('origin'):
                    if pdf_page.origin is None:
                        pdf_page.origin = Pdf_Origin(annotation)
                    else:
                        self.messages('Page %s has multiple origins' % page_number)
                elif annotation.get('/T', '').lower().startswith('scale'):
                    if pdf_page.scale is None:
                        pdf_page.scale = Pdf_Scale(annotation)
                    else:
                        self.messages('Page %s has multiple scales' % page_number)
                elif annotation.get('/Subtype') == '/Polygon':
                    pdf_page.polygons.append(Pdf_Polygon(annotation))

    def __verify_specials(self):

        '''Verify contents of each page'''

        valid_poly_attrs = ['Z', 'H', 'HP', 'PH', 'X', 'Y']

        for name, page in self.pages.items():

            # check spaces
            floor_name_counter = Counter()
            space_names_set = set()
            for polygon in page.polygons:
                if not polygon.name.count('-') == 1:
                    self.messages.append('Space %s has wrong number of hyphens' % (polygon.name))

                if polygon.name in space_names_set:
                    self.messages.append('Space %s is defined multiple times' % (polygon.name))
                else:
                    space_names_set.add(polygon.name)
                floor_name_counter[polygon.name.split('-')[0]] += 1

                for key in polygon.attrs.keys():
                    if not key in valid_poly_attrs:
                        self.messages.append('Invalid attribute "%s" in %s' % (key, polygon.name))

            floor_name = floor_name_counter.most_common(1)[0][0]
            if len(floor_name_counter) > 1:
                self.messages.append('Floor %s has spaces assigned to multiple floors' % (floor_name))

            for key in page.origin.attrs:
                if not key in valid_poly_attrs:
                    self.messages.append('Invalid attribute "%s" in %s' % (key, polygon.name))
           
            # assign floor name from dominent space
            page.name = floor_name

            if page.scale is None:
                self.messages.append('Page %s has no scale' % (page.name ))
        
        for name, count in Counter([page.name for page in self.pages.values()]).items():
            if count > 1:
                self.messages.append('Floor %s is defined multiple items' % name)

    def create(self):

        '''Create the building from pdf'''

        b = eo.Building()

        for name, page in self.pages.items():

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
                if not polygon.is_ccw():
                    polygon.reverse()
                self.__create_space(b, floor, fdf_polygon, polygon, page)

        return b

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
                    self.messages.append(('Points in polygon %s has vertices'
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


class Pdf_Page(object):

    def __init__(self):
        self.polygons = []
        self.origin = None
        self.scale = None


class Pdf_Origin(object):

    def __init__(self, annotation):

        self.attrs = {}

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
            self.activity = annotation.get('/Subj')
        else:
            self.activity == None

        self.name, self.attrs = process_name(annotation.get('/T'))


def process_name(s):

    fields = re.sub(r'[\[\]\;\(\)]', ' ', s).split()
    
    name = fields[0]
    attrs = {}

    for pair in fields[1:]:
        key, value = pair.split(':')
        if key != 'HP':
            attrs[key] = float(value)
        else:  
            attrs[key] = value.upper().startswith('Y')

    return name, attrs


def from_pdf(pdf_file, seed_file):

    '''Create a building from an pdf file'''

    project_name = os.getcwd().split(os.sep)[-1]

    with open(project_name + '.pd2', 'wb') as f:
        f.write(utils.project_pd2_text(project_name))

    b = eo.Building()
    b.load(seed_file)

    pdf = Pdf_File(pdf_file)
    if pdf.messages:
        for message in pdf.messages:
            print ' ', message
        return None
        
    pdf_building = pdf.create()

    b.extend(pdf_building)

    if pdf.messages:
        for message in pdf.messages:
            print ' ', message
        raw_input()

    return b

def create(pdf, seed_file):

    '''Helper to dump building from pdf to prescribed input file name'''

    b = from_pdf(pdf, seed_file)
    if b is None:
        print '  Exiting...'
        return None
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
