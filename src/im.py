from e_math import convert_feet, distance
from collections import OrderedDict
import json
import math
import eo
import re
import sys
import os
import utils
import ref
import copy

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
    
    def __init__(self, pdf_path, seed=None):
        self.pdf_path = pdf_path
        self.page_numbers = OrderedDict()
        self.pages = OrderedDict()
        self.messages = []
        self.polygons = []
        self.origins = []
        self.scales = []
        self.b = eo.Building()
        self.read_pdf()

    def define(self):
        '''Query user to provide information about the building floors'''

        self.define_floors()
    
    def create(self):
        '''
        Once the pdf file is read and the floors are defined, the building
        can be created
        '''
        
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
                page.origins[0].set_orientation()

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
        valid_poly_attrs = ['Z', 'H', 'HP', 'PH']
        for name, page in self.pages.items():
            for polygon in page.polygons:                
                for key in polygon.attrs.keys():
                    if not key in valid_poly_attrs:
                        self.messages.append('Invalid attribute "%s" in %s' % (key, polygon.name))

    def define_floors(self):
        '''Read the json file which contains the floor definitions'''

        attrs = OrderedDict([('x',0), ('y',0), ('z',0), 
            ('floor height',None), ('plenum height',None), 
            ('default plenum',False)])

        if os.path.exists(ref.spaces_json):
            with open(ref.spaces_json) as f:
                self.spec = json.load(f, object_pairs_hook=OrderedDict)
        else:
            self.spec = OrderedDict()

        for page_name in self.pages.keys():
            print 'Page %s' % page_name

            if not page_name in self.spec:
                self.spec[page_name] = OrderedDict()

            for attr, default in attrs.items():
                if not attr in self.spec[page_name]:
                    resp = raw_input(' %s [%s] >> ' % (attr, default))
                    if not resp:
                        print default
                        resp = default
                    elif resp.lower() in ['t', 'true']:
                        resp = True
                    elif resp.lower() in ['f', 'false']:
                        resp = False
                    else:
                        try:
                            resp = float(resp)
                        except ValueError:
                            resp = str(resp)
                    self.spec[page_name][attr] = resp

            # inherit defaults
            for attr, new_default in self.spec[page_name].items():
                if attr == 'z':
                    attrs['z'] = self.spec[page_name]['floor height'] + self.spec[page_name]['z']
                else:
                    attrs[attr] = new_default
        
        with open(ref.spaces_json, 'wb') as f:
            json.dump(self.spec, f, indent=4, separators=(',', ': '))

    def create_floors(self):
        '''Create floors'''
        
        for floor_name, spec_attrs in self.spec.items():
            floor = eo.Floor(self.b, name=str(floor_name))
            floor.attr['Z'] = self.spec[floor_name]['z']

            floor.attr['FLOOR-HEIGHT'] = self.spec[floor_name]['floor height']
            floor.attr['SPACE-HEIGHT'] = (floor.attr['FLOOR-HEIGHT'] - 
                self.spec[floor_name]['plenum height'])

    def process_polygons(self):

        for page_name, page in self.pages.items():
            for fdf_polygon in page.polygons:
                name = '"%s-%s_poly"' % (page.name, fdf_polygon.name)
                polygon = eo.Polygon(self.b, name=name)
                polygon.vertices = self.set_vertices(page, fdf_polygon)
                self.create_space(page, fdf_polygon, polygon)

    def set_vertices(self, page, fdf_polygon):                
        '''Set vertices for the newly created polygon'''

        reversed = page.origins[0].reversed
        x_mirror = page.origins[0].x_mirror
        y_mirror = page.origins[0].y_mirror
        factor = page.scales[0].factor
        origin_x = page.origins[0].x
        origin_y = page.origins[0].y

        vertices = []
        x_offset = self.spec[page.name]['x']
        y_offset = self.spec[page.name]['y']
        for verticy in fdf_polygon.vertices:
            if not reversed:
                x = (factor * (verticy[0]-origin_x) * x_mirror + 
                    x_offset)
                y = (factor * (verticy[1]-origin_y) * y_mirror + 
                    y_offset)
            else:
                x = (factor * (verticy[1]-origin_x) * x_mirror + 
                    x_offset)
                y = (factor * (verticy[0]-origin_y) * y_mirror + 
                    y_offset)
            vertices.append([x,y])
        return vertices

    def create_space(self, page, fdf_polygon, polygon):

        floor = self.b.objects[page.name]

        z = fdf_polygon.attrs.get('Z')
        h = fdf_polygon.attrs.get('H')

        if h != None:
            floor_height = float(fdf_polygon.attrs['H'])
        elif z != None:
            floor_height = floor.attr['SPACE-HEIGHT'] - float(z)
        else:
            floor_height = self.spec[page.name]['floor height']
            
        if 'PH' in fdf_polygon.attrs:
            plenum_height = float(fdf_polygon.attrs['PH'])
        else:
            plenum_height = self.spec[page.name]['plenum height']
        
        if not plenum_height:
            has_plenum = False
        elif 'HP' in fdf_polygon.attrs:
            has_plenum = fdf_polygon.attrs['HP'][0] == 'Y'
        else:
            has_plenum = self.spec[page.name]['default plenum']
        
        space_height = floor_height - plenum_height
        if z != None:
            plenum_z = float(z) + space_height
        else:
            plenum_z = space_height
        
        name = '"' + page.name + '-' + fdf_polygon.name + '"'
        space = eo.Space(self.b, name, 'SPACE', floor)

        space.attr['ZONE-TYPE'] = 'CONDITIONED'
        space.attr['POLYGON'] = polygon.name
        space.attr['SHAPE'] = 'POLYGON'

        if abs(space_height - floor.attr['SPACE-HEIGHT']) > 0.1:
            space.attr['H'] = space_height

        if z:
            space.attr['Z'] = z
            
        if floor.has_plenum():
            name = name[:-1] + '_p"'
            plenum_space = eo.Space(self.b, name=name)
            plenum_space.attr['ZONE-TYPE'] = 'PLENUM'
            plenum_space.attr['POLYGON'] = polygon.name
            if abs(plenum_height - (floor.attr['FLOOR-HEIGHT']-floor.attr['SPACE-HEIGHT'])) > 0.1:
                plenum_space.attr['H'] = plenum_space_height
            if abs(plenum_z - floor.attr['SPACE-HEIGHT']) > 0.1:
                plenum_space.attr['Z'] = plenum_z

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


def main():
    
    client = utils.choices(ref.clients)
    project_name = os.getcwd().split(os.sep)[-1]
    seed_file = utils.client_seed_file(client)
    fdf_file = [f for f in os.listdir('.') if f[-4:] == '.fdf'][0]

    seed_building = eo.Building()
    seed_building.load(seed_file)
    seed_building.dump(project_name.lower() + '.inp')

    pdf = Pdf_File(fdf_file)
    pdf.define()
    pdf.create()

    pdf.b.extend(seed_building)
    pdf.b.dump(project_name.lower() + '.inp')

    print '\n'.join(pdf.messages)

if __name__ == '__main__':
    main()


#pd2Seed = 'E:\\Files\\Documents\\Jared\\Work\\DMI\\eQuest\\Scripts\\seed.pd2'
