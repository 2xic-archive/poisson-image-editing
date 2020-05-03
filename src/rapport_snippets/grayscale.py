from backend import grayscale
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
from engine import image_handler

def compile(output_dir="./rapport_snippets/output"):
	contrast_obj = grayscale.grayscale("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}


	results_doc = compile_doc(contrast_obj, epoch_count, "{}/grayscale/".format(output_dir), "farge_gråtone/grayscale")
	results_doc.save("{}/grayscale/results.tex".format(output_dir))

def compule_side_by_side(output_dir="./rapport_snippets/output/"):
	#contrast_obj = matting.matting()
	contrast_obj = grayscale.grayscale("./files/test_images/lena.png", True)


	results_doc = doc()
	path_latex = "farge_gråtone/grayscale_side"
	contrast_obj.fit(10)

	naming = "grayscale_side"

	contrast_obj.save("{}{}/metode.png".format(output_dir,naming))
	

	contrast_obj = image_handler.ImageHandler("./files/test_images/lena.png", False)
	contrast_obj.save("{}{}/standard.png".format(output_dir,naming))

	#contrast_obj.save("{}{}/source.png".format(output_dir,naming))


	results_doc.add_row_element(subfigure(path=path_latex + "/standard.png", text="vektet image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/metode.png", text="metode image"))
	results_doc.add_row()
	results_doc.add_ref("gray_side_by_side")
	results_doc.save("{}/grayscale_side/results.tex".format(output_dir))
	
#	Image.fromarray(np.uint8(255 * contrast_obj.source.data_copy)).save("{}{}/source.png".format(output_dir,naming))
#	contrast_obj.reset()
#	Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/target.png".format(output_dir,naming))
#	contrast_obj.bad_fit()
#	Image.fromarray(np.uint8(255 * contrast_obj.data)).save("{}{}/bad_fit.png".format(output_dir,naming))


