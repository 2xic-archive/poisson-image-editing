from backend import demosaicing
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np



def compile(output_dir="demosaic"):
	contrast_obj = demosaicing.Demosaic("./files/test_images/lena.png", True)

	epoch_count = {
		0.25:[1, 3, 5],
		0.5:[1, 3, 5],
		0.75:[1, 3, 5]
	}


	#contrast_obj = inpaiting.inpaint("./files/test_images/lena.png")
	#input_image = contrast_obj.destroy_information()#.copy()

	for color in [True]:
		for numeric in [0, 1]:
			contrast_obj.mode_poisson = numeric
		#	print(contrast_obj, numeric)
		#	print(numeric)
		#	continue


			naming = "demosaic"
			naming += "_color" if color else "_gray"
			naming += "_explicit" if contrast_obj.mode_poisson == 0 else "_implicit"
	#		if not (color == contrast_obj.color):
	#			contrast_obj.change_color_state()

	#		if not os.path.isdir("{}inpainting{}/".format(output_path, naming)):
	#			os.mkdir("{}inpainting{}/".format(output_path,naming))		

			if not os.path.isdir("{}/{}/".format(output_dir, naming)):
				os.mkdir("{}/{}/".format(output_dir, naming))
		#	print("{}/{}/".format(output_dir, naming))
		#	exit(0)
			results_doc = doc()
	#		results_doc
			results_doc.add_row_element(subfigure(path="demosaicing/{}/input.png".format(naming), text="Input image"))
			results_doc.add_row_element(subfigure(path="demosaicing/{}/mosaic.png".format(naming), text="simulated mosaic"))
			results_doc.add_row()

#			results_doc = compile_doc(contrast_obj, epoch_count, "{}inpainting{}/".format(output_path,naming), "inpainting/inpainting{}".format(naming),
#										extra=lambda x: x.destroy_information(), results_doc=results_doc)
#			results_doc.save("{}inpainting{}/results.tex".format(output_path,naming))
			results_doc = compile_doc(contrast_obj, epoch_count, "{}/{}/".format(output_dir, naming), "demosaicing/{}".format(naming), extra=lambda x: x.simulate(),
			results_doc=results_doc)#,
			results_doc.save("{}/{}/results.tex".format(output_dir, naming))

			Image.fromarray(np.uint8(255 * contrast_obj.data_copy)).save("{}{}/input.png".format(output_dir,naming))
			contrast_obj.reset()
			Image.fromarray(np.uint8(255 * contrast_obj.simulate())).save("{}{}/mosaic.png".format(output_dir,naming))



#	results_doc = compile_doc(contrast_obj, epoch_count, "{}/demosaic/".format(output_dir), "demosaicing/demosaic", extra=lambda x: x.simulate())#,
#	results_doc.save("{}/demosaic/results.tex".format(output_dir))


