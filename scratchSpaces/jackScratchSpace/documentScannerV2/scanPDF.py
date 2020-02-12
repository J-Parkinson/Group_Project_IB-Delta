from tempfile import NamedTemporaryFile
import fitz
from scanFuncNew import scanImage
from os import listdir

##TODO: THE USER MUST INSTALL POPPLER

def scanPDF(source, destFolder, filename, suffix, offset=0):

    allImages = fitz.open(source)
    for x, page in enumerate(allImages):
        with NamedTemporaryFile(suffix=suffix) as temp:
            page.getPixmap().writePNG(temp.name)
            scanImage(temp.name, destFolder + filename + str(x + offset) + suffix)
    return len(allImages)

def scanDirectoryOfPDFsAndImagesInAlphaOrder(directory, destFolder, filename, suffix):
    countNoImages = 0

    for file in listdir(directory):
        currentFilename = file.lower()

        if currentFilename.endswith(".pdf"):

            countNoImages += scanPDF(directory + currentFilename, destFolder, filename, suffix, countNoImages)

        elif currentFilename.endswith((".png", ".jpg", ".jpeg")):

            scanImage(directory + currentFilename, destFolder + filename + str(countNoImages) + suffix)
            countNoImages += 1

        else:
            continue
    return


scanPDF("images/logbook.png", "images/pdftest4/", "image", ".png")
#scanPDF("images/Scan 5 Feb 2020 at 14.57 (1).pdf", "images/pdftest3/", "image", ".png")
#scanDirectoryOfPDFsAndImagesInAlphaOrder("images/New Scans/", "images/pdftest2/", "image", ".png")