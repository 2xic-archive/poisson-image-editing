# from gui.interfaces import blurring_qt
import sys

sys.path.append("./")
from PIL import Image
from rapport_snippets.figs import *
from backend import blurring
import numpy as np
from scipy.ndimage import gaussian_filter


def compile(output_dir="./rapport_snippets/output/glatting/"):
    """
    Compiles a .tex file for the blur function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)

    color = True
    epoch_count = {
        0.25: [1, 10, 100],
        0.5: [1, 10, 100],
        0.75: [1, 10, 100]
    }
    for color in [True, False]:
        blurring_obj = blurring.Blur("./files/test_images/lena.png", color)

        naming = "_color" if color else "_gray"
        naming += "_explicit" if blurring_obj.mode_poisson == 0 else "_implicit"

        output_path_location = "{}/blur{}/".format(output_dir, naming)
        output_path_location_latex = "glatting/blur/blur{}".format(naming)

        make_dir(output_path_location)

        results_doc = compile_doc(blurring_obj, epoch_count, output_path=output_path_location,
                                  path_latex=output_path_location_latex)
        # results_doc.add_ref(naming)
        results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iteration")
        results_doc.save("{}/results.tex".format(output_path_location, naming))


def test_blur_filter(output_dir):
    """
    Creates a blurred image with a gaussian filter

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)

    blurring_obj = blurring.Blur("./files/test_images/lena.png", False)
    result = gaussian_filter(blurring_obj.data, sigma=2)
    Image.fromarray(np.uint8(255 * result)).convert("RGB").save(output_dir + 'filter.png')
