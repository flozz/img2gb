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

    def test_put_tile_with_offset(self, tileset):
        tileset.offset = 10
        tilemap = GBTilemap(gbtileset=tileset)
        assert tilemap.data[0] == 0
        tilemap.put_tile(0, 0, tileset.tiles[4])
        assert tilemap.data[0] == 14

    @pytest.mark.parametrize(
        "x,y",
        [
            (-1, 0),
            (0, -1),
            (8, 0),
            (0, 8),
        ],
    )
    def test_put_tile_with_out_of_map_coord(self, tile, x, y):
        tilemap = GBTilemap(width=8, height=8)
        with pytest.raises(ValueError):
            tilemap.put_tile(x, y, tile)

    def test_put_tile_with_missing_append(self, tile):
        tilemap = GBTilemap()
        tilemap.put_tile(0, 0, tile, missing="append")
        assert tilemap.tileset.length == 1

    def test_put_tile_with_missing_error(self, tile):
        tilemap = GBTilemap()
        with pytest.raises(ValueError):
            tilemap.put_tile(0, 0, tile, missing="error")

    def test_put_tile_with_missing_replace(self, tile):
        tilemap = GBTilemap()
        tilemap.put_tile(0, 0, tile, missing="replace", replace=42)
        assert tilemap.data[0] == 42

    def test_put_tile_with_missing_set_to_wrong_value(self, tile):
        tilemap = GBTilemap()
        with pytest.raises(ValueError):
            tilemap.put_tile(0, 0, tile, missing="foo")

    def test_put_tile_with_missing_append_and_dedup_true(self, tile):
        tilemap = GBTilemap()
        tilemap.put_tile(0, 0, tile, missing="append", dedup=True)
        tilemap.put_tile(0, 0, tile, missing="append", dedup=True)
        assert tilemap.tileset.length == 1

    def test_put_tile_with_missing_append_and_dedup_false(self, tile):
        tilemap = GBTilemap()
        tilemap.put_tile(0, 0, tile, missing="append", dedup=False)
        tilemap.put_tile(0, 0, tile, missing="append", dedup=False)
        assert tilemap.tileset.length == 2

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

    def test_to_c_string(self):
        tilemap = GBTilemap(width=4, height=4)
        result = "const UINT8 TILEMAP[] = {\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "};"
        assert tilemap.to_c_string() == result

    def test_to_c_string_with_custom_name(self):
        tilemap = GBTilemap(width=4, height=4)
        result = "const UINT8 FOO[] = {\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "    0x00, 0x00, 0x00, 0x00,\n"
        result += "};"
        assert tilemap.to_c_string(name="Foo") == result

    def test_to_c_header_string(self):
        tilemap = GBTilemap(width=4, height=4)
        result = "extern const UINT8 TILEMAP[];\n"
        result += "#define TILEMAP_WIDTH 4\n"
        result += "#define TILEMAP_HEIGHT 4"
        assert tilemap.to_c_header_string() == result

    def test_to_c_header_string_with_custom_name(self):
        tilemap = GBTilemap(width=4, height=4)
        result = "extern const UINT8 FOO[];\n"
        result += "#define FOO_WIDTH 4\n"
        result += "#define FOO_HEIGHT 4"
        assert tilemap.to_c_header_string(name="Foo") == result

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
