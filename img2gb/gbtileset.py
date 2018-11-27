from .gbtile import GBTile
from .helpers import to_pil_rgb_image


class GBTileset(object):

    @classmethod
    def from_image(Cls, pil_image):
        image = to_pil_rgb_image(pil_image)
        width, height = image.size

        if width % 8 or height % 8:
            raise ValueError("The input image width and height must be a multiple of 8")  # noqa

        # TODO check tile count <= 255

        tileset = Cls()

        for tile_y in range(0, height, 8):
            for tile_x in range(0, width, 8):
                tile = GBTile.from_image(image, tile_x, tile_y)
                tileset.add_tile(tile)

        return tileset

    def __init__(self):
        self.tiles = []

    def add_tile(self, gbtile, dedup=False):
        if dedup and gbtile in self.tiles:
            return self.tiles.index(gbtile)
        # TODO check tile count <= 255
        self.tiles.append(gbtile)
        return len(self.tiles) - 1

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
