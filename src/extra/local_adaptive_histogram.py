import numpy as np

"""
From the book "Computer Vision - Algorithms and Applications" by Springer
"""


def intensity(img):
    intensity_scale = np.zeros(256, np.int32)
    for y in range(0, img.shape[0]):
        for x in range(0, img.shape[1]):
            for z in range(img.shape[2]):
                intensity = img[y][x][z]
                intensity_scale[intensity] += 1
    return intensity_scale / (img.shape[0] * img.shape[1] * img.shape[2])


def contrast_enhancement(img):
    if len(img.shape) == 2:
        img = img.reshape(img.shape + (1,))
    if np.max(img) <= 1:
        img *= 255
        img = img.astype(np.uint8)
    else:
        img = img.astype(np.uint8)

    old_intensity = intensity(img)
    new_intensity = np.cumsum(old_intensity)

    new_image = np.zeros((img.shape[0], img.shape[1]))
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            for z in range(img.shape[2]):
                new_image[x, y] = new_intensity[img[x, y, z]]
    return new_image
