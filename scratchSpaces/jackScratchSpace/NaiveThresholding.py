import numpy
from PIL import Image
from imageio import imwrite

img = Image.open("photo.jpg")


def threshold_picture(imgFile, pageLow, pageHigh):
    threshold = (pageLow + pageHigh) / 2

    img = imgFile.convert('L')  # convert to monochrome
    img.save("photo2.jpg")
    imgBinary = numpy.array(img)

    thresholdedData = (imgBinary > threshold) * 1.0  # 0/1 if below/above threshold
    imwrite("photoout.jpg", thresholdedData)
    return


threshold_picture(img, 0, 90)
