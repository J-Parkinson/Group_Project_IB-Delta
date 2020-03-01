''' splitCellsAndNormalise
    Normalises the image, splits into cells, performs word detection, deslants words, and resizes ready for our NN.
    Returns a directory for the images to be word-detected.
'''

'''def safeMakeDir(dir):
    if not path.exists(dir):
        makedirs(dir)
    else:
        stderr.write("Path " + dir + " already exists.\n")
        stderr.flush()'''

'''def pdfToImages(source, destFolder, filename, suffix, offset=0):

    safeMakeDir(destFolder[:-1])

    allImages = fitz.open(source)
    for x, page in enumerate(allImages):
        with NamedTemporaryFile(suffix=suffix) as temp:
            page.getPixmap().writePNG(temp.name)
            #scanImage(temp.name, destFolder + filename + str(x + offset) + suffix)
            safeMakeDir(destFolder + "Page " + str(x + offset))
            findLinesandNormalise(temp.name, destFolder + "Page " + str(x + offset) + "/")
    return len(allImages)'''



''' handleColumns
    Checks with the user if the columns are in the correct location, and returns the new user-made columns
    Returns user-checked columns
'''


'''def handleColumns(cols, height, image):
    columnObjects = PageLayout(1)
    for x in range(0, len(cols) - 2):
        newColumn = Column((cols[x], 0), (cols[x + 1], height), 0, "COLUMN NAME HERE")
        columnObjects.addColumn(newColumn)

    newCols = queryUserAboutColumns(columnObjects)

    maxY, maxX, minY, minX = 0

    for columm in newCols:
        maxY = max(maxY, columm.getCoords()[0][1], columm.getCoords()[1][1])
        minY = min(minY, columm.getCoords()[0][1], columm.getCoords()[1][1])
        maxX = max(maxX, columm.getCoords()[0][0], columm.getCoords()[1][0])
        minX = min(minX, columm.getCoords()[0][0], columm.getCoords()[1][0])

    allColX = [col[0][0] - minX for col in newCols.getCoords()] + [col[1][0] - minX for col in newCols.getCoords()]

    newImage = image[minY:maxY][minX:maxX]

    return (newImage, newCols, minX, maxX, minY, maxY, allColX)'''
