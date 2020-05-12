from PyQt5.QtGui import QImage, QPixmap


# from :
#	https://stackoverflow.com/questions/28086613/pillow-pil-to-qimage-conversion-python-exe-has-stopped-working
#	https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue
def pil2pixmap(input_image):
    """
    Converts the input into a format QT likes

    Parameters
    ----------
    input_image : ndarray
        the input_image to convert to QT format

    Returns
    -------
    QImage
        a QImage with the input_image data
    """
    if input_image.mode == "RGB":
        pass
    elif input_image.mode == "L":
        input_image = input_image.convert("RGBA")

    width, height = input_image.size
    if 512 < width:
        scale = 2
        input_image = input_image.resize((width // scale, height // scale))

    data = input_image.convert("RGBA").tobytes()
    qim = QImage(data, input_image.size[0], input_image.size[1], QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(qim)
    return pixmap
