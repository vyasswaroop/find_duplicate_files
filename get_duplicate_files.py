import hashlib, os

unique = dict()
for filename in os.listdir('.'):
    if os.path.isfile(filename):
        filehash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        if not unique.get(filehash):
            unique[filehash] = [filename]
        else:
            unique[filehash].append(filename)
print(list(unique.values()))
