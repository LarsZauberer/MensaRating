from pathlib import Path

LIST_OF_FILES = [
    Path("core/models.py")
]


for i in LIST_OF_FILES:
    with open(i, 'r') as f:
        content = f.read()
        with open("Documentation/code/" + i.stem + ".tex", "w") as c:
            c.write("\\begin{lstlisting}[language=Python]\n")
            c.write(content)
            c.write("\n\\end{lstlisting}")

with open("Documentation/code/main_code.tex", "w") as f:
    for i in LIST_OF_FILES:
        f.write("\\section{" + i.stem + "}\\label{code:" + i.stem + "}\n")
        f.write("\\input{code/" + i.stem + "}\n")
