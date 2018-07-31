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

def IsListed(formula):
    for listedFormula in ignoreList:
        if listedFormula == formula:
            return True
    return False

def SetDeps(formula):
    depString = subprocess.getoutput('brew deps ' + formula)
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

def Main():
    loopList = ignoreList[:]
    for formula in loopList:
        SetDeps(formula)

    loopList = GetAllFormulae()

    for formula in loopList:
        if not IsListed(formula):
            subprocess.getoutput('brew uninstall --ignore-dependencies ' + formula)

Main()