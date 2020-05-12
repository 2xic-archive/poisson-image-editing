from backend import grayscale
from engine import image_handler
from rapport_snippets.figs import *


def compile(output_dir="./rapport_snippets/output"):
    """
    Compiles a .tex file for the grayscale function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    contrast_obj = grayscale.Grayscale("./files/test_images/lena.png", True)

    epoch_count = {
        0.25: [1, 3, 5],
        0.5: [1, 3, 5],
        0.75: [1, 3, 5]
    }
    results_doc = compile_doc(contrast_obj, epoch_count, "{}/".format(output_dir), "farge_gråtone/grayscale")
    results_doc.save("{}/results.tex".format(output_dir))


def compule_side_by_side(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the grayscale function

    Compares it with the standard way of converting a color image
    to grayscale

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    epochs = 10
    grayscale_obj = grayscale.Grayscale("./files/test_images/lena.png", True)
    results_doc = doc()

    path_latex = "farge_gråtone/grayscale_side"
    grayscale_obj.fit(epochs)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    grayscale_obj.save("{}/metode.png".format(output_dir))

    # load a grayscale image with weighing
    contrast_obj = image_handler.ImageHandler("./files/test_images/lena.png", False)
    contrast_obj.save("{}/standard.png".format(output_dir))

    results_doc.add_row_element(subfigure(path=path_latex + "/standard.png", text="vektet image"))
    results_doc.add_row_element(subfigure(path=path_latex + "/metode.png",
                                          text="poisson image($\\alpha={}$, iteration={})".format(grayscale_obj.alpha,
                                                                                                  epochs)))
    results_doc.add_row()
    results_doc.add_caption("Sammenligning av metode")
    results_doc.add_ref("GraySideBySide")
    results_doc.save("{}/results.tex".format(output_dir))
