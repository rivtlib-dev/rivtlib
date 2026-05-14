import ast
import os
import sys
from pathlib import Path


def analyze_source(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    # lines = source.splitlines()

    # 1. List Imports
    print("\nIMPORTS:")
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # Get the exact segment of text for the import
            segment = ast.get_source_segment(source, node)
            print(f"  - {segment}")

    # 2. List Classes and Methods
    print("\nCLASSES & METHODS:")
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_len = node.end_lineno - node.lineno + 1
            print(f"    Class: {node.name} ({class_len} lines total)")

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_len = item.end_lineno - item.lineno + 1
                    print(f"    └─ Method: {item.name}() -> {method_len} lines")

    # 3. List Top-Level Functions
    funct_len = 0
    funcs_len = 0
    print("\n TOP-LEVEL FUNCTIONS:")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcs_len = node.end_lineno - node.lineno + 1
        funct_len = funct_len + funcs_len
    if funct_len == "0":
        print(f" ({funct_len} lines total)")
    else:
        pass

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_len = node.end_lineno - node.lineno + 1
            print(f"  - {node.name}() -> {func_len} lines")


# Usage
filenmS = sys.argv[1]
pathS = os.getcwd()
fileP = Path(pathS, "src", "rivtlib", filenmS)
with open(fileP, "r") as file:
    line_count = str(len(file.readlines()))
print(" ")
print("=========================================================")
print("Module Name: " + filenmS + "   | Total Lines: " + line_count)
print("=========================================================")
analyze_source(fileP)
print("=========================================================")
