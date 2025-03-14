import os
from PIL import Image, ImageDraw, ImageFont

# folders
root_dirS = 'rivt-toy-report'
main_dirL = ['div01L', 'div02L', 'privateL', 'functionsL', 'rivtdocL']
main_dir_nameL = ['div01-division-one',
                  'div02-division-two',
                  'data-private',
                  'functions',
                  'rivt-docs']
div01L = [
    'data01',
]

div02L = [
    'data02'
]

privateL = [
    'data',
    'functions',
    'functions\\output',
    'functions\\input',
    'rivt-docs',
    'temp',
    'rivt-docs\\text',
    'rivt-docs\\pdf'
]

rivtdocL = [
    'pdf',
    'text'
]

functionsL = [
    'input',
    'output'
]


dirL = zip(main_dirL, main_dir_nameL)

# data
csvS = "col1, col2, col3" + "\n" + "1,2,3" + "\n" + "4,5,6"

img = Image.new('RGB', (200, 100), (255, 255, 255))
d = ImageDraw.Draw(img)
ImageFont.load_default()
d.text((20, 20), 'rivt', fill=(255, 0, 0), font_size=48)

licenseS = """MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

gitignoreS = """#.gitignore

# rivt files
data-private/
"""

file4P = os.path.relpath(root_dirS + "/LICENSE")
file5P = os.path.relpath(root_dirS + "/.gitignore")

os.makedirs(root_dirS)
with open(file4P, 'w') as f:
    f.write(licenseS)

with open(file5P, 'w') as f:
    f.write(gitignoreS)


def main():
    for i in dirL:
        for j in eval(i[0]):
            dirNameS = root_dirS + '/' + str(i[1]) + '/' + str(j)
            divNameS = root_dirS + '/' + str(i[1])
            try:
                # Create target Directories
                os.makedirs(dirNameS)
                print("Directory ", dirNameS,  " Created ")
                # write data files
                file3P = os.path.relpath(dirNameS + "/table.csv")
                if "data" in dirNameS and "private" not in dirNameS:
                    with open(file3P, 'w') as f:
                        f.write(csvS)
                    img.save("./" + dirNameS + "/image.png")
                if "rivt-docs" in divNameS:
                    file6P = os.path.relpath(dirNameS + "/README.txt")
                    if "pdf" in dirNameS:
                        try:
                            with open(file6P, 'w') as f:
                                f.write("rivt PDF documents\n")
                        except:
                            print("File ", file6P,  " already exists")
                    elif "text" in dirNameS:
                        try:
                            with open(file6P, 'w') as f:
                                f.write("rivt text documents\n")
                        except:
                            print("File ", file6P,  " already exists")
            except FileExistsError:
                print("Directory ", dirNameS,  " already exists")

        # rivt file paths
        file1P = os.path.relpath(divNameS + "/riv01-sample-doc1.py")
        file2P = os.path.relpath(divNameS + "/riv02-sample-doc2.py")

        # generate rivt files
        rivtS = f'''
        import rivtlib.rivtapi as rv

        rv.R("""Rivtinit Section | notoc, 1 

            Example of Rivtinit-string for a rivt file in the division folder
            {str(i[1])}.

            ||init | config.ini

            """)

        rv.I("""Insert Section | nocolor

            Example of Insert-string.
            
            Sample equation _[e]
            a^2 + b^2 = c^2

            Sample figure _[f]
            || image | data/image.png | 0.9


            Sample table _[t]
            || table | data/table.csv | 15,C

            """)

        rv.V("""Sample Value Section | sub

            Sample Insert-string.
                    
            a1 = 1.0             |IN, M| define a1
            b1 = 2.2             |IN, M| define b1

            product of a1 and b1 _[e]
            c1 = a1 * b1         |IN^2, M^2| 2,2

            quotient of a1 and b1 _[e]
            d1 = a1 / b1         |IN^2, M^2| 2,2

            """)
            
            '''

        if "div01" in divNameS or "div02" in divNameS:
            try:
                with open(file1P, 'w') as f:
                    f.write(rivtS)
                with open(file2P, 'w') as f:
                    f.write(rivtS)
            except:
                print("File in", dirNameS,  " already exists")


if __name__ == '__main__':
    main()
