from backend import matting
from extra import local_adaptive_histogram
from PIL import Image
from rapport_snippets.figs import *
import numpy as np

contrast_obj = matting.matting()#"./files/test_images/lena.png", False)

epoch_count = {
	#0.25:[1, 3, 5],
	0.5:[1, 3, 5],
	0.75:[1, 3, 5]
}


#for alpha in [0.25, 0.5, 0.75]:
#	for epoch in [1, 3, 8]:
#output_folder = "rapport_snippets/output/"



#contrast_obj.destroy_information()
#contrast_obj.show()
#contrast_obj.fit()
#contrast_obj.show()
results_doc = doc()
path_latex = "sømløs kloning/matting"
results_doc.add_row_element(subfigure(path=path_latex + "source.png", text="Source image"))
results_doc.add_row_element(subfigure(path=path_latex + "target.png", text="target image"))
results_doc.add_row()

results_doc = compile_doc(contrast_obj, epoch_count, "./rapport_snippets/output/matting/", path_latex,
							extra=lambda x: x.reset_full(), results_doc=results_doc)
results_doc.padding_heigth=0.3
# this should proably be in the document elsewhere
'''
output = local_adaptive_histogram.matting_enhancement(matting_obj.data_copy)

# saves the local adaptive histogram iamge
Image.fromarray(np.uint8(255 * output)).save(output_folder + "matting/adaptive.png")

results_doc.add_row_element(subfigure(path="kontrastforsterkning/" + "matting/adaptive.png", text="local adaptive histogram"))
results_doc.add_row()
'''


results_doc.save("rapport_snippets/output/matting/results.tex")


