import pytest
from PIL import Image
from img2gb.gbtile import GBTile


class Test_GBTile(object):
    @pytest.fixture
    def image(self):
        return Image.open("./test/assets/tileset.png")

    @pytest.mark.parametrize(
        "x,result",
        [
            (0, "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"),
            (8, "FF 01 81 7F BD 7F A5 7B A5 7B BD 63 81 7F FF FF"),
            (16, "7E 00 81 7F 81 7F 81 7F 81 7F 81 7F 81 7F 7E 7E"),
            (24, "3C 00 54 2A A3 5F C1 3F 83 7F C5 3F 2A 7E 3C 3C"),
            (32, "04 04 04 04 0A 0A 12 12 66 00 99 77 99 77 66 66"),
        ],
    )
    def test_from_image(self, image, x, result):
        tile = GBTile.from_image(image, x)
        assert tile.to_hex_string() == result

    def test_put_pixel(self):
        tile = GBTile()

        for b in tile.data:
            assert b == 0

        tile.put_pixel(0, 0, 3)

        assert tile.data[0] == 0x80
        assert tile.data[1] == 0x80

        tile.put_pixel(4, 0, 2)

        assert tile.data[0] == 0x80
        assert tile.data[1] == 0x88

    def test_get_pixel(self, image):
        tile = GBTile.from_image(image, 32)
        assert tile.get_pixel(0, 0) == 0b00
        assert tile.get_pixel(0, 6) == 0b01
        assert tile.get_pixel(2, 6) == 0b10
        assert tile.get_pixel(5, 0) == 0b11

    def test_to_hex_string(self):
        tile = GBTile()

        assert tile.to_hex_string() == "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"

        tile.put_pixel(0, 0, 3)
        tile.put_pixel(1, 0, 3)

        assert tile.to_hex_string() == "C0 C0 00 00 00 00 00 00 00 00 00 00 00 00 00 00"

    def test_to_image(self, image):
        tile = GBTile.from_image(image, 32)
        tile_image = tile.to_image()
        assert tile_image.getpixel((0, 0)) == 0b00
        assert tile_image.getpixel((0, 6)) == 0b01
        assert tile_image.getpixel((2, 6)) == 0b10
        assert tile_image.getpixel((5, 0)) == 0b11

    def test_gbtile_equality(self):
        tile1 = GBTile()
        tile2 = GBTile()

        assert tile1 == tile2

        tile1.put_pixel(0, 0, 3)

        assert tile1 != tile2

        tile2.put_pixel(0, 0, 3)

        assert tile1 == tile2

    def test_data(self):
        tile = GBTile()
        assert len(tile.data) == 16
        assert tile.data[0] == 0x00
        assert tile.data[1] == 0x00
        tile.put_pixel(0, 0, 3)
        assert tile.data[0] == 0x80
        assert tile.data[1] == 0x80
