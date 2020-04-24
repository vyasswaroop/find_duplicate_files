import hashlib, os

def getChunk(file, chunkSize=1024):
    with open(file, 'rb') as fileObj:
        chunk = fileObj.read(chunkSize)
        return hashlib.md5(chunk).hexdigest()

def groupBymd5(group):
    unique = {}
    for filename in group:
        filehash = getChunk(filename)
        filehash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        if not unique.get(filehash):
            unique[filehash] = [filename]
        else:
            unique[filehash].append(filename)
    print(list(unique.values()))
    return unique

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
        groupBymd5(group)
