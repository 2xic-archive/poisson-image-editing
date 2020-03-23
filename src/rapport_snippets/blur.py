#from gui.interfaces import blurring_qt


from backend import blurring


"""
Basic snippet !
"""
blur_object = blurring.blur("./files/test_images/lena.png", False)
blur_object.fit(13)
blur_object.save("test.png")