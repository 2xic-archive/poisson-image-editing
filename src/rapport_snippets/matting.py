from backend import matting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np


def compile(output_dir="./rapport_snippets/output/"):
	contrast_obj = matting.matting()

	epoch_count = {
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}

	results_doc = doc()
	path_latex = "sømløs kloning/matting"
	results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target image"))
	results_doc.add_row()

	results_doc = compile_doc(contrast_obj, epoch_count, "{}/matting/".format(output_dir), path_latex,
								extra=lambda x: x.reset_full(), results_doc=results_doc)
	results_doc.padding_heigth=0.3

	results_doc.save("{}/matting/results.tex".format(output_dir))
	naming = "matting"

	Image.fromarray(np.uint8(255 * contrast_obj.source.data_copy)).save("{}{}/source.png".format(output_dir,naming))
	contrast_obj.reset()
	Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/target.png".format(output_dir,naming))

