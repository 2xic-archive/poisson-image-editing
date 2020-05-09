import sys
sys.path.append('./')

from backend import demosaicing

x = demosaicing.Demosaic("./files/test_images/lena.png")
x.mode_poisson = "Explicit"
x.simulate()



#print(x.alpha)
#exit(0)
x.alpha = 0.05


x.fit(500)

x.show()
