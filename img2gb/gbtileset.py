from .gbtile import GBTile
from .helpers import rgba_brightness, brightness_to_color_id


class GBTileset(object):

    @classmethod
    def from_image(Cls, pil_image):
        width, height = pil_image.size

        if width % 8 or height % 8:
            raise ValueError("The input image width and height must be a multiple of 8")  # noqa

        # TODO check tile count <= 255

        tileset = Cls()

        for tile_y in range(0, height, 8):
            for tile_x in range(0, width, 8):
                tile = GBTile()
                for y in range(8):
                    for x in range(8):
                        pix_rgb = pil_image.getpixel((tile_x + x, tile_y + y))
                        pix_brightness = rgba_brightness(*pix_rgb)
                        color_id = brightness_to_color_id(pix_brightness)
                        tile.put_pixel(x, y, color_id)
                tileset.add_tile(tile)

        return tileset

    def __init__(self):
        self.tiles = []

    def add_tile(self, gbtile):
        # TODO check tile count <= 255
        self.tiles.append(gbtile)

    def to_hex_string(self):
        result = ""
        for tile in self.tiles:
            result += "%s\n" % tile.to_hex_string()
        return result

    @property
    def length(self):
        return len(self.tiles)

    @property
    def data(self):
        data = []
        for tile in self.tiles:
            data += tile.data
        return data
