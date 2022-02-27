import codecs
import os
import game
from hacktools import common


def extract(data):
    infolder = data + "extract/"

    scriptfiles = []
    for file in common.getFiles(infolder, ".bin"):
        if "/script/" in file:
            scriptfiles.append(file)

    common.logMessage("Extracting SCRIPT ...")
    with codecs.open(data + "script_output.txt", "w", "utf-8") as out:
        for file in common.showProgress(scriptfiles):
            common.logDebug("Processing", file)
            filesize = os.path.getsize(infolder + file)
            strings, positions = common.extractBinaryStrings(infolder + file, [(0, filesize)], game.readShiftJIS)
            if len(strings) > 0:
                out.write("!FILE:" + file + "\n")
                for i in range(len(strings)):
                    sjis = strings[i]
                    if sjis.endswith("|"):
                        sjis = sjis[:-1]
                    if sjis != "":
                        out.write(sjis + "=\n")
    common.logMessage("Done!")
