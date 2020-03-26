import os

"""
	Makes it easy to export results to latex 
"""
class subfigure:
	def __init__(self, path, text):
		self.path = path
		self.text = text
		self.width = -1
		self.heigth = 1
		self.filler = True

	def __str__(self):
		block = "\subfloat[" + self.text + "]{%\n" \
				"\includegraphics[width=" + str(self.width) + "\\textwidth, "\
				"height=" + str(self.height) + "\\paperheight, keepaspectratio]{" + self.path + "}}"
		if(self.filler):
			block += "\hfill"
		else:
			block += "\\\\"
		return block

	def __repr__(self):
		return self.__str__()

class doc:
	def __init__(self, padding_heigth=0.1):
		self.rows = [
			"\\begin{figure}[!htb]",
			"\\centering",
		]
		self.row = [

		]
		self.padding_heigth = padding_heigth# 0.1
		self.padding_width = 0.1
		self.row_count = 0

	def add_row_element(self, data):
		self.row.append(data)

	def add_row(self):
		for i in self.row:
			i.width = round((1/len(self.row)) * (1 - self.padding_width), 3)
		self.row[-1].filler = False
		self.rows += self.row
		self.row_count += 1
		self.row = []

	def save(self, path):
		for i in self.rows:
			if(type(i) != str):
				i.height = 1 / (self.row_count * (1 + self.padding_heigth))
		self.rows += ["\\end{figure}"]
		print(path)
		open(path, "w").write("\n".join(map(str, self.rows)))

	def __str__(self):
		for i in self.rows:
			print(i)

def compile_doc(method, alpha_epochs, path, path_latex="", extra=lambda x: x, results_doc=None):
	path_latex += "/" if not path_latex.endswith("/")  and not len(path_latex) == 0 else ""
	path += "/" if not path.endswith("/") and not len(path) == 0 else ""
		
	if(results_doc is None):
		results_doc = doc()

	for alpha,epochs in alpha_epochs.items():
		for index, epoch in enumerate(epochs):
			method.reset()
			extra(method)
			FILE_PATH = "alpha_{}_epoch_{}.png".format(alpha, epoch)

#			if not os.path.isfile(path + "source.png"):
#				method.save(path + "/target.png")
#				method.source.save(path + "/source.png")
			if not (os.path.isfile(path + "/" + FILE_PATH)):
				method.fit(epochs=epoch)
				method.data = method.data.clip(0, 1)
				method.save(path + "/" + FILE_PATH)

			#	"example-image-c"
			results_doc.add_row_element(subfigure(path=path_latex + FILE_PATH, text="$\\alpha = {}$\\newline Iteration $= {}$".format(alpha, epoch)))
		results_doc.add_row()
#		method.reset()
	return results_doc






