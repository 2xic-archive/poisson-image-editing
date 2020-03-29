from PyQt5.QtGui import QImage, QPixmap
import os


# from :
#	https://stackoverflow.com/questions/28086613/pillow-pil-to-qimage-conversion-python-exe-has-stopped-working
#	https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue
def pil2pixmap(input_image):
    """
    Convers the input into a format QT liks

    Parameters
    ----------
    input_image : ndarray
        the input_image to convert to QT format
    """
    if input_image.mode == "RGB":
        pass
    elif input_image.mode == "L":
        input_image = input_image.convert("RGBA")

    width, height = input_image.size
    if 512 < width:
        scale = 2
        input_image = input_image.resize((width//scale, height//scale))
    

    data = input_image.convert("RGBA").tobytes()    
    qim = QImage(data, input_image.size[0], input_image.size[1], QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qim)
    return pixmap


def get_path(file: str) -> str:
    """
    Get the path to current file

    Parameters
    ----------
    file : str
        The file to check path against
    """
    dir_path = os.path.dirname(os.path.realpath(file)) + "/"
    return dir_path
