from backend import matting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np


def compile(output_dir="./rapport_snippets/output/"):
	contrast_obj = matting.matting()
	
	epoch_count = {
		0.2:[1, 10, 100],
		0.5:[1, 10, 100]
	}

	results_doc = doc()
	path_latex = "sømløs kloning/matting"
	results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="bad fit image"))
	results_doc.add_row()

	results_doc = compile_doc(contrast_obj, epoch_count, "{}/matting/".format(output_dir), path_latex,
								extra=lambda x: x.reset_full(), results_doc=results_doc)
	results_doc.padding_heigth=0.3

	results_doc.save("{}/matting/results.tex".format(output_dir))
	naming = "matting"

	Image.fromarray(np.uint8(255 * contrast_obj.source.data_copy)).save("{}{}/source.png".format(output_dir,naming))
	contrast_obj.reset()
	Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/target.png".format(output_dir,naming))
	contrast_obj.bad_fit()
	Image.fromarray(np.uint8(255 * contrast_obj.data)).save("{}{}/bad_fit.png".format(output_dir,naming))


def compile_noisy(output_dir="./rapport_snippets/output/"):
	#contrast_obj = matting.matting()
	contrast_obj = matting.matting("./files/test_images/sky.jpg", "./files/test_images/moon.png")
	contrast_obj.padding = [
		200, 600
	]
	contrast_obj.area_full = [(None, None), (None, None)]

	epoch_count = {
		0.2:[1, 100, 1000],
		0.5:[1, 100, 1000]
	}

	results_doc = doc()
	path_latex = "sømløs kloning/matting_noise"
	results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="bad fit image"))
	results_doc.add_row()

	results_doc = compile_doc(contrast_obj, epoch_count, "{}/matting_noise/".format(output_dir), path_latex,
								extra=lambda x: x.reset_full(), results_doc=results_doc)
	results_doc.padding_heigth=0.3

	results_doc.save("{}/matting_noise/results.tex".format(output_dir))
	naming = "matting_noise"

	Image.fromarray(np.uint8(255 * contrast_obj.source.data_copy)).save("{}{}/source.png".format(output_dir,naming))
	contrast_obj.reset()
	Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/target.png".format(output_dir,naming))
	contrast_obj.bad_fit()
	Image.fromarray(np.uint8(255 * contrast_obj.data)).save("{}{}/bad_fit.png".format(output_dir,naming))

def compile_parameters(output_dir="./rapport_snippets/output/"):
	path = "parametere"

	contrast_obj = matting.matting()

	contrast_obj.padding = [50, 250]
	contrast_obj.area_full = [
					[0, 70],
					[0, 70],
				]
	contrast_obj.bad_fit()
	contrast_obj.save("{}/{}/bad_fit.png".format(output_dir, path))

	contrast_obj.reset()
	contrast_obj.fit(epochs=100)
	contrast_obj.save("{}/{}/good_fit.png".format(output_dir, path))

	contrast_obj.reset()
	contrast_obj.area_full = [
					[10, 65],
					[10, 65],
				]
	contrast_obj.fit(epochs=100)
	contrast_obj.save("{}/{}/best_fit.png".format(output_dir, path))

	contrast_obj.bad_fit()
	contrast_obj.save("{}/{}/best_ugly_fit.png".format(output_dir, path))

	x = doc()
	x.add_row_element(subfigure(path="./sømløs kloning/parametere/bad_fit.png", text="Target bilde lagt på source bilde"))
	x.add_row_element(subfigure(path="./sømløs kloning/parametere/good_fit.png", text="Bilde med 100 iterations"))
	x.add_row()
	x.add_row_element(subfigure(path="./sømløs kloning/parametere/bad_fit.png", text="Target bilde lagt på source bilde"))
	x.add_row_element(subfigure(path="./sømløs kloning/parametere/good_fit.png", text="Bilde med 100 iterations"))
	x.add_row()
	x.add_caption("Parametere er viktig")
	x.add_ref("parametere")
	x.save("{}/{}/results.tex".format(output_dir, path))

def compile_moapple(output_dir="./rapport_snippets/output/"):
	contrast_obj = matting.matting("./files/test_images/orange.png", "./files/test_images/apple.png")
	contrast_obj.area_full = [
		(300, None),
		(10, None)
	]
	contrast_obj.padding = [
		0, 0
	]

	epoch_count = {
		0.2:[1, 3, 5],
		0.2:[10, 100, 1000]
	}

	results_doc = doc()
	path_latex = "sømløs kloning/moragen"
	results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target image"))
	results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="Bad_fit"))
	results_doc.add_row()


	results_doc = compile_doc(contrast_obj, epoch_count, "{}/moragen/".format(output_dir), path_latex,
								extra=lambda x: x.reset_full(), results_doc=results_doc)
	results_doc.padding_heigth=0.3


	results_doc.add_caption("Oraple")
	results_doc.add_ref("Oraple")
	results_doc.save("{}/moragen/results.tex".format(output_dir))
	naming = "moragen"

	Image.fromarray(np.uint8(255 * contrast_obj.source.data_copy)).save("{}{}/source.png".format(output_dir,naming))
	contrast_obj.reset()
	Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/target.png".format(output_dir,naming))
	contrast_obj.bad_fit()
	Image.fromarray(np.uint8(255 * contrast_obj.data)).save("{}{}/bad_fit.png".format(output_dir,naming))












