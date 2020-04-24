import hashlib, os, argparse

def getAbsolutePath(fileName, fileDir):
    if fileDir != ".":
        return fileDir + "/" + fileName
    return fileName

def readByChunk(fileObj, chunkSize=1024):
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            return
        yield data

def hashFileByChunk(fileObj):
    hashChunk = []
    for chunk in readByChunk(fileObj):
        hashChunk.append(hashlib.md5(chunk).hexdigest())
    return tuple(hashChunk)

def groupBymd5(group, fileDir):
    unique = {}
    for filename in group:
        with open(getAbsolutePath(filename, fileDir), 'rb') as fileObj:
            filehash = hashFileByChunk(fileObj)
        if not filehash in unique:
            unique[filehash] = [filename]
        else:
            unique[filehash].append(filename)
    return list(unique.values())

def groupBySize(fileDir, fileList):
    unique = {}
    for filename in fileList:
        filesize = os.path.getsize(getAbsolutePath(filename, fileDir))
        if not unique.get(filesize):
            unique[filesize] = [filename]
        else:
            unique[filesize].append(filename)
    return list(unique.values())

def displayDuplicates(sortedFiles):
    for filesList in sortedFiles:
        if len(filesList) != 1 :
            print(" ".join(filesList))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Find duplicate files.')
    parser.add_argument(
        'path', metavar='N',
        help='an integer for the accumulator'
    )
    args = parser.parse_args()
    hashSorted = []
    fileList = [filename for filename in os.listdir(args.path) if os.path.isfile(args.path + "/" +filename)]
    sizeSorted = groupBySize(args.path, fileList)
    for group in sizeSorted:
        displayDuplicates(groupBymd5(group, args.path))
