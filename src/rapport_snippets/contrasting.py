

#from gui.interfaces import blurring_qt

"""
	Makes it easy to export results to latex 
"""
class subfigure:
	def __init__(self, path, text):
		self.path = path
		self.text = text
		self.width = -1
		self.filler = True

	def __str__(self):
		block = "\subfloat[" + self.text + "]{%\n" \
				"\includegraphics[width=" + str(self.width) + "\\textwidth]{" + self.path + "}}"
		if(self.filler):
			block += "\hfill"
		else:
			block += "\\\\"
		return block

	def __repr__(self):
		return self.__str__()

class doc:
	def __init__(self):
		self.rows = [
			"\\begin{figure}[htb]",
			"\\centering",
		]
		self.row = [

		]

		self.padding = 0.1

	def add_row_element(self, data):
		self.row.append(data)

	def add_row(self):
		for i in self.row:
			i.width = round((1/len(self.row)) * (1 - self.padding), 3)
		self.row[-1].filler = False
		self.rows += self.row
		self.row = []

	def save(self, path):
		self.rows += ["\\end{figure}"]
		print(path)
		open(path, "w").write("\n".join(map(str, self.rows)))

	def __str__(self):
		for i in self.rows:
			print(i)

#x = subfigure("test", "test")
#print(x)
#exit(0)

from backend import contrasting
from extra import local_adaptive_histogram
from PIL import Image
import numpy as np

contrast_obj = contrasting.Contrast("./files/test_images/contrast.jpg", False)

epoch_count = {
	0.25:[1, 3, 5],
	0.5:[1, 3, 5],
	0.75:[1, 3, 5]
}

x = doc()

#for alpha in [0.25, 0.5, 0.75]:
#	for epoch in [1, 3, 8]:
output_folder = "rapport_snippets/output/"

for alpha,epochs in epoch_count.items():
	for epoch in epochs:
		FILE_PATH = "contrast/alpha_{}_epoch_{}.png".format(alpha, epoch)
		contrast_obj.fit(epoch)
		contrast_obj.save(output_folder + FILE_PATH)

		#	"example-image-c"
		x.add_row_element(subfigure(path=FILE_PATH, text="$\\alpha = {}$\\newline Iteration $= {}$".format(alpha, epoch)))
	x.add_row()
	contrast_obj.reset()


output = local_adaptive_histogram.contrast_enhancement(contrast_obj.data_copy)

im = Image.fromarray(np.uint8(255 * output))
im.save(output_folder + "contrast/adaptive.png")

x.add_row_element(subfigure(path="contrast/adaptive.png", text="local adaptive histogram"))
x.add_row()

x.save("rapport_snippets/output/contrast/results.tex")


#





