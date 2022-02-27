import math
import os
from hacktools import common, nitro


def readImage(infolder, file, extension):
    # Extensions can be lowercase or uppercase
    palettefile = file.replace(extension, ".NCLR")
    if not os.path.isfile(infolder + palettefile):
        palettefile = file.replace(extension, ".nclr")
    mapfile = file.replace(extension, ".NSCR")
    if not os.path.isfile(infolder + mapfile):
        mapfile = file.replace(extension, ".nscr")
    cellfile = file.replace(extension, ".NCER")
    if not os.path.isfile(infolder + cellfile):
        cellfile = file.replace(extension, ".ncer")
    # Sometimes palettes are stored ina raw ".pal" file
    if not os.path.isfile(infolder + palettefile):
        palettefile = file.replace(extension, ".pal")
        if not os.path.isfile(infolder + palettefile):
            common.logError("Palette", palettefile, "not found")
            return [], None, None, None, 0, 0, "", ""
        palette = []
        with common.Stream(infolder + palettefile, "rb") as f:
            pallen = f.readUInt()
            for i in range(pallen // 2):
                palette.append(common.readPalette(f.readUShort()))
        palettes = {0: palette}
    else:
        palettes = nitro.readNCLR(infolder + palettefile)
    if extension == ".chr":
        image = nitro.NCGR()
        image.tiles = []
        image.bpp = 8 if len(palettes[0]) > 16 else 4
        image.tilesize = 8
        with common.Stream(infolder + file, "rb") as f:
            image.tilelen = f.readUInt() - 4
            try:
                last3 = int(file[-7:-4])
            except ValueError:
                last3 = 0
            if "knightmare" in file:
                image.width = 80
                image.height = 80
            elif "au_bg" in file and last3 >= 583 and last3 <= 590:
                image.width = 256
                image.height = 200
            elif "au_bg" in file and last3 >= 606 and last3 < 626:
                image.width = 256
                image.height = 200
            elif "au_bg" in file:
                image.width = 272
                image.height = 216
            else:
                if "chiba/status/bg/pilot" in file or "ohshima/bg/status" in file:
                    image.width = 80
                else:
                    image.width = 256
                image.height = math.floor(image.tilelen / (64 if image.bpp == 8 else 32) / (image.width / 8)) * 8
            tiledata = f.read(image.tilelen)
            nitro.readNCGRTiles(image, tiledata)
        return palettes, image, None, None, image.width, image.height, mapfile, cellfile
    # Read tiles
    image = nitro.readNCGR(infolder + file)
    width = image.width
    height = image.height
    # Read maps
    map = None
    if os.path.isfile(infolder + mapfile):
        map = nitro.readNSCR(infolder + mapfile)
        width = map.width
        height = map.height
    # Read banks
    cell = None
    if os.path.isfile(infolder + cellfile):
        cell = nitro.readNCER(infolder + cellfile)
    return palettes, image, map, cell, width, height, mapfile, cellfile


def readShiftJIS(f, encoding="shift_jis"):
    try:
        ret = common.detectEncodedString(f, encoding)
    except:
        return ""
    ret = ret.replace("\\n", "|")
    return ret
