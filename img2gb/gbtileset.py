"""
The :class:`GBTileset` represents a GameBoy tileset. It is composed of
:class:`GBTile` (up to 255 tiles).

Creating a tileset from scratch::

    from img2gb import GBTile, GBTileset

    tileset = GBTileset()
    tile = GBTile()

    tileset.add_tile(tile)  # -> 0
    tileset.length  # -> 1

Creating a tileset from a PIL image::

    from img2gb import GBTileset
    from PIL import Image

    image = Image.open("./my_tileset.png")
    tileset = GBTileset.from_image(image)
"""


from .gbtile import GBTile
from .helpers import to_pil_rgb_image


class GBTileset(object):
    """Stores and manipulate a GameBoy tileset (up to 255 tiles)."""

    @classmethod
    def from_image(Cls, pil_image):
        """Create a new GBTileset from the given image.

        :param PIL.Image.Image pil_image: The input PIL (or Pillow) image.
        :rtype: GBTileset

        .. NOTE::

           * The image width and height must be a multiple of 8.
           * The image can contain up to 255 different tiles.
        """
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
        """Adds a tile to the tileset.

        :param GBTile gbtile: The tile to add.
        :param bool dedup: If ``True``, the tile will be added only if there is
                           no identical tile in the tileset (default =
                           ``False``).

        :rtype: int
        :returns: The id of the tile in the tileset.
        """
        if dedup and gbtile in self.tiles:
            return self.tiles.index(gbtile)
        # TODO check tile count <= 255
        self.tiles.append(gbtile)
        return len(self.tiles) - 1

    def to_hex_string(self):
        """Returns the tileset as an hexadecimal-encoded string (one tile per
        line).

        :rtype: str
        """
        result = ""
        for tile in self.tiles:
            result += "%s\n" % tile.to_hex_string()
        return result

    @property
    def length(self):
        """Number of tiles in the tileset."""
        return len(self.tiles)

    @property
    def data(self):
        """Raw data of the tiles in the tileset (list of int)."""
        data = []
        for tile in self.tiles:
            data += tile.data
        return data
