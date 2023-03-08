import os

class Utils:
    @staticmethod
    def bytesToU16(buf, offset, isLE):
        num = 0
        for i in range(2):
            num <<= 8
            if isLE:
                num += buf[offset + 1 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToU32(buf, offset, isLE):
        num = 0
        for i in range(4):
            num <<= 8
            if isLE:
                num += buf[offset + 3 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToU64(buf, offset, isLE):
        num = 0
        for i in range(8):
            num <<= 8
            if isLE:
                num += buf[offset + 7 - i]
            else:
                num += buf[offset + i]
        return num
    def bytesToString(buf, offset, length):
        dest = bytearray(0)
        byte = bytearray(1)
        i = 0
        while length is None or i < length:
            if buf[offset + i] == 0:
                break
            byte[0] = buf[offset + i]
            dest += byte
            i += 1
        return dest.decode("UTF-8", errors="replace")
    def bytesToFile(buf, fileName):
        try:
            os.makedirs(os.path.dirname(fileName), exist_ok=True)
        except FileNotFoundError:
            pass
        try:
            f = open(fileName, 'wb')
            f.write(buf)
            f.close()
        except:
            return False
        else:
            return True
    def U16ToBytes(buf, offset, val, isLE):
        for i in range(2):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((1 - i) * 8)) & 0xFF
    def U32ToBytes(buf, offset, val, isLE):
        for i in range(4):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((3 - i) * 8)) & 0xFF
    def U64ToBytes(buf, offset, val, isLE):
        for i in range(8):
            if isLE:
                buf[offset + i] = (val >> (i * 8)) & 0xFF
            else:
                buf[offset + i] = (val >> ((7 - i) * 8)) & 0xFF
    def fileToBytes(fileName):
        try:
            f = open(fileName, 'rb')
            buf = f.read()
        except:
            return False
        else:
            return bytearray(buf)
    def stringToBytes(buf, offset, length, val):
        src = val.encode()
        i = 0
        while length is None or i < length:
            if len(val) <= i:
                if length is None:
                    break
                buf[offset + i] = 0
            else:
                buf[offset + i] = src[i]
            i += 1
    def memcpy(destBuf, destOffset, srcBuf, srcOffset, length):
        for i in range(length):
            destBuf[destOffset + i] = srcBuf[srcOffset + i]
    def findAllFiles(srcDir):
        for curDir, dirs, files in os.walk(srcDir):
            for file in files:
                yield os.path.join(curDir, file)
    def makeFileList(srcDir):
        dest = list()
        for file in Utils.findAllFiles(srcDir):
            dest.append(file)
        return dest
    def getLastSlashIndex(src):#srcの最後から一番近い"/"か"\"のインデックスを返す
        slashIndex = len(src) - 1
        while src[slashIndex] != "\\" and src[slashIndex] != "/":
            slashIndex = slashIndex - 1
            if slashIndex < 0:
                return slashIndex#見つからなかったら-1を返す
        return slashIndex
    def getDirName(src):
        slashIndex = Utils.getLastSlashIndex(src)
        if slashIndex < 0:
            return src
        return src[:slashIndex]
    def getFileName(src):
        slashIndex = Utils.getLastSlashIndex(src)
        if slashIndex < 0:
            return src
        return src[slashIndex + 1:]