from backend import demosaicing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile(output_dir="demosaic"):
	demosaic_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[5, 50, 500],
		0.5:[5, 50, 500],
		0.75:[5, 50, 500]
	}

	for color in [True]:
		for numeric in [0]:#, 1]:
			demosaic_obj.mode_poisson = numeric

			naming = "demosaic"
			naming += "_color" if color else "_gray"
			naming += "_explicit" if demosaic_obj.mode_poisson == 0 else "_implicit"

			if not os.path.isdir("{}/{}/".format(output_dir, naming)):
				os.mkdir("{}/{}/".format(output_dir, naming))

			results_doc = doc()
			results_doc.add_row_element(subfigure(path="demosaicing/{}/input.png".format(naming), text="Input image"))
			results_doc.add_row_element(subfigure(path="demosaicing/{}/mosaic.png".format(naming), text="simulated mosaic"))
			results_doc.add_row()

			results_doc = compile_doc(demosaic_obj, epoch_count, "{}/{}/".format(output_dir, naming), "demosaicing/{}".format(naming), extra=lambda x: x.simulate(),
			results_doc=results_doc)#,
			results_doc.save("{}/{}/results.tex".format(output_dir, naming))

			Image.fromarray(np.uint8(255 * demosaic_obj.data_copy)).save("{}{}/input.png".format(output_dir,naming))
			demosaic_obj.reset()
			Image.fromarray(np.uint8(255 * demosaic_obj.simulate())).save("{}{}/mosaic.png".format(output_dir,naming))



