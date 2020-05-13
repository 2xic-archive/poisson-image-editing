import numpy as np
from PIL import Image

from backend import inpaiting
from extra.median_filter import median_filter
from rapport_snippets.figs import *


def compile(output_path):
    """
    Compiles a .tex file for the inpaiting function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """

    epoch_count = {
        0.25: [1, 10, 100],
        0.5: [1, 10, 100],
        0.75: [1, 10, 100]
    }

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    inpainting_obj = inpaiting.Inpaint("./files/test_images/lena.png")
    input_image = inpainting_obj.destroy_information()  # .copy()

    for color in [True, False]:
        naming = "_color" if color else "_gray"

        output_path_new = "{}inpainting{}/".format(output_path, naming)

        if not (color == inpainting_obj.color):
            inpainting_obj.change_color_state()
        make_dir(output_path_new)

        results_doc = doc()
        results_doc.add_row_element(
            subfigure(path="inpainting/inpainting{}/input.png".format(naming), text="Input image"))
        results_doc.add_row()

        results_doc = compile_doc(inpainting_obj, epoch_count, "{}".format(output_path_new),
                                  "inpainting/inpainting{}".format(naming),
                                  extra=lambda x: x.destroy_information(), results_doc=results_doc)
        results_doc.add_caption("Resultat med ulike verdier av $\\alpha$ og iterasjoner")
        results_doc.add_ref("inpaitngResultat" + naming.replace("_", ""))
        results_doc.save("{}/results.tex".format(output_path_new))
        Image.fromarray(np.uint8(255 * inpainting_obj.original_data_copy)).save("{}/input.png".format(output_path_new))


def compile_median(output_path):
    """
    Compiles a .tex file for the median filter function

    Parameters
    ----------
    output_path : str
        the location to store the .tex with images
    """
    make_dir(output_path)

    method = inpaiting.Inpaint("./files/test_images/lena.png", True)

    method.destroy_information(3)

    median = method.original_data_copy.copy()

    for i in range(10):
        median = median_filter(median, method.mask)
    method.fit(epochs=10)

    Image.fromarray(np.uint8(255 * method.data)).save("{}/poisson.png".format(output_path))
    Image.fromarray(np.uint8(255 * median)).save("{}/median.png".format(output_path))
    Image.fromarray(np.uint8(255 * method.original_data_copy)).save("{}/input.png".format(output_path))

    results_doc = doc()
    results_doc.add_row_element(subfigure(path="inpainting/median/input.png", text="Input image"))
    results_doc.add_row_element(subfigure(path="inpainting/median/poisson.png", text="poisson image"))
    results_doc.add_row_element(subfigure(path="inpainting/median/median.png", text="median image"))
    results_doc.add_ref("median_vs_poisson")
    results_doc.add_row()

    results_doc.save("{}/results.tex".format(output_path))


def zoom_at(img, x, y, zoom):
    """
    Compiles a .tex file for the inpaiting function

    Parameters
    ----------
    img : PIL.Image
        the image to zoom into
    x : float
        the x location to zoom into
    y : float
        the y location to zoom into
    zoom : float
        the zoom zie

    Returns
    ----------
    PIL.Image
        the zoomed image
    """
    w, h = img.size
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2,
                    x + w / zoom2, y + h / zoom2))
    return img.resize((w, h), Image.LANCZOS).convert('RGB')


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
    inpainting_obj = inpaiting.Inpaint("./files/test_images/lena.png", True)
    mask = np.ones((inpainting_obj.data.shape[:2]))

    x_m, y_m, _ = inpainting_obj.data.shape

    mask[x_m // 2: x_m // 2 + SIZE,
    y_m // 2: y_m // 2 + SIZE] = 0

    og = np.zeros((inpainting_obj.data.shape))
    for i in range(inpainting_obj.data.shape[-1]):
        og[:, :, i] = inpainting_obj.data[:, :, i] * mask

    inpainting_obj.data = og

    IN = Image.fromarray(np.uint8(og * 255))
    out_mask = zoom_at(IN,
                       x_m // 2, y_m // 2, 5)

    epochs = 100
    inpainting_obj.fit(
        og,
        og,
        mask,
        epochs=epochs
    )

    IN = Image.fromarray(np.uint8(inpainting_obj.data * 255))
    out_fixed = zoom_at(IN,
                        x_m // 2, y_m // 2, 5)  # .show()

    IN = Image.fromarray(np.uint8(inpainting_obj.data_copy * 255))
    out_original = zoom_at(IN,
                           x_m // 2, y_m // 2, 5)  # .show()

    out_mask.save(location + "mask_{}.png".format(SIZE))
    out_fixed.save(location + "fixed_{}.png".format(SIZE))
    out_original.save(location + "original_{}.png".format(SIZE))

    Image.fromarray(np.uint8(inpainting_obj.data * 255)).save(location + "full.png")

    x = doc()
    x.add_row_element(subfigure(path="./inpainting/extra/mask_{}.png".format(SIZE), text="Bilde med glitch"))
    x.add_row_element(
        subfigure(path="./inpainting/extra/fixed_{}.png".format(SIZE), text="Bilde med {} iterations".format(epochs)))
    x.add_row_element(subfigure(path="./inpainting/extra/original_{}.png".format(SIZE), text="original bilde"))
    x.add_row()
    x.add_caption("Inpainting er kontrollert blurring")
    x.add_ref("Zoom{}".format(SIZE))
    x.save(location + "results_{}.tex".format(SIZE))
