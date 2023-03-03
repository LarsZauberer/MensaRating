from pathlib import Path

LIST_OF_FILES = [
    Path("core/models.py"),
    Path("core/webscraper.py"),
    Path("core/views.py"),
    Path("core/urls.py"),
    Path("users/views.py"),
    Path("core/webscraper.py"),
]


for i in LIST_OF_FILES:
    with open(i, 'r') as f:
        content = f.read()
        name = str(i).replace("/", ".").replace("\\", ".")

        print(name)
        
        # Extra characters removal
        content = content.replace("ä", "ae")
        content = content.replace("ö", "oe")
        content = content.replace("ü", "ue")
        content = content.replace("Ä", "Ae")
        content = content.replace("Ö", "Oe")
        content = content.replace("Ü", "Ue")
        
        with open("Documentation/code/" + name + ".tex", "w") as c:
            c.write("\\begin{lstlisting}[language=Python]\n")
            c.write(content)
            c.write("\n\\end{lstlisting}")

with open("Documentation/code/main_code.tex", "w") as f:
    for i in LIST_OF_FILES:
        name = str(i).replace("/", ".")
        f.write("\\section{" + name + "}\\label{code:" + name + "}\n")
        f.write("\\input{code/" + name + "}\n")
