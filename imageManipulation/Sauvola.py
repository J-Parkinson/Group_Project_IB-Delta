import skimage.io as skimg
from skimage.filters import threshold_sauvola
from skimage.util import img_as_uint


def sauvola(image, chunkSize=11):
    thresholdFunc = threshold_sauvola(image, chunkSize, 0.15)
    return image > thresholdFunc


image = skimg.imread("jackScratchSpace/test.png", True)

normalisedImage = sauvola(image)

skimg.imsave("jackScratchSpace/photoout3.png", img_as_uint(normalisedImage))
