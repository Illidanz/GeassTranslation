import codecs
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
            common.logMessage(file)
            # TODO
    common.logMessage("Done!")


def readShiftJIS(f):
    return common.detectEncodedString(f, "shift_jis")
