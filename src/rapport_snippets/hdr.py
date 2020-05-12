import sys

sys.path.append("./")

# from backend import hdr
from engine import hdr_image_handler
from PIL import Image
from rapport_snippets.figs import *
from backend import reconstruction_HDR
import os


def compile(output_path, images, latex_name="res"):
    """
    Compiles a .tex file for the HDR function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    make_dir(output_path)

    results_doc = doc()
    handler = hdr_image_handler.hdr_handler(images)

    path_latex = "HDR/" + latex_name
    for index, j in enumerate(handler.images):
        file = "input_{}.png".format(index)

        Image.open(j.path).save("{}/{}".format(output_path, file))
        results_doc.add_row_element(
            subfigure(path=path_latex + "/" + file, text="{}".format(os.path.basename(j.path).replace("_", "\\_"))))
        if index % 3 == 0:
            results_doc.add_row()

    output = reconstruction_HDR.ReconstructionHDR(images)
    output.fit(1)
    output.save(output_path + "output.png")

    results_doc.add_row_element(subfigure(path=path_latex + "/" + "output.png", text="output"))
    results_doc.add_row()
    results_doc.save(output_path + "results.tex")
