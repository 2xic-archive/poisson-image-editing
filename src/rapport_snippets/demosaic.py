import numpy as np
from PIL import Image

from backend import demosaicing
from rapport_snippets.figs import *


def compile(output_dir="demosaic"):
    """
    Compiles a .tex file for the demosaic function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    demosaic_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)

    epoch_count = {
        0.25: [5, 50, 500],
        0.5: [5, 50, 500],
        0.75: [5, 50, 500]
    }
    make_dir(output_dir)

    results_doc = doc()
    results_doc.add_row_element(subfigure(path="demosaicing/{}/input.png".format(naming), text="Orginal bilde"))
    results_doc.add_row_element(subfigure(path="demosaicing/{}/mosaic.png".format(naming), text="simulert gråtone mosaikk"))
    results_doc.add_row()

    results_doc = compile_doc(demosaic_obj, epoch_count, "{}/".format(output_dir), "demosaicing/{}".format(naming),
                              extra=lambda x: x.simulate(),
                              results_doc=results_doc)
    results_doc.save("{}/{}/results.tex".format(output_dir))

    Image.fromarray(np.uint8(255 * demosaic_obj.data_copy)).save("{}/input.png".format(output_dir))
    demosaic_obj.reset()
    Image.fromarray(np.uint8(255 * demosaic_obj.simulate())).save("{}/mosaic.png".format(output_dir))
