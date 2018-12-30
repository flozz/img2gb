import pytest
from PIL import Image
from img2gb.gbtile import GBTile
from img2gb.gbtileset import GBTileset


class Test_GBTileset(object):

    @pytest.fixture
    def image(self):
        return Image.open("./test/assets/tileset.png")

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

    def test_add_tile(self, tile1):
        tileset = GBTileset()
        assert tileset.add_tile(tile1) == 0
        assert tileset.add_tile(tile1) == 1

    def test_add_tile_with_deduplication(self, tile1, tile2):
        tileset = GBTileset()
        assert tileset.add_tile(tile1, dedup=True) == 0
        assert tileset.add_tile(tile1, dedup=True) == 0
        assert tileset.add_tile(tile2, dedup=True) == 1

    def test_to_hex_string(self, tile2):
        tileset = GBTileset()
        assert tileset.to_hex_string() == ""
        tileset.add_tile(tile2)
        assert tileset.to_hex_string() == "80 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00"  # noqa

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
