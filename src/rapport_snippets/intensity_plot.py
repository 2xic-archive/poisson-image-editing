import matplotlib.pyplot as plt

def plot_intensity(old_instensity, new_intensity, dest, dest_solo):
	plt.plot(old_instensity, color="r")
	plt.plot(new_intensity, color="g")
	plt.savefig(dest)
	plt.cla()
	plt.plot(old_instensity, color="r")
	plt.savefig(dest_solo)