#!/usr/bin/python
# Homebrew Cleaner
# Author: Fang2hou

import subprocess
import re

ignoreList = [
    "telnet",
    "zsh",
    "you-get",
    "ffmpeg",
    "libav",
    "wget",
    "go",
    "node",
    "python",
    "python3",
    "vim",
    "imagemagick",
    "gnuplot",
    "lua",
]

def IsListed(formulaName):
    for listedFormula in ignoreList:
        if listedFormula == formulaName:
            return True
    return False

def SetDeps(formulaName):
    depString = subprocess.check_output(["brew", "deps", formulaName])
    depList = str(depString).split("\n")
    if depList != [""]:
        for ignoreDeps in depList:
            if not IsListed(ignoreDeps):
                ignoreList.append(ignoreDeps)
                SetDeps(ignoreDeps)

def GetAllFormulae():
    formulaString = subprocess.check_output(["brew", "list"])
    formulaList = re.split(r"\t|\n", str(formulaString))
    return formulaList

def Delete():
    for formula in ignoreList:
        SetDeps(formula)

    formulae = GetAllFormulae()

    for formula in formulae:
        if not IsListed(formula):
            # subprocess.run(['brew uninstall --ignore-dependencies ' + formula])
            print("%s" % formula)
Delete()
print("Done!")