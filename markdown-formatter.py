import subprocess
import sys
import os

NEWLINE = "\n"
MD_NEWLINE_SYMBOL = "\\"
STUDENT_NAME = "Student Name"
CLASS = "ECEN 424"
TITLE = "# "
HEADING = "### "
HEADING_2 = "#### "
CODE_START = "//begcpy\n"
CODE_END = "\n//endcpy"
CODE_SNIPPET = "```"
C_SNIPPET = "c"
ALLOWED_EXTENSIONS = [".c", ".txt"]


def get_problems(directory):
    """
    lists all files in HW dir with extensions that are in the
    allowed extensions constant. The intended usage is to name
    all files in HW dir as the problem that they are.
    (i.e. HW_1/2_81.c to represent problem 2.81 from text)
    :param directory: path to hw dir
    :return: list of all files in dir
    """
    problem_set = []
    dir_files = os.listdir(directory)
    # get all files of interest
    for file in dir_files:
        file_tuple = os.path.splitext(file)
        if file_tuple[1] in ALLOWED_EXTENSIONS:
            problem_set.append(file_tuple[0])
    # get set to identify only unique problems
    problem_set = sorted(set(problem_set))
    # convert set to comma-separated string
    problem_str = ""
    for problem in problem_set:
        problem_str = problem_str + ", " + problem
    return problem_str[1:]

def get_your_code(filename):
    """
    parses .c files for code that is surrounded by
    CODE_START and CODE_END comments
    :param filename: code filename
    :return: code snippet
    """
    code = ""
    if (os.path.splitext(filename)[1] == ".c"):
        text = ""
        with open (filename, "r") as file:
            text = file.read()
        start_ind = text.find(CODE_START) + len(CODE_START)
        end_ind = text.find(CODE_END)
        if (start_ind != -1):
            code = text[start_ind:end_ind]
    return code

def handle_md_paragraph(input_text):
    """
    in md, paragraph newlines must be in the format "\" followed by the newline.
    reformats paragraph string this way
    :param text: text to reformat
    :return: reformatted text string
    """
    alt_text = input_text.replace("\n\n", "\n")
    alt_text = alt_text.replace("\n", "\\\n")
    if len(alt_text) > 0 and alt_text[-2:] == "\\\n":
        return alt_text[:-2]
    return alt_text

if __name__ == "__main__":
    # Create markdown file
    directory = sys.argv[1]
    new_filename = os.path.basename(os.path.normpath(directory))
    markdown_file = os.path.join(directory, new_filename + ".md")
    problems = get_problems(directory)
    with open(markdown_file, "w") as f:
        # output usual info
        f.write(TITLE + new_filename.replace("_", " ") + NEWLINE)
        f.write(HEADING + STUDENT_NAME + NEWLINE)
        f.write(HEADING + CLASS + NEWLINE)
        f.write(HEADING + new_filename.replace("_", " ") + NEWLINE)
        f.write(HEADING + "Problems:" + problems + NEWLINE)
        f.write(NEWLINE)

    # loop through all files in HW dir and add to md file
    for file in os.listdir(directory):
        file_tuple = os.path.splitext(file)
        path = os.path.join(directory, file)
        with open(markdown_file, "a") as f:
            if file_tuple[1] == ".c":
                f.write(HEADING + file_tuple[0] + NEWLINE)
                # write user code to file
                f.write(HEADING_2 + "Code" + NEWLINE)
                f.write(CODE_SNIPPET + C_SNIPPET + NEWLINE)
                f.write(get_your_code(path) + NEWLINE)
                f.write(CODE_SNIPPET + NEWLINE)
                # compile c program
                print (f"compiling {file}...")
                out_file = os.path.join(directory, "a") # output location
                p = subprocess.Popen(["gcc", path, "-o", out_file])
                p.wait()
                # execute c program
                print (f"executing {file}...")
                p = subprocess.Popen([out_file], stdout=subprocess.PIPE)
                p.wait()
                # capture output
                binary_out = p.communicate()[0]
                f.write(HEADING_2 + "Results" + NEWLINE)
                # handle output for markdown
                output = binary_out.decode("utf-8")
                formatted_output = handle_md_paragraph(output)
                f.write(formatted_output + NEWLINE)
            elif file_tuple[1] == ".txt":
                print (f"copying {file}...")
                # add heading only if this doesn't correspond to a .c file
                if file_tuple[0] + ".c" not in os.listdir(directory):
                    f.write(HEADING + file_tuple[0] + NEWLINE)
                f.write(HEADING_2 + "Answer" + NEWLINE)
                with open (path) as f2:
                    text = f2.read()
                    f.write(handle_md_paragraph(text) + NEWLINE)