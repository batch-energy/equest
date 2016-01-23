from shapely.geometry import LineString, Point, MultiPolygon, MultiLineString, Polygon,  GeometryCollection, MultiPoint


def shapely_polygon_to_point_list(shapely_polygon):
    return list(shapely_polygon.exterior.coords)[:-1]

def point_list_to_shapely_polygon(point_list):
    return Polygon(point_list)


def decompose(shape):
    
    if isinstance(shape, GeometryCollection):
        uncollecteds = list(shape)
    else:
        uncollecteds = [shape]
    
    flattened = []
    for uncollected in uncollecteds:
        if isinstance(uncollected, (MultiPolygon, MultiLineString, MultiPoint)):
            flattened += list(uncollected)
        else:
            flattened += [uncollected]
    return flattened


