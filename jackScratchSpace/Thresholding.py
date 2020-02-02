import numpy


def splitIntoPixelChunks(imgBin):
    # Find the size of our image
    height, width = numpy.ma.size(imgBin, 0), numpy.ma.size(imgBin, 1)
    # Find the number of sections to split our image into
    noHeightChunks, noWidthChunks = max(height // 2, 1), max(width // 2, 1)

    heightChunks = numpy.array_split(imgBin, noWidthChunks)
    chunks = numpy.array(list(map(lambda q: numpy.array_split(q, noHeightChunks), heightChunks)))

    chunks = numpy.concatenate(chunks)
    return chunks


def threshold_picture(imgFile):
    img = imgFile.convert('L')  # convert to monochrome
    img.save("photo2.jpg")
    imgBinary = numpy.array(img)
    imgChunks = splitIntoPixelChunks(imgBinary)
    print(imgBinary)
    # thresholdedData = (imgBinary > threshold) * 1.0 #0/1 if below/above threshold
    # imwrite("photoout.jpg", thresholdedData)
    return


array = numpy.arange(72).reshape((8, 9))
splitIntoPixelChunks(array)
"""
img = Image.open("photo.jpg")
threshold_picture(img)"""
