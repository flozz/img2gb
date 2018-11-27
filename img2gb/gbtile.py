from .helpers import (
        to_pil_rgb_image,
        rgba_brightness,
        brightness_to_color_id)


class GBTile(object):

    @classmethod
    def from_image(Cls, pil_image, tile_x=0, tile_y=0):
        image = to_pil_rgb_image(pil_image)
        tile = Cls()

        for y in range(8):
            for x in range(8):
                pix_rgb = image.getpixel((tile_x + x, tile_y + y))
                pix_brightness = rgba_brightness(*pix_rgb)
                color_id = brightness_to_color_id(pix_brightness)
                tile.put_pixel(x, y, color_id)

        return tile

    def __init__(self):
        self.data = [0x00] * 16

    def put_pixel(self, x, y, color_id):
        mask = 0b00000001 << (7 - x)
        mask1 = mask if color_id & 0b01 else 0b00000000
        mask2 = mask if color_id & 0b10 else 0b00000000

        # Clear changing bits
        self.data[y*2+0] &= ~mask
        self.data[y*2+1] &= ~mask

        # Set bits
        self.data[y*2+0] |= mask1
        self.data[y*2+1] |= mask2

    def to_hex_string(self):
        return " ".join(["%02X" % b for b in self.data])

    def __eq__(self, other):
        if not isinstance(other, GBTile):
            return False
        return self.to_hex_string() == other.to_hex_string()
