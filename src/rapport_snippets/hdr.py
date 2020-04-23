#from backend import hdr
from extra import local_adaptive_histogram
from engine import hdr_image_handler
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
from backend import hdr_reconstruction

def compile(output_path):
	"""
	epoch_count = {
		0.25:[3, 5, 8],
		0.5:[3, 5, 8],
		0.75:[3, 5, 8]
	}
	"""

	results_doc = doc()
	x = hdr_image_handler.hdr_handler()
	path_latex = "HDR/res"
	output = "{}".format(output_path)
	for index, j in enumerate(x.images):
		file = "input_{}.png".format(index)

	#	Image.open(j.path).save("{}/{}".format(output, file))

		results_doc.add_row_element(subfigure(path=path_latex + "/" + file, text="Input {}".format(index)))
		if index % 3 == 0:
			results_doc.add_row()

	output = hdr_reconstruction.hdr_reconstruction()
	output.fit(1)
	#Image.fromarray(np.uint8(255 * output.data)).save("{}/output.png".format(output_path))

	results_doc.add_row_element(subfigure(path=path_latex + "/" + "output.png", text="output"))
	results_doc.add_row()
	
	results_doc.save(output_path + "results.tex")

	"""
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
	"""


	"""
	contrast_obj = inpaiting.inpaint("./files/test_images/lena.png")
	input_image = contrast_obj.destroy_information()#.copy()

	for color in [True, False]:
		for numeric in [0, 1]:
			contrast_obj.mode_poisson = numeric

			naming = "_color" if color else "_gray"
			naming += "_explicit" if contrast_obj.mode_poisson == 0 else "_implicit"

			if not (color == contrast_obj.color):
				contrast_obj.change_color_state()

			if not os.path.isdir("{}inpainting{}/".format(output_path, naming)):
				os.mkdir("{}inpainting{}/".format(output_path,naming))		

			results_doc = doc()
	#		results_doc
			results_doc.add_row_element(subfigure(path="inpainting/inpainting{}/input.png".format(naming), text="Input image"))
			results_doc.add_row()

			results_doc = compile_doc(contrast_obj, epoch_count, "{}inpainting{}/".format(output_path,naming), "inpainting/inpainting{}".format(naming),
										extra=lambda x: x.destroy_information(), results_doc=results_doc)
			results_doc.save("{}inpainting{}/results.tex".format(output_path,naming))

			Image.fromarray(np.uint8(255 * contrast_obj.original_data_copy)).save("{}inpainting{}/input.png".format(output_path,naming))

		#		"{}inpainting/input.png")
	#		exit(0)
	# x.destroy_information()
	"""