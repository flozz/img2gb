"""
The :class:`GBTileset` class represents a GameBoy tileset. It is composed of
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
    def from_image(Cls, pil_image, dedup=False):
        """Create a new GBTileset from the given image.

        :param PIL.Image.Image pil_image: The input PIL (or Pillow) image.
        :param bool dedup: If ``True``, deduplicate the tiles (default =
                           ``False``).
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
                tileset.add_tile(tile, dedup=dedup)

        return tileset

    def __init__(self):
        self._tiles = []

    @property
    def length(self):
        """Number of tiles in the tileset.

        :type: int
        """
        return len(self._tiles)

    @property
    def data(self):
        """Raw data of the tiles in the tileset.

        :type: list of int
        """
        data = []
        for tile in self._tiles:
            data += tile.data
        return data

    @property
    def tiles(self):
        """Tiles of the tileset.

        :type: GBTile
        """
        return self._tiles

    def add_tile(self, gbtile, dedup=False):
        """Adds a tile to the tileset.

        :param GBTile gbtile: The tile to add.
        :param bool dedup: If ``True``, the tile will be added only if there is
                           no identical tile in the tileset (default =
                           ``False``).

        :rtype: int
        :returns: The id of the tile in the tileset.
        """
        if dedup and gbtile in self._tiles:
            return self._tiles.index(gbtile)
        # TODO check tile count <= 255
        self._tiles.append(gbtile)
        return len(self._tiles) - 1

    def to_hex_string(self):
        """Returns the tileset as an hexadecimal-encoded string (one tile per
        line).

        :rtype: str

        e.g.::

            '''00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
            FF 01 81 7F BD 7F A5 7B A5 7B BD 63 81 7F FF FF
            7E 00 81 7F 81 7F 81 7F 81 7F 81 7F 81 7F 7E 7E
            3C 00 54 2A A3 5F C1 3F 83 7F C5 3F 2A 7E 3C 3C
            04 04 04 04 0A 0A 12 12 66 00 99 77 99 77 66 66'''

        """
        return "\n".join([tile.to_hex_string() for tile in self._tiles])
