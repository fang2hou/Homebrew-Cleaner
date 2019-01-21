# This Python file uses the following encoding: utf-8
import subprocess
import re

default_ignore_formulae = [
    "telnet",
    "zsh",
    "fish",
    "clang-format",
    "wget",
    "go",
    "node",
    "python",
    "python3",
    "vim",
    "imagemagick",
    "gnuplot"
]

class HomebrewCleaner():
    def __init__(self, ignore=None):
        self.ignore_formulae = ignore if ignore else default_ignore_formulae
        self.get_all_formulae()

    def is_listed(self, name_of_formula):
        if name_of_formula in self.formulae:
            return True
        else:
            return False

    def get_all_formulae(self):
        system_string = subprocess.check_output(["brew", "list"]).rstrip()
        formulae = re.split(r"\t|\n", system_string)
        self.formulae = formulae

    def ignore_dependencies(self, name_of_formula):
        system_string = subprocess.check_output(["brew", "deps", name_of_formula])
        dependencies = system_string.rstrip().split("\n")
        
        if dependencies[0] != "":
            next_dependencies = []

            for dependency in dependencies:
                if self.is_listed(dependency):
                    self.formulae.remove(dependency)
                    next_dependencies.append(dependency)

            for dependency in next_dependencies:
                self.ignore_dependencies(dependency)

    def clean(self):
        print("\033[94mHomebrew Cleaner:\033[0m Start analyzing... 🔍")

        for formula in self.ignore_formulae:
            if self.is_listed(formula):
                self.formulae.remove(formula)
                self.ignore_dependencies(formula)

        print("================================================")

        if len(self.formulae) != 0:
            for formula in self.formulae: self.delete(formula)
            print("\033[94mHomebrew Cleaner:\033[0m Done! ✅")
        else:
            print("\033[94mHomebrew Cleaner:\033[0m Nothing needs to be removed! 💯")

    def delete(self, name_of_formula):
       subprocess.check_output(["brew", "uninstall", "--ignore-dependencies", name_of_formula])
       print("\033[94mHomebrew Cleaner:\033[0m \"%s\" has been deleted. ♻️" % name_of_formula)

if __name__ == "__main__":
    hc = HomebrewCleaner()
    hc.clean()