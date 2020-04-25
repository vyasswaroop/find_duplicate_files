import hashlib, os, argparse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

def getAbsolutePath(fileName, fileDir):
    if fileDir != ".":
        return fileDir + "/" + fileName
    return fileName

def readByChunk(fileObj, chunkSize=1024000):
    while True:
        data = fileObj.read(chunkSize)
        if not data:
            return
        yield data

def groupBymd5Duplicates(group, fileDir):
    fileObjList = []
    for filename in group:
        fileObj =  open(getAbsolutePath(filename, fileDir), 'rb')
        fileObjList.append(fileObj)
    groupList = groupByChunkHash(fileObjList)
    refineList = []
    for group in groupList:
        itemList = []
        if len(group) > 1:
            for item in group:
                itemList.append(os.path.basename(item.name))
                item.close()
            refineList.append(itemList)
    return refineList

def groupByChunkHash(fileObjList):
    groupList = []
    unique = {}
    if len(fileObjList) == 1:
        return [fileObjList]
    for fileObj in fileObjList:
        try:
            chunk = next(readByChunk(fileObj))
            hash = hashlib.md5(chunk).hexdigest()
            del(chunk)
            if not unique.get(hash):
                unique[hash] = [fileObj]
            else:
                unique[hash].append(fileObj)
        except:
            if unique.get("nil"):
                unique["nil"].append(fileObj)
            else:
                unique["nil"] = [fileObj]
    for key, value in unique.items():
        if not key == "nil":
            group = groupByChunkHash(value)
            groupList.append(group[0])
        else:
            groupList.append(value)
    return groupList


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
        print(" ".join(filesList))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Find duplicate files.')
    parser.add_argument(
        'path', metavar='path',
        help='Directory path to search duplicate files.'
    )
    args = parser.parse_args()
    fileList = [filename for filename in os.listdir(args.path) if os.path.isfile(args.path + "/" +filename)]
    sizeSorted = groupBySize(args.path, fileList)
    sizeSorted = [item for item in sizeSorted if len(item) > 1]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(groupBymd5Duplicates, group, args.path) for group in sizeSorted]
        for future in as_completed(futures):
            displayDuplicates(future.result())
