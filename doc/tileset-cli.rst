Tileset CLI
===========

::

    usage: img2gb tileset [-h] [-c FILE] [-H FILE] [-i FILE] [-d] [-a] [-n NAME]
                          image [image ...]

    positional arguments:
      image                 input image file

    optional arguments:
      -h, --help            show this help message and exit
      -c FILE, --output-c-file FILE
                            output C file
      -H FILE, --output-header-file FILE
                            output C header file
      -i FILE, --output-image FILE
                            output image file representing the tileset (required
                            to generate a tilemap)
      -d, --deduplicate     remove duplicated tiles from the tileset
      -a, --alternative-palette
                            invert the colors to allow tiles to be used with the
                            sprites alternative palette
      -s, --sprite8x16      Rearrange the tiles to be used in 8x16 sprites
      -n NAME, --name NAME  name of the tileset (used for variable names in
                            generated code, default=TILESET)
