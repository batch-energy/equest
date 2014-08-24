from e_math import convert_feet, distance
from collections import OrderedDict
import json
import math
import eo
import re

def convert_json(input):
    if isinstance(input, dict):
        return {convert_json(key): convert_json(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_json(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
    
def get_fdf_attribute(attr, line):
    pat = '(?<=/%s\\b).*?(?=[>/])' % attr
    chunk_re = re.findall(pat, line)
    if chunk_re:
        return chunk_re[0].strip()
    else:
        return None
    

class Pdf_File(object):
    
    def __init__(self, pdf_path, json_path):
        self.pdf_path = pdf_path
        self.json_path = json_path
        self.page_numbers = OrderedDict()
        self.pages = OrderedDict()
        self.messages = []
        self.polygons = []
        self.origins = []
        self.scales = []

        self.b = eo.Building()

        self.read_pdf()
        self.read_json()
        self.create_floors()
        self.process_polygons()

    def read_pdf(self):
        f = open(self.pdf_path, 'rb')
        text = f.read()
        lines = [line.replace('\n', ' ') 
            for line in re.findall('obj.*?endobj', text, re.DOTALL)]

        self.parse(lines)
        if self.messages:
            return self.messages

        self.verify_specials()        
        if self.messages:
            return self.messages

        self.make_page_dict()        

        self.verify_polygons()
        if self.messages:
            return self.messages
            
    def parse(self, lines):
        '''Need to search through the objects... we don't know the 
        page names yet so we create an OrderedDict based on the page number'''
        for line in lines:
            page_number = get_fdf_attribute('Page', line)

            if page_number:
                if not page_number in self.page_numbers:
                    self.page_numbers[page_number] = Pdf_Page(page_number)
                p = self.page_numbers[page_number]
                if '(origin' in line.lower():
                    p.origins.append(Pdf_Origin(line, page_number))
                elif '(scale' in line.lower():
                    p.scales.append(Pdf_Scale(line, page_number))
                elif (re.search('Subtype ?/Polygon', line) and not
                    'PolygonCloud' in line):
                    p.polygons.append(Pdf_Polygon(line, page_number))

    def verify_specials(self):
        '''Here we verify each page has one origin and one scale, and the origins
        are uniquly named, THEN we can map the origin name to the page'''

        page_names = []
        for name, page in self.page_numbers.items():

            # check origins
            if len(page.origins) != 1:
                self.messages.append('Page %s has %s origins' % (name, len(page.origins)))
            else:
                page.name = page.origins[0].name
                if page.name in page_names:
                    self.messages.append('Multiple Origins with name %s' % (page.name))
                self.messages += page.origins[0].set_orientation()

            # check scales
            if len(page.scales) != 1:
                self.messages.append('Page %s has %s scales' % (name, len(page.scales)))

            # check duplicate spaces
            page_polygons = []
            for polygon in page.polygons:
                if polygon.name in page_polygons:
                    self.messages.append('Duplicate polygon %s - Page: %s' % (
                        polygon.name, page.name))
                else:
                    page_polygons.append(polygon.name)

    def make_page_dict(self):
        '''Map page name to Pdf_File object in pages{}'''
        for number, page in self.page_numbers.items():
            self.pages[page.name] = page

    def verify_polygons(self):
        '''Ensure the polygons were filled out correctly'''
        valid_poly_attrs = ['Z', 'H', 'HP', 'PH', 'X', 'Y', 'R', 'ET']
        for name, page in self.pages.items():
            for polygon in page.polygons:                
                for key in polygon.attrs.keys():
                    if not key in valid_poly_attrs:
                        self.messages.append('Invalid attribute "%s" in %s' % (key, polygon.name))
                    elif key == 'ET':       
                        if polygon.attrs['ET'] not in self.pages:
                            self.messages.append('No matching extend to for %s on floor %s' % (polygon.name, page.name))
                if not polygon.name:
                    self.messages.append('Missing name in polygon on floor %s' % polygon.attrs['ET'])

    def read_json(self):
        '''Read the json file which contains the floor definitions'''
        self.spec = OrderedDict()

        f = open(self.json_path, 'r')
        text = f.read()
        self.spec = json.loads(text, object_pairs_hook=OrderedDict)

        spec_keys = set(self.spec.keys()) 
        fdf_keys = set(self.pages.keys()) 
        
        missing_spec = fdf_keys - spec_keys
        if missing_spec:
            self.messages.append('Missing in spec, Pages ' + ', '.join(missing_spec))

        missing_fdf = spec_keys - fdf_keys
        if missing_fdf:
            self.messages.append('Missing in fdf, Pages ' + ', '.join(missing_fdf))

    def create_floors(self):
        '''Create floors
        
        Some data in the spec file may be omitted and derived from the
        surrounding data.  This function fills in those values so that the 
        data is explicit
        '''
        
        cur_f, cur_z, cur_h, cur_ph, cur_hp = None, 0,0,3,0

        for i, (floor_name, spec_attrs) in enumerate(self.spec.items()):
            floor = eo.Floor(self.b, name=str(floor_name))
            floor.attr['Z'] = self.spec[floor_name].get('Z', cur_z + cur_h)


            # Establish has plenum and plenum height
            if 'PH' in spec_attrs or 'HP' in spec_attrs:
                floor.has_plenum = 1                
                if 'PH' in spec_attrs:
                    floor.plenum_height = self.spec[floor_name]['PH']
                else:
                    floor.plenum_height = cur_ph
            else:
                floor.has_plenum = 0

            # Assign floor and space heights
            floor.attr['FLOOR-HEIGHT'] = self.spec[floor_name].get('H', cur_h)
            if floor.has_plenum:
                floor.attr['SPACE-HEIGHT'] = floor.attr['FLOOR-HEIGHT'] - self.spec[floor_name]['PH']
            else:
                floor.attr['SPACE-HEIGHT'] = floor.attr['FLOOR-HEIGHTs']
                
            # Check gap
            if i:
                gap = ((floor.attr['Z'] - cur_h ) - cur_z)
                if abs(gap) > 0.1:            
                    self.messages.append('Unexpected Gap of %.2f between %s and %s' % (gap , cur_f, floor_name))

            # Set defaults for next go around
            cur_z = floor.attr['Z']
            cur_h = floor.attr['FLOOR-HEIGHT']
            cur_ph = self.spec[floor_name].get('PH', cur_ph)
            cur_hp = self.spec[floor_name].get('HP', cur_hp)
            cur_f = floor_name

    def process_polygons(self):

        for name, page in self.pages.items():
            reversed = page.origins[0].reversed
            x_mirror = page.origins[0].x_mirror
            y_mirror = page.origins[0].y_mirror
            factor = page.scales[0].factor
            origin_x = page.origins[0].x
            origin_y = page.origins[0].y

            for fdf_polygon in page.polygons:
                name = '"%s-%s_poly"' % (page.name, fdf_polygon.name)
                polygon = eo.Polygon(self.b, name=name)
                for verticy in fdf_polygon.vertices:
                    if not reversed:
                        x = factor * (verticy[0]-origin_x) * x_mirror
                        y = factor * (verticy[1]-origin_y) * y_mirror
                    else:
                        x = factor * (verticy[1]-origin_x) * x_mirror
                        y = factor * (verticy[0]-origin_y) * y_mirror
                    polygon.vertices.append([x,y])

                self.create_space(fdf_polygon, page, polygon)
                
    def create_space(self, fdf_polygon, page, polygon):
        floor = self.b.objects[page.name]

        name = '"' + page.name + '-' + fdf_polygon.name + '"'
        space = eo.Space(self.b, name=name)

        space.parent = floor
        space.attr['ZONE-TYPE'] = 'CONDITIONED'
        space.attr['POLYGON'] = polygon.name
        space.attr['SHAPE'] = 'POLYGON'
            
        if floor.has_plenum:
            name = name[:-1] + '_p"'
            space = eo.Space(self.b, name=name)
            space.attr['ZONE-TYPE'] = 'PLENUM'
            space.attr['POLYGON'] = polygon.name


class Pdf_Page(object):

    def __init__(self, page_number):
        self.page_number = page_number
        self.polygons = []
        self.origins = []
        self.scales = []
    

class Pdf_Origin(object):

    def __init__(self, line, page):

        self.page = page
        self.line = line
        self.name = get_fdf_attribute('T', line)[1:-1].split()[1]
        vertices_string = get_fdf_attribute('Vertices', line)[1:-1]
        vl = [float(n) for n in vertices_string.split()]
        self.vertices = [vl[i:i+2] for i in range(0, len(vl), 2)]
        
    def set_orientation(self):

        messages = []
        
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
                
        return messages
        
        
class Pdf_Scale(object):

    def __init__(self, line, page):

        self.page = page
        self.line = line
        self.length = convert_feet(get_fdf_attribute('T', line)[7:-2])
        pl = [float(n) for n in get_fdf_attribute('L', line)[1:-1].split()]
        self.start, self.end = [pl[0], pl[1]], [pl[2], pl[3]]
        self.distance = distance(self.start, self.end)
        self.factor = self.length/self.distance


class Pdf_Polygon(object):

    def __init__(self, line, page):

        self.page = page
        self.line = line
        self.attrs = {}

        vertices_string = get_fdf_attribute('Vertices', line)[1:-1]
        vl = [float(n) for n in vertices_string.split()]
        self.vertices = [vl[i:i+2] for i in range(0, len(vl), 2)]
        
        name = get_fdf_attribute('T', line)
        name_clean = re.sub(r'[\[\]\;\(\)]', ' ', name)
        name_split = name_clean.split()
        self.name = name_split[0]
        for pair in name_split[1:]:
            k, v = pair.split(':')
            self.attrs[k] = v



pd2Seed = 'E:\\Files\\Documents\\Jared\\Work\\DMI\\eQuest\\Scripts\\seed.pd2'

pdf = Pdf_File('../test/pdf/JC_Takeoffs.fdf', '../test/pdf/fdf.json')


pdf.b.write('../test/output/new.inp')
print '\n'.join(pdf.messages)
