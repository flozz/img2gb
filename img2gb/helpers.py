from PIL import Image


def rgba_brightness(r, g, b, a=None):
    if a is not None and a < 128:
        return 255
    return max(r, g, b)


def brightness_to_color_id(brightness):
    if brightness > 240:
        return 0
    if brightness < 15:
        return 3
    if brightness < 128:
        return 2
    return 1


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
