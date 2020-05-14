import numpy as np
from PIL import Image

from backend import matting
from rapport_snippets.figs import *


def compile(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the matting function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)
    matting_obj = matting.Matting()

    epoch_count = {
        0.2: [1, 10, 100],
        0.5: [1, 10, 100]
    }

    for color in [False, True]:
        naming = "_color" if color else "_gray"

        output_path_new = "{}/matting{}/".format(output_dir, naming)

        if not (color == matting_obj.color):
            matting_obj.change_color_state()
            matting_obj.source.change_color_state()
        make_dir(output_path_new)

        results_doc = doc()
        path_latex = "sømløs kloning/matting{}".format(naming)
        results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source"))
        results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="Target"))
        results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="Direkte klipp og lim"))
        results_doc.add_row()

        results_doc = compile_doc(matting_obj, epoch_count, "{}".format(output_path_new),
                                  path_latex, results_doc=results_doc)
        results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iterasjoner")
        results_doc.add_ref("mattingResultat" + naming.replace("_", ""))
        results_doc.save("{}/results.tex".format(output_path_new))

        Image.fromarray(np.uint8(255 * matting_obj.source.data_copy)).save("{}/source.png".format(output_path_new))
        matting_obj.reset()
        Image.fromarray(np.uint8(255 * matting_obj.data_copy)).save("{}/target.png".format(output_path_new))
        matting_obj.bad_fit()
        Image.fromarray(np.uint8(255 * matting_obj.data)).save("{}/bad_fit.png".format(output_path_new))

def compile_noisy(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the matting function

    Showing that using the correct image is important

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)

    # matting_obj = matting.Matting()
    matting_obj = matting.Matting("./files/test_images/sky.jpg", "./files/test_images/moon.png")
    matting_obj.padding = [
        200, 600
    ]
    matting_obj.working_area = [(None, None), (None, None)]

    epoch_count = {
        0.2: [1, 100, 1000],
        0.5: [1, 100, 1000]
    }

    results_doc = doc()
    path_latex = "sømløs kloning/matting_noise"
    results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source"))
    results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="Target"))
    results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="Direkte klipp og lim"))
    results_doc.add_row()

    results_doc = compile_doc(matting_obj, epoch_count, "{}/".format(output_dir), path_latex,
                              extra=lambda x: x.reset_full(), results_doc=results_doc)
    results_doc.padding_heigth = 0.3
    results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iterasjoner")

    results_doc.save("{}/results.tex".format(output_dir))

    Image.fromarray(np.uint8(255 * matting_obj.source.data_copy)).save("{}/source.png".format(output_dir))
    matting_obj.reset()
    Image.fromarray(np.uint8(255 * matting_obj.data_copy)).save("{}/target.png".format(output_dir))
    matting_obj.bad_fit()
    Image.fromarray(np.uint8(255 * matting_obj.data)).save("{}/bad_fit.png".format(output_dir))


def compile_parameters(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the anonymizing function

    Showing that parameters are important

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    make_dir(output_dir)

    matting_obj = matting.Matting()

    matting_obj.padding = [50, 250]
    matting_obj.working_area = [
        [0, 70],
        [0, 70],
    ]
    matting_obj.bad_fit()
    matting_obj.save("{}/bad_fit.png".format(output_dir))

    matting_obj.reset()
    matting_obj.fit(epochs=100)
    matting_obj.save("{}/good_fit.png".format(output_dir))

    matting_obj.reset()
    matting_obj.working_area = [
        [10, 65],
        [10, 65],
    ]
    matting_obj.fit(epochs=100)
    matting_obj.save("{}/best_fit.png".format(output_dir))

    matting_obj.bad_fit()
    matting_obj.save("{}/best_ugly_fit.png".format(output_dir))

    x = doc()
    x.add_row_element(
        subfigure(path="./sømløs kloning/parametere/bad_fit.png", text="Target bilde lagt på source bilde"))
    x.add_row_element(subfigure(path="./sømløs kloning/parametere/good_fit.png", text="Bilde med 100 iterasjoner"))
    x.add_row()
    x.add_row_element(
        subfigure(path="./sømløs kloning/parametere/best_ugly_fit.png", text="Target bilde lagt på source bilde"))
    x.add_row_element(subfigure(path="./sømløs kloning/parametere/best_fit.png", text="Bilde med 100 iterasjoner"))
    x.add_row()
    x.add_caption("Parametere er viktig")
    x.add_ref("parametere")
    x.save("{}/results.tex".format(output_dir))


def compile_oraple(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the anonymizing function

    Creates a oraple

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)

    matting_obj = matting.Matting("./files/test_images/orange.png", "./files/test_images/apple.png")
    matting_obj.working_area = [
        (300, None),
        (10, None)
    ]
    matting_obj.padding = [
        0, 0
    ]

    epoch_count = {
        0.2: [1, 3, 5],
        0.2: [10, 100, 1000]
    }

    results_doc = doc()
    path_latex = "sømløs kloning/moragen"
    results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source"))
    results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target"))
    results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="Bad_fit"))
    results_doc.add_row()

    results_doc = compile_doc(matting_obj, epoch_count, "{}/".format(output_dir), path_latex,
                              extra=lambda x: x.reset_full(), results_doc=results_doc)
    results_doc.padding_heigth = 0.3

    results_doc.add_caption("Oraple")
    results_doc.add_ref("Oraple")
    results_doc.save("{}/results.tex".format(output_dir))

    Image.fromarray(np.uint8(255 * matting_obj.source.data_copy)).save("{}/source.png".format(output_dir))
    matting_obj.reset()
    Image.fromarray(np.uint8(255 * matting_obj.data_copy)).save("{}/target.png".format(output_dir))
    matting_obj.bad_fit()
    Image.fromarray(np.uint8(255 * matting_obj.data)).save("{}/bad_fit.png".format(output_dir))

def compile_applange(output_dir="./rapport_snippets/output/"):
    """
    Compiles a .tex file for the anonymizing function

    Creates a oraple

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    make_dir(output_dir)

    matting_obj = matting.Matting("./files/test_images/orange.png", "./files/test_images/apple.png")
    matting_obj.working_area = [
        (0, 300),
        (10, None)
    ]
    matting_obj.padding = [
        0, 0
    ]

    epoch_count = {
        0.2: [1, 3, 5],
        0.2: [10, 100, 1000]
    }
    #print(matting_obj.data.shape)
    #print(matting_obj.source.shape)
    #    exit(0)
    results_doc = doc()
    path_latex = "sømløs kloning/applange"
    results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source"))
    results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target"))
    results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="Bad_fit"))
    results_doc.add_row()

    results_doc = compile_doc(matting_obj, epoch_count, "{}/".format(output_dir), path_latex,
                              extra=lambda x: x.reset_full(), results_doc=results_doc)
    results_doc.padding_heigth = 0.3

    results_doc.add_caption("Applange")
    results_doc.add_ref("Applange")
    results_doc.save("{}/results.tex".format(output_dir))

    Image.fromarray(np.uint8(255 * matting_obj.source.data_copy)).save("{}/source.png".format(output_dir))
    matting_obj.reset()
    Image.fromarray(np.uint8(255 * matting_obj.data_copy)).save("{}/target.png".format(output_dir))
    matting_obj.bad_fit()
    Image.fromarray(np.uint8(255 * matting_obj.data)).save("{}/bad_fit.png".format(output_dir))
