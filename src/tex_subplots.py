import glob
import re
import copy
import math as m
from pathlib import Path


def sorted_nicely(l):
    """Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)


def get_pdf_files(path):
    return sorted_nicely(glob.glob(f"{path}/*.pdf"))


def generate_tex_figures(subplots=(1, 1)):
    """Generates and prints LaTex string for figure or subfigure.

    Parameters
    ----------
    subplots: array-like, optional
        The number of rows and columns of subplots.

    Returns
    -------
    tex_figure: str
        Figure string.

    References
    ----------
    - https://www.overleaf.com/learn/latex/How_to_Write_a_Thesis_in_LaTeX_(Part_3):_Figures,_Subfigures_and_Tables

    """
    base = lambda t: "\n{}\\centering\n{}\\includegraphics[width=1\\textwidth]{{IMAGE}}\n{}\\caption{{CAPTION}}\n{}\\label{{fig: < >}}\n".format(
        *(4 * ["    " * t])
    )

    tex_figure = ""

    if subplots[0] == subplots[1] == 1:
        tex_figure += "\\begin{{figure}}[h!]{}\\end{{figure}}".format(base(1))
        return tex_figure

    tex_figure += "\\begin{figure}[h!]\n    \\centering\n"

    for i in range(subplots[0]):
        for j in range(subplots[1]):
            tex_figure += "    \\begin{{subfigure}}[t]{{{:.2f}\\textwidth}}".format(1 / subplots[1] - 0.01)
            tex_figure += "{}    \\end{{subfigure}}\n    \\hfill\n".format(base(2))

    tex_figure = tex_figure[:-7]
    tex_figure += "\\caption{}\n    \\label{fig: < >}"
    tex_figure += "\n\\end{figure}"

    return tex_figure


def find_str_idx(to_find, find_in):
    start_end = []
    for match in re.finditer(to_find, find_in):
        start_end.append((match.start(), match.end()))
    return start_end


def make_tex_str(files, subplots, total_tex_str=""):
    subplots_tex = generate_tex_figures(subplots)

    mult = subplots[0] * subplots[1]
    tex_str = copy.copy(subplots_tex)

    for i, f in enumerate(files):
        if i % mult == 0 and i != 0:
            total_tex_str += tex_str + "\n\n\\newpage\n\n"
            tex_str = copy.copy(subplots_tex)

        image_idx = find_str_idx("IMAGE", tex_str)[0]
        tex_str = tex_str[: image_idx[0]] + tex_str[image_idx[1] :]
        tex_str = tex_str[: image_idx[0]] + f + tex_str[image_idx[0] :]

        caption_str = Path(f).stem
        caption_str = caption_str.replace("_", " ")
        caption_idx = find_str_idx("CAPTION", tex_str)[0]
        tex_str = tex_str[: caption_idx[0]] + tex_str[caption_idx[1] :]
        tex_str = tex_str[: caption_idx[0]] + caption_str + tex_str[caption_idx[0] :]

        if i == len(files) - 1:
            total_tex_str += tex_str

    return total_tex_str


def construct_tex_subplots(path, subplots):
    files = get_pdf_files(path)

    mult = subplots[0] * subplots[1]
    leftover = (len(files)) % mult

    if leftover != 0:
        total_tex_str = make_tex_str(files[:-leftover], subplots)
        total_tex_str += "\n\n\\newpage\n\n"

        a = m.ceil(m.sqrt(mult))
        b = m.ceil(mult / a)

        total_tex_str = make_tex_str(files[-leftover:], (a, b), total_tex_str=total_tex_str)
    else:
        total_tex_str = make_tex_str(files, subplots)

    return total_tex_str


if __name__ == "__main__":
    path = "plots"
    subplots = (3, 3)
    tex_str = construct_tex_subplots(path, subplots)
    print(tex_str)
