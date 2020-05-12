import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from backend import contrasting
from extra import local_adaptive_histogram
from rapport_snippets.figs import *

contrast_obj = contrasting.Contrast("./files/test_images/contrast.jpg", False)

epoch_count = {
    0.25: [1, 10, 100],
    0.5: [1, 10, 100],
    0.75: [1, 10, 100]
}


def process(img):
    """
    Make sure image is in range [0, 255]

    Parameters
    ----------
    img : ndarray
        the image

    Returns
    -------
    array
        the new image array
    """
    if len(img.shape) == 2:
        img = img.reshape(img.shape + (1,))
    if np.max(img) <= 1:
        img *= 255
        img = img.astype(np.uint8)
    else:
        img = img.astype(np.uint8)
    return img


def intensity(path, contrast_obj, epochs=3):
    """
    Creates intensity plots

    Using local adaptive histogram and poisson function

    Parameters
    ----------
    path : str
        the location to store the plots
    contrast_obj: Contrast
        the contrast object
    epochs : int
        the amount of epochs to run before creating the plot
    """
    contrast_obj.save(path + "orginal.png")

    plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="r")

    contrast_obj.fit(epochs)
    plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="g")
    plt.savefig(path + "poisson.png")

    contrast_obj.save(path + "poisson_output.png")
    contrast_obj.reset()

    plt.cla()
    plt.plot(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())), color="r")

    lah = np.cumsum(local_adaptive_histogram.intensity(process(contrast_obj.data.copy())))
    plt.plot(lah, color="g")
    plt.savefig(path + "intensity_adaptive.png")

    output_file = (local_adaptive_histogram.contrast_enhancement(process(contrast_obj.data.copy())))
    im = Image.fromarray(np.uint8(output_file * 255))
    im.save(path + "lah_output.png")


def compile(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the constrast function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    make_dir(output_dir)

    intensity(output_dir, contrast_obj, epochs=10)
    results_doc = compile_doc(contrast_obj, epoch_count, output_path=output_dir,
                              path_latex="kontrastforsterkning/contrast/")
    results_doc.add_caption(
        "Resultat med ulike verdier av $\\alpha$ og iteration. $k = {}$ på alle bildene.".format(contrast_obj.k))
    results_doc.add_ref("contrastResultsGray")
    results_doc.save("{}/results.tex".format(output_dir))


def compile_color(output_dir):
    """
    Compiles a .tex file for the constrast function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    make_dir(output_dir)
    contrast_obj = contrasting.Contrast("./files/test_images/contrast_color.jpg", True)

    color_image_lah = contrast_obj.data.copy()
    for i in range(color_image_lah.shape[-1]):
        output_file = (local_adaptive_histogram.contrast_enhancement(process(color_image_lah[:, :, i].copy())))
        color_image_lah[:, :, i] = output_file

    im = Image.fromarray(np.uint8(color_image_lah * 255))
    im.save(output_dir + "color_lah.png")

    results_doc = compile_doc(contrast_obj, epoch_count, output_path=output_dir,
                              path_latex="kontrastforsterkning/contrast_color/")
    results_doc.add_caption(
        "Resultat med ulike verdier av $\\alpha$ og iteration. $k = {}$ på alle bildene.".format(contrast_obj.k))
    results_doc.save("{}/results.tex".format(output_dir))
    intensity(output_dir, contrast_obj, epochs=10)
