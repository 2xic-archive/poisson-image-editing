
from PIL import Image
from rapport_snippets.figs import *
from backend import non_edge_blurring

blurring_obj = non_edge_blurring.non_edge_blur("./files/test_images/lena.png", False)

epoch_count = {
	0.25:[3, 5, 10],
	0.5:[1, 3, 5, 10],
	0.75:[1, 3, 5, 10]
}

results_doc = compile_doc(blurring_obj, epoch_count, "./rapport_snippets/output/nom_edge_blur/", "glatting/blur")
results_doc.save("rapport_snippets/output/nom_edge_blur/results.tex")