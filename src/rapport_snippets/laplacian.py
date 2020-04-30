from backend import matting, blurring
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

def compile_parameters(output_dir="./rapport_snippets/output/"):
	path = "img"

	#os.mkdir("{}/img/".format(output_dir))

	blurring_obj = blurring.blur("./files/test_images/lena.png", False)
	blurring_obj.data[1:-1, 1:-1] = blurring_obj.get_laplace_explicit(blurring_obj.data, alpha=False)

	blurring_obj.save("{}/img/laplacian.png".format(output_dir))

	x = doc()
#	x.add_row_element(subfigure(path="./sømløs kloning/parametere/bad_fit.png", text="Target bilde lagt på source bilde"))
#	x.add_row_element(subfigure(path="./sømløs kloning/parametere/good_fit.png", text="Bilde med 100 iterations"))
#	x.add_row()
#	x.add_row_element(subfigure(path="./sømløs kloning/parametere/bad_fit.png", text="Target bilde lagt på source bilde"))
	x.add_row_element(subfigure(path="./img/laplacian.png", text="Bilde med 100 iterations"))
	x.add_row()
	x.add_caption("Parametere er viktig")
	x.add_ref("parametere")
	x.save("{}/{}/results.tex".format(output_dir, path))
