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
    "ruby",
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
    depString = subprocess.getoutput('brew deps ' + formulaName)
    depList = depString.split("\n")
    if depList != [""]:
        for ignoreDeps in depList:
            if not IsListed(ignoreDeps):
                ignoreList.append(ignoreDeps)
                SetDeps(ignoreDeps)

def GetAllFormulae():
    formulaString = subprocess.getoutput('brew list')
    formulaList = re.split("\t|\n", formulaString)
    return formulaList

def Delete():
    formulae = ignoreList[:]
    for formula in formulae:
        SetDeps(formula)

    formulae = GetAllFormulae()

    for formula in formulae:
        if not IsListed(formula):
            subprocess.getoutput('brew uninstall --ignore-dependencies ' + formula)

Delete()