import os
import sys

"""
	Makes it easy to export results to latex 
"""


class subfigure:
    """
    This class describes a subfigure.
    """

    def __init__(self, path, text):
        """
        Creates the subfigure object

        Parameters
        ----------
        path : str
            the path to load the image from
        text : str
            the text set as caption
        """
        self.path = path
        self.text = text
        self.width = -1
        self.heigth = 1
        self.filler = True

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        block = "\subfloat[" + self.text + "]{%\n" \
                                           "\includegraphics[width=" + str(self.width) + "\\textwidth, " \
                                                                                         "height=" + str(
            self.height) + "\\paperheight, keepaspectratio]{" + self.path + "}}"
        if (self.filler):
            block += "\hfill"
        else:
            block += "\\\\"
        return block

    def __repr__(self):
        """
        Returns a string representation of the object
        """
        return self.__str__()


class doc:
    """
    This class describes a document.
    """

    def __init__(self, padding_heigth=0.1):
        """
        Created a doc object

        Parameters
        ----------
        padding_heigth : float
            the height padding
        """
        self.rows = [
            "\\begin{figure}[!htb]",
            "\\centering",
        ]
        self.row = [

        ]
        self.padding_heigth = padding_heigth
        self.padding_width = 0.1
        self.row_count = 0

    def add_row_element(self, data):
        """
        Add element to current row

        Parameters
        ----------
        data : str
            image location
        """
        self.row.append(data)

    def add_row(self):
        """
        Start on new row
        """
        for i in self.row:
            i.width = round((1 / len(self.row)) * (1 - self.padding_width), 3)
        self.row[-1].filler = False
        self.rows += self.row
        self.row_count += 1
        self.row = []

    def save(self, path):
        """
        Save the document

        Parameters
        ----------
        path : str
            save the .tex to path
        """
        for i in self.rows:
            if (type(i) != str):
                i.height = 1 / (self.row_count * (1 + self.padding_heigth))
        self.rows += ["\\end{figure}"]
        print(path)
        open(path, "w").write("\n".join(map(str, self.rows)))

    def add_caption(self, text):
        """
        Add caption for the figure

        Parameters
        ----------
        text : str
            the caption
        """
        self.rows.append("\\caption{" + text + " }")

    def add_ref(self, name):
        """
        Add label for the figure

        Parameters
        ----------
        name : str
            the label
        """
        self.rows.append("\\label{fig:" + name + "}")

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        for i in self.rows:
            print(i)


def compile_doc(method, alpha_epochs, output_path, path_latex="", extra=lambda x: x, results_doc=None):
    """
    Creates a .tex document based on the method and alpha_epochs

    Parameters
    ----------
    method : class
        the class method
    alpha_epochs : dict
        the key should be the alpha value and the value is a list of epochs
    output_path : str
         location to save the data
    path_latex : str
        the path to reference from latex
    extra : lambda
        run extra function to make sure method is fully reset
    results_doc : doc
        if you want to add data to a existing document

    Returns
    ----------
    doc
        a document with all the images generated from alpha_epochs
    """
    path_latex += "/" if not path_latex.endswith("/") and not len(path_latex) == 0 else ""
    output_path += "/" if not output_path.endswith("/") and not len(output_path) == 0 else ""

    if (results_doc is None):
        results_doc = doc()

    make_dir(output_path)

    """
    alpha_peochs should be a dict on the form
        {
            alpha_val_0 = [epoch_count_0, epoch_count_1, ..., epoch_count_n],
            alpha_val_1 = [epoch_count_0, epoch_count_1, ..., epoch_count_n],
            ...
            alpha_val_n = [epoch_count_0, epoch_count_1, ..., epoch_count_n]
        }
    """
    for alpha, epochs in alpha_epochs.items():
        for index, epoch in enumerate(epochs):
            method.reset()
            """
            Sometiems a method needs some extra code to be ran for the method to be fully reset
            """
            extra(method)
            FILE_PATH = "alpha_{}_epoch_{}.png".format(alpha, epoch)

            if not (os.path.isfile(output_path + "/" + FILE_PATH)) or "ow" in sys.argv:
                method.fit(epochs=epoch)
                method.data = method.data.clip(0, 1)
                method.save(output_path + "/" + FILE_PATH)
            else:
                print("{}\n\tFile already exist (add sys arg ow to overwrite)".format(FILE_PATH))

            results_doc.add_row_element(subfigure(path=path_latex + FILE_PATH,
                                                  text="$\\alpha = {}$\\newline Iteration $= {}$".format(alpha, epoch)))
        results_doc.add_row()
    return results_doc


def make_dir(path):
    """
    Make sure the dir does exist

    Parameters
    ----------
    path : str
        dir to check if exist
    """
    if not os.path.isdir(path):
        os.mkdir(path)
