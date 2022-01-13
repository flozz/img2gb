import os.path

from .gbtile import GBTile
from .gbtileset import GBTileset
from .gbtilemap import GBTilemap
from .c_export import generate_c_file, generate_c_header_file
from .version import VERSION


def generate_tileset(
    input_images,
    output_c=None,
    output_h=None,
    output_image=None,
    name="TILESET",
    dedup=False,
    alternative_palette=False,
    sprite8x16=False,
):
    """Function that generates tileset's C file, C header and image from an
    input image.

    :param PIL.Image.Image|list input_images: The input image to generate the
            tileset from.
    :param file output_c: A file-like object where the C code will be generated
            (``None`` to not generate C code).
    :param file output_h: A file-like object where the C header (.h) code will
            be generated (``None`` to not generate C header code).
    :param file output_image: A file-like object where the image representing
            the tileset will be generated (``None`` to not generate the image).

            .. NOTE::

               The file must be openend in binary mode (``open("file", "wb")``)
               or you must be using a binary-compatible file-like object, like
               a :class:`io.BytesIO`.

    :param str name: The name of the tileset (will be used in the generated
            code, default = ``"TILESET"``)
    :param bool dedup: Deduplicate the tiles of the tileset (default =
            ``False``)
    :param bool alternative_palette: Use the sprite's alternative palette
            (inverted colors, default = ``False``)
    :param bool sprite8x16: Rearrange the tiles to be used in 8x16 sprites
            (default = ``False``).

    Example using files::

        from PIL import Image
        import img2gb

        image = Image.open("./my_tileset.png")
        c_file = open("example.c", "w")
        h_file = open("example.h", "w")
        image_file = open("example.png", "wb")

        img2gb.generate_tileset(
            [image],
            output_c=c_file,
            output_h=h_file,
            output_image=image_file,
            dedup=True)

        c_file.close()
        h_file.close()
        image_file.close()

    Example using file-like objects::

        from io import StringIO, BytesIO
        from PIL import Image
        import img2gb

        image = Image.open("./my_tileset.png")
        c_code_io = StringIO()
        h_code_io = StringIO()
        output_image = BytesIO()

        img2gb.generate_tileset(
            [image],
            output_c=c_code_io,
            output_h=h_code_io,
            output_image=output_image,
            dedup=True)

        # Print the C code for the example:
        c_code_io.seek(0)
        c_code = c_code_io.read()
        print(c_code)
    """
    if type(input_images) is not list:
        tileset = GBTileset.from_image(
            input_images,
            dedup=dedup,
            alternative_palette=alternative_palette,
            sprite8x16=sprite8x16,
        )
    else:
        tileset = GBTileset()
        for image in input_images:
            tileset.merge(
                GBTileset.from_image(
                    image,
                    alternative_palette=alternative_palette,
                    sprite8x16=sprite8x16,
                ),
                dedup=dedup,
            )

    if output_c:
        c_code = generate_c_file(tileset.to_c_string(name=name))
        output_c.write(c_code)

    if output_h:
        filename = "%s.h" % name.lower()
        if hasattr(output_h, "name"):
            filename = os.path.basename(output_h.name)
        h_code = generate_c_header_file(
            tileset.to_c_header_string(name=name), filename=filename
        )
        output_h.write(h_code)

    if output_image:
        image = tileset.to_image()
        image.save(output_image, "PNG")


def generate_tilemap(
    input_tileset,
    input_tilemap_image,
    output_c=None,
    output_h=None,
    name="TILEMAP",
    offset=0,
    missing="error",
    replace=0,
):
    """Function that generates tilemap's C file and C header from an input
    tileset and image.

    :param PIL.Image.Image input_tileset: The tileset that contains the tiles
            used in the tilemap.
    :param PIL.Image.Image input_tilemap_image: An image that represents the
            tilemap (its size must be a multiple of 8 and 256x256px maximum).
    :param file output_c: A file-like object where the C code will be generated
            (``None`` to not generate C code).
    :param file output_h: A file-like object where the C header (.h) code will
            be generated (``None`` to not generate C header code).
    :param str name: The name of the tilemap (will be used in the generated
            code, default = ``"TILEMAP"``).
    :param int offset: Offset where the tileset starts (useful only of you will
            load the given tileset at a place different from ``0`` in the
            GameBoy video memeory).
    :param string missing: Action to do if a tile of the tilemap is missing
            from the tileset:

            * ``"error"`` (default): raise an error,
            * ``"replace"``: replace the missing tile by an other one (see
              ``replace`` option).

    :param int replace: The id of the replacement tile when
            ``missing="replace"``.

    Example:

    .. code-block:: C

        from io import BytesIO
        from PIL import Image
        import img2gb

        image = Image.open("./my_tilemap.png")

        # Generate the tileset image from the tilemap image
        tileset_io = BytesIO()
        img2gb.generate_tileset(
            [image],
            output_image=tileset_io,
            dedup=True)
        tileset_io.seek(0)

        # Generate the tilemap
        tileset_image = Image.open(tileset_io)
        img2gb.generate_tilemap(
            tileset_image,
            image,
            output_c=open("tilemap.c", "w"),
            output_h=open("tilemap.h", "w"))

    """
    if missing == "append":
        raise ValueError("missing=append is not available from high level functions")

    tileset = GBTileset.from_image(input_tileset, dedup=False, offset=offset)
    tilemap = GBTilemap.from_image(
        input_tilemap_image,
        gbtileset=tileset,
        missing=missing,
        replace=replace,
    )

    if output_c:
        c_code = generate_c_file(tilemap.to_c_string(name=name))
        output_c.write(c_code)

    if output_h:
        filename = "%s.h" % name.lower()
        if hasattr(output_h, "name"):
            filename = os.path.basename(output_h.name)
        h_code = generate_c_header_file(
            tilemap.to_c_header_string(name=name), filename=filename
        )
        output_h.write(h_code)


__all__ = [
    "GBTile",
    "GBTileset",
    "GBTilemap",
    "generate_tileset",
    "generate_tilemap",
    "VERSION",
]
