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


from PIL import Image

from .gbtile import GBTile
from .helpers import to_pil_rgb_image, tileset_iterator


class GBTileset(object):
    """Stores and manipulate a GameBoy tileset (up to 255 tiles).

    :param int offset: An offset to apply to tile ids.
    """

    @classmethod
    def from_image(
        Cls,
        pil_image,
        dedup=False,
        alternative_palette=False,
        sprite8x16=False,
        offset=0,
    ):
        """Create a new GBTileset from the given image.

        :param PIL.Image.Image pil_image: The input PIL (or Pillow) image.
        :param bool dedup: If ``True``, deduplicate the tiles (default =
                ``False``).
        :param bool alternative_palette: Use the sprite's alternative palette
                (inverted colors, default = ``False``).
        :param bool sprite8x16: Rearrange the tiles to be used in 8x16 sprites
                (default = ``False``).
        :param int offset: An offset to apply to tile ids.
        :rtype: GBTileset

        .. NOTE::

           * The image width and height must be a multiple of 8.
           * The image can contain up to 255 different tiles.
        """
        image = to_pil_rgb_image(pil_image)
        width, height = image.size

        if width % 8 or height % 8:
            raise ValueError("The input image width and height must be a multiple of 8")

        if height % 16 and sprite8x16:
            raise ValueError(
                "The input image height must be a multiple of 16 when sprite8x16=True"
            )

        # TODO check tile count <= 255

        tileset = Cls(offset=offset)

        for tile_x, tile_y in tileset_iterator(width, height, sprite8x16):
            tile = GBTile.from_image(
                image, tile_x, tile_y, alternative_palette=alternative_palette
            )
            tileset.add_tile(tile, dedup=dedup)

        return tileset

    def __init__(self, offset=0):
        self._offset = offset
        self._tiles = []

    @property
    def offset(self):
        """An offset applied to each tiles.

        :type: int
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

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
        :returns: The id of the tile in the tileset (including offset).
        """
        if dedup and gbtile in self._tiles:
            return self._tiles.index(gbtile) + self._offset
        # TODO check tile count <= 255
        self._tiles.append(gbtile)
        return len(self._tiles) - 1 + self._offset

    def merge(self, gbtileset, dedup=False):
        """Merges the tiles of the given tileset in the current tileset.

        :param GBTileset gbtileset: The tileset to merge into the current one.
        :param bool dedup: Add only the tiles that are note already present in
                the current tileset (default = ``False``).
        """
        for tile in gbtileset.tiles:
            self.add_tile(tile, dedup=dedup)

    def index(self, gbtile):
        """Get the id of the given tile in the tileset (including offset).

        :param GBTile gbtile: The tile.
        :rtype: int
        :returns: The id of the tile in the tileset (including offset).
        """
        return self._tiles.index(gbtile) + self._offset

    def to_hex_string(self):
        """Returns the tileset as an hexadecimal-encoded string (one tile per
        line).

        :rtype: str

        e.g.::

            00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
            FF 01 81 7F BD 7F A5 7B A5 7B BD 63 81 7F FF FF
            7E 00 81 7F 81 7F 81 7F 81 7F 81 7F 81 7F 7E 7E
            3C 00 54 2A A3 5F C1 3F 83 7F C5 3F 2A 7E 3C 3C
            04 04 04 04 0A 0A 12 12 66 00 99 77 99 77 66 66

        """
        return "\n".join([tile.to_hex_string() for tile in self._tiles])

    def to_c_string(self, name="TILESET"):
        """Returns C code that represents the data of the tileset.

        :param str name: The name of the variable in the generated code (always
                converted to uppercase in the generated code, default =
                ``"TILESET"``)

        :rtype: str

        Example:

        .. code-block:: C

            const UINT8 TILESET[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xFF, 0x01, 0x81, 0x7F, 0xBD, 0x7F, 0xA5, 0x7B, 0xA5, 0x7B, 0xBD, 0x63, 0x81, 0x7F, 0xFF, 0xFF,
                0x7E, 0x00, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x7E, 0x7E,
                0x3C, 0x00, 0x54, 0x2A, 0xA3, 0x5F, 0xC1, 0x3F, 0x83, 0x7F, 0xC5, 0x3F, 0x2A, 0x7E, 0x3C, 0x3C,
                0x04, 0x04, 0x04, 0x04, 0x0A, 0x0A, 0x12, 0x12, 0x66, 0x00, 0x99, 0x77, 0x99, 0x77, 0x66, 0x66,
            };
        """
        c = "const UINT8 %s[] = {\n" % name.upper()
        for tile in self._tiles:
            c += "    %s,\n" % ", ".join(["0x%02X" % b for b in tile.data])
        c += "};"
        return c

    def to_c_header_string(self, name="TILESET"):
        """Returns the C header (.h) code for the tileset.

        :param str name: The name of the variable in the generated code (always
                converted to uppercase in the generated code, default =
                ``"TILESET"``)
        :rtype: str

        Example:

        .. code-block:: C

            extern const UINT8 TILESET[];
            define TILESET_TILE_COUNT 5
        """
        result = "extern const UINT8 %s[];\n" % name.upper()
        result += "#define %s_TILE_COUNT %i" % (name.upper(), self.length)
        return result

    def to_image(self):
        """Generates a PIL image from the tileset. The generated image is an
        indexed image with a 4 shades of gray palette.

        :rtype: PIL.Image.Image
        """
        if self.length <= 16:
            width = self.length * 8
            height = 1 * 8
        else:
            width = 16 * 8
            height = (self.length // 16 + bool(self.length % 16)) * 8

        image = Image.new("P", (width, height))
        image.putpalette(
            [
                # fmt: off
                0xFF, 0xFF, 0xFF,
                0xBB, 0xBB, 0xBB,
                0x55, 0x55, 0x55,
                0x00, 0x00, 0x00,
                # fmt: on
            ]
        )

        for i in range(self.length):
            tile_image = self._tiles[i].to_image()
            x = (i * 8) % width
            y = (i * 8) // width * 8
            image.paste(tile_image, (x, y))

        return image
