import ast
import os

import pyobf2.lib as obf


class DoObfuscate:
    """
    Obfuscate code using https://github.com/0x3C50/pyobf2
    """

    def __init__(self) -> None:
        self.build_dir = os.path.join(os.getcwd(), 'build')
        self.src_dir = os.path.join(self.build_dir, 'src')
        self.config = {
            "removeTypeHints.enabled": True,
            "fstrToFormatSeq.enabled": True,
            "encodeStrings.enabled": True,
            "encodeStrings.mode": "xortable",
            "floatsToComplex.enabled": True,
            "intObfuscator.enabled": True,
            "intObfuscator.mode": "decode",
            "renamer.enabled": True,
            "renamer.rename_format": "f'{kind}{get_counter(kind)}'",
            "replaceAttribSet.enabled": True,
            "unicodeTransformer.enabled": True,
        }

    def walk(self, path: str) -> dict:
        """
        Walk a directory and return a dict of files
        """
        files = {}
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                files[os.path.join(root, filename)] = os.path.join(
                    root, filename).replace(path, '')
        return files

    def run(self) -> None:
        """
        Run the obfuscation
        """
        obf.set_config_dict(self.config)

        tree = self.walk(self.src_dir)
        for file in tree:
            if file.endswith('.py'):
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree[file] = ast.parse(code)
                tree[file] = obf.do_obfuscation_single_ast(
                    tree[file], tree[file])
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(ast.unparse(tree[file]))
'''def main() -> None:
    """
    The main function of the script. It performs the following steps:
    1. Defines the input and output directories
    2. Enables renamer obfuscation in the pyobf2 library
    3. Reads the content of all python files in the input directory
    4. Parses the content of each file into an AST (Abstract Syntax Tree)
    5. Passes the ASTs and their corresponding file paths to the pyobf2 library's obfuscation function
    6. Writes the obfuscated ASTs to the output directory, preserving the original file structure
    """

    in_dir = os.path.join(os.path.dirname(__file__), "input")
    out_dir = os.path.join(os.path.dirname(__file__), "output")

    obf.set_config_dict({"renamer.enabled": True})

    in_files = {x: open(x, "r", encoding="utf-8").read() for x in walk(in_dir)}
    in_asts = {x: ast.parse(y) for x, y in in_files.items()}

    for _ in obf.do_obfuscation_batch_ast(list(in_asts.values()), list(in_asts.keys())):
        pass

    for x, y in in_asts.items():
        out_file = os.path.join(out_dir, os.path.relpath(x, in_dir))
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(ast.unparse(y))


if __name__ == "__main__":
    main()'''