CLI
===

Main CLI
--------

::

    usage: img2gb [-h] [-V] {tileset,tilemap} ...

    Converts images to GameBoy tilesets and tilemaps

    positional arguments:
      {tileset,tilemap}
        tileset          Generates GameBoy tilesets
        tilemap          Generates GameBoy tilemaps

    optional arguments:
      -h, --help         show this help message and exit
      -V, --version      show program's version number and exit


Tileset CLI
-----------

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
      -b FILE, --output-binary FILE
                            output binary file
      -d, --deduplicate     remove duplicated tiles from the tileset
      -a, --alternative-palette
                            invert the colors to allow tiles to be used with the
                            sprites alternative palette
      -s, --sprite8x16      Rearrange the tiles to be used in 8x16 sprites
      -n NAME, --name NAME  name of the tileset (used for variable names in
                            generated code, default=TILESET)

Tilemap CLI
-----------

::

    usage: img2gb tilemap [-h] [-c FILE] [-H FILE] [-o OFFSET]
                          [-m {error,replace}] [-r TILE_ID] [-n NAME]
                          tileset tilemap

    positional arguments:
      tileset               the tileset (generated by img2gb tileset -i)
      tilemap               an image representing the tilemap

    optional arguments:
      -h, --help            show this help message and exit
      -c FILE, --output-c-file FILE
                            output C file
      -H FILE, --output-header-file FILE
                            output C header file
      -b FILE, --output-binary FILE
                            output binary file
      -o OFFSET, --offset OFFSET
                            offset of the tileset in the video memory (default =
                            0)
      -m {error,replace}, --missing {error,replace}
                            action to do when a tile of the tilemap is missing
                            from the tileset (default = error)
      -r TILE_ID, --replace TILE_ID
                            replace missing tiles by the given one when
                            --missing=replace
      -n NAME, --name NAME  name of the tileset (used for variable names in
                            generated code, default=TILEMAP)
