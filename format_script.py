import codecs
import os
import game
from hacktools import common


def extract(data):
    infolder = data + "extract/"
    outfile = data + "out_translations/script-ja-JP.xliff"

    common.logMessage("Extracting SCRIPT to", "...")
    scriptfiles = []
    for file in common.getFiles(infolder, ".bin"):
        if "/script/" in file:
            scriptfiles.append(file)

    t = common.TranslationFile()
    for file in common.showProgress(scriptfiles):
        common.logDebug("Processing", file)
        filesize = os.path.getsize(infolder + file)
        strings, positions = common.extractBinaryStrings(infolder + file, [(0, filesize)], game.readShiftJIS)
        if len(strings) > 0:
            # Order strings
            unorderedstrings = []
            for i in range(len(strings)):
                for j in range(len(positions[i])):
                    unorderedstrings.append({"str": strings[i], "offset": positions[i][j]})
            # Write them to the file
            orderedstrings = sorted(unorderedstrings, key=lambda x: x["offset"]) 
            for i in range(len(orderedstrings)):
                sjis = orderedstrings[i]["str"]
                if sjis.endswith("|"):
                    sjis = sjis[:-1]
                if sjis != "":
                    t.addEntry(sjis, file, orderedstrings[i]["offset"])
    t.save(outfile, True)
    common.logMessage("Done!")
