from tempfile import NamedTemporaryFile
import fitz
from scanFuncNew import findLinesandNormalise#, scanImage
from os import listdir, makedirs, path
from sys import stderr


def safeMakeDir(dir):
    if not path.exists(dir):
        makedirs(dir)
    else:
        stderr.write("Path " + dir + " already exists.\n")
        stderr.flush()

def pdfToImages(source, destFolder, filename, suffix, offset=0):

    safeMakeDir(destFolder[:-1])

    allImages = fitz.open(source)
    for x, page in enumerate(allImages):
        with NamedTemporaryFile(suffix=suffix) as temp:
            page.getPixmap().writePNG(temp.name)
            #scanImage(temp.name, destFolder + filename + str(x + offset) + suffix)
            safeMakeDir(destFolder + "Page " + str(x + offset))
            findLinesandNormalise(temp.name, destFolder + "Page " + str(x + offset) + "/")
    return len(allImages)

def directoryMixedToDirectoryImages(directory, destFolder, filename, suffix):
    countNoImages = 0

    for file in listdir(directory):
        currentFilename = file.lower()

        if currentFilename.endswith(".pdf"):

            countNoImages += pdfToImages(directory + currentFilename, destFolder, filename, suffix, countNoImages)

        elif currentFilename.endswith((".png", ".jpg", ".jpeg")):

            safeMakeDir(destFolder + "Page " + str(countNoImages))

            #scanImage(directory + currentFilename, destFolder + filename + str(countNoImages) + suffix)
            findLinesandNormalise(directory + currentFilename, destFolder + "Page " + str(countNoImages) + "/")
            countNoImages += 1

        else:
            continue
    return

pdfToImages("images/scantest.pdf", "images/pdftest/", "image", ".png")

#directoryMixedToDirectoryImages("images/New Scans Small/", "images/segmentedImagesOut/", "image", ".png")