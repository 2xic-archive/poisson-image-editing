from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

def compile():
	epoch_count = {
		0.25:[3, 5, 8],
		0.5:[3, 5, 8],
		0.75:[3, 5, 8]
	}


	contrast_obj = inpaiting.inpaint("./files/test_images/lena.png")
	input_image = contrast_obj.destroy_information()#.copy()

	for color in [True, False]:
		for numeric in [0, 1]:
			contrast_obj.mode_poisson = numeric

			naming = "_color" if color else "_gray"
			naming += "_explicit" if contrast_obj.mode_poisson == 0 else "_implicit"

			if not (color == contrast_obj.color):
				contrast_obj.change_color_state()

			if not os.path.isdir("./rapport_snippets/output/inpainting{}/".format(naming)):
				os.mkdir("./rapport_snippets/output/inpainting{}/".format(naming))		

			results_doc = doc()
	#		results_doc
			results_doc.add_row_element(subfigure(path="inpainting/inpainting{}/input.png".format(naming), text="Input image"))
			results_doc.add_row()

			results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/inpainting{}/".format(naming), "inpainting/inpainting{}".format(naming),
										extra=lambda x: x.destroy_information(), results_doc=results_doc)
			results_doc.save("./rapport_snippets/output/inpainting{}/results.tex".format(naming))

			Image.fromarray(np.uint8(255 * contrast_obj.original_data_copy)).save("./rapport_snippets/output/inpainting{}/input.png".format(naming))

		#		"./rapport_snippets/output/inpainting/input.png")
	#		exit(0)
	# x.destroy_information()
