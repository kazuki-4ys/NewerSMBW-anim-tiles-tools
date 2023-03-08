import sys, os, shutil
from PIL import Image
from utils import Utils

def rgb5a3ToRgba(val):
    dest = bytearray(4)
    if (val & 0x8000) == 0x8000:
        dest[0] = ((val >> 10) & 0x1F) << 3
        dest[1] = ((val >> 5) & 0x1F) << 3
        dest[2] = (val & 0x1F) << 3
        dest[3] = 0xFF
    else:
        dest[0] = ((val >> 8) & 0xF) << 4
        dest[1] = ((val >> 4) & 0xF) << 4
        dest[2] = (val & 0xF) << 4
        dest[3] = ((val >> 12) & 7) << 5
    return dest

def rgbaTorgb5a3(val):
    dest = 0
    if val[3] == 0xFF:
        dest |= 0x8000
        dest |= ((val[0] >> 3) << 10)
        dest |= ((val[1] >> 3) << 5)
        dest |= (val[2] >> 3)
    else:
        dest |= ((val[3] >> 5) << 12)
        dest |= ((val[0] >> 4) << 8)
        dest |= ((val[1] >> 4) << 4)
        dest |= (val[2] >> 4)
    return dest

def pngPixelPosToTplPixelIndex(x, y):
    xTilePos = int(x / 4)
    yTilePos = int(y / 4)
    inXTilePos = x & 3
    inYTilePos = y & 3
    inTileTplPixelIndex = inYTilePos * 4 + inXTilePos
    tilePixelIndex = yTilePos * 8 + xTilePos
    return tilePixelIndex * 16 + inTileTplPixelIndex

def getPixelFromRawTpl(raw, x, y):
    index = pngPixelPosToTplPixelIndex(x, y)
    return rgb5a3ToRgba(Utils.bytesToU16(raw, index * 2, False))

def decodeBinToFolder(raw, folder):
    count = int(len(raw) / (32 * 32 * 2))
    for i in range(count):
        srcImg = Image.new("RGBA", (32, 32), color=(0, 0, 0, 0))
        for y in range(32):
            for x in range(32):
                curPixel = getPixelFromRawTpl(raw, x, y + i * 32)
                srcImg.putpixel((x, y),(curPixel[0], curPixel[1], curPixel[2], curPixel[3]))
        destImg = srcImg.crop((4, 4, 28, 28))
        destImg.save(folder + "/" + str(i) + ".png")

def encodeBinFromFolder(folder):
    count = 0
    while True:
        if os.path.isfile(folder + "/" + str(count) + ".png"):
            count += 1
        else:
            break
    if count == 0:
        return None
    destRaw = bytearray(count * 32 * 32 * 2)
    srcImg = Image.new("RGBA", (32, 32 * count), color=(0, 0, 0, 0))
    for i in range(count):
        try:
            curImg = Image.open(folder + "/" + str(i) + ".png")
            srcImg.paste(curImg, (4, 4 + i * 32))
        except:
            return None
    for y in range(count * 32):
        for x in range(32):
            r, g, b, a = srcImg.getpixel((x, y))
            pixel = bytearray(4)
            pixel[0] = r
            pixel[1] = g
            pixel[2] = b
            pixel[3] = a
            index = pngPixelPosToTplPixelIndex(x, y)
            Utils.U16ToBytes(destRaw, index * 2, rgbaTorgb5a3(pixel), False)
    return destRaw


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("    " + sys.argv[0] + " d <nsmbw animation tex file> <png files output folder>")
        print("    " + sys.argv[0] + " e <png files input folder> <nsmbw animation tex file>")
        sys.exit()
    if sys.argv[1] == "d":
        raw = Utils.fileToBytes(sys.argv[2])
        if raw is None:
            print("error: cannot open " + sys.argv[2])
            sys.exit()
        if os.path.exists(sys.argv[3]):
            shutil.rmtree(sys.argv[3])
        os.mkdir(sys.argv[3])
        decodeBinToFolder(raw, sys.argv[3])
    elif sys.argv[1] == "e":
        rawDest = encodeBinFromFolder(sys.argv[2])
        if Utils.bytesToFile(rawDest, sys.argv[3]) == False:
            print("error: cannot write to " + sys.argv[3])
    else:
        print("error: invalid command")