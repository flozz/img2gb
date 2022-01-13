"""
The :class:`GBTilemap` class represents a GameBoy tilemap. It can map up to
32x32 tiles that are stored in a :class:`GBTileset` (if not given, a new empty
tileset is created.

Creating a new tilemap::

    from img2gb import GBTilemap, GBTileset, GBTile

    tileset = GBTileset()
    tilemap = GBTilemap(
            width=32,
            height=32,
            gbtileset=tilset
            )

    tile = GBTile()  # blank tile

    tilemap.put_tile(0, 0, tile)  # The tile will be added in the tileset


Creating a tilemap from an image::

    from img2gb import GBTilemap
    from PIL import Image

    image = Image.open("./my_tilemap.png")
    tilemap = tilemap.from_image(image)
"""


from .gbtile import GBTile
from .gbtileset import GBTileset
from .helpers import to_pil_rgb_image


class GBTilemap(object):

    """Stores and manipulates GameBoy tilemaps.

    :param int width: With of the tilemap in tile (default = ``32``).
    :param int height: Height of the tilemap in tile (default = ``32``).
    :param GBTileset gbtileset: The tileset to use (a new empty one will be
                                created if set to ``None``, default =
                                ``None``).
    """

    @classmethod
    def from_image(
        Cls, pil_image, gbtileset=None, missing="append", replace=0, dedup=True
    ):
        """Generates the tilemap from the given image. The tileset can also be
        generated at the same time.

        :param PIL.Image.Image pil_image: The image that represents the
                tilemap.
        :param GBTileset gbtileset: The tileset that contains the tiles used in
                the tilemap (a new empty one is created if not provided).
        :param str missing: What to do if a tile is missing from the tileset:

                * ``"append"`` (default): append the tile to the tileset,
                * ``"error"``: raise an error,
                * ``"replace"``: relpace by an other tile (see the ``replace``
                  argument).

        :param int replace: The id of the replacement tile when
                ``missing="replace"``.
        :param bool dedup: Deduplicate tiles when ``missing="append"`` (default
                = ``True``).
        """
        image = to_pil_rgb_image(pil_image)
        width, height = image.size

        if width % 8 or height % 8:
            raise ValueError("The input image width and height must be a multiple of 8")

        tilemap = Cls(width / 8, height / 8, gbtileset=gbtileset)

        for tile_y in range(0, height, 8):
            for tile_x in range(0, width, 8):
                tile = GBTile.from_image(image, tile_x, tile_y)
                tilemap.put_tile(
                    tile_x / 8,
                    tile_y / 8,
                    tile,
                    missing=missing,
                    replace=replace,
                    dedup=dedup,
                )

        return tilemap

    def __init__(self, width=32, height=32, gbtileset=None):
        self._tileset = gbtileset if gbtileset else GBTileset()
        self._map = [0x00] * int(width * height)
        self._width = width
        self._height = height

    @property
    def tileset(self):
        """The tileset that contains the tiles used by the tilemap.

        :type: GBTileset
        """
        return self._tileset

    @property
    def width(self):
        """The width of the tilemap.

        :type: int
        """
        return self._width

    @property
    def height(self):
        """The height of the tilemap.

        :type: int
        """
        return self._height

    @property
    def size(self):
        """The with and height of the tilemap.

        :type: tuple of two int ``(width, height)``
        """
        return self._width, self._height

    @property
    def data(self):
        """Raw data of the tilemap.

        :type: list of int
        """
        return self._map

    def put_tile(self, x, y, gbtile, missing="append", replace=0, dedup=True):
        """Put a tile at the given position in the tilemap.

        :param int x: The x coordinate where to put the tile in the tilemap.
        :param int y: The y coordinate where to put the tile in the tilemap.
        :param GBTile gbtile: The tile to put in the tilemap.
        :param str missing: What to do if a tile is missing from the tileset:

                * ``"append"`` (default): append the tile to the tileset,
                * ``"error"``: raise an error,
                * ``"replace"``: relpace by an other tile (see the ``replace``
                  argument).

        :param int replace: The id of the replacement tile when
                ``missing="replace"``.
        :param bool dedup: Deduplicate tiles when ``missing="append"`` (default
                = ``True``).
        """
        if x < 0 or y < 0:
            raise ValueError("x and y coordinates cannot be negative")
        if x >= self._width:
            raise ValueError(
                "The x coordinate is greater than the width of the tilemap"
            )
        if y >= self._height:
            raise ValueError(
                "The y coordinate is greater than the height of the tilemap"
            )

        if missing not in ("append", "error", "replace"):
            raise ValueError(
                "Wrong value '%s' for the missing argument. Authorised values are 'append', 'error' and 'replace'."
            )

        if gbtile in self._tileset.tiles and dedup:
            tile_id = self._tileset.index(gbtile)
        else:
            if missing == "append":
                tile_id = self._tileset.add_tile(gbtile, dedup=dedup)
            elif missing == "error":
                raise ValueError("The given tile is missing from the tileset.")
            elif missing == "replace":
                tile_id = replace

        index = int(y * self._width + x)
        self._map[index] = tile_id

    def to_hex_string(self):
        """Returns the tilemap as an hexadecimal-encoded string.

        :rtype: str

        e.g. (4x4 tiles)::

            00 00 00 00
            00 01 02 00
            00 03 04 00
            00 00 00 00
        """
        result = ""
        for index in range(len(self._map)):
            tile_id = self._map[index]
            result += "%02X" % tile_id
            if (index + 1) % self._width == 0:
                result += "\n"
            else:
                result += " "
        return result.strip()

    def to_c_string(self, name="TILEMAP"):
        """Returns C code that represents the tilemap.

        :param str name: The name of the variable in the generated code (always
                converted to uppercase in the generated code, default =
                ``"TILEMAP"``)

        :rtype: str
        """
        c = "const UINT8 %s[] = {\n" % name.upper()
        for index in range(len(self._map)):
            if index % self._width == 0:
                c += "    "
            tile_id = self._map[index]
            c += "0x%02X," % tile_id
            if (index + 1) % self._width == 0:
                c += "\n"
            else:
                c += " "
        c += "};"
        return c

    def to_c_header_string(self, name="TILEMAP"):
        """Returns the C header (.h) code for the tilemap.

        :param str name: The name of the variable in the generated code (always
                converted to uppercase in the generated code, default =
                ``"TILEMAP"``)
        :rtype: str
        """
        h = "extern const UINT8 %s[];\n" % name.upper()
        h += "#define %s_WIDTH %i\n" % (name.upper(), self._width)
        h += "#define %s_HEIGHT %i" % (name.upper(), self._height)
        return h
