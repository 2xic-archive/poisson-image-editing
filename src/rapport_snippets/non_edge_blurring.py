from backend import non_edge_blurring
from rapport_snippets.figs import *


def compile(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the non edge blurring function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    for color in [True, False]:
        name = ("color" if color else "gray")
        output_dir_path = output_dir + name
        make_dir(output_dir_path)

        blurring_obj = non_edge_blurring.NonEdgeBlur("./files/test_images/lena.png", color)
        epoch_count = {
            0.25: [1, 10, 100],
            0.5: [1, 10, 100],
            0.75: [1, 10, 100]
        }
        results_doc = compile_doc(blurring_obj, epoch_count, "{}/".format(output_dir_path),
                                  "glatting/non_edge_blur/{}/".format(name))
        results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iterasjoner. $K={}$ på alle bildene.".format(blurring_obj.k))
        results_doc.add_ref("nonEdgeBlur" + name)
        results_doc.save("{}/results.tex".format(output_dir_path))
