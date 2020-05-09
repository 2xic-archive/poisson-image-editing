import sys
sys.path.append('./')

from backend import contrasting
x = contrasting.Contrast('./files/test_images/contrast.jpg')
x.set_mode("Explicit")
x.show()
x.fit(1000)
x.show()


#print(x)
#print(x.mode_boundary)
#print(x.mode_poisson)