from tex_subplots import find_str_idx
import os


def read_file(path):
    with open(path) as f:
        tex_str = f.read()
    return tex_str


def write_file(file_path, file_name, content):
    with open(file_path + "/" + file_name, "w") as f:
        f.write(content)


def insert_image_path(tex_str, path):
    image_idx = find_str_idx("IMAGE_PATH", tex_str)[0]
    tex_str = tex_str[:image_idx[0]] + tex_str[image_idx[1]:]
    tex_str = tex_str[:image_idx[0]] + path + tex_str[image_idx[0]:]
    return tex_str


def get_tex_template(template_path, image_path):
    tex_str = read_file(template_path)
    tex_str = insert_image_path(tex_str, image_path)
    return tex_str


def run_latex_compile(file):
    os.system(f"pdflatex {file}")


if __name__ == "__main__":
    tex_template = get_tex_template("tex_templates/template.tex", "~/Downloads/plots")
    write_file("tex_generated/", "generated_template.tex", tex_template)
    print(tex_template)
