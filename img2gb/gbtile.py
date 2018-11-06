class GBTile(object):

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
