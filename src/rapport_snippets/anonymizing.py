from backend import anonymizing
from rapport_snippets.figs import *


def compile(output_dir="./rapport_snippets/output"):
    """
    Compiles a .tex file for the anonymizing function

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    make_dir(output_dir)
    epoch_count = {
        0.25: [1, 10, 100],
        0.5: [1, 10, 100],
        0.75: [1, 10, 100],
    }

    for color in [True, False]:
        naming = "color" if color else "gray"
        output_path_location = "{}/{}/".format(output_dir, naming)
        path_latex = "anonymisering/resultat/{}".format(naming)

        make_dir(output_path_location)

        anon_obj = anonymizing.Anonymous("./files/test_images/lena.png", color)

        results_doc = compile_doc(anon_obj, epoch_count, output_path=output_path_location, path_latex=path_latex)
        results_doc.save("{}/resultat.tex".format(output_path_location))


def compile_faces(output_dir="./rapport_snippets/output"):
    """
    Compiles a .tex file for the anonymizing function for the faces image

    Parameters
    ----------
    output_dir : str
        the location to store the .tex with images
    """
    anon_obj = anonymizing.Anonymous("./files/test_images/workshop-photo-small.jpeg", True)
    anon_obj.save(output_dir + "mange.png")

    anon_obj.fit(300)
    anon_obj.save(output_dir + "mange_out.png")

    results_doc = doc()
    results_doc.add_row_element(subfigure(path="anonymisering/mange_out.png", text="Bilde med glitch"))
    results_doc.add_row_element(subfigure(path="anonymisering/mange.png", text="Bilde med glitch"))
    results_doc.add_row()
    results_doc.add_caption("Metoden funker også for mange ansikt")
    results_doc.save("{}/resultat.tex".format(output_dir))
