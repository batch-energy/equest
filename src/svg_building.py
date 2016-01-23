from e_math import convert_feet, distance
import eo
import utils
import svg
import os
from ref import pd2, input_seed
from utils import rewrap, wrap
from shapely.geometry import Point

class Svg_Building():
    
    def __init__(self, fn):

        self.scale = 1
        self.svg_floors = []
        self.svg = svg.Svg_File(fn)

    def check(self):
        self.messages = []
        self._check_scale()
        self._check_layers()

    def _check_scale(self):

        scales = [r for r in self.svg.all_rects() if 'scale ' in r.title]
        if len(scales) == 0:
            self.add_messages('No scale found')
        elif len(scales) > 1:
            self.add_message('More than one scale found')
        else:
            scale_rect = scales[0]
            
            if 'transform' in scale_rect.dict:
                self.add_messages('Scale has been transformed, this may ' + 
                    'cause unexpected behavior')

            scale_split = scale_rect.title.split()
            if len(scale_split) != 2:
                self.add_messages('Scale malformed')
            else:
                scale_length_string = scale_split[1]
                try:
                    scale_input = convert_feet(scale_length_string)
                    self.scale = float(scale_input) / float(scale_rect.longest())
                except:
                    self.add_messages('Scale malformed')

    def _check_layers(self):
        floor_names = []
        for layer in self.svg.layers:
            if '_floor_name' in layer.dict:
                svg_floor = Svg_Floor(self, layer)
                self.svg_floors.append(svg_floor)
                if svg_floor.floor_name in floor_names:
                    self.add_message('Duplicate floor name ' + floor_name)
                else:
                    floor_names.append(svg_floor.floor_name)

    def add_message(self, message):
        self.messages.append(message)


class Svg_Floor():
    
    REQUIRED_ATTRIBUTES = ['_z', '_space_height', '_floor_height']

    def __init__(self, svg_building, floor_layer):
        self.svg_building = svg_building
        self.floor_name = floor_layer.dict['_floor_name']
        self.floor_layer = floor_layer
        self.svg_polygons = []
        self.svg_spaces = []
        self._check_required()
        self._check_paths()

    def _check_required(self):
        for attr in Svg_Floor.REQUIRED_ATTRIBUTES:
            try:
                setattr(self, attr[1:], self.floor_layer.dict[attr])
            except:
                self.add_message('%s not defined on %s' % 
                    (attr, self.floor_layer.name))

    def add_message(self, message):
        self.svg_building.add_message(message)

    def _check_paths(self):
        path_titles = []
        for path in self.floor_layer.paths:
            polygon = Svg_Polygon(self, path)
            self.svg_polygons.append(polygon)
            zone_kind = path.dict.get('_zone_type') or 'CONDITIONED'
            space = Svg_Space(self, path, zone_kind, polygon)
            self.svg_spaces.append(space)

            if self.__has_plenum():
                space = Svg_Space(self, path, 'PLENUM', polygon)
                self.svg_spaces.append(space)

            if 'transform' in path.dict:
                self.add_message('Path %s has been transformed - this can ' + 
                    'cause unexpected behavior')

            if not path.title:
                self.add_message('No title for path ' + path.id)
            elif path.title in path_titles:
                self.add_message('Duplicate path title %s in %s' % (
                    path.title, path.id))
            else:
                path_titles.append(path.title)

    def __has_plenum(self):
        return not self.space_height == self.floor_height
    
class Svg_Space():
    
    def __init__(self, svg_floor, path, zone_kind, svg_polygon):
        self.svg_floor = svg_floor
        self.svg_polygon = svg_polygon
        self.zone_kind = zone_kind
        self.path = path

    def add_message(self, message):
        self.svg_floor.add_message(message)

class Svg_Polygon():
    
    def __init__(self, svg_floor, path):
        self.path = path
        self.svg_floor = svg_floor
        self.points = path.points
        self._check_points()
        self._scale_points()

    def _check_points(self, tol=0.0001):
        # remove sequential duplicated (including wraparound)
        utils.dedupe(self.points)

        # message for self intersection polygons
        for i, point in enumerate(self.points):
            if point in self.points[:i]:
                self.add_message('Path %s is self intersecting at %s, %s' %
                    (self.path.title, point[0], point[1]))

    def _scale_points(self):
        self.scaled_points = []
        scale = self.svg_floor.svg_building.scale
        for x, y in self.points:
            self.scaled_points.append([x * scale, y * scale])

    def add_message(self, message):
        self.svg_floor.add_message(message)
