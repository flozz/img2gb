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
