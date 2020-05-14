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
        0.25: [1, 10, 100],
        0.5: [1, 10, 100],
        0.75: [1, 10, 100]
    }
    make_dir(output_dir)

    naming = "demosaic"
    results_doc = doc()
    results_doc.add_row_element(subfigure(path="demosaicing/{}/input.png".format(naming), text="Orginal bilde"))
    results_doc.add_row_element(subfigure(path="demosaicing/{}/mosaic.png".format(naming), text="simulert gråtone mosaikk"))
    results_doc.add_row()

    results_doc = compile_doc(demosaic_obj, epoch_count, "{}/".format(output_dir), "demosaicing/{}".format(naming),
                              extra=lambda x: x.simulate(),
                              results_doc=results_doc)
    results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iterasjoner")
    results_doc.save("{}/results.tex".format(output_dir))

    Image.fromarray(np.uint8(255 * demosaic_obj.data_copy)).save("{}/input.png".format(output_dir))
    demosaic_obj.reset()
    Image.fromarray(np.uint8(255 * demosaic_obj.simulate())).save("{}/mosaic.png".format(output_dir))

from rapport_snippets.inpaiting import *

def compile_zoom(location, SIZE=5):
    """
    Compiles a small .tex file for the inpaiting function zoomed in

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    size:
        the amount to zoom into the output image
    """
    demosaic_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)
    demosaic_obj.simulate()

    make_dir(location)

    x_m, y_m = demosaic_obj.data.shape

    epochs = 100
    demosaic_obj.fit(
        epochs=epochs
    )

    IN = Image.fromarray(np.uint8(demosaic_obj.data * 255))
    out_fixed = zoom_at(IN,
                        x_m // 2, y_m // 2, 5) 

    IN = Image.fromarray(np.uint8(demosaic_obj.data_copy * 255))
    out_original = zoom_at(IN,
                           x_m // 2, y_m // 2, 5)

#    out_mask.save(location + "mask_{}.png".format(SIZE))
    out_fixed.save(location + "fixed_{}.png".format(SIZE))
    out_original.save(location + "original_{}.png".format(SIZE))

    Image.fromarray(np.uint8(demosaic_obj.data * 255)).save(location + "full.png")

    x = doc()
    x.add_row_element(
        subfigure(path="./demosaicing/demosaic_zoom/fixed_{}.png".format(SIZE), text="Bilde med {} iterations, $\\alpha = {} $".format(epochs, demosaic_obj.alpha)))
    x.add_row_element(subfigure(path="./demosaicing/demosaic_zoom/original_{}.png".format(SIZE), text="original bilde"))
    x.add_row()
    x.add_ref("ZoomDeomsaic{}".format(SIZE))
    x.save(location + "results_{}.tex".format(SIZE))
