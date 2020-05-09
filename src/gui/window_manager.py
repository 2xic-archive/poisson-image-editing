class window:
	def __init__(self):
		self.WINDOWS = {

		}
		self.built = False

	def build(self):
		"""
		Build the window manager
		"""
		if not self.built:
			import gui.interfaces.blurring_qt as blur_window
			import gui.interfaces.inpaiting_qt as inpait_window
			import gui.interfaces.contrast_qt as contrast_window
			import gui.interfaces.demosaic_qt as demonsaic_window
			import gui.interfaces.matting_qt as matting_window
			import gui.interfaces.grayscale_qt as grayscale_window
			import gui.interfaces.anonymizing_qt as anonymizing_window
			import gui.interfaces.hdr_qt as hdr_window
			import gui.interfaces.non_edge_blurring_qt as non_edge_blurring			
			
			self.WINDOWS["Blurring"] = blur_window.blur_window()
			self.WINDOWS["Inpainting"] = inpait_window.inpait_window()
			self.WINDOWS["Contrasting"] = contrast_window.contrast_window()
			self.WINDOWS["Demosaicing"] = demonsaic_window.demonsaic_window()
			self.WINDOWS["Matting"] = matting_window.matting_window()
			self.WINDOWS["Grayscale"] = grayscale_window.grayscale_window()
			self.WINDOWS["Anonymous"] = anonymizing_window.anonymizing_window()
			self.WINDOWS["Edge preserving blur"] = anonymizing_window.anonymizing_window()
			self.WINDOWS["Edge preserving blur"] = non_edge_blurring.non_edge_blurring_window()
			self.WINDOWS["HDR"] = hdr_window.hdr_window()
			self.built = True
		
	def filter(self, current_file):
		"""
		Update the geometry

		of the last image or one specified

		Parameters
		----------
		current_file : str
			the file to exclude

		Returns
		-------
		dict
			the avaible windows excluding the current_file
		"""
		scope = {

		}
		for file_views, refrence in self.WINDOWS.items():
			if current_file not in file_views :
				scope[file_views] = refrence
		return scope



