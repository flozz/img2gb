import pytest
from PIL import Image
from img2gb.gbtile import GBTile
from img2gb.gbtileset import GBTileset
from img2gb.gbtilemap import GBTilemap


class Test_GBTilemap(object):

    @pytest.fixture
    def image(self):
        return Image.open("./test/assets/tilemap.png")

    @pytest.fixture
    def tileset(self):
        image = Image.open("./test/assets/tileset.png")
        return GBTileset.from_image(image)

    @pytest.fixture
    def tile(self, image):
        return GBTile.from_image(image, 8, 0)

    def test_from_image(self, image):
        tilemap = GBTilemap.from_image(image)
        assert tilemap.tileset.length == 4
        assert tilemap.width == 8
        assert tilemap.height == 8

    def test_put_tile(self, tileset):
        tilemap = GBTilemap(gbtileset=tileset)
        assert tilemap.data[0] == 0
        tilemap.put_tile(0, 0, tileset.tiles[4])
        assert tilemap.data[0] == 4

    def test_to_hex_string(self, tileset):
        tilemap = GBTilemap(width=2, height=2)
        tilemap.put_tile(0, 0, tileset.tiles[0])
        tilemap.put_tile(1, 0, tileset.tiles[1])
        tilemap.put_tile(0, 1, tileset.tiles[2])
        tilemap.put_tile(1, 1, tileset.tiles[3])
        result = ""
        result += "00 01\n"
        result += "02 03"
        assert tilemap.to_hex_string() == result

    def test_tileset(self):
        tilemap = GBTilemap()
        assert type(tilemap.tileset) is GBTileset

    def test_width(self):
        tilemap = GBTilemap(width=2, height=3)
        assert tilemap.width == 2

    def test_height(self):
        tilemap = GBTilemap(width=2, height=3)
        assert tilemap.height == 3

    def test_size(self):
        tilemap = GBTilemap(width=2, height=3)
        assert tilemap.size == (2, 3)

    def test_data(self):
        tilemap = GBTilemap(width=2, height=2)
        assert type(tilemap.data) is list
        assert tilemap.data[0] == 0
        assert tilemap.data[1] == 0
        assert tilemap.data[2] == 0
        assert tilemap.data[3] == 0
