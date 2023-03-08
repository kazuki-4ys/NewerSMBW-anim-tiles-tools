from utils import Utils
import json, sys

def makeOneEntryDict(raw, offset):
    dest = dict()
    dest["tex_name"] = Utils.bytesToString(raw, Utils.bytesToU16(raw, offset, False), None)
    frameDelayOffset = Utils.bytesToU16(raw, offset + 2, False)
    frameDelay = list()
    while True:
        fd = raw[frameDelayOffset]
        if fd == 0:
            break
        frameDelay.append(fd)
        frameDelayOffset += 1
    dest["frame_delay"] = frameDelay
    dest["tile_num"] = Utils.bytesToU16(raw, offset + 4, False)
    dest["tileset_num"] = raw[offset + 6]
    dest["reverse"] = True
    if raw[offset + 7] == 0:
        dest["reverse"] = False
    return dest

def decodeNwra(raw, destFilePath):
    if Utils.bytesToU32(raw, 0, False) != 0x4E575261:
        print("error: invalid file")
        return
    entryCount = Utils.bytesToU32(raw, 4, False)
    dictArray = list()
    for i in range(entryCount):
        dictArray.append(makeOneEntryDict(raw, 8 + i * 8))
    jsonDict = dict()
    jsonDict["anim_tiles"] = dictArray
    with open(destFilePath, "w") as f:
        json.dump(jsonDict, f, indent=4)

def encodeNwra(jsonFile):
    f = open(jsonFile, "r")
    jsonDict = json.load(f)
    dictEntries = jsonDict["anim_tiles"]
    count = len(dictEntries)
    destFileWithoutPool = bytearray(count * 8 + 8)
    curStringPoolOffset = 0
    curFrameDelayOffset = 0
    stringPoolOffsets = list()
    frameDelayPoolOffsets = list()
    Utils.U32ToBytes(destFileWithoutPool, 0, 0x4E575261, False)
    Utils.U32ToBytes(destFileWithoutPool, 4, count, False)
    for i in range(count):
        stringPoolOffsets.append(curStringPoolOffset)
        curStringPoolOffset += (len(dictEntries[i]["tex_name"]) + 1)
        frameDelayPoolOffsets.append(curFrameDelayOffset)
        curFrameDelayOffset += (len(dictEntries[i]["frame_delay"]) + 1)
        Utils.U16ToBytes(destFileWithoutPool, 8 + i * 8 + 4, dictEntries[i]["tile_num"],  False)
        destFileWithoutPool[8 + i * 8 + 6] = dictEntries[i]["tileset_num"]
        if dictEntries[i]["reverse"]:
            destFileWithoutPool[8 + i * 8 + 7] = 1
    destFileStringPool = bytearray(curStringPoolOffset)
    destFileFrameDelayPool = bytearray(curFrameDelayOffset)
    for i in range(count):
        Utils.U16ToBytes(destFileWithoutPool, 8 + i * 8 + 0, stringPoolOffsets[i] + len(destFileWithoutPool), False)
        Utils.stringToBytes(destFileStringPool, stringPoolOffsets[i], None, dictEntries[i]["tex_name"])
        Utils.U16ToBytes(destFileWithoutPool, 8 + i * 8 + 2, frameDelayPoolOffsets[i] + len(destFileWithoutPool) + len(destFileStringPool), False)
        for j in range(len(dictEntries[i]["frame_delay"])):
            destFileFrameDelayPool[frameDelayPoolOffsets[i] + j] = dictEntries[i]["frame_delay"][j]
    return destFileWithoutPool + destFileStringPool + destFileFrameDelayPool
    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("    " + sys.argv[0] + " d AnimTiles.bin <decoded json file output path>")
        print("    " + sys.argv[0] + " e <json file input path> AnimTiles.bin")
        sys.exit()
    if sys.argv[1] == "d":
        raw = Utils.fileToBytes(sys.argv[2])
        if raw is None:
            print("error: cannot open " + sys.argv[2])
            sys.exit()
        decodeNwra(raw, sys.argv[3])
    elif sys.argv[1] == "e":
        raw = encodeNwra(sys.argv[2])
        if Utils.bytesToFile(raw, sys.argv[3]) == False:
            print("error: cannot write to " + sys.argv[3])
    else:
        print("error: invalid command")
