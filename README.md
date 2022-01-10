## Python Homework Formatter
This tool will compile all your files for your homework into one markdown file. Markdown files are easy to work with and have a fixed-width font for code snippets. I use a vscode extension to compile my markdown files into pdf files when I'm ready to turn them in. 
### Use
Clone the `markdown-formatter.py` script into the top level of your 424 directory. To run the formatter, run something like this in your terminal: `python3 markdown-formatter/markdown-formatter.py HW1`.
### Explanation
The only argument to the formatter is the directory containing all of your relevant files for the homework assignment. The formatter is designed to take all of the files in that folder and format them for submission. As is, the formatter compiles and runs .c files, capturing the output. It also copies .txt files directly. Such text files might include discussion or answers to questions.
### Code
In order to include your code as part of the submission, the formatter searches your .c files for code surrounded by the following comments: `//begcpy` and `//endcpy`. Note that the only one code block will be copied for each .c file.
### Extensibility
I did my best to put all of the major strings as constants so this code should be easily customizable for you. Feel free to make it your own.