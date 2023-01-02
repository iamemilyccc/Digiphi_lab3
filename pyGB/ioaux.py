import os

def getTxtFiles(dataDir):
    files = []
    for _, _, fnames in os.walk(dataDir):
        for f in fnames:
            if f.endswith(".txt"):
                files.append(f)
    files.sort()
    return files