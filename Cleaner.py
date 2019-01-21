# This Python file uses the following encoding: utf-8
import re
import os

default_ignore_formulae_list = [
    "telnet",
    "zsh",
    "fish",
    "clang-format",
    "wget",
    "go",
    "node",
    "python",
    "python3",
    "ruby",
    "vim",
    "imagemagick",
    "gnuplot"
]


class HomebrewCleaner():
    def __init__(self, ignore=None):
        self.ignore_formulae_list = ignore if ignore else default_ignore_formulae_list
        self.get_all_formulae()

    def is_listed(self, name_of_formula):
        if name_of_formula in self.formulae:
            return True
        else:
            return False

    def get_all_formulae(self):
        command = os.popen("brew list")
        system_string = command.read().rstrip()
        formulae = re.split(r"\t|\n", system_string)
        self.formulae = formulae

    def ignore_dependencies(self, name_of_formula):
        command = os.popen("brew deps " + name_of_formula)
        system_string = command.read()
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
        self.send_message("Start analyzing...🔍   0%", True)

        display_step = 1/len(self.ignore_formulae_list) * 100
        display_percent = 0

        for formula in self.ignore_formulae_list:
            if self.is_listed(formula):
                self.formulae.remove(formula)
                self.ignore_dependencies(formula)

            display_percent += display_step
            print("\b\b\b%2.0f%%" % display_percent, end="", flush=True)

        print("\n================================================")

        if len(self.formulae) != 0:
            for formula in self.formulae:
                self.delete(formula)
            self.send_message("Done! ✅")
        else:
            self.send_message("Nothing needs to be removed! 💯")

    def delete(self, name_of_formula):
        command = os.popen(
            "brew uninstall --ignore-dependencies " + name_of_formula)
        results = command.read()

        for result in results:
            if "Error" in result:
                self.send_message(result)
                return

        self.send_message("\"%s\" has been deleted. ♻️" % name_of_formula)

    def send_message(self, message_string, no_new_line=None):
        end_symbol = '' if no_new_line else '\n'
        print("\033[94mHomebrew Cleaner:\033[0m " +
              message_string, end=end_symbol, flush=True)


if __name__ == "__main__":
    hc = HomebrewCleaner()
    hc.clean()
