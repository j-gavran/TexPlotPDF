import argparse
import os

from tex_subplots import construct_tex_subplots
from tex_file import get_tex_template, write_file, run_latex_compile


parser = argparse.ArgumentParser(description="Combines pdf plots into a tex file and makes a joint pdf.")
parser.add_argument("-path", metavar="path", type=str, help="path to plots folder")
parser.add_argument("-subplots", metavar="subplots", nargs='+', type=tuple, help="subplot layout per page")

args = parser.parse_args()

path, subplots = args.path, args.subplots
subplots = (int(subplots[0][0]), int(subplots[0][1]))

tex_subplots = construct_tex_subplots(path, subplots)
write_file("tex_generated/", "generated_plots.tex", tex_subplots)

tex_template = get_tex_template("tex_templates/template.tex", path)
write_file("tex_generated/", "generated_template.tex", tex_template)

run_latex_compile("tex_generated/generated_template.tex")

os.system(f"cp tex_generated/generated_template.pdf {path}")
os.system(f"mv {path}/generated_template.pdf {path}/plots.pdf ")
