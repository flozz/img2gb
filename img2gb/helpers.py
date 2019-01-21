from PIL import Image


def rgba_brightness(r, g, b, a=None):
    if a is not None and a < 128:
        return 255
    return max(r, g, b)


def brightness_to_color_id(brightness, invert=False):
    if brightness > 240:
        return 0 if not invert else 3
    if brightness < 15:
        return 3 if not invert else 0
    if brightness < 128:
        return 2 if not invert else 1
    return 1 if not invert else 2


def to_pil_rgb_image(image):
    if image.mode == "RGB":
        return image

    image.load()
    rgb_image = Image.new("RGB", image.size, (0x00, 0x00, 0x00))
    mask = None

    if image.mode == "RGBA":
        mask = image.split()[3]  # bands: R=0, G=1, B=2, 1=3

    rgb_image.paste(image, mask=mask)

    return rgb_image


def tileset_iterator(width, height, sprite8x16=False):
    for y in range(0, height, 16 if sprite8x16 else 8):
        for x in range(0, width, 8):
            for d in (0, 8) if sprite8x16 else (0,):
                yield x, y + d
