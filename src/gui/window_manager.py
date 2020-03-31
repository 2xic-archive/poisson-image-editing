class window:
	def __init__(self):
		self.WINDOWS = {

		}
		self.build_val = False

	def build(self):
		if not self.build_val:
			import gui.interfaces.blurring_qt as blur_window
			import gui.interfaces.inpaiting_qt as inpait_window
			import gui.interfaces.contrast_qt as contrast_window
			import gui.interfaces.demosaic_qt as demonsaic_window
			import gui.interfaces.matting_qt as matting_window
			import gui.interfaces.grayscale_qt as grayscale_window
			import gui.interfaces.anonymizing_qt as anonymizing_window
			import gui.interfaces.hdr_qt as hdr_window
			import gui.interfaces.non_edge_blurring_qt as non_edge_blurring
			INFILE = ""
			
			if blur_window.__file__ not in INFILE:
				self.WINDOWS["Blurring"] = blur_window.blur_window()
			if inpait_window.__file__ not in INFILE:
				self.WINDOWS["Inpainting"] = inpait_window.inpait_window()
			if contrast_window.__file__ not in INFILE:
				self.WINDOWS["Contrasting"] = contrast_window.contrast_window()
			if demonsaic_window.__file__ not in INFILE:
				self.WINDOWS["Demosaicing"] = demonsaic_window.demonsaic_window()
			if matting_window.__file__ not in INFILE:
				self.WINDOWS["Matting"] = matting_window.matting_window()
			if grayscale_window.__file__ not in INFILE:
				self.WINDOWS["Grayscale"] = grayscale_window.grayscale_window()
			if anonymizing_window.__file__ not in INFILE:
				self.WINDOWS["Anonymous"] = anonymizing_window.anonymizing_window()
			if anonymizing_window.__file__ not in INFILE:
				self.WINDOWS["Edge preserving blur"] = anonymizing_window.anonymizing_window()
			if non_edge_blurring.__file__ not in INFILE:
				self.WINDOWS["Edge preserving blur"] = non_edge_blurring.non_edge_blurring_window()
			if non_edge_blurring.__file__ not in INFILE:
				self.WINDOWS["HDR"] = hdr_window.hdr_window()
			print("build_valing")
			self.build_val = True
		
	def filter(self, x):
		scope = {

		}
		for i, v in self.WINDOWS.items():
			if x not in i :
				scope[i] = v
		return scope
