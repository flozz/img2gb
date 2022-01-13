import pytest
from PIL import Image
from img2gb.gbtile import GBTile
from img2gb.gbtileset import GBTileset


class Test_GBTileset(object):
    @pytest.fixture
    def image(self):
        return Image.open("./test/assets/tileset.png")

    @pytest.fixture
    def image2(self):
        return Image.open("./test/assets/tilemap.png")

    @pytest.fixture
    def tile1(self):
        return GBTile()

    @pytest.fixture
    def tile2(self):
        tile = GBTile()
        tile.put_pixel(0, 0, 3)
        return tile

    def test_from_image(self, image):
        tileset = GBTileset.from_image(image)
        result = ""
        result += "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        result += "FF 01 81 7F BD 7F A5 7B A5 7B BD 63 81 7F FF FF\n"
        result += "7E 00 81 7F 81 7F 81 7F 81 7F 81 7F 81 7F 7E 7E\n"
        result += "3C 00 54 2A A3 5F C1 3F 83 7F C5 3F 2A 7E 3C 3C\n"
        result += "04 04 04 04 0A 0A 12 12 66 00 99 77 99 77 66 66"
        assert tileset.to_hex_string() == result

    @pytest.mark.parametrize("dedup,count", [(False, 64), (True, 4)])
    def test_from_image_dedup(self, image2, dedup, count):
        tileset = GBTileset.from_image(image2, dedup=dedup)
        assert tileset.length == count

    def test_add_tile(self, tile1):
        tileset = GBTileset()
        assert tileset.add_tile(tile1) == 0
        assert tileset.add_tile(tile1) == 1

    def test_add_tile_with_offset(self, tile1):
        tileset = GBTileset(offset=10)
        assert tileset.add_tile(tile1) == 10
        assert tileset.add_tile(tile1) == 11

    def test_add_tile_with_deduplication(self, tile1, tile2):
        tileset = GBTileset()
        assert tileset.add_tile(tile1, dedup=True) == 0
        assert tileset.add_tile(tile1, dedup=True) == 0
        assert tileset.add_tile(tile2, dedup=True) == 1

    def test_to_hex_string(self, tile2):
        tileset = GBTileset()
        assert tileset.to_hex_string() == ""
        tileset.add_tile(tile2)
        assert (
            tileset.to_hex_string() == "80 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
        )

    def test_length(self, tile1):
        tileset = GBTileset()
        assert tileset.length == 0
        tileset.add_tile(tile1)
        assert tileset.length == 1
        tileset.add_tile(tile1)
        assert tileset.length == 2

    def test_data(self, tile1):
        tileset = GBTileset()
        assert len(tileset.data) == 0
        tileset.add_tile(tile1)
        assert len(tileset.data) == 16
        tileset.add_tile(tile1)
        assert len(tileset.data) == 32

    def test_tiles(self, tile1):
        tileset = GBTileset()
        assert len(tileset.tiles) == 0
        tileset.add_tile(tile1)
        assert len(tileset.tiles) == 1
        assert tileset.tiles[0] == tile1
        tileset.add_tile(tile1)
        assert len(tileset.tiles) == 2
        assert tileset.tiles[1] == tile1

    def test_to_c_string(self, image):
        tileset = GBTileset.from_image(image)
        result = "const UINT8 TILESET[] = {\n"
        result += "    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,\n"
        result += "    0xFF, 0x01, 0x81, 0x7F, 0xBD, 0x7F, 0xA5, 0x7B, 0xA5, 0x7B, 0xBD, 0x63, 0x81, 0x7F, 0xFF, 0xFF,\n"
        result += "    0x7E, 0x00, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x81, 0x7F, 0x7E, 0x7E,\n"
        result += "    0x3C, 0x00, 0x54, 0x2A, 0xA3, 0x5F, 0xC1, 0x3F, 0x83, 0x7F, 0xC5, 0x3F, 0x2A, 0x7E, 0x3C, 0x3C,\n"
        result += "    0x04, 0x04, 0x04, 0x04, 0x0A, 0x0A, 0x12, 0x12, 0x66, 0x00, 0x99, 0x77, 0x99, 0x77, 0x66, 0x66,\n"
        result += "};"
        assert tileset.to_c_string() == result

    def test_to_c_string_with_custom_name(self):
        tileset = GBTileset()
        assert tileset.to_c_string(name="Foo") == "const UINT8 FOO[] = {\n};"

    def test_to_c_header_string(self, image):
        tileset = GBTileset.from_image(image)
        result = ""
        result += "extern const UINT8 TILESET[];\n"
        result += "#define TILESET_TILE_COUNT 5"
        assert tileset.to_c_header_string() == result

    def test_to_image(self, image2):
        tileset = GBTileset.from_image(image2, dedup=True)
        tileset_image = tileset.to_image()
        assert tileset_image.width == 32
        assert tileset_image.height == 8

    def test_to_c_header_string_with_custom_name(self, image):
        tileset = GBTileset.from_image(image)
        result = ""
        result += "extern const UINT8 FOO[];\n"
        result += "#define FOO_TILE_COUNT 5"
        assert tileset.to_c_header_string(name="Foo") == result

    def test_merge(self, image):
        tileset1 = GBTileset.from_image(image)
        tileset2 = GBTileset.from_image(image)
        tileset1.merge(tileset2)
        assert tileset1.length == 10

    def test_merge_with_dedup(self, image):
        tileset1 = GBTileset.from_image(image)
        tileset2 = GBTileset.from_image(image)
        tileset1.merge(tileset2, dedup=True)
        assert tileset1.length == 5

    def test_index(self, tile1):
        tileset = GBTileset()
        tileset.add_tile(tile1)
        assert tileset.index(tile1) == 0

    def test_index_with_offset(self, tile1):
        tileset = GBTileset(offset=10)
        tileset.add_tile(tile1)
        assert tileset.index(tile1) == 10

    def test_offset(self, tile1):
        tileset = GBTileset()
        tileset.add_tile(tile1)
        assert tileset.index(tile1) == 0
        tileset.offset = 10
        assert tileset.index(tile1) == 10
