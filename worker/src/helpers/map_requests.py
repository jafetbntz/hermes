
import uuid
import polyline
from urllib import parse as u_parse
import os 


class MapSnapshotRequest():
    def __init__(self, points, style_id ="mapbox/streets-v11", width = 400, height = 400, fill_color = 'ff0000', fill_opacity = 0.8, base_folder='/var/www/pictures'):
        self.style_id = style_id
        self.width = width
        self.height = height
        self.stroke_width = 5
        self.fill_color = fill_color
        self.fill_opacity = fill_opacity

        self.coordinates_list = points
        self.base_folder = base_folder


    def get_mapbox_polyline(self):

        if self.coordinates_list == None or len(self.coordinates_list) <= 2:
            return

        # Encodes a list of coordinates (in tuples) into Google's Polyline format
        polyline_hash = polyline.encode(self.coordinates_list, 5)

        # URI-encodes the polyne hash so we can use it in a URL
        uri_encoded_polyline = u_parse.quote_plus(polyline_hash)

        # Create a single string that contains the polyline and the styles of the path.
        # Check https://docs.mapbox.com/api/maps/static-images/#path 
        # for more info about the available parameters
        result = f'path-{self.stroke_width}+{self.fill_color}-{self.fill_opacity}({uri_encoded_polyline})'

        return result


    def generate_filename(self):
        path = os.path.join(self.base_folder, f'{uuid.uuid4()}.png')
        return path

    def is_valid(self):
        if not self.coordinates_list:
            return False

        if len(self.coordinates_list) <= 2:
            return False

        if not self.base_folder:
            return False

        return True

