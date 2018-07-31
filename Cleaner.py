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
    depString = depString.decode("UTF-8").rstrip()
    depList   = depString.split("\n")
    print(depList)
    if len(depList) > 1:
        for ignoreDeps in depList:
            if not IsListed(ignoreDeps):
                ignoreList.append(ignoreDeps)
                SetDeps(ignoreDeps)

def GetAllFormulae():
    formulaString = subprocess.check_output(["brew", "list"])
    formulaString = formulaString.decode("UTF-8").rstrip()
    formulaList   = re.split(r"\t|\n", formulaString)
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