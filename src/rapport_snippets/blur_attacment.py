
from PIL import Image
import sys
sys.path.append("./")
from backend import inpaiting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np
#from figs import *
from backend import blurring


def compile(output_dir):
	results_doc = doc()
	path_latex = "glatting/attachemnts/"

	path = "attachemnts"

	blurring_obj = blurring.blur("./files/test_images/lena.png", True)
	l = 0.4
	epochs = 1000

	blurring_obj.alpha = 0.4

	blurring_obj.fit(epochs)
	name = "fit_{}_lambda_{}.png".format(epochs, 0)
	blurring_obj.save("{}/{}/{}".format(output_dir, path, name))
	results_doc.add_row_element(subfigure(path=path_latex + "/" + name, text="Bilde uten attachemnts"))
	
	for i in [10, 100, epochs]:
		blurring_obj.reset()
		blurring_obj.set_lambda_size(l)
		blurring_obj.fit(i)

		name = "fit_{}_lambda_{}.png".format(i, l)
		blurring_obj.save("{}/{}/{}".format(output_dir, path,name))
		results_doc.add_row_element(subfigure(path=path_latex + "/" + name, text="Bilde med attachemnts"))
#	results_doc.add_row_element(subfigure(path=path_latex + "/source.png", text="Source image"))
#	results_doc.add_row_element(subfigure(path=path_latex + "/target.png", text="target image"))
#	results_doc.add_row_element(subfigure(path=path_latex + "/bad_fit.png", text="bad fit image"))
	results_doc.add_row()
	results_doc.save(output_dir + "/" + path + "/results.tex")
