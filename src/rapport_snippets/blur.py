#from gui.interfaces import blurring_qt

from PIL import Image
from rapport_snippets.figs import *
from backend import blurring


blurring_obj = blurring.blur("./files/test_images/lena.png", False)
epoch_count = {
	0.5:[3, 5, 10],
	0.75:[3, 5, 10]
}

results_doc = compile_doc(blurring_obj, epoch_count, "./rapport_snippets/output/blur/", "glatting/blur")
results_doc.save("rapport_snippets/output/blur/results.tex")

