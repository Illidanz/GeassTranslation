import codecs
from hacktools import common


def extract(data):
    infolder = data + "extract/"

    dbfiles = []
    for file in common.getFiles(infolder, ".bin"):
        if "database" in file:
            dbfiles.append(file)

    common.logMessage("Extracting DB ...")
    with codecs.open(data + "db_output.txt", "w", "utf-8") as out:
        for file in common.showProgress(dbfiles):
            if "bdb_enpt" in file or "bdb_EXP" in file or "bdb_wpef" in file or "mdb_achieve." in file or "mdb_chart_charaflag" in file:
                continue
            if "mdb_evo" in file:
                continue
            startoff = 8
            if "bdb_pcpm" in file:
                startoff = 7
            with common.Stream(infolder + file, "rb") as f:
                out.write("!FILE:" + file + "\n")
                datalen = f.readUInt()
                datanum = f.readUInt()
                for i in range(datanum):
                    f.seek(startoff + datalen * i)
                    stroffs = [0x2]
                    if "bdb_pcpm" in file:
                        f.readByte()
                        num = f.readByte()
                    elif "mdb_scenarioname" in file or "bdb_BG" in file or "bdb_emes" in file or "bdb_enmy" in file or "bdb_enpt" in file or "bdb_kf" in file or "bdb_pmes" in file or "bdb_prot" in file:
                        stroffs = [0x1]
                        num = f.readByte()
                    elif "cg_endroll" in file:
                        num = i
                    elif "mdb_opmp" in file:
                        stroffs = [0x4]
                        num = f.readUInt()
                    else:
                        num = f.readUShort()
                    if "mdb_wp" in file or "mdb_char_database" in file:
                        stroffs = [0x4]
                        f.readUShort()
                    if i != num:
                        common.logError("Malformed database file", file, common.toHex(f.tell()), i, num)
                        break
                    if "bdb_pcpm" in file:
                        stroffs += [0x2b, 0x3f, 0x53]
                    elif "mdb_opmp" in file:
                        stroffs += [0x30, 0x54, 0x78]
                    elif "bdb_prot" in file:
                        stroffs += [0x2a, 0x3e, 0x52]
                    elif "mdb_char_database" in file:
                        stroffs += [0x2c, 0x45, 0x5e, 0x77, 0x90]
                    elif "mdb_item" in file:
                        stroffs += [0x20, 0x35, 0x4a, 0x6a, 0x8a]
                    elif "bdb_emes" in file or "bdb_pmes" in file:
                        stroffs += [0x18, 0x58, 0x98, 0xd8, 0x118, 0x158, 0x198, 0x1d8, 0x218, 0x258, 0x298, 0x2d8, 0x318, 0x358, 0x398]
                    for stroff in stroffs:
                        f.seek(startoff + datalen * i + stroff)
                        dbstr = readShiftJIS(f)
                        if len(dbstr) > 1 and dbstr.endswith("|"):
                            dbstr = dbstr[:-1]
                        if dbstr != "":
                            out.write(dbstr + "=\n")
    common.logMessage("Done!")


def readShiftJIS(f):
    return common.detectEncodedString(f, "shift_jis")
