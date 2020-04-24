import hashlib, os

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

def groupBymd5(group):
    unique = {}
    for filename in group:
        with open(filename, 'rb') as fileObj:
            filehash = hashFileByChunk(fileObj)
        if not filehash in unique:
            unique[filehash] = [filename]
        else:
            unique[filehash].append(filename)
    return list(unique.values())

def groupBySize(fileList):
    unique = {}
    for filename in fileList:
        filesize = os.path.getsize(filename)
        if not unique.get(filesize):
            unique[filesize] = [filename]
        else:
            unique[filesize].append(filename)
    return list(unique.values())

if __name__=='__main__':
    fileList = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
    groupList = groupBySize(fileList)
    for group in groupList:
        print(groupBymd5(group))
