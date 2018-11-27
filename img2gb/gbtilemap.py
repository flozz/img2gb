from .gbtile import GBTile
from .gbtileset import GBTileset
from .helpers import to_pil_rgb_image


class GBTilemap(object):

    @classmethod
    def from_image(Cls, pil_image, gbtileset=None, dedup=True):
        image = to_pil_rgb_image(pil_image)
        width, height = image.size

        if width % 8 or height % 8:
            raise ValueError("The input image width and height must be a multiple of 8")  # noqa

        if width > 32 * 8 or height > 32 * 8:
            raise ValueError("The input image maximum with and height is 256x256 px (32x32 tiles)")  # noqa

        tilemap = Cls(width / 8, height / 8, gbtileset=gbtileset)

        for tile_y in range(0, height, 8):
            for tile_x in range(0, width, 8):
                tile = GBTile.from_image(image, tile_x, tile_y)
                tilemap.put_tile(tile_x / 8, tile_y / 8, tile, dedup=dedup)

        return tilemap

    def __init__(self, width=32, height=32, gbtileset=None):
        self.tileset = gbtileset if gbtileset else GBTileset()
        self.map = [0x00] * int(width * height)
        self.width = width
        self.height = height

    def put_tile(self, x, y, gbtile, dedup=True):
        if x < 0 or y < 0:
            raise ValueError("x and y coordinates cannot be negative")
        if x >= self.width:
            raise ValueError("The x coordinate is greater than the width of the tilemap")  # noqa
        if y >= self.height:
            raise ValueError("The y coordinate is greater than the height of the tilemap")  # noqa

        tile_id = self.tileset.add_tile(gbtile, dedup)
        index = int(y * self.width + x)

        self.map[index] = tile_id

    def to_hex_string(self):
        result = ""
        for index in range(len(self.map)):
            tile_id = self.map[index]
            result += "%02X " % tile_id
            if (index + 1) % self.width == 0:
                result += "\n"
        return result

    @property
    def size(self):
        return self.width, self.height

    @property
    def data(self):
        return self.map
        # return [self.tileset.tiles.index(t) if t in self.tileset.tiles else 0 for t in self.map]  # noqa
