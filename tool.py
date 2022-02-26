import os
import click
import game
from hacktools import common, nds, nitro

version = "0.1.0"
data = "GeassData/"
romfile = data + "geass.nds"
rompatch = data + "geass_patched.nds"
bannerfile = data + "repack/banner.bin"
patchfile = data + "patch.xdelta"
infolder = data + "extract/"
replacefolder = data + "replace/"
outfolder = data + "repack/"


@common.cli.command()
@click.option("--rom", is_flag=True, default=False)
@click.option("--narc", is_flag=True, default=False)
@click.option("--img", is_flag=True, default=False)
@click.option("--db", is_flag=True, default=False)
@click.option("--script", is_flag=True, default=False)
def extract(rom, narc, img, db, script):
    all = not rom and not narc and not img and not db and not script
    if all or rom:
        nds.extractRom(romfile, infolder, outfolder)
        # nds.extractRom(data + "geass_en.nds", data + "extract_en/", "dummy")
        common.logMessage("Decompressing files ...")
        for file in common.showProgress(common.getFiles(infolder + "data/", ".bin")):
            complength = os.path.getsize(infolder + "data/" + file)
            if complength < 4 or "script" in file:
                continue
            with common.Stream(infolder + "data/" + file, "rb") as f:
                firstbyte = f.readByte()
                if firstbyte == 0x10:
                    f.seek(0)
                    decomp = nds.decompress(f, complength)
                    with common.Stream(infolder + "data/" + file.replace(".bin", ".narc"), "wb") as f:
                        f.write(decomp)
        common.logMessage("Done!")
    if all or narc:
        common.logMessage("Decompressing archives ...")
        common.makeFolder(data + "extract_NARC/")
        for file in common.showProgress(common.getFiles(infolder + "data/", ".narc")):
            outfolder = data + "extract_NARC/" + file.replace(".narc", "")
            common.makeFolders(outfolder)
            nitro.extractNARCFile(infolder + "data/" + file, outfolder)
        common.logMessage("Done!")
    if all or img:
        nitro.extractIMG(infolder + "data/", data + "out_IMG/", [".NCGR", ".ncgr", ".chr"], readfunc=game.readImage)
        nitro.extractIMG(data + "extract_NARC/", data + "out_NIMG/", [".NCGR", ".ncgr", ".chr"], readfunc=game.readImage)
    if all or db:
        import format_db
        format_db.extract(data)
    if all or script:
        import format_script
        format_script.extract(data)


@common.cli.command()
@click.option("--no-rom", is_flag=True, default=False)
def repack(no_rom):
    all = True  # not sub and not dat and not bin and not img and not wsb
    if not no_rom:
        if os.path.isdir(replacefolder):
            common.mergeFolder(replacefolder, outfolder)
        # nds.editBannerTitle(bannerfile, "Something")
        nds.repackRom(romfile, rompatch, outfolder, patchfile)

if __name__ == "__main__":
    click.echo("GeassTranslation version " + version)
    if not os.path.isdir(data):
        common.logError(data, "folder not found.")
        quit()
    common.runCLI(common.cli)
