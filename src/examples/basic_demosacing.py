import sys
sys.path.append('./')

from backend import demosaicing

x = demosaicing.Demosaic("./files/test_images/lena.png")
x.set_mode("Explicit")
x.simulate()
x.fit(8)
x.show()
